"""WorldCat / libraries.org / ArchiveGrid enrichment (not a model feature).

OCLC's Library Profiles API and the old WorldCat Registry API need a WSKey
(the public Registry API was retired 2025-11-30). This module uses public
HTML that still exposes the same identifiers:

- libraries.org (Library Technology Guides): OCLC symbol, WorldCat Registry
  ID, and NCES LIBID (typically the IPEDS UNITID). That is the UNITID→OCLC
  crosswalk.
- ArchiveGrid (researchworks.oclc.org) collection titles, when the page is
  reachable.
- A committed, cited overlay for collection *transfers* that no catalog API
  will emit (e.g. Finlandia → Finlandia Foundation National).

Never copy libraries.org volume counts into ``lib_physical_books`` — IPEDS AL
remains the holdings source. Missing / generic circulating stock is stated as
no distinctive special collections found in WorldCat/public sources.
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote_plus

import pandas as pd
import requests

from college_closure.config import Settings

LOGGER = logging.getLogger(__name__)

LIBRARIES_ORG_BASE = "https://librarytechnology.org"
ARCHIVEGRID_SEARCH = "https://researchworks.oclc.org/archivegrid/"
WORLDCAT_REGISTRY_SEARCH = "https://registry.worldcat.org/"

NOTHING_WORLDCAT_NOTE = (
    "No distinctive special collections found in WorldCat/public sources "
    "(libraries.org identifiers, ArchiveGrid, and cited transfer notices). "
    "Generic circulating stock is not treated as a rare-book claim."
)

CROSSWALK_COLS = [
    "unitid",
    "inst_name",
    "oclc_symbol",
    "worldcat_registry_id",
    "libraries_org_id",
    "related_oclc_symbol",
    "related_note",
    "source",
    "source_url",
]

_OCLC_SYMBOL_RE = re.compile(
    r"OCLC\s*</span>\s*Symbol</th>\s*<td>\s*([A-Z0-9]{3,5})\s*</td>",
    re.I,
)
_REGISTRY_RE = re.compile(
    r"WorldCat Registry ID</th>\s*<td>(?:<a[^>]*>)?\s*(\d+)",
    re.I,
)
_NCES_RE = re.compile(r"NCES LIBID</th>\s*<td>\s*(\d+)\s*</td>", re.I)
_LT_ID_RE = re.compile(r"libraries\.org ID</th>\s*<td>\s*(\d+)\s*</td>", re.I)
_LT_TITLE_RE = re.compile(r"<h2[^>]*>\s*(.*?)\s*</h2>", re.I | re.S)
_LT_SEARCH_ACTION_RE = re.compile(
    r'action="https?://librarytechnology\.org/library/(\d+)"',
    re.I,
)
_LT_SEARCH_NAME_RE = re.compile(
    r'value="([^"]+)"[^>]*class="SubmitLink"|class="SubmitLink"\s+value="([^"]+)"',
    re.I,
)
_ARCHIVEGRID_TITLE_RE = re.compile(
    r"<h2[^>]*>\s*(?:<a[^>]*>)?\s*([^<]{12,180})\s*(?:</a>)?\s*</h2>",
    re.I,
)
_TAG_RE = re.compile(r"<[^>]+>")


def parse_libraries_org_profile(raw_html: str) -> dict[str, Any]:
    """Pull OCLC / Registry / NCES identifiers from a libraries.org profile."""
    text = raw_html or ""
    title_m = _LT_TITLE_RE.search(text)
    title = _TAG_RE.sub("", title_m.group(1)).strip() if title_m else ""
    title = re.sub(r"\s+", " ", title)
    oclc = _OCLC_SYMBOL_RE.search(text)
    registry = _REGISTRY_RE.search(text)
    nces = _NCES_RE.search(text)
    ltid = _LT_ID_RE.search(text)
    consortia = []
    for label in ("SEO Library Consortium", "SCELC", "Northern Michigan University Consortium"):
        if label.lower() in text.lower():
            consortia.append(label)
    return {
        "library_name": title or None,
        "oclc_symbol": oclc.group(1).upper() if oclc else None,
        "worldcat_registry_id": registry.group(1) if registry else None,
        "nces_libid": int(nces.group(1)) if nces else None,
        "libraries_org_id": int(ltid.group(1)) if ltid else None,
        "closed": bool(re.search(r"PERMANENTLY CLOSED", text, re.I)),
        "consortia": consortia,
    }


def parse_libraries_org_search(raw_html: str) -> list[dict[str, Any]]:
    """Collect profile IDs and display names from a libraries.org search page."""
    html = raw_html or ""
    hits = []
    for block in re.split(r"<form\b", html, flags=re.I):
        act = _LT_SEARCH_ACTION_RE.search(block)
        if not act:
            continue
        name_m = re.search(r'class="SubmitLink"\s+value="([^"]+)"', block, re.I)
        if not name_m:
            name_m = re.search(r'value="([^"]+)"\s+class="SubmitLink"', block, re.I)
        hits.append(
            {
                "libraries_org_id": int(act.group(1)),
                "library_name": name_m.group(1) if name_m else None,
                "profile_url": f"{LIBRARIES_ORG_BASE}/library/{act.group(1)}",
            }
        )
    # de-dupe preserving order
    seen: set[int] = set()
    out = []
    for hit in hits:
        lid = hit["libraries_org_id"]
        if lid in seen:
            continue
        seen.add(lid)
        out.append(hit)
    return out


def parse_archivegrid_hits(raw_html: str, institution_name: str) -> list[dict[str, str]]:
    """Keep ArchiveGrid collection titles that mention the institution."""
    if not raw_html or "archivegrid" not in raw_html.lower():
        return []
    needle = re.sub(r"\s+", " ", institution_name or "").strip().lower()
    if len(needle) < 6:
        return []
    tokens = [t for t in re.findall(r"[a-z0-9']{4,}", needle) if t not in {"college", "university", "the"}]
    hits = []
    for title in _ARCHIVEGRID_TITLE_RE.findall(raw_html):
        clean = re.sub(r"\s+", " ", title).strip()
        low = clean.lower()
        if needle in low or (tokens and all(t in low for t in tokens[:2])):
            hits.append({"title": clean})
    return hits[:8]


def load_oclc_crosswalk(settings: Settings | None = None, path: Path | None = None) -> pd.DataFrame:
    dest = path
    if dest is None and settings is not None:
        dest = Path(settings.raw.get("paths", {}).get("root", ".")) if False else None
    if dest is None:
        root = Path(__file__).resolve().parents[2]
        dest = root / "data" / "external" / "oclc_unitid_crosswalk.csv"
    if not dest.exists():
        return pd.DataFrame(columns=CROSSWALK_COLS)
    frame = pd.read_csv(dest, dtype=str)
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    return frame


def load_authority_notes(settings: Settings | None = None, path: Path | None = None) -> pd.DataFrame:
    if path is None:
        path = Path(__file__).resolve().parents[2] / "data" / "external" / "library_authority_notes.csv"
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path, dtype=str)
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    if "unique_flag" in frame.columns:
        frame["unique_flag"] = frame["unique_flag"].astype(str).str.lower().isin({"1", "true", "yes"})
    return frame


def merge_worldcat_into_notes(
    html_notes: pd.DataFrame,
    authority: pd.DataFrame,
    registry: pd.DataFrame,
) -> pd.DataFrame:
    """Overlay sourced WorldCat/transfer notes onto campus-HTML notes.

    Authority unique notes win. Identifiers always attach. Holdings columns
    are not present here and must not be invented.
    """
    base = html_notes.copy() if html_notes is not None and not html_notes.empty else pd.DataFrame()
    if "unitid" not in base.columns:
        ids = []
        if authority is not None and not authority.empty:
            ids.extend(authority["unitid"].tolist())
        if registry is not None and not registry.empty:
            ids.extend(registry["unitid"].tolist())
        base = pd.DataFrame({"unitid": pd.to_numeric(pd.Series(ids), errors="coerce").dropna().unique()})
    base["unitid"] = pd.to_numeric(base["unitid"], errors="coerce")
    if "lib_special_collections_note" not in base.columns:
        base["lib_special_collections_note"] = pd.NA
        base["lib_unique_flag"] = False
        base["lib_note_url"] = pd.NA

    if registry is not None and not registry.empty:
        slim = registry.copy()
        slim["unitid"] = pd.to_numeric(slim["unitid"], errors="coerce")
        keep = [c for c in ("unitid", "oclc_symbol", "worldcat_registry_id", "libraries_org_id", "related_oclc_symbol", "related_note", "source_url") if c in slim.columns]
        base = base.drop(columns=[c for c in keep if c != "unitid" and c in base.columns], errors="ignore")
        base = base.merge(slim[keep].drop_duplicates("unitid"), on="unitid", how="left")
    for col in ("oclc_symbol", "worldcat_registry_id", "libraries_org_id", "related_oclc_symbol", "related_note"):
        if col not in base.columns:
            base[col] = pd.NA

    if authority is not None and not authority.empty:
        auth = authority.dropna(subset=["unitid"]).copy()
        by_id = {int(r.unitid): r for r in auth.itertuples(index=False)}
        notes = base["lib_special_collections_note"].astype("string")
        unique = base["lib_unique_flag"].fillna(False).astype(bool)
        urls = base["lib_note_url"]
        for i, row in base.iterrows():
            uid = row.get("unitid")
            if pd.isna(uid):
                continue
            rec = by_id.get(int(uid))
            if rec is None:
                continue
            auth_unique = bool(getattr(rec, "unique_flag", False))
            auth_note = str(getattr(rec, "note", "") or "").strip()
            auth_url = str(getattr(rec, "source_url", "") or "").strip() or pd.NA
            if auth_unique and auth_note:
                notes.loc[i] = auth_note
                unique.loc[i] = True
                urls.loc[i] = auth_url
            elif auth_note and not unique.loc[i]:
                notes.loc[i] = auth_note
                urls.loc[i] = auth_url
        base["lib_special_collections_note"] = notes
        base["lib_unique_flag"] = unique
        base["lib_note_url"] = urls

    # If we resolved a libraries.org / OCLC row but still have no unique note,
    # replace campus-unknown with the WorldCat-negative wording.
    have_id = base["oclc_symbol"].notna() | base["libraries_org_id"].notna()
    not_unique = ~base["lib_unique_flag"].fillna(False).astype(bool)
    note_s = base["lib_special_collections_note"].astype("string").fillna("")
    weak = note_s.str.contains("Unknown —|nothing distinctive|Web note not collected", case=False, regex=True)
    upgrade = have_id & not_unique & weak
    base.loc[upgrade, "lib_special_collections_note"] = NOTHING_WORLDCAT_NOTE

    base = base.rename(
        columns={
            "oclc_symbol": "lib_oclc_symbol",
            "worldcat_registry_id": "lib_worldcat_registry_id",
            "libraries_org_id": "lib_libraries_org_id",
        }
    )
    return base


def _cache_path(cache_dir: Path, kind: str, key: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", key)[:80]
    return cache_dir / f"{kind}_{safe}.html"


def _get(session: requests.Session, url: str, dest: Path, timeout: int, cache_only: bool) -> str | None:
    if dest.exists() and dest.stat().st_size > 80:
        return dest.read_text(encoding="utf-8", errors="replace")
    if cache_only:
        return None
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        if resp.status_code >= 400:
            LOGGER.info("WorldCat/LT fetch %s -> %s", url, resp.status_code)
            return None
        text = resp.text or ""
        if len(text) < 80:
            return None
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        dest.with_suffix(".url").write_text(url, encoding="utf-8")
        return text
    except requests.RequestException as exc:
        LOGGER.info("WorldCat/LT fetch failed %s: %s", url, exc)
        return None


def lookup_libraries_org(
    schools: pd.DataFrame,
    settings: Settings,
    session: requests.Session | None = None,
    cache_only: bool = False,
) -> pd.DataFrame:
    """Search libraries.org by name; accept a profile only when NCES LIBID == UNITID."""
    cfg = (getattr(settings, "raw", None) or {}).get("libraries") or {}
    timeout = int(cfg.get("request_timeout_seconds", 20))
    cache_dir = settings.raw_dir / "libraries" / "worldcat"
    cache_dir.mkdir(parents=True, exist_ok=True)
    sess = session or requests.Session()
    sess.headers.update(
        {
            "User-Agent": (
                "college-closure-early-warning/0.2 "
                "(+https://github.com/atnickallen/college-closure-early-warning)"
            ),
            "Accept": "text/html",
        }
    )
    records = []
    for _, row in schools.iterrows():
        unitid = int(row["unitid"])
        name = str(row.get("inst_name") or "")
        rec = {
            "unitid": unitid,
            "inst_name": name,
            "oclc_symbol": pd.NA,
            "worldcat_registry_id": pd.NA,
            "libraries_org_id": pd.NA,
            "related_oclc_symbol": pd.NA,
            "related_note": pd.NA,
            "source": pd.NA,
            "source_url": pd.NA,
        }
        query = quote_plus(name)
        search_url = f"{LIBRARIES_ORG_BASE}/libraries/search.pl?Name={query}"
        search_html = _get(sess, search_url, _cache_path(cache_dir, "search", f"{unitid}_{name}"), timeout, cache_only)
        candidates = parse_libraries_org_search(search_html or "")
        # Prefer a previously known libraries.org id from the committed crosswalk later;
        # here try the first few search hits.
        for hit in candidates[:6]:
            lid = hit["libraries_org_id"]
            prof_url = f"{LIBRARIES_ORG_BASE}/library/{lid}"
            prof_html = _get(sess, prof_url, _cache_path(cache_dir, "profile", str(lid)), timeout, cache_only)
            parsed = parse_libraries_org_profile(prof_html or "")
            if parsed.get("nces_libid") == unitid:
                rec.update(
                    {
                        "oclc_symbol": parsed.get("oclc_symbol") or pd.NA,
                        "worldcat_registry_id": parsed.get("worldcat_registry_id") or pd.NA,
                        "libraries_org_id": lid,
                        "source": "libraries.org",
                        "source_url": prof_url,
                    }
                )
                break
        if pd.isna(rec["libraries_org_id"]) and not cache_only:
            time.sleep(float(cfg.get("scrape_pause_seconds", 0.25)))
        records.append(rec)
    return pd.DataFrame(records)


def combine_registry_tables(committed: pd.DataFrame, live: pd.DataFrame) -> pd.DataFrame:
    """Live NCES-matched rows fill blanks; committed rows win when already sourced."""
    cols = CROSSWALK_COLS
    empty = pd.DataFrame(columns=cols)
    left = committed.copy() if committed is not None and not committed.empty else empty.copy()
    right = live.copy() if live is not None and not live.empty else empty.copy()
    for frame in (left, right):
        if "unitid" in frame.columns:
            frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
        for c in cols:
            if c not in frame.columns:
                frame[c] = pd.NA
    if left.empty:
        return right[cols] if not right.empty else empty
    if right.empty:
        return left[cols]
    merged = left.merge(right, on="unitid", how="outer", suffixes=("_c", "_l"))
    out = pd.DataFrame({"unitid": merged["unitid"]})
    for c in cols:
        if c == "unitid":
            continue
        a, b = f"{c}_c", f"{c}_l"
        out[c] = merged[a].where(merged[a].notna() & (merged[a].astype(str).str.strip() != ""), merged[b])
    return out


def write_oclc_crosswalk(frame: pd.DataFrame, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cols = [c for c in CROSSWALK_COLS if c in frame.columns]
    frame[cols].drop_duplicates("unitid").to_csv(dest, index=False)
    LOGGER.info("Wrote %s (%s rows)", dest, len(frame))
    return dest


def enrich_worldcat_shortlist(
    schools: pd.DataFrame,
    settings: Settings,
    *,
    html_notes: pd.DataFrame | None = None,
    session: requests.Session | None = None,
    cache_only: bool = False,
    skip_live: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (notes_with_ids, crosswalk). Live libraries.org is optional."""
    committed = load_oclc_crosswalk(settings)
    live = pd.DataFrame()
    if not skip_live:
        live = lookup_libraries_org(schools, settings, session=session, cache_only=cache_only)
    registry = combine_registry_tables(committed, live)
    # Seed libraries.org ids from committed so cache-only still attaches IDs.
    authority = load_authority_notes(settings)
    notes = merge_worldcat_into_notes(html_notes if html_notes is not None else pd.DataFrame(), authority, registry)
    return notes, registry
