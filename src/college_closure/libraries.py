"""IPEDS Academic Libraries enrichment for watch-list evidence cards.

Holdings, expenditures, and librarian FTE come from Urban Institute
Education Data Portal ``academic-libraries`` (IPEDS AL, 2013–2023) or an
NCES AL complete-data fallback. Special-collection notes are best-effort
extracts from public library pages. Nothing here is a model training
feature: it is cultural/asset-value context on an elevated-risk watch
list, not a closure verdict.

Never invent holdings or rare-book claims. Missing AL or a failed scrape
means unknown — not “no library.”
"""

from __future__ import annotations

import hashlib
import html as html_mod
import json
import logging
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests

from college_closure.config import Settings
from college_closure.constants import SENTINEL_VALUES
from college_closure.filters import replace_sentinels
from college_closure.urban import UrbanClient, read_csv_filtered
from college_closure.worldcat import enrich_worldcat_shortlist, write_oclc_crosswalk

LOGGER = logging.getLogger(__name__)

# Urban portal (verified 2026-09 against /api/v1/api-endpoints/ + api-downloads/).
# endpoint_id 45: /api/v1/college-university/ipeds/academic-libraries/{year}/
# CSV (underscore): colleges_ipeds_academic_libraries.csv  (hyphenated name 404s)
URBAN_AL_ENDPOINT_ID = 45
URBAN_AL_CSV = "colleges_ipeds_academic_libraries.csv"
URBAN_AL_CSV_DIR = "ipeds"

# NCES IPEDS Academic Libraries complete-data stems (AL{year}.zip).
NCES_AL_BASE = "https://nces.ed.gov/ipeds/datacenter/data"
NCES_AL_MAP = {
    "physical_books": ["LPBOOKS", "LPBKVOL"],
    "electronic_books": ["LDBOOKS"],
    "electronic_media": ["LDMEDIA"],
    "electronic_serials": ["LDSERIAL"],
    "electronic_databases": ["LDBASES", "LDBASE"],
    "total_electronic_collections": ["LDELECT", "LDCOL"],
    "total_physical_collections": ["LPCOL"],
    "exp_total": ["LEXPTOT"],
    "librarians_fte": ["LSCLIB"],
    "total_lib_staff_fte": ["LSCTOT"],
    "physical_media": ["LPMEDIA"],
    "physical_serials": ["LPSERIAL"],
}

LIB_VALUE_COLS = [
    "lib_physical_books",
    "lib_digital_items",
    "lib_expenditures",
    "lib_fte",
    "lib_staff_fte",
    "lib_electronic_books",
    "lib_physical_media",
    "lib_branches",
]

LIB_WATCHLIST_COLS = [
    "lib_year",
    "lib_source",
    "lib_physical_books",
    "lib_digital_items",
    "lib_expenditures",
    "lib_fte",
    "lib_staff_fte",
    "lib_arl_member",
    "lib_special_collections_note",
    "lib_unique_flag",
    "lib_note_url",
    "lib_oclc_symbol",
    "lib_worldcat_registry_id",
    "lib_libraries_org_id",
]

UNKNOWN_NOTE = (
    "Unknown — no distinctive special-collections or rare-book note found on "
    "public library pages. Missing text does not mean the school has no library."
)
OUTSIDE_SHORTLIST_NOTE = "Web note not collected (outside top-50 / nonprofit shortlist)."
NOTHING_DISTINCTIVE_NOTE = (
    "Public library pages were reached; nothing distinctive (named special "
    "collection, archive, or rare-book area) was published."
)

_SKIP_TAGS = {"script", "style", "noscript", "svg"}
_LIBRARY_HREF_RE = re.compile(
    r"library|libraries|special[-_\s]?collect|archives?|rare[-_\s]?book|digital[-_\s]?collect|repository",
    re.I,
)
_KEYWORD_RE = re.compile(
    r"special collections?|rare books?|university archives?|college archives?|"
    r"manuscripts?|distinctive collections?|named collections?|"
    r"digital (?:library|repository|collections?)|institutional repository|"
    r"historical (?:library|collection|society)|memorial library",
    re.I,
)
_GENERIC_RE = re.compile(
    r"library hours|ask a librarian|interlibrary loan|search the catalog|"
    r"renew your books|off[- ]campus access|database list|hours of operation|"
    r"chat with a librarian|course reserves|citation (?:style|guide)",
    re.I,
)
_PROMO_RE = re.compile(
    r"thrilled|delighted|excited to|proud to (?:announce|launch)|"
    r"click here|learn more|sign up|subscribe|newsletter|"
    r"donate now|give now|follow us|online encyclopedia|wupedia",
    re.I,
)
_EXTRA_VERB_RE = re.compile(
    r"\b(is|are|was|were|has|have|holds|includes|contains|documents|"
    r"houses|preserves|features|maintains|collects)\b",
    re.I,
)
_COLLECTION_NAME_RE = re.compile(
    r"""
    (?:the\s+)?
    (
      (?:[A-Z][\w'’\-.]+(?:\s+(?:and|of|the|for|in|at|de|del|la|los|las|san|st\.?))?\s+){0,6}
      [A-Z][\w'’\-.]+
      \s+
      (?:
        Special\s+Collections?
        |Rare\s+Books?(?:\s+and\s+Manuscripts?)?(?:\s+Collection)?
        |Archives?
        |Manuscript(?:s|\s+Collection)
        |Historical\s+(?:Library|Collection|Society)
        |Memorial\s+Library
        |Research\s+Collection
        |Digital\s+(?:Library|Collection|Repository)
      )
    )
    """,
    re.VERBOSE,
)
_BOILERPLATE_NAMES = {
    "special collections",
    "the special collections",
    "university archives",
    "the university archives",
    "college archives",
    "the college archives",
    "rare books",
    "the rare books",
    "digital library",
    "the digital library",
    "digital collections",
    "the digital collections",
    "digital repository",
    "institutional repository",
    "the archives",
    "archives",
    "academic catalog archive",
    "hnu academic catalog archive",
    "sage digital library",
    "ebsco digital library",
    "proquest digital library",
    "blog archive",
    "view full blog archive",
    "news archive",
    "press archive",
}
_JUNK_NAME_RE = re.compile(
    r"\b(hours|contact us|policies|mission|staff|alumni and friends|"
    r"academic catalog|course catalog|resources alumni|menu|skip to|"
    r"sage |ebsco|proquest|jstor|gale |credo |"
    r"blog|newsletter|press release|view full|"
    r"(?:news|press|photo|email|video|event)s?\s+archive)\b",
    re.I,
)
_GENERIC_NAME_WORDS = {
    "digital",
    "academic",
    "university",
    "college",
    "library",
    "learning",
    "studio",
    "commons",
    "institutional",
    "online",
    "the",
    "and",
    "of",
    "for",
    "in",
    "at",
    "pm",
    "resources",
    "alumni",
    "friends",
    "former",
    "faculty",
    "staff",
    "home",
    "main",
}

# Common paths relative to the institution homepage.
_LIBRARY_PATHS = (
    "/library",
    "/libraries",
    "/academics/library",
    "/academics/libraries",
    "/student-life/library",
    "/students/library",
    "/library/special-collections",
    "/library/archives",
    "/library/about",
    "/libraries/special-collections",
    "/special-collections",
    "/archives",
    "/library/collections",
    "/about/library",
)

# Public ARL member-name snapshot used only if the live list cannot be fetched.
# Source: Association of Research Libraries member directory (public).
_ARL_FALLBACK_NAMES = (
    "Harvard University",
    "Yale University",
    "Princeton University",
    "Columbia University",
    "University of Chicago",
    "Stanford University",
    "Massachusetts Institute of Technology",
    "University of California, Berkeley",
    "University of Michigan",
    "University of Illinois Urbana-Champaign",
    "University of Texas at Austin",
    "New York University",
    "Cornell University",
    "University of Pennsylvania",
    "Duke University",
    "Johns Hopkins University",
    "Northwestern University",
    "Brown University",
    "Dartmouth College",
    "University of Washington",
    "University of Wisconsin–Madison",
    "Ohio State University",
    "Pennsylvania State University",
    "University of North Carolina at Chapel Hill",
    "University of Minnesota",
    "Indiana University",
    "University of Virginia",
    "Boston Public Library",
    "Library of Congress",
    "New York Public Library",
    "Smithsonian Libraries",
)


class _HTMLText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self.parts: list[str] = []
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _SKIP_TAGS:
            self._skip += 1
            return
        if tag in {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "section", "article"}:
            self.parts.append("\n")
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP_TAGS and self._skip:
            self._skip -= 1
        if tag in {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "section", "article"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self.parts.append(data)


def html_to_text_and_links(raw: str) -> tuple[str, list[str]]:
    parser = _HTMLText()
    try:
        parser.feed(raw or "")
        parser.close()
    except Exception:  # noqa: BLE001 — tolerate broken markup
        text = re.sub(r"<[^>]+>", " ", raw or "")
        return re.sub(r"\s+", " ", text).strip(), []
    text = re.sub(r"[ \t]+", " ", "".join(parser.parts))
    text = re.sub(r"\n{2,}", "\n", text).strip()
    return text, parser.hrefs


def _sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text)
    out = []
    for chunk in chunks:
        s = re.sub(r"\s+", " ", chunk).strip(" •\t-|")
        if 25 <= len(s) <= 400:
            out.append(s)
    return out


def _usable_extra_sentence(sent: str) -> bool:
    """Keep supporting prose; drop promo copy and heading fragments."""
    if not sent or _PROMO_RE.search(sent) or _GENERIC_RE.search(sent):
        return False
    if len(sent) < 40:
        return False
    if _EXTRA_VERB_RE.search(sent):
        return True
    return len(re.findall(r"\b[a-z]{3,}\b", sent)) >= 3


def _is_mashed_nav(line: str) -> bool:
    caps = re.findall(r"\b[A-Z][A-Za-z]{2,}\b", line)
    lowers = re.findall(r"\b[a-z]{3,}\b", line)
    return len(caps) >= 5 and len(lowers) <= 1


def _named_collections(text: str) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip(" •\t-|")
        if len(line) < 15 or _is_mashed_nav(line):
            continue
        for match in _COLLECTION_NAME_RE.finditer(line):
            name = re.sub(r"\s+", " ", match.group(1)).strip(" ,.;:")
            key = name.lower()
            if key in _BOILERPLATE_NAMES or len(name) < 12:
                continue
            if _JUNK_NAME_RE.search(name):
                continue
            if re.match(r"^(Search|Using|Advanced|Home|Menu|Skip)\b", name, re.I):
                continue
            words = name.split()
            if len(words) > 8 or len(set(w.lower() for w in words)) < len(words) - 1:
                continue
            core = re.sub(
                r"\s+(?:Special\s+Collections?|Rare\s+Books?.*|Archives?|"
                r"Manuscript(?:s|\s+Collection)|Historical\s+(?:Library|Collection|Society)|"
                r"Memorial\s+Library|Research\s+Collection|"
                r"Digital\s+(?:Library|Collection|Repository))$",
                "",
                name,
                flags=re.I,
            )
            distinctive = [
                w for w in re.findall(r"[A-Za-z']+", core) if w.lower() not in _GENERIC_NAME_WORDS
            ]
            if not distinctive:
                continue
            if key not in seen:
                seen.add(key)
                names.append(name)
    return names[:8]


def extract_special_collections_note(raw_html: str, page_url: str | None = None) -> dict[str, Any]:
    """Pull distinctive collection/archive language from a library page.

    Returns note / unique_flag / names. Does not invent holdings counts.
    """
    text, _hrefs = html_to_text_and_links(raw_html)
    if not text or len(text) < 40:
        return {
            "note": UNKNOWN_NOTE,
            "unique_flag": False,
            "names": [],
            "source_url": page_url,
        }

    names = _named_collections(text)
    hits = []
    for sent in _sentences(text):
        if _GENERIC_RE.search(sent):
            continue
        if _KEYWORD_RE.search(sent):
            hits.append(sent)

    if names:
        named = "; ".join(names[:5])
        extra = ""
        for sent in hits:
            if not _usable_extra_sentence(sent):
                continue
            if any(n.lower() in sent.lower() for n in names):
                extra = " " + sent
                break
        if not extra:
            for sent in hits:
                if _usable_extra_sentence(sent):
                    extra = " " + sent
                    break
        note = f"Named holdings on a public library page: {named}.{extra}".strip()
        if page_url:
            note += f" Source: {page_url}"
        return {
            "note": note[:700],
            "unique_flag": True,
            "names": names,
            "source_url": page_url,
        }

    if hits:
        note = (
            "Library page mentions special collections / archives / rare books "
            f"but no named collection was published. {hits[0]}"
        )
        if page_url:
            note += f" Source: {page_url}"
        return {
            "note": note[:700],
            "unique_flag": False,
            "names": [],
            "source_url": page_url,
        }

    return {
        "note": NOTHING_DISTINCTIVE_NOTE,
        "unique_flag": False,
        "names": [],
        "source_url": page_url,
    }


def normalize_academic_libraries(raw: pd.DataFrame, source: str = "urban") -> pd.DataFrame:
    """Map Urban or NCES AL columns onto ``lib_*`` fields; sentinels → NA."""
    if raw is None or raw.empty:
        return pd.DataFrame(columns=["unitid", "year", "lib_source", *LIB_VALUE_COLS])

    work = raw.copy()
    work.columns = [str(c).strip() for c in work.columns]
    lower = {c.lower(): c for c in work.columns}

    def _col(*names: str) -> pd.Series:
        for name in names:
            if name in work.columns:
                return work[name]
            key = name.lower()
            if key in lower:
                return work[lower[key]]
        return pd.Series(pd.NA, index=work.index)

    if "unitid" not in {c.lower() for c in work.columns}:
        raise ValueError(f"Academic Libraries extract missing unitid. Columns: {list(work.columns)[:20]}")

    out = pd.DataFrame(
        {
            "unitid": pd.to_numeric(_col("unitid", "UNITID"), errors="coerce"),
            "year": pd.to_numeric(_col("year", "YEAR"), errors="coerce"),
        }
    )
    urban_physical = _col("physical_books")
    urban_digital = _col("total_electronic_collections")
    urban_ebooks = _col("electronic_books")
    urban_emedia = _col("electronic_media")
    urban_eserials = _col("electronic_serials")
    urban_exp = _col("exp_total")
    urban_fte = _col("librarians_fte")
    urban_staff = _col("total_lib_staff_fte")
    urban_pmedia = _col("physical_media")
    urban_branches = _col("branches_and_independent_lib")

    # NCES complete-data aliases when Urban names are absent.
    if urban_physical.isna().all():
        urban_physical = _first_mapped(work, NCES_AL_MAP["physical_books"])
    if urban_digital.isna().all():
        mapped_digital = _first_mapped(work, NCES_AL_MAP["total_electronic_collections"])
        if mapped_digital.isna().all():
            mapped_digital = _sum_mapped(
                work,
                NCES_AL_MAP["electronic_books"]
                + NCES_AL_MAP["electronic_media"]
                + NCES_AL_MAP["electronic_serials"],
            )
        urban_digital = mapped_digital
    if urban_ebooks.isna().all():
        urban_ebooks = _first_mapped(work, NCES_AL_MAP["electronic_books"])
    if urban_exp.isna().all():
        urban_exp = _first_mapped(work, NCES_AL_MAP["exp_total"])
    if urban_fte.isna().all():
        urban_fte = _first_mapped(work, NCES_AL_MAP["librarians_fte"])
    if urban_staff.isna().all():
        urban_staff = _first_mapped(work, NCES_AL_MAP["total_lib_staff_fte"])
    if urban_pmedia.isna().all():
        urban_pmedia = _first_mapped(work, NCES_AL_MAP["physical_media"])

    if urban_digital.isna().all():
        urban_digital = (
            pd.to_numeric(urban_ebooks, errors="coerce").fillna(0)
            + pd.to_numeric(urban_emedia, errors="coerce").fillna(0)
            + pd.to_numeric(urban_eserials, errors="coerce").fillna(0)
        )
        # If every piece was NA, the 0-fill would fabricate a zero collection.
        any_piece = (
            pd.to_numeric(urban_ebooks, errors="coerce").notna()
            | pd.to_numeric(urban_emedia, errors="coerce").notna()
            | pd.to_numeric(urban_eserials, errors="coerce").notna()
        )
        urban_digital = urban_digital.where(any_piece, pd.NA)

    out["lib_physical_books"] = pd.to_numeric(urban_physical, errors="coerce")
    out["lib_digital_items"] = pd.to_numeric(urban_digital, errors="coerce")
    out["lib_electronic_books"] = pd.to_numeric(urban_ebooks, errors="coerce")
    out["lib_expenditures"] = pd.to_numeric(urban_exp, errors="coerce")
    out["lib_fte"] = pd.to_numeric(urban_fte, errors="coerce")
    out["lib_staff_fte"] = pd.to_numeric(urban_staff, errors="coerce")
    out["lib_physical_media"] = pd.to_numeric(urban_pmedia, errors="coerce")
    out["lib_branches"] = pd.to_numeric(urban_branches, errors="coerce")
    out["lib_source"] = source
    out = replace_sentinels(out, [c for c in out.columns if c not in {"unitid", "year", "lib_source"}])
    out = out.dropna(subset=["unitid", "year"])
    return out


def _first_mapped(df: pd.DataFrame, names: list[str]) -> pd.Series:
    lower = {c.lower(): c for c in df.columns}
    for name in names:
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce")
        if name.lower() in lower:
            return pd.to_numeric(df[lower[name.lower()]], errors="coerce")
    return pd.Series(pd.NA, index=df.index)


def _sum_mapped(df: pd.DataFrame, names: list[str]) -> pd.Series:
    pieces = []
    for name in names:
        series = _first_mapped(df, [name])
        if series.notna().any():
            pieces.append(series)
    if not pieces:
        return pd.Series(pd.NA, index=df.index)
    stacked = pd.concat(pieces, axis=1)
    return stacked.sum(axis=1, min_count=1)


def latest_library_snapshot(al: pd.DataFrame, score_year: int | None) -> pd.DataFrame:
    """One row per UNITID: latest AL year at or before ``score_year``, else latest."""
    if al is None or al.empty:
        return pd.DataFrame()
    work = al.copy()
    work["unitid"] = pd.to_numeric(work["unitid"], errors="coerce")
    work["year"] = pd.to_numeric(work["year"], errors="coerce")
    work = work.dropna(subset=["unitid", "year"]).sort_values(["unitid", "year"])
    if score_year is not None:
        prior = work.loc[work["year"] <= int(score_year)]
        chosen = prior.drop_duplicates("unitid", keep="last")
        missing_ids = set(work["unitid"].unique()) - set(chosen["unitid"].unique())
        if missing_ids:
            extra = work.loc[work["unitid"].isin(missing_ids)].drop_duplicates("unitid", keep="last")
            chosen = pd.concat([chosen, extra], ignore_index=True)
    else:
        chosen = work.drop_duplicates("unitid", keep="last")
    chosen = chosen.rename(columns={"year": "lib_year"})
    return chosen.reset_index(drop=True)


def _libraries_cfg(settings: Settings) -> dict[str, Any]:
    raw = getattr(settings, "raw", None) or {}
    return dict(raw.get("libraries") or {})


def ingest_academic_libraries(
    settings: Settings,
    client: UrbanClient | None = None,
    *,
    force: bool = False,
) -> pd.DataFrame:
    """Download Urban AL CSV (preferred) and write ``libraries.parquet``."""
    dest = settings.processed_dir / "libraries.parquet"
    if dest.exists() and dest.stat().st_size > 0 and not force:
        LOGGER.info("Using cached %s", dest)
        return pd.read_parquet(dest)

    client = client or UrbanClient(settings)
    spec = (getattr(settings, "sources", None) or {}).get("academic_libraries") or {}
    csv_name = spec.get("csv_file") or URBAN_AL_CSV
    csv_dir = spec.get("csv_dir") or URBAN_AL_CSV_DIR
    path = client.download_csv(csv_name, csv_dir)
    if path is None:
        LOGGER.warning("Urban Academic Libraries CSV missing; tried %s/%s/%s", settings.csv_base, csv_dir, csv_name)
        empty = pd.DataFrame(columns=["unitid", "year", "lib_source", *LIB_VALUE_COLS])
        empty.to_parquet(dest, index=False)
        return empty

    raw = read_csv_filtered(path)
    out = normalize_academic_libraries(raw, source="urban")
    settings.processed_dir.mkdir(parents=True, exist_ok=True)
    out.to_parquet(dest, index=False)
    if not out.empty:
        LOGGER.info(
            "Academic Libraries %s rows, years %s–%s -> %s",
            len(out),
            int(out["year"].min()),
            int(out["year"].max()),
            dest,
        )
    return out


def _norm_inst_name(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()
    return re.sub(r"\s+", " ", s).strip()


def parse_arl_member_names(raw_html: str) -> list[str]:
    text, _ = html_to_text_and_links(raw_html)
    names: list[str] = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip(" •-\t")
        if 8 <= len(line) <= 90 and re.search(r"University|College|Library|Institute|Smithsonian", line):
            if re.search(r"join|member directory|association of research", line, re.I):
                continue
            names.append(line)
    return names


def load_arl_members(settings: Settings, session: requests.Session | None = None) -> set[str]:
    cfg = _libraries_cfg(settings)
    cache = settings.raw_dir / "libraries" / "arl_members.json"
    if cache.exists():
        try:
            payload = json.loads(cache.read_text(encoding="utf-8"))
            names = payload.get("names") or []
            if names:
                return {str(n) for n in names}
        except (OSError, json.JSONDecodeError):
            pass

    urls = cfg.get("arl_urls") or [
        "https://www.arl.org/list-of-arl-members/",
        "https://en.wikipedia.org/wiki/List_of_members_of_the_Association_of_Research_Libraries",
    ]
    sess = session or requests.Session()
    names: list[str] = []
    for url in urls:
        try:
            resp = sess.get(
                url,
                timeout=int(cfg.get("request_timeout_seconds", 20)),
                headers={"User-Agent": "college-closure-early-warning/0.2"},
            )
            if resp.status_code == 200 and len(resp.text) > 500:
                names = parse_arl_member_names(resp.text)
                if len(names) >= 20:
                    break
        except requests.RequestException as exc:
            LOGGER.info("ARL list fetch failed %s: %s", url, exc)

    if len(names) < 20:
        names = list(_ARL_FALLBACK_NAMES)
        LOGGER.info("Using built-in ARL member-name snapshot (%s names)", len(names))

    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"names": names}, indent=2), encoding="utf-8")
    return set(names)


def match_arl_member(inst_name: str, arl_names: Iterable[str]) -> bool:
    needle = _norm_inst_name(inst_name)
    if not needle or len(needle) < 6:
        return False
    for raw in arl_names:
        hay = _norm_inst_name(raw)
        if not hay or len(hay) < 6:
            continue
        if needle == hay:
            return True
        # Containment only when the shorter name is long enough to be distinctive
        # ("harvard university" in a longer official string). Never collapse
        # "Notre Dame College" into ARL member "University of Notre Dame".
        shorter, longer = (needle, hay) if len(needle) <= len(hay) else (hay, needle)
        if len(shorter) >= 18 and shorter in longer:
            return True
    return False


def _abs_url(base: str, href: str) -> str | None:
    if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
        return None
    joined = urljoin(base if base.endswith("/") else base + "/", href)
    parsed = urlparse(joined)
    if parsed.scheme not in {"http", "https"}:
        return None
    return joined.split("#")[0]


def normalize_school_url(url: Any) -> str | None:
    if url is None or (isinstance(url, float) and pd.isna(url)):
        return None
    text = str(url).strip()
    if not text or text in {"-1", "-2", "-3", "nan", "None"}:
        return None
    if not re.match(r"^https?://", text, re.I):
        text = "https://" + text.lstrip("/")
    return text.rstrip("/")


def fetch_directory_urls(
    settings: Settings,
    unitids: Iterable[Any],
    year: int,
    client: UrbanClient | None = None,
) -> pd.DataFrame:
    """Look up ``url_school`` for a shortlist via Urban directory API (cached)."""
    ids = sorted({int(u) for u in pd.to_numeric(pd.Series(list(unitids)), errors="coerce").dropna()})
    cache = settings.raw_dir / "libraries" / "directory_urls.json"
    cached: dict[str, Any] = {}
    if cache.exists():
        try:
            cached = json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cached = {}

    client = client or UrbanClient(settings)
    rows = []
    for unitid in ids:
        key = str(unitid)
        if key in cached:
            rows.append(cached[key])
            continue
        path = f"college-university/ipeds/directory/{year}"
        frame = client.fetch_api_pages(path, params={"unitid": unitid}, cache_name=f"dir_url_{year}_{unitid}")
        rec = {"unitid": unitid, "url_school": None, "inst_name": None}
        if not frame.empty:
            rec["url_school"] = frame.iloc[0].get("url_school")
            rec["inst_name"] = frame.iloc[0].get("inst_name")
        cached[key] = rec
        rows.append(rec)
        time.sleep(0.15)

    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(cached, indent=2), encoding="utf-8")
    return pd.DataFrame(rows)


def _cache_html_path(cache_dir: Path, unitid: int, url: str) -> Path:
    slug = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return cache_dir / f"{int(unitid)}_{slug}.html"


def _get_html(
    session: requests.Session,
    url: str,
    dest: Path,
    timeout: int,
    cache_only: bool = False,
) -> str | None:
    if dest.exists() and dest.stat().st_size > 0:
        sidecar = dest.with_suffix(".url")
        if not sidecar.exists():
            sidecar.write_text(url, encoding="utf-8")
        return dest.read_text(encoding="utf-8", errors="replace")
    if cache_only:
        return None
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        if resp.status_code >= 400:
            LOGGER.info("Library page %s -> %s", url, resp.status_code)
            return None
        ctype = (resp.headers.get("Content-Type") or "").lower()
        if "html" not in ctype and "text" not in ctype and ctype:
            return None
        text = resp.text or ""
        if len(text) < 80:
            return None
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        dest.with_suffix(".url").write_text(url, encoding="utf-8")
        return text
    except requests.RequestException as exc:
        LOGGER.info("Library fetch failed %s: %s", url, exc)
        return None


def discover_library_urls(homepage: str, homepage_html: str | None) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()

    def _add(url: str | None) -> None:
        if not url or url in seen:
            return
        seen.add(url)
        urls.append(url)

    parsed = urlparse(homepage)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    host = parsed.netloc
    if host.startswith("www."):
        bare = host[4:]
    else:
        bare = host
    _add(f"{parsed.scheme}://library.{bare}")
    _add(f"{parsed.scheme}://libraries.{bare}")
    for path in _LIBRARY_PATHS:
        _add(origin + path)
    if homepage_html:
        _text, hrefs = html_to_text_and_links(homepage_html)
        for href in hrefs:
            abs_url = _abs_url(homepage, href)
            if abs_url and _LIBRARY_HREF_RE.search(abs_url):
                _add(abs_url)
    return urls[:20]


def scrape_library_notes(
    schools: pd.DataFrame,
    settings: Settings,
    session: requests.Session | None = None,
    cache_only: bool = False,
) -> pd.DataFrame:
    """Fetch library / special-collections pages for a shortlist; cache HTML."""
    cfg = _libraries_cfg(settings)
    timeout = int(cfg.get("request_timeout_seconds", 20))
    cache_only = cache_only or bool(cfg.get("cache_only", False))
    cache_dir = settings.raw_dir / "libraries" / "html"
    cache_dir.mkdir(parents=True, exist_ok=True)
    sess = session or requests.Session()
    sess.headers.update(
        {
            "User-Agent": (
                "college-closure-early-warning/0.2 "
                "(+https://github.com/atnickallen/college-closure-early-warning)"
            ),
            "Accept": "text/html,application/xhtml+xml",
        }
    )

    records = []
    for _, row in schools.iterrows():
        unitid = int(row["unitid"])
        name = str(row.get("inst_name") or f"UNITID {unitid}")
        home = normalize_school_url(row.get("url_school"))
        best = {
            "unitid": unitid,
            "lib_special_collections_note": UNKNOWN_NOTE,
            "lib_unique_flag": False,
            "lib_note_url": pd.NA,
        }
        if not home:
            records.append(best)
            continue

        home_dest = _cache_html_path(cache_dir, unitid, home)
        home_html = _get_html(sess, home, home_dest, timeout, cache_only=cache_only)
        if home_html is None:
            parsed = urlparse(home)
            host = parsed.netloc[4:] if parsed.netloc.startswith("www.") else parsed.netloc
            candidates = [f"{parsed.scheme}://library.{host}"]
        else:
            candidates = discover_library_urls(home, home_html)
        # Prefer collection/archive URLs, then generic library pages, then homepage.
        def _rank(url: str) -> tuple[int, int]:
            u = url.lower()
            if "special" in u or "rare" in u or "archive" in u:
                return (0, len(u))
            if "library" in u:
                return (1, len(u))
            return (2, len(u))

        ordered = sorted(candidates, key=_rank)
        if home not in ordered:
            ordered.append(home)

        found_any_page = False
        seen_urls = set(ordered)
        idx = 0
        while idx < len(ordered) and idx < 10:
            url = ordered[idx]
            idx += 1
            dest = _cache_html_path(cache_dir, unitid, url)
            html_text = (
                home_html
                if url.rstrip("/") == home.rstrip("/")
                else _get_html(sess, url, dest, timeout, cache_only=cache_only)
            )
            if not html_text:
                continue
            found_any_page = True
            extracted = extract_special_collections_note(html_text, page_url=url)
            if not extracted["unique_flag"]:
                _text, hrefs = html_to_text_and_links(html_text)
                for href in hrefs:
                    extra = _abs_url(url, href)
                    if (
                        extra
                        and extra not in seen_urls
                        and re.search(r"special|rare|archive|digitalcollect", extra, re.I)
                    ):
                        seen_urls.add(extra)
                        ordered.append(extra)
            if extracted["unique_flag"]:
                best = {
                    "unitid": unitid,
                    "lib_special_collections_note": extracted["note"],
                    "lib_unique_flag": True,
                    "lib_note_url": extracted.get("source_url") or url,
                }
                break
            if extracted["note"] and extracted["note"] != UNKNOWN_NOTE:
                best = {
                    "unitid": unitid,
                    "lib_special_collections_note": extracted["note"],
                    "lib_unique_flag": False,
                    "lib_note_url": extracted.get("source_url") or url,
                }
        if cache_only and not best.get("lib_unique_flag"):
            for cached in sorted(cache_dir.glob(f"{int(unitid)}_*.html")):
                sidecar = cached.with_suffix(".url")
                page_url = sidecar.read_text(encoding="utf-8").strip() if sidecar.exists() else None
                if page_url and not _LIBRARY_HREF_RE.search(page_url) and found_any_page:
                    continue
                html_text = cached.read_text(encoding="utf-8", errors="replace")
                extracted = extract_special_collections_note(html_text, page_url=page_url)
                if not extracted["unique_flag"]:
                    continue
                found_any_page = True
                best = {
                    "unitid": unitid,
                    "lib_special_collections_note": extracted["note"],
                    "lib_unique_flag": True,
                    "lib_note_url": extracted.get("source_url") or page_url or pd.NA,
                }
                break
        if not found_any_page:
            best["lib_special_collections_note"] = (
                f"Unknown — public website did not yield a usable library page for {name}."
            )
        records.append(best)
        if not cache_only:
            time.sleep(float(cfg.get("scrape_pause_seconds", 0.35)))

    return pd.DataFrame(records)


def attach_library_columns(
    watch: pd.DataFrame,
    snapshot: pd.DataFrame,
    notes: pd.DataFrame | None = None,
    arl_names: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Left-join AL snapshot + optional scrape notes. Never fills holdings with zeros."""
    out = watch.copy()
    out["unitid"] = pd.to_numeric(out["unitid"], errors="coerce")
    drop_existing = [c for c in (*LIB_WATCHLIST_COLS, *LIB_VALUE_COLS) if c in out.columns]
    if drop_existing:
        out = out.drop(columns=drop_existing)
    keep = ["unitid", "lib_year", "lib_source", *LIB_VALUE_COLS]
    if snapshot is None or snapshot.empty:
        slim = pd.DataFrame(columns=keep)
    else:
        slim = snapshot[[c for c in keep if c in snapshot.columns]].drop_duplicates("unitid")
    out = out.merge(slim, on="unitid", how="left")

    if notes is not None and not notes.empty:
        note_cols = [
            c
            for c in (
                "unitid",
                "lib_special_collections_note",
                "lib_unique_flag",
                "lib_note_url",
                "lib_oclc_symbol",
                "lib_worldcat_registry_id",
                "lib_libraries_org_id",
            )
            if c in notes.columns
        ]
        out = out.merge(notes[note_cols].drop_duplicates("unitid"), on="unitid", how="left")
    if "lib_special_collections_note" not in out.columns:
        out["lib_special_collections_note"] = pd.NA
    if "lib_unique_flag" not in out.columns:
        out["lib_unique_flag"] = False
    if "lib_note_url" not in out.columns:
        out["lib_note_url"] = pd.NA
    for col in ("lib_oclc_symbol", "lib_worldcat_registry_id", "lib_libraries_org_id"):
        if col not in out.columns:
            out[col] = pd.NA

    arl_names = list(arl_names or [])
    if "inst_name" in out.columns:
        out["lib_arl_member"] = out["inst_name"].map(lambda n: match_arl_member(n, arl_names) if pd.notna(n) else False)
    else:
        out["lib_arl_member"] = False
    # ARL membership is independently notable even without a scrape hit.
    out["lib_unique_flag"] = (
        out["lib_unique_flag"].fillna(False).astype(bool) | out["lib_arl_member"].astype(bool)
    )
    missing_note = out["lib_special_collections_note"].isna() | (
        out["lib_special_collections_note"].astype("string").str.strip() == ""
    )
    out.loc[missing_note, "lib_special_collections_note"] = OUTSIDE_SHORTLIST_NOTE
    return out


def enrich_watchlist_libraries(
    watch: pd.DataFrame,
    settings: Settings,
    *,
    score_year: int | None = None,
    scrape_ids: Iterable[Any] | None = None,
    academic_libraries: pd.DataFrame | None = None,
    skip_scrape: bool = False,
    cache_only: bool = False,
    client: UrbanClient | None = None,
    session: requests.Session | None = None,
) -> pd.DataFrame:
    """Attach AL numbers (all rows) and scraped notes (shortlist UNITIDs)."""
    al = academic_libraries if academic_libraries is not None else ingest_academic_libraries(settings, client=client)
    snapshot = latest_library_snapshot(al, score_year)
    notes = pd.DataFrame()
    schools = pd.DataFrame()
    ids: list[int] = []
    if scrape_ids is not None:
        ids = [int(u) for u in pd.to_numeric(pd.Series(list(scrape_ids)), errors="coerce").dropna()]
        schools = watch.loc[watch["unitid"].isin(ids), ["unitid", "inst_name"]].drop_duplicates("unitid")
    if not skip_scrape and ids:
        year = int(score_year or watch["year"].max())
        urls = fetch_directory_urls(settings, ids, year, client=client)
        schools = schools.merge(urls, on="unitid", how="left")
        if "inst_name_x" in schools.columns:
            schools["inst_name"] = schools["inst_name_x"].fillna(schools.get("inst_name_y"))
        notes = scrape_library_notes(
            schools, settings, session=session, cache_only=cache_only
        )
    if ids:
        notes, registry = enrich_worldcat_shortlist(
            schools if not schools.empty else watch.loc[watch["unitid"].isin(ids), ["unitid", "inst_name"]],
            settings,
            html_notes=notes if not notes.empty else None,
            session=session,
            cache_only=cache_only,
            skip_live=skip_scrape,
        )
        write_oclc_crosswalk(registry, settings.outputs_dir / "libraries_oclc_crosswalk.csv")
    arl = load_arl_members(settings, session=session) if not skip_scrape else set(_ARL_FALLBACK_NAMES)
    if skip_scrape:
        arl = set(_ARL_FALLBACK_NAMES)
    return attach_library_columns(watch, snapshot, notes if not notes.empty else None, arl)


def distinctive_notes_html(shortlist: pd.DataFrame) -> str:
    """Banner listing named collections on the top-50 ∪ nonprofit shortlist."""
    if shortlist is None or shortlist.empty or "lib_unique_flag" not in shortlist.columns:
        return ""
    unique = shortlist.loc[shortlist["lib_unique_flag"].fillna(False).astype(bool)]
    if unique.empty:
        return ""
    items = []
    for _, row in unique.iterrows():
        name = html_mod.escape(str(row.get("inst_name") or f"UNITID {row.get('unitid')}"))
        note = html_mod.escape(str(row.get("lib_special_collections_note") or "").strip())
        items.append(f"<li><strong>{name}</strong> — {note}</li>")
    return (
        '<div class="banner lib-unique">'
        "<strong>Distinctive collections on the shortlist</strong> "
        "(top 50 ∪ nonprofit). Named holdings only when WorldCat/public sources "
        "or a cited transfer notice support them; other cards say unknown or "
        "nothing distinctive."
        f"<ul>{''.join(items)}</ul></div>"
    )


def write_libraries_summary(shortlist: pd.DataFrame, dest: Path) -> Path:
    """Markdown summary of unique / unknown library findings for the shortlist."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    rows = shortlist.copy()
    n = len(rows)
    n_al = int(rows["lib_physical_books"].notna().sum()) if "lib_physical_books" in rows.columns else 0
    n_unique = int(rows["lib_unique_flag"].fillna(False).astype(bool).sum()) if "lib_unique_flag" in rows.columns else 0
    lines = [
        "# Libraries & book collections — watch-list shortlist",
        "",
        "Enrichment context for the elevated-risk watch list (top 50 plus the",
        "nonprofit shortlist). **Not a closure verdict** and **not a model feature**.",
        "Holdings and expenditures are IPEDS Academic Libraries via the Urban",
        "Institute Education Data Portal. Unique notes come from campus pages,",
        "libraries.org (UNITID = NCES LIBID → OCLC / WorldCat Registry), ArchiveGrid",
        "when reachable, and cited transfer notices. Missing AL or a failed",
        "lookup means unknown — not that the school has no library. Collection",
        "sizes are never invented from WorldCat or libraries.org volume counts.",
        "",
        f"- Shortlist rows: **{n}**",
        f"- Rows with any IPEDS AL physical-book count: **{n_al}**",
        f"- Rows with a named distinctive collection / ARL flag: **{n_unique}**",
        "",
        "## Distinctive / unique notes",
        "",
    ]
    unique = rows.loc[rows.get("lib_unique_flag", False) == True]  # noqa: E712
    if unique.empty:
        lines.append("_No named special collections were extracted for this shortlist._")
        lines.append("")
    else:
        for _, row in unique.iterrows():
            lines.append(f"### {row.get('inst_name')} (UNITID {row.get('unitid')})")
            lines.append("")
            lines.append(f"- AL year: {_md_year(row.get('lib_year'))}")
            lines.append(f"- Physical books: {_md_num(row.get('lib_physical_books'))}")
            lines.append(f"- Digital items: {_md_num(row.get('lib_digital_items'))}")
            lines.append(f"- Expenditures: {_md_money(row.get('lib_expenditures'))}")
            lines.append(f"- Librarian FTE: {_md_num(row.get('lib_fte'), digits=1)}")
            lines.append(f"- ARL member: {'yes' if bool(row.get('lib_arl_member')) else 'no / not listed'}")
            lines.append(f"- OCLC symbol: {_md_id(row.get('lib_oclc_symbol'))}")
            lines.append(f"- Note: {row.get('lib_special_collections_note')}")
            lines.append("")

    lines.extend(["## Other shortlist schools", ""])
    other = rows.loc[rows.get("lib_unique_flag", False) != True]  # noqa: E712
    for _, row in other.iterrows():
        lines.append(
            f"- **{row.get('inst_name')}** (UNITID {row.get('unitid')}): "
            f"physical books {_md_num(row.get('lib_physical_books'))}; "
            f"{row.get('lib_special_collections_note')}"
        )
    lines.append("")
    dest.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("Wrote %s", dest)
    return dest


def _md_id(v: Any) -> str:
    if v is None:
        return "unknown"
    try:
        if pd.isna(v):
            return "unknown"
    except (TypeError, ValueError):
        pass
    text = str(v).strip()
    if text.lower() in {"", "nan", "none", "<na>"}:
        return "unknown"
    return text


def _md_year(v: Any) -> str:
    if v is None:
        return "unknown"
    try:
        if pd.isna(v):
            return "unknown"
        return str(int(v))
    except (TypeError, ValueError):
        return "unknown"


def _md_num(v: Any, digits: int = 0) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "unknown"
    try:
        if pd.isna(v):
            return "unknown"
        x = float(v)
    except (TypeError, ValueError):
        return "unknown"
    if digits == 0:
        return f"{int(round(x)):,}"
    return f"{x:.{digits}f}"


def _md_money(v: Any) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "unknown"
    try:
        if pd.isna(v):
            return "unknown"
        return f"${int(round(float(v))):,}"
    except (TypeError, ValueError):
        return "unknown"


def library_section_html(row: pd.Series) -> str:
    """Evidence-card block. Framing: enrichment context, not a verdict."""

    def _esc(s: Any) -> str:
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return "—"
        try:
            if pd.isna(s):
                return "—"
        except (TypeError, ValueError):
            pass
        return html_mod.escape(str(s))

    def _count(v: Any) -> str:
        if v is None:
            return "—"
        try:
            if pd.isna(v):
                return "—"
            return f"{int(round(float(v))):,}"
        except (TypeError, ValueError):
            return "—"

    def _money(v: Any) -> str:
        if v is None:
            return "—"
        try:
            if pd.isna(v):
                return "—"
            return f"${int(round(float(v))):,}"
        except (TypeError, ValueError):
            return "—"

    def _fte(v: Any) -> str:
        if v is None:
            return "—"
        try:
            if pd.isna(v):
                return "—"
            return f"{float(v):.1f}"
        except (TypeError, ValueError):
            return "—"

    year = row.get("lib_year")
    year_txt = "—"
    try:
        if year is not None and not pd.isna(year):
            year_txt = str(int(year))
    except (TypeError, ValueError):
        year_txt = _esc(year)
    def _truthy(v: Any) -> bool:
        try:
            if v is None or pd.isna(v):
                return False
        except (TypeError, ValueError):
            return False
        return bool(v)

    arl = "yes (public ARL list)" if _truthy(row.get("lib_arl_member")) else "no / not listed"
    note = row.get("lib_special_collections_note")
    if note is None or (isinstance(note, float) and pd.isna(note)) or str(note).strip() == "":
        note_html = UNKNOWN_NOTE
    else:
        note_html = html_mod.escape(str(note))
    unique = "yes" if _truthy(row.get("lib_unique_flag")) else "no"
    return f"""
      <h3>Libraries &amp; collections</h3>
      <p class="lib-context">Enrichment context — cultural / asset value that may be at
      stake, not a model feature and not a closure verdict. IPEDS Academic Libraries
      counts are unknown when the survey cell is missing; that is not evidence the
      school has no library. Notes use campus pages plus WorldCat/public
      identifiers (libraries.org NCES LIBID) and cited transfer notices.</p>
      <table>
        <tr><th>Physical books</th><td>{_count(row.get("lib_physical_books"))}</td>
            <th>Digital items</th><td>{_count(row.get("lib_digital_items"))}</td></tr>
        <tr><th>Library expenditures</th><td>{_money(row.get("lib_expenditures"))}</td>
            <th>Librarian FTE</th><td>{_fte(row.get("lib_fte"))}</td></tr>
        <tr><th>AL year / source</th><td>{year_txt} / {_esc(row.get("lib_source"))}</td>
            <th>ARL member</th><td>{_esc(arl)}</td></tr>
        <tr><th>Unique / notable</th><td>{unique}</td>
            <th>OCLC symbol</th><td>{_esc(row.get("lib_oclc_symbol"))}</td></tr>
      </table>
      <p class="lib-note">{note_html}</p>
    """
