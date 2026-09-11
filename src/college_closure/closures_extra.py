"""Supplemental closure/merger lists (Higher Ed Dive, BestColleges) — labels only."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import pandas as pd
import requests

from college_closure.config import Settings
from college_closure.download import DEFAULT_HEADERS
from college_closure.ids import add_id_keys

LOGGER = logging.getLogger(__name__)

YEAR_RE = re.compile(r"\b(20[0-2]\d)\b")
# "Name closed in 2023" / "Name will merge with X in 2024"
ROW_RE = re.compile(
    r"(?P<name>[A-Z][^.\n]{5,90}?)\s+(?P<verb>closed|will close|shut down|merged|will merge|is merging|announced it would close)"
    r"(?:[^.\n]{0,80}?\b(?P<year>20[0-2]\d)\b)?",
    flags=re.I,
)


def _get(url: str, dest: Path, timeout: int = 40) -> str | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 500:
        return dest.read_text(encoding="utf-8", errors="replace")
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        if resp.status_code >= 400:
            LOGGER.warning("Closure page %s: %s", resp.status_code, url)
            return None
        dest.write_text(resp.text, encoding="utf-8")
        return resp.text
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Closure page failed %s: %s", url, exc)
        return None


def _clean_name(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip(" \t:-–—")
    text = re.sub(r"^(the)\s+", "", text, flags=re.I)
    return text[:120]


def parse_tracker_html(html: str, source: str) -> pd.DataFrame:
    """Conservative regex extract — keep only rows with a 20xx year."""
    rows = []
    # Prefer list items / table cells
    chunks = re.findall(r"<li[^>]*>(.*?)</li>|<tr[^>]*>(.*?)</tr>|<p[^>]*>(.*?)</p>", html, flags=re.I | re.S)
    texts = []
    for a, b, c in chunks:
        blob = a or b or c
        blob = re.sub(r"<[^>]+>", " ", blob)
        blob = re.sub(r"&amp;", "&", blob)
        blob = re.sub(r"&nbsp;", " ", blob)
        blob = re.sub(r"\s+", " ", blob).strip()
        if 15 < len(blob) < 240:
            texts.append(blob)
    if not texts:
        plain = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
        plain = re.sub(r"<[^>]+>", " ", plain)
        texts = [re.sub(r"\s+", " ", t).strip() for t in plain.split(".") if 15 < len(t) < 240]
    for text in texts:
        years = YEAR_RE.findall(text)
        if not years:
            continue
        year = int(years[-1])
        if year < 2005 or year > 2030:
            continue
        m = ROW_RE.search(text)
        if not m:
            continue
        name = _clean_name(m.group("name"))
        if len(name) < 6:
            continue
        verb = m.group("verb").lower()
        etype = "merger" if "merge" in verb else "closure"
        # state if ", XX" present
        st = re.search(r",\s*([A-Z]{2})\b", text)
        rows.append(
            {
                "inst_name": name,
                "state_abbr": st.group(1) if st else "",
                "event_year": year,
                "event_type": etype,
                "event_source": source,
                "raw_text": text[:240],
            }
        )
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows).drop_duplicates(subset=["inst_name", "event_year", "event_source"])
    return out


def _match_to_directory(events: pd.DataFrame, directory: pd.DataFrame) -> pd.DataFrame:
    """Unique name(+state) matches only — never fuzzy-join the full panel."""
    if events.empty or directory.empty:
        return pd.DataFrame()
    d = add_id_keys(directory)
    d["unitid"] = pd.to_numeric(d["unitid"], errors="coerce")
    name_col = "inst_name" if "inst_name" in d.columns else None
    if name_col is None:
        return pd.DataFrame()
    d["_key"] = d[name_col].astype("string").str.lower().str.replace(r"[^a-z0-9]+", " ", regex=True).str.strip()
    d["_st"] = d["state_abbr"].astype("string").str.upper() if "state_abbr" in d.columns else ""
    # latest directory row per unitid for name
    d = d.sort_values("year").drop_duplicates("unitid", keep="last")
    ev = events.copy()
    ev["_key"] = ev["inst_name"].astype("string").str.lower().str.replace(r"[^a-z0-9]+", " ", regex=True).str.strip()
    ev["_st"] = ev["state_abbr"].astype("string").str.upper()
    matched = []
    for rec in ev.to_dict(orient="records"):
        cand = d[d["_key"] == rec["_key"]]
        st = rec.get("_st") or ""
        if st:
            cand_st = cand[cand["_st"] == st]
            if len(cand_st):
                cand = cand_st
        if len(cand) != 1:
            continue
        hit = cand.iloc[0]
        matched.append(
            {
                "unitid": hit["unitid"],
                "opeid6": hit.get("opeid6", ""),
                "event_year": int(rec["event_year"]),
                "event_type": rec["event_type"],
                "event_source": rec["event_source"],
                "matched_name": hit[name_col],
                "source_name": rec["inst_name"],
            }
        )
    return pd.DataFrame(matched)


def ingest_closure_trackers(settings: Settings, directory: pd.DataFrame | None = None) -> pd.DataFrame:
    cfg = settings.raw.get("closure_trackers") or {}
    cache = settings.raw_dir / "closures"
    frames = []
    sources = [
        (
            "higher_ed_dive",
            cfg.get(
                "higher_ed_dive_url",
                "https://www.highereddive.com/news/tracker-college-closings-and-mergers/546692/",
            ),
        ),
        (
            "bestcolleges",
            cfg.get(
                "bestcolleges_url",
                "https://www.bestcolleges.com/research/closed-colleges-list-statistics-major-closures/",
            ),
        ),
    ]
    for source, url in sources:
        html = _get(url, cache / f"{source}.html")
        if not html:
            continue
        parsed = parse_tracker_html(html, source)
        LOGGER.info("%s extracted %s candidate rows from HTML", source, len(parsed))
        if not parsed.empty:
            frames.append(parsed)
    curated = settings.root / str(cfg.get("curated_csv") or "data/external/closures_curated.csv")
    if curated.exists() and curated.stat().st_size > 10:
        extra = pd.read_csv(curated)
        extra["event_source"] = extra.get("event_source", "curated_csv")
        frames.append(extra)
        LOGGER.info("Loaded curated closure CSV %s rows", len(extra))

    raw = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if not raw.empty:
        raw.to_parquet(settings.processed_dir / "closure_trackers_raw.parquet", index=False)

    if directory is None:
        dpath = settings.processed_dir / "directory_raw.parquet"
        alt = settings.processed_dir / "directory.parquet"
        directory = pd.read_parquet(dpath if dpath.exists() else alt) if (dpath.exists() or alt.exists()) else pd.DataFrame()

    matched = _match_to_directory(raw, directory) if not raw.empty else pd.DataFrame()
    dest = settings.processed_dir / "closure_trackers.parquet"
    if not matched.empty:
        matched.to_parquet(dest, index=False)
    elif dest.exists():
        dest.unlink()
    LOGGER.info("Closure tracker unique directory matches: %s", len(matched))
    return matched
