"""WICHE Knocking at the College Door — state HS graduate trends."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from college_closure.config import Settings
from college_closure.download import download_first

LOGGER = logging.getLogger(__name__)

USPS = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS",
    "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA",
    "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY",
}


def _urls(settings: Settings) -> list[str]:
    cfg = settings.raw.get("wiche") or {}
    urls = list(cfg.get("urls") or [])
    default = (
        "https://www.wiche.edu/wp-content/uploads/2024/12/"
        "Knocking-at-the-College-Door-11th-Edition-Projections-Dataset-12-11-2024.xlsx"
    )
    if default not in urls:
        urls.append(default)
    if cfg.get("url") and cfg["url"] not in urls:
        urls.insert(0, str(cfg["url"]))
    return urls


def _write_placeholder(path: Path, reason: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    readme = path.with_name("wiche_README.md")
    readme.write_text(
        "# WICHE Knocking at the College Door\n\n"
        "Expected columns for the derived CSV: `state_abbr`, `year`, `hs_graduates`.\n\n"
        f"Download did not produce a usable table this run: {reason}\n\n"
        "Official dataset page: https://www.wiche.edu/knocking/data/\n"
        "11th edition workbook (when reachable):\n"
        "https://www.wiche.edu/wp-content/uploads/2024/12/"
        "Knocking-at-the-College-Door-11th-Edition-Projections-Dataset-12-11-2024.xlsx\n",
        encoding="utf-8",
    )
    if not path.exists():
        pd.DataFrame(columns=["state_abbr", "year", "hs_graduates"]).to_csv(path, index=False)


def parse_knocking_workbook(path: Path) -> pd.DataFrame:
    """Grand-total HS graduates by USPS state and graduating class year."""
    xl = pd.ExcelFile(path)
    sheet = "Data" if "Data" in xl.sheet_names else xl.sheet_names[0]
    raw = pd.read_excel(path, sheet_name=sheet)
    cols = {c.lower().replace(" ", ""): c for c in raw.columns}
    stabbr = cols.get("stabbr") or cols.get("state") or next(
        (c for c in raw.columns if "stabbr" in str(c).lower() or str(c).lower() == "state"), None
    )
    classof = cols.get("classof") or next((c for c in raw.columns if "class" in str(c).lower()), None)
    grade = cols.get("grade") or next((c for c in raw.columns if "grade" in str(c).lower()), None)
    sector = cols.get("schoolsector") or next((c for c in raw.columns if "sector" in str(c).lower()), None)
    race = cols.get("raceethnicity") or next((c for c in raw.columns if "race" in str(c).lower()), None)
    students = cols.get("students") or next((c for c in raw.columns if "student" in str(c).lower()), None)
    if not all([stabbr, classof, students]):
        raise ValueError(f"WICHE workbook missing expected columns: {list(raw.columns)[:20]}")
    work = raw.copy()
    if grade is not None:
        work = work[work[grade].astype("string").str.contains("high school graduate", case=False, na=False)]
    if sector is not None:
        work = work[work[sector].astype("string").str.contains("grand total", case=False, na=False)]
    if race is not None:
        work = work[work[race].astype("string").str.contains("total", case=False, na=False)]
    work["state_abbr"] = work[stabbr].astype("string").str.upper().str.strip()
    work = work[work["state_abbr"].isin(USPS)]
    class_year = work[classof].astype("string").str.extract(r"(19\d{2}|20\d{2})", expand=False)
    work["year"] = pd.to_numeric(class_year, errors="coerce")
    work["hs_graduates"] = pd.to_numeric(work[students], errors="coerce")
    out = (
        work.dropna(subset=["state_abbr", "year", "hs_graduates"])
        .groupby(["state_abbr", "year"], as_index=False)["hs_graduates"]
        .sum()
    )
    out["year"] = out["year"].astype(int)
    return out


def ingest_wiche(settings: Settings) -> pd.DataFrame:
    cfg = settings.raw.get("wiche") or {}
    csv_path = settings.root / str(cfg.get("path") or "data/external/wiche_hs_graduates.csv")
    urls = _urls(settings)
    xlsx = download_first(
        urls,
        settings.raw_dir / "wiche",
        "wiche_knocking.xlsx",
        timeout=(15, 90),
        max_retries=2,
        source="wiche",
    )
    if xlsx is None:
        LOGGER.warning("WICHE workbook not downloaded; writing placeholder CSV")
        _write_placeholder(csv_path, "workbook URL did not download")
        return pd.DataFrame()
    try:
        out = parse_knocking_workbook(xlsx)
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("WICHE parse failed: %s", exc)
        _write_placeholder(csv_path, f"parse failed: {exc}")
        return pd.DataFrame()
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(csv_path, index=False)
    dest = settings.processed_dir / "wiche_hs_graduates.parquet"
    out.to_parquet(dest, index=False)
    LOGGER.info(
        "WICHE HS graduates %s state-years %s–%s -> %s",
        len(out),
        int(out["year"].min()),
        int(out["year"].max()),
        csv_path,
    )
    return out
