"""FSA accountability extracts: composite scores, HCM, closed schools."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import pandas as pd

from college_closure.config import Settings
from college_closure.download import download_file, download_first
from college_closure.ids import add_id_keys, normalize_opeid8, opeid6
from college_closure.urban import UrbanClient

LOGGER = logging.getLogger(__name__)


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
    dest_p = settings.processed_dir / "fsa_composite.parquet"
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


def ingest_hcm_snapshot(settings: Settings) -> pd.DataFrame:
    """Current HCM list only — do not back-apply to historical training years."""
    cfg = settings.raw.get("fsa") or {}
    urls = list(cfg.get("hcm_urls") or [])
    path = download_first(urls, settings.raw_dir / "fsa", "hcm")
    if path is None:
        LOGGER.warning("HCM snapshot not downloaded; watchlist will omit HCM flags")
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
    import re

    import requests

    from college_closure.download import DEFAULT_HEADERS

    page = "https://fsapartners.ed.gov/additional-resources/reports/weekly-closed-school-search-file"
    found: list[str] = []
    try:
        resp = requests.get(page, headers=DEFAULT_HEADERS, timeout=60)
        if resp.status_code < 400:
            hrefs = re.findall(r'href="([^"]+\.(?:xls|xlsx))"', resp.text, flags=re.I)
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
    path = download_first(urls, settings.raw_dir / "fsa", "closed_school")
    if path is None:
        LOGGER.warning("FSA Closed School file not downloaded; labels will use IPEDS status only")
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
    """Optional FSA Data Center composite workbook (often newer than Urban 2016)."""
    cfg = settings.raw.get("fsa") or {}
    urls = list(cfg.get("composite_urls") or [])
    path = download_first(urls, settings.raw_dir / "fsa", "composite_official")
    if path is None:
        LOGGER.info("Official FSA composite workbook not downloaded; Urban CSV only")
        return pd.DataFrame()
    raw = _read_tabular(path)
    raw.columns = [str(c).strip() for c in raw.columns]
    opeid_col = _guess_col(raw, ["opeid", "ope_id", "opecode"])
    year_col = _guess_col(raw, ["year", "fiscal", "fy"])
    score_col = _guess_col(raw, ["composite", "score", "financial_resp"])
    if opeid_col is None or score_col is None:
        LOGGER.warning("Official composite file missing OPEID/score: %s", list(raw.columns)[:25])
        return pd.DataFrame()
    out = pd.DataFrame(
        {
            "opeid_raw": raw[opeid_col],
            "composite_score": pd.to_numeric(raw[score_col], errors="coerce"),
        }
    )
    if year_col:
        out["year"] = pd.to_numeric(raw[year_col], errors="coerce")
        if out["year"].isna().all():
            years = pd.to_datetime(raw[year_col], errors="coerce")
            out["year"] = years.dt.year
    out["opeid6"] = out["opeid_raw"].map(opeid6)
    out["opeid8"] = out["opeid_raw"].map(normalize_opeid8)
    out = out[out["opeid6"] != ""].dropna(subset=["composite_score"])
    dest = settings.processed_dir / "fsa_composite_official.parquet"
    out.to_parquet(dest, index=False)
    LOGGER.info("Official FSA composite %s rows", len(out))
    return out


def merge_composite_sources(urban: pd.DataFrame, official: pd.DataFrame) -> pd.DataFrame:
    """Prefer official FSA scores when they overlap Urban; keep Urban history."""
    if official is None or official.empty:
        return urban
    if urban is None or urban.empty:
        return official
    keep_u = [c for c in urban.columns if c in {"unitid", "year", "opeid", "opeid8", "opeid6", "composite_score"}]
    keep_o = [c for c in official.columns if c in {"unitid", "year", "opeid", "opeid8", "opeid6", "composite_score"}]
    u = urban[keep_u].copy()
    o = official[keep_o].copy()
    u["source"] = "urban"
    o["source"] = "fsa_official"
    stacked = pd.concat([u, o], ignore_index=True)
    stacked["year"] = pd.to_numeric(stacked.get("year"), errors="coerce")
    stacked["unitid"] = pd.to_numeric(stacked.get("unitid"), errors="coerce")
    stacked["_pref"] = (stacked["source"] == "fsa_official").astype(int)
    stacked = stacked.sort_values(["unitid", "opeid6", "year", "_pref"])
    # Prefer unitid×year when unitid exists, else opeid6×year
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
        # Prefer a single row per opeid6×year
        by6 = by6.sort_values(["opeid6", "year"])
        by6 = by6.drop_duplicates(subset=["opeid6", "year"], keep="last")
        add = by6[["opeid6", "year", "composite_score"]].rename(columns={"composite_score": "_c6"})
        out = out.merge(add, on=["opeid6", "year"], how="left")
        if "composite_score" not in out.columns:
            out["composite_score"] = out["_c6"]
        else:
            out["composite_score"] = out["composite_score"].where(out["composite_score"].notna(), out["_c6"])
        out = out.drop(columns=["_c6"])
        # If several UNITIDs share an OPEID6, only the main campus (or singleton) keeps the join.
        if "opeid6_n_unitids" in out.columns:
            shared = (out["opeid6_n_unitids"] > 1) & ~out.get("opeid_is_main", False)
            # Don't assign the OPEID6-level score to non-main branches when the root is shared
            # unless they already had a UNITID match (those rows were not NA before this step
            # only if unitid matched — we already filled those). Clear ambiguous leftovers:
            out.loc[shared & still.reindex(out.index, fill_value=True), "composite_score"] = pd.NA
    return out


def write_fsa_notes(settings: Settings, results: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# FSA accountability ingest",
        "",
        "Tried current FSA Data Center / Partner Connect URLs and the Urban FSA CSV.",
        "Missing files are skipped; they are **not** invented.",
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
    if not (os.environ.get("DATA_GOV_API_KEY") or os.environ.get("SCORECARD_API_KEY")):
        lines.append("")
        lines.append("College Scorecard skipped (no `DATA_GOV_API_KEY` / `SCORECARD_API_KEY`).")
    lines.append("")
    lines.append("HCM is a **current snapshot** and must not be used as a historical training feature.")
    dest = settings.outputs_dir / "fsa_ingest.md"
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    LOGGER.info("Wrote %s", dest)


def ingest_scorecard_optional(settings: Settings) -> pd.DataFrame:
    key = os.environ.get("DATA_GOV_API_KEY") or os.environ.get("SCORECARD_API_KEY")
    if not key:
        LOGGER.info("No DATA_GOV_API_KEY / SCORECARD_API_KEY; skipping College Scorecard")
        return pd.DataFrame()
    cfg = settings.raw.get("scorecard") or {}
    base = str(cfg.get("api_base", "https://api.data.gov/ed/collegescorecard/v1/schools"))
    # Latest operating flag only — not used as a historical feature.
    try:
        import requests

        rows = []
        page = 0
        while page < 80:
            resp = requests.get(
                base,
                params={
                    "api_key": key,
                    "fields": "id,ope6_id,school.name,school.operating",
                    "per_page": 100,
                    "page": page,
                },
                timeout=60,
            )
            if resp.status_code >= 400:
                LOGGER.warning("Scorecard API %s: %s", resp.status_code, resp.text[:200])
                break
            payload = resp.json()
            results = payload.get("results") or []
            if not results:
                break
            rows.extend(results)
            page += 1
        if not rows:
            return pd.DataFrame()
        frame = pd.json_normalize(rows)
        dest = settings.processed_dir / "scorecard_operating.parquet"
        frame.to_parquet(dest, index=False)
        LOGGER.info("Scorecard operating snapshot %s rows", len(frame))
        return frame
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Scorecard fetch failed: %s", exc)
        return pd.DataFrame()


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
