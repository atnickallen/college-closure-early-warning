"""FSA accountability extracts: composite scores, HCM, closed schools."""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path

import pandas as pd
import requests

from college_closure.attempts import AttemptLog
from college_closure.config import Settings
from college_closure.download import (
    DEFAULT_HEADERS,
    attempt_log,
    download_file,
    download_first,
    wayback_candidates,
)
from college_closure.ids import add_id_keys, normalize_opeid8, opeid6
from college_closure.scorecard import ingest_scorecard
from college_closure.urban import UrbanClient

LOGGER = logging.getLogger(__name__)

DATA_ED_COMPOSITE_PACKAGE = "ff51fef3-9d22-49a7-b34b-54329a290307"


def _read_tabular(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        try:
            return pd.read_excel(path)
        except Exception as exc:  # noqa: BLE001
            LOGGER.warning("Excel read failed %s: %s; trying CSV", path, exc)
    return pd.read_csv(path, encoding="latin-1", low_memory=False)


def ingest_urban_composite(settings: Settings) -> pd.DataFrame:
    cfg = settings.raw.get("fsa") or {}
    csv_name = cfg.get("urban_composite_csv", "colleges_fsa_composite_scores.csv")
    csv_dir = cfg.get("urban_csv_dir", "fsa")
    client = UrbanClient(settings)
    dest = client.download_csv(csv_name, csv_dir)
    if dest is None:
        LOGGER.warning("Urban FSA composite CSV missing")
        return pd.DataFrame()
    raw = pd.read_csv(dest, low_memory=False)
    raw = add_id_keys(raw)
    score_col = next(
        (c for c in raw.columns if c.lower() in {"financial_resp_score", "composite_score", "score"}),
        None,
    )
    if score_col is None:
        LOGGER.warning("Composite CSV has no score column: %s", list(raw.columns)[:20])
        return pd.DataFrame()
    out = raw.rename(columns={score_col: "composite_score"})
    keep = [c for c in ("unitid", "year", "opeid", "opeid8", "opeid6", "composite_score", "inst_name_fsa") if c in out.columns]
    out = out[keep]
    out["composite_score"] = pd.to_numeric(out["composite_score"], errors="coerce")
    out["composite_fail"] = out["composite_score"] < 1.0
    out["composite_zone"] = (out["composite_score"] >= 1.0) & (out["composite_score"] < 1.5)
    out["composite_file_source"] = "urban"
    dest_p = settings.processed_dir / "fsa_composite_urban.parquet"
    out.to_parquet(dest_p, index=False)
    LOGGER.info(
        "Urban composite %s rows years %s–%s",
        len(out),
        out["year"].min() if "year" in out.columns else "?",
        out["year"].max() if "year" in out.columns else "?",
    )
    return out


def _guess_col(df: pd.DataFrame, needles: list[str]) -> str | None:
    lower = {c.lower().replace(" ", "_"): c for c in df.columns}
    for n in needles:
        for key, orig in lower.items():
            if n in key:
                return orig
    return None


def _filename_year(name: str) -> int | None:
    """Map official FSA filenames onto the fiscal-year-end calendar year."""
    m = re.search(r"ay\s*(\d{2})\s*[-_/]?\s*(\d{2})", name, flags=re.I)
    if m:
        return 2000 + int(m.group(2))
    m = re.search(r"(20\d{2})\s*[-_/]?\s*(20\d{2})", name)
    if m:
        return int(m.group(2))
    m = re.search(r"(?:^|[^0-9])(\d{2})(\d{2})composite", name, flags=re.I)
    if m:
        return 2000 + int(m.group(2))
    return None


def parse_official_composite_workbook(path: Path, fallback_year: int | None = None) -> pd.DataFrame:
    """Parse FSA eZ-Audit composite workbooks (header row is often not row 0)."""
    try:
        xl = pd.ExcelFile(path)
        sheets = xl.sheet_names
    except Exception:
        sheets = [0]
    frames = []
    for sheet in sheets:
        try:
            raw = pd.read_excel(path, sheet_name=sheet, header=None)
        except Exception as exc:  # noqa: BLE001
            LOGGER.warning("Could not read %s sheet %s: %s", path.name, sheet, exc)
            continue
        header_idx = None
        for i, row in raw.iterrows():
            joined = " ".join(str(v) for v in row.tolist() if pd.notna(v)).lower()
            if "ope" in joined and "composite" in joined:
                header_idx = int(i)
                break
            if "ope id" in joined or "opeid" in joined.replace(" ", ""):
                header_idx = int(i)
                break
        if header_idx is None:
            continue
        header = [str(v).strip() if pd.notna(v) else f"col_{j}" for j, v in enumerate(raw.iloc[header_idx])]
        body = raw.iloc[header_idx + 1 :].copy()
        body.columns = header
        body = body.dropna(how="all")
        opeid_col = _guess_col(body, ["opeid", "ope_id", "ope id", "opecode"])
        score_col = _guess_col(body, ["composite", "score", "financial_resp"])
        year_col = None
        for c in body.columns:
            key = str(c).lower().replace("\n", " ")
            if any(x in key for x in ("ope", "composite", "score", "name", "city", "state", "zip")):
                continue
            if "fiscal year end" in key or key.strip() in {"year", "fy", "fiscal_year", "fy_end"}:
                year_col = c
                break
        if opeid_col is None or score_col is None:
            continue
        out = pd.DataFrame(
            {
                "opeid_raw": body[opeid_col],
                "composite_score": pd.to_numeric(body[score_col], errors="coerce"),
            }
        )
        if year_col:
            years = pd.to_datetime(body[year_col], errors="coerce")
            numeric_y = pd.to_numeric(body[year_col], errors="coerce")
            out["year"] = years.dt.year.astype("float")
            still = out["year"].isna()
            out.loc[still, "year"] = numeric_y.loc[still].to_numpy()
        else:
            out["year"] = fallback_year
        out["opeid_raw"] = out["opeid_raw"].map(lambda v: "" if pd.isna(v) else str(v))
        out["opeid6"] = out["opeid_raw"].map(opeid6)
        out["opeid8"] = out["opeid_raw"].map(normalize_opeid8)
        out["year"] = pd.to_numeric(out.get("year"), errors="coerce")
        out["composite_score"] = pd.to_numeric(out["composite_score"], errors="coerce")
        out = out[out["opeid6"] != ""].dropna(subset=["composite_score"])
        if out["year"].isna().all() and fallback_year:
            out["year"] = fallback_year
        frames.append(out)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _ckan_composite_urls() -> list[tuple[str, str]]:
    """(name, url) from data.ed.gov CKAN — official FSA year files through 2017-18."""
    api = f"https://data.ed.gov/api/3/action/package_show?id={DATA_ED_COMPOSITE_PACKAGE}"
    try:
        resp = requests.get(api, headers=DEFAULT_HEADERS, timeout=30)
        if resp.status_code >= 400:
            LOGGER.warning("data.ed.gov CKAN %s", resp.status_code)
            return []
        resources = (resp.json().get("result") or {}).get("resources") or []
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("data.ed.gov CKAN failed: %s", exc)
        return []
    out = []
    for rec in resources:
        url = rec.get("url") or rec.get("download_url") or ""
        name = rec.get("name") or url
        if not url or "studentaid.gov/data-center" in url:
            continue
        if not re.search(r"\.(xls|xlsx)$", url, flags=re.I) and "download" not in url:
            continue
        out.append((str(name), str(url)))
    return out


def ingest_data_ed_composites(settings: Settings) -> pd.DataFrame:
    dest_dir = settings.raw_dir / "fsa" / "data_ed_gov"
    pairs = _ckan_composite_urls()
    frames = []
    for name, url in pairs:
        fname = url.rstrip("/").split("/")[-1] or re.sub(r"\W+", "_", name) + ".xls"
        path = download_file(url, dest_dir / fname, timeout=(10, 60), max_retries=2, source="data.ed.gov_composite")
        if path is None:
            continue
        parsed = parse_official_composite_workbook(path, fallback_year=_filename_year(fname + " " + name))
        if parsed.empty:
            LOGGER.warning("Official composite parsed empty: %s", path.name)
            continue
        parsed["composite_file_source"] = f"data.ed.gov:{path.name}"
        frames.append(parsed)
        LOGGER.info("Official composite %s -> %s rows years %s", path.name, len(parsed), parsed["year"].dropna().unique().tolist())
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    out = out.dropna(subset=["composite_score"])
    for c in ("opeid_raw", "opeid6", "opeid8", "composite_file_source"):
        if c in out.columns:
            out[c] = out[c].astype("string")
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    dest = settings.processed_dir / "fsa_composite_official.parquet"
    out.to_parquet(dest, index=False)
    LOGGER.info(
        "Official data.ed.gov composites %s rows years %s–%s",
        len(out),
        int(out["year"].min()) if out["year"].notna().any() else "?",
        int(out["year"].max()) if out["year"].notna().any() else "?",
    )
    return out


def ingest_hcm_snapshot(settings: Settings) -> pd.DataFrame:
    """Current HCM list only — do not back-apply to historical training years."""
    cfg = settings.raw.get("fsa") or {}
    urls = list(cfg.get("hcm_urls") or [])
    for extra in wayback_candidates("studentaid.gov/sites/default/files/*hcm*", limit=12):
        if extra not in urls:
            urls.append(extra)
    path = download_first(urls, settings.raw_dir / "fsa", "hcm", source="hcm")
    if path is None:
        LOGGER.warning("HCM snapshot workbook not downloaded; Scorecard HCM2 flag may still apply")
        return pd.DataFrame()
    raw = _read_tabular(path)
    raw.columns = [str(c).strip() for c in raw.columns]
    opeid_col = _guess_col(raw, ["opeid", "ope_id", "opecode"])
    name_col = _guess_col(raw, ["school", "institution", "name"])
    level_col = _guess_col(raw, ["hcm", "method", "monitoring", "status"])
    if opeid_col is None:
        LOGGER.warning("HCM file missing OPEID columns: %s", list(raw.columns)[:25])
        return pd.DataFrame()
    out = pd.DataFrame(
        {
            "opeid_raw": raw[opeid_col],
            "hcm_name": raw[name_col] if name_col else pd.NA,
            "hcm_status_raw": raw[level_col] if level_col else pd.NA,
        }
    )
    out["opeid6"] = out["opeid_raw"].map(opeid6)
    text = out["hcm_status_raw"].astype("string").str.lower().fillna("")
    out["hcm2_current"] = text.str.contains("hcm2|hcm 2|reimbursement")
    out["hcm1_current"] = text.str.contains("hcm1|hcm 1|heightened cash monitoring 1") | (
        text.str.contains("hcm") & ~out["hcm2_current"]
    )
    out = out[out["opeid6"] != ""].drop_duplicates(subset=["opeid6"])
    dest = settings.processed_dir / "fsa_hcm_current.parquet"
    out.to_parquet(dest, index=False)
    LOGGER.info("HCM snapshot %s OPEID6 roots -> %s", len(out), dest)
    return out


def _discover_closed_school_urls() -> list[str]:
    """Best-effort scrape of FSA Partner Connect closed-school page for .xls links."""
    page = "https://fsapartners.ed.gov/additional-resources/reports/weekly-closed-school-search-file"
    found: list[str] = []
    try:
        resp = requests.get(page, headers=DEFAULT_HEADERS, timeout=40)
        if resp.status_code < 400:
            hrefs = re.findall(r'href="([^"]+\.(?:xls|xlsx))"', resp.text, flags=re.I)
            hrefs += re.findall(r"https?://[^\"']+ClosedSchool[^\"']+\.(?:xls|xlsx)", resp.text, flags=re.I)
            for href in hrefs:
                if href.startswith("/"):
                    href = "https://fsapartners.ed.gov" + href
                found.append(href)
    except Exception as exc:  # noqa: BLE001
        LOGGER.info("Closed-school page scrape skipped: %s", exc)
    return found


def ingest_closed_school(settings: Settings) -> pd.DataFrame:
    cfg = settings.raw.get("fsa") or {}
    urls = list(cfg.get("closed_school_urls") or [])
    for extra in _discover_closed_school_urls():
        if extra not in urls:
            urls.insert(0, extra)
    for extra in wayback_candidates("fsapartners.ed.gov/sites/default/files/*ClosedSchool*", limit=10):
        if extra not in urls:
            urls.append(extra)
    path = download_first(urls, settings.raw_dir / "fsa", "closed_school", source="closed_school")
    if path is None:
        LOGGER.warning("FSA Closed School file not downloaded; labels will use IPEDS + optional trackers")
        return pd.DataFrame()
    raw = _read_tabular(path)
    raw.columns = [str(c).strip() for c in raw.columns]
    opeid_col = _guess_col(raw, ["opeid", "ope_id", "opecode"])
    date_col = _guess_col(raw, ["close_date", "closedate", "date_closed", "closure", "closed"])
    name_col = _guess_col(raw, ["school", "institution", "name"])
    if opeid_col is None:
        LOGGER.warning("Closed school file missing OPEID: %s", list(raw.columns)[:25])
        return pd.DataFrame()
    out = pd.DataFrame(
        {
            "opeid_raw": raw[opeid_col],
            "closed_name": raw[name_col] if name_col else pd.NA,
            "closed_date_raw": raw[date_col] if date_col else pd.NA,
        }
    )
    out["opeid6"] = out["opeid_raw"].map(opeid6)
    dates = pd.to_datetime(out["closed_date_raw"], errors="coerce")
    out["closed_year"] = dates.dt.year
    out = out[out["opeid6"] != ""].dropna(subset=["closed_year"])
    dest = settings.processed_dir / "fsa_closed_school.parquet"
    out.to_parquet(dest, index=False)
    LOGGER.info("FSA closed school %s rows years %s–%s", len(out), out["closed_year"].min(), out["closed_year"].max())
    return out


def ingest_published_composite(settings: Settings) -> pd.DataFrame:
    """data.ed.gov official year files + any Data Center workbook URL that still works."""
    official = ingest_data_ed_composites(settings)
    cfg = settings.raw.get("fsa") or {}
    urls = list(cfg.get("composite_urls") or [])
    for extra in wayback_candidates("studentaid.gov/sites/default/files/*omposite*", limit=10):
        if extra not in urls:
            urls.append(extra)
    path = download_first(urls, settings.raw_dir / "fsa", "composite_official", source="fsa_composite_workbook")
    extra = pd.DataFrame()
    if path is not None:
        extra = parse_official_composite_workbook(path, fallback_year=_filename_year(path.name))
        if extra.empty:
            # fallback to naive first-sheet reader
            raw = _read_tabular(path)
            raw.columns = [str(c).strip() for c in raw.columns]
            opeid_col = _guess_col(raw, ["opeid", "ope_id", "opecode"])
            year_col = _guess_col(raw, ["year", "fiscal", "fy"])
            score_col = _guess_col(raw, ["composite", "score", "financial_resp"])
            if opeid_col and score_col:
                extra = pd.DataFrame(
                    {
                        "opeid_raw": raw[opeid_col],
                        "composite_score": pd.to_numeric(raw[score_col], errors="coerce"),
                    }
                )
                if year_col:
                    extra["year"] = pd.to_numeric(raw[year_col], errors="coerce")
                    if extra["year"].isna().all():
                        extra["year"] = pd.to_datetime(raw[year_col], errors="coerce").dt.year
                extra["opeid6"] = extra["opeid_raw"].map(opeid6)
                extra["opeid8"] = extra["opeid_raw"].map(normalize_opeid8)
                extra = extra[extra["opeid6"] != ""].dropna(subset=["composite_score"])
        if not extra.empty:
            extra["composite_file_source"] = f"workbook:{path.name}"
    if official.empty:
        return extra
    if extra.empty:
        return official
    return pd.concat([official, extra], ignore_index=True)


def merge_composite_sources(urban: pd.DataFrame, official: pd.DataFrame) -> pd.DataFrame:
    """Prefer official FSA scores when they overlap Urban; keep Urban history."""
    if official is None or official.empty:
        return urban
    if urban is None or urban.empty:
        return official
    keep_u = [c for c in urban.columns if c in {"unitid", "year", "opeid", "opeid8", "opeid6", "composite_score", "composite_file_source"}]
    keep_o = [c for c in official.columns if c in {"unitid", "year", "opeid", "opeid8", "opeid6", "composite_score", "composite_file_source"}]
    u = urban[keep_u].copy()
    o = official[keep_o].copy()
    u["source"] = "urban"
    o["source"] = "fsa_official"
    stacked = pd.concat([u, o], ignore_index=True)
    stacked["year"] = pd.to_numeric(stacked.get("year"), errors="coerce")
    stacked["unitid"] = pd.to_numeric(stacked.get("unitid"), errors="coerce")
    stacked["_pref"] = (stacked["source"] == "fsa_official").astype(int)
    stacked = stacked.sort_values(["unitid", "opeid6", "year", "_pref"])
    has_id = stacked["unitid"].notna()
    a = stacked.loc[has_id].drop_duplicates(subset=["unitid", "year"], keep="last")
    b = stacked.loc[~has_id].drop_duplicates(subset=["opeid6", "year"], keep="last")
    out = pd.concat([a, b], ignore_index=True)
    out["composite_fail"] = out["composite_score"] < 1.0
    out["composite_zone"] = (out["composite_score"] >= 1.0) & (out["composite_score"] < 1.5)
    return out.drop(columns=["_pref"], errors="ignore")


def attach_composite(panel: pd.DataFrame, composite: pd.DataFrame) -> pd.DataFrame:
    """Join composite scores: UNITID×year first, then unambiguous OPEID6×year."""
    if composite is None or composite.empty:
        return panel
    out = panel.copy()
    out["unitid"] = pd.to_numeric(out["unitid"], errors="coerce")
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    comp = composite.copy()
    comp["year"] = pd.to_numeric(comp.get("year"), errors="coerce")
    if "unitid" in comp.columns:
        comp["unitid"] = pd.to_numeric(comp["unitid"], errors="coerce")
        by_id = comp.dropna(subset=["unitid", "year"])[["unitid", "year", "composite_score"]].drop_duplicates(
            subset=["unitid", "year"], keep="last"
        )
        out = out.merge(by_id, on=["unitid", "year"], how="left", suffixes=("", "_comp"))
        if "composite_score_comp" in out.columns:
            out["composite_score"] = out["composite_score"].where(out["composite_score"].notna(), out["composite_score_comp"])
            out = out.drop(columns=["composite_score_comp"])
    still = out["composite_score"].isna() if "composite_score" in out.columns else pd.Series(True, index=out.index)
    if still.any() and "opeid6" in out.columns and "opeid6" in comp.columns:
        by6 = comp.dropna(subset=["opeid6", "year"]).copy()
        by6 = by6.sort_values(["opeid6", "year"])
        by6 = by6.drop_duplicates(subset=["opeid6", "year"], keep="last")
        add = by6[["opeid6", "year", "composite_score"]].rename(columns={"composite_score": "_c6"})
        out = out.merge(add, on=["opeid6", "year"], how="left")
        if "composite_score" not in out.columns:
            out["composite_score"] = out["_c6"]
        else:
            out["composite_score"] = out["composite_score"].where(out["composite_score"].notna(), out["_c6"])
        out = out.drop(columns=["_c6"])
        if "opeid6_n_unitids" in out.columns:
            shared = (out["opeid6_n_unitids"] > 1) & ~out.get("opeid_is_main", False)
            out.loc[shared & still.reindex(out.index, fill_value=True), "composite_score"] = pd.NA
    return out


def write_fsa_notes(settings: Settings, results: dict[str, pd.DataFrame], log: AttemptLog | None = None) -> None:
    lines = [
        "# FSA accountability ingest (v2)",
        "",
        "Tried Urban FSA CSV, **data.ed.gov official year workbooks**, current FSA Data Center /",
        "Partner Connect URLs, Wayback CDX (best-effort), and College Scorecard (API or bulk ZIP).",
        "Missing files are skipped; they are **not** invented.",
        "",
        "## Row counts this run",
        "",
    ]
    for key, frame in results.items():
        if frame is None or (hasattr(frame, "empty") and frame.empty):
            lines.append(f"- **{key}**: not available this run")
        else:
            extra = ""
            if "year" in frame.columns and frame["year"].notna().any():
                extra = f" years {int(frame['year'].min())}–{int(frame['year'].max())}"
            elif "closed_year" in frame.columns and frame["closed_year"].notna().any():
                extra = f" years {int(frame['closed_year'].min())}–{int(frame['closed_year'].max())}"
            lines.append(f"- **{key}**: {len(frame):,} rows{extra}")
    lines += [
        "",
        "## HTTP attempts (verified live vs still impossible)",
        "",
        (log or attempt_log()).markdown_table(),
        "",
        "## Join rules",
        "",
        "- OPEID: 6-digit FSA roots are **not** left-padded to 8 (that would shift the root).",
        "  Six-digit values become `root + '00'` via `ids.normalize_opeid8`.",
        "- Composites join UNITID×year first, then unambiguous OPEID6×year (main campus if shared).",
        "- Official data.ed.gov files are preferred on overlap with Urban; Urban keeps 2006–2016 history.",
        "",
        "HCM / Scorecard `UNDER_INVESTIGATION` are **current snapshots** and must not be used as",
        "historical training features unless a lagged year-by-year series is present (it is not in this build).",
        "",
    ]
    if not (os.environ.get("DATA_GOV_API_KEY") or os.environ.get("SCORECARD_API_KEY")):
        lines.append("College Scorecard API key absent; bulk ZIP path used when the official file downloaded.")
    dest = settings.outputs_dir / "fsa_ingest.md"
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (settings.outputs_dir / "fsa_attempts.json").write_text(
        __import__("json").dumps((log or attempt_log()).to_dicts(), indent=2),
        encoding="utf-8",
    )
    LOGGER.info("Wrote %s", dest)


def ingest_scorecard_optional(settings: Settings) -> pd.DataFrame:
    return ingest_scorecard(settings)


def run_fsa_ingest(settings: Settings) -> dict[str, pd.DataFrame]:
    urban = ingest_urban_composite(settings)
    official = ingest_published_composite(settings)
    composite = merge_composite_sources(urban, official)
    if not composite.empty:
        composite.to_parquet(settings.processed_dir / "fsa_composite.parquet", index=False)
    results = {
        "composite_urban": urban,
        "composite_official": official,
        "composite": composite,
        "hcm": ingest_hcm_snapshot(settings),
        "closed_school": ingest_closed_school(settings),
        "scorecard": ingest_scorecard_optional(settings),
    }
    write_fsa_notes(settings, results)
    return results
