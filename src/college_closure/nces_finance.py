"""NCES IPEDS Finance complete-data backfill (post-2017 Urban gap)."""

from __future__ import annotations

import io
import logging
import zipfile
from pathlib import Path

import pandas as pd

from college_closure.config import Settings
from college_closure.constants import FINANCE_PANEL_COLUMNS, SENTINEL_VALUES
from college_closure.download import download_file
from college_closure.filters import replace_sentinels

LOGGER = logging.getLogger(__name__)

# Map NCES complete-data columns → Urban-style names. First hit wins.
# F2 = FASB private nonprofit; F1A = GASB public; F3 = for-profit.
FORM_MAP = {
    "F2": {
        "rev_tuition_fees_net": ["F2D014", "F2D01"],
        "rev_total_current": ["F2D164", "F2D16", "F2B01"],
        "exp_total_current": ["F2E131", "F2B02"],
        "exp_total_salaries": ["F2E132"],
        "exp_instruc_total": ["F2E011"],
        "sch_grants_institutional": ["F2C08", "F2C07"],
        "sch_allowances_tuition_fees": ["F2C08", "F2C07"],
        "endowment_end": ["F2H02"],
        "assets": ["F2A19", "F2A06"],
        "liabilities": ["F2A13", "F2A20"],
        "assets_net": ["F2A18", "F2A16", "F2A04"],
        "longterm_debt": ["F2A03"],
        "income_net": ["F2B05", "F2B03"],
        "rev_investment_return": ["F2D08", "F2D084"],
        "rev_gifts_grants_contracts": ["F2D03", "F2D034"],
    },
    "F1A": {
        "rev_tuition_fees_net": ["F1B01"],
        "rev_total_current": ["F1B25", "F1B21"],
        "exp_total_current": ["F1C191"],
        "exp_total_salaries": ["F1C192"],
        "exp_instruc_total": ["F1C011"],
        "endowment_end": ["F1H02"],
        "assets": ["F1A18", "F1A01"],
        "liabilities": ["F1A13"],
        "assets_net": ["F1A18"],  # overwritten if net position exists
        "longterm_debt": ["F1A10", "F1A09"],
        "income_net": ["F1D03", "F1D01"],
        "rev_investment_return": ["F1B11"],
        "rev_gifts_grants_contracts": ["F1B10", "F1B04"],
    },
    "F3": {
        "rev_tuition_fees_net": ["F3D01"],
        "rev_tuition_fees_gross": ["F3D01"],
        "rev_total_current": ["F3D09", "F3D08", "F3B01"],
        "exp_total_current": ["F3E071", "F3B02"],
        "exp_total_salaries": ["F3E072"],
        "exp_instruc_total": ["F3E011"],
        "assets": ["F3A01"],
        "liabilities": ["F3A02"],
        "assets_net": ["F3A06", "F3A04"],
        "longterm_debt": ["F3A02A", "F3A03"],
        "income_net": ["F3B04", "F3B03"],
        "sch_allowances_tuition_fees": ["F3C08"],
        "sch_grants_institutional": ["F3C08"],
    },
}


def _nces_year_stem(year: int, form: str) -> str:
    """F1819_F2 for Urban/IPEDS year 2018 (FY 2018, collection 2018-19)."""
    yy0 = year % 100
    yy1 = (year + 1) % 100
    return f"F{yy0:02d}{yy1:02d}_{form}"


def _read_zip_csv(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not names:
            raise ValueError(f"No CSV in {path}")
        # Prefer non-_rv / data table
        names_sorted = sorted(names, key=lambda n: ("rv" in n.lower(), len(n)))
        raw = zf.read(names_sorted[0])
    return pd.read_csv(io.BytesIO(raw), encoding="latin-1", low_memory=False)


def _first_present(df: pd.DataFrame, candidates: list[str]) -> str | None:
    upper = {c.upper(): c for c in df.columns}
    for name in candidates:
        if name.upper() in upper:
            return upper[name.upper()]
    return None


def _harmonize(df: pd.DataFrame, form: str, year: int) -> pd.DataFrame:
    unitid_col = _first_present(df, ["UNITID"])
    if unitid_col is None:
        LOGGER.warning("NCES %s %s missing UNITID", form, year)
        return pd.DataFrame()
    out = pd.DataFrame({"unitid": pd.to_numeric(df[unitid_col], errors="coerce"), "year": year})
    mapping = FORM_MAP[form]
    for dest, candidates in mapping.items():
        src = _first_present(df, candidates)
        if src is None:
            out[dest] = pd.NA
            continue
        out[dest] = pd.to_numeric(df[src], errors="coerce")
        out[dest] = out[dest].mask(out[dest].isin(SENTINEL_VALUES))
    out["nces_finance_form"] = form
    return out.dropna(subset=["unitid"])


def ingest_nces_finance(settings: Settings) -> pd.DataFrame:
    cfg = settings.raw.get("nces") or {}
    base = str(cfg.get("base_url", "https://nces.ed.gov/ipeds/datacenter/data")).rstrip("/")
    year_start = int(cfg.get("year_start", 2018))
    year_end = int(cfg.get("year_end", 2023))
    forms = list(cfg.get("forms") or ["F1A", "F2", "F3"])
    dest_dir = settings.raw_dir / "nces"
    frames: list[pd.DataFrame] = []
    got: list[str] = []
    missing: list[str] = []

    for year in range(year_start, year_end + 1):
        year_frames: list[pd.DataFrame] = []
        for form in forms:
            stem = _nces_year_stem(year, form)
            url = f"{base}/{stem}.zip"
            path = download_file(url, dest_dir / f"{stem}.zip")
            if path is None:
                missing.append(f"{url}")
                continue
            try:
                raw = _read_zip_csv(path)
                harm = _harmonize(raw, form, year)
            except Exception as exc:  # noqa: BLE001 — keep going per year/form
                LOGGER.warning("Failed to parse %s: %s", path, exc)
                missing.append(str(path))
                continue
            if harm.empty:
                continue
            year_frames.append(harm)
            got.append(f"{year}:{form}({len(harm)})")
        if year_frames:
            # One row per UNITID: prefer the form that actually reported revenue.
            stacked = pd.concat(year_frames, ignore_index=True)
            stacked["_has_rev"] = pd.to_numeric(stacked.get("rev_total_current"), errors="coerce").notna()
            stacked = stacked.sort_values(["unitid", "_has_rev"])
            stacked = stacked.drop_duplicates(subset=["unitid", "year"], keep="last")
            frames.append(stacked.drop(columns=["_has_rev"]))

    notes_path = settings.outputs_dir / "nces_finance_years.md"
    if not frames:
        notes_path.write_text(
            "# NCES finance backfill\n\nNo files parsed.\n\nTried:\n"
            + "\n".join(f"- {u}" for u in missing)
            + "\n",
            encoding="utf-8",
        )
        LOGGER.warning("NCES finance backfill produced no rows")
        return pd.DataFrame()

    out = pd.concat(frames, ignore_index=True)
    keep = ["unitid", "year", "nces_finance_form"] + [c for c in FINANCE_PANEL_COLUMNS if c in out.columns]
    out = replace_sentinels(out[keep], [c for c in keep if c not in {"unitid", "year", "nces_finance_form"}])
    dest = settings.processed_dir / "finance_nces.parquet"
    out.to_parquet(dest, index=False)
    year_min, year_max = int(out["year"].min()), int(out["year"].max())
    notes_path.write_text(
        "# NCES IPEDS Finance backfill\n\n"
        f"- Harmonized rows: **{len(out):,}**\n"
        f"- Years successfully parsed: **{year_min}–{year_max}**\n"
        f"- Forms: {', '.join(forms)}\n"
        f"- Naming: `{base}/F{{yy}}{{yy+1}}_{{form}}.zip` "
        "(e.g. F1819_F2.zip = FY 2018 / Urban year 2018)\n\n"
        "## Parsed files\n\n"
        + "\n".join(f"- {g}" for g in got)
        + "\n\n## Missing / failed URLs\n\n"
        + ("\n".join(f"- `{u}`" for u in missing) if missing else "- none\n")
        + "\n",
        encoding="utf-8",
    )
    LOGGER.info("NCES finance %s rows years %s–%s -> %s", len(out), year_min, year_max, dest)
    return out


def merge_urban_and_nces(urban: pd.DataFrame, nces: pd.DataFrame) -> pd.DataFrame:
    """Prefer Urban values when present; fill gaps (especially post-2017) from NCES."""
    if urban.empty and nces.empty:
        return pd.DataFrame()
    if nces.empty:
        return urban
    if urban.empty:
        return nces
    urban = urban.copy()
    nces = nces.copy()
    urban["unitid"] = pd.to_numeric(urban["unitid"], errors="coerce")
    urban["year"] = pd.to_numeric(urban["year"], errors="coerce")
    nces["unitid"] = pd.to_numeric(nces["unitid"], errors="coerce")
    nces["year"] = pd.to_numeric(nces["year"], errors="coerce")
    keys = ["unitid", "year"]
    value_cols = [c for c in FINANCE_PANEL_COLUMNS if c in set(urban.columns) | set(nces.columns)]
    extra = [c for c in ("nces_finance_form",) if c in nces.columns]
    merged = urban.merge(
        nces[keys + [c for c in value_cols + extra if c in nces.columns]],
        on=keys,
        how="outer",
        suffixes=("", "_nces"),
    )
    for col in value_cols:
        nces_col = f"{col}_nces"
        if col not in merged.columns:
            merged[col] = merged[nces_col] if nces_col in merged.columns else pd.NA
        elif nces_col in merged.columns:
            merged[col] = merged[col].where(merged[col].notna(), merged[nces_col])
        if nces_col in merged.columns:
            merged = merged.drop(columns=[nces_col])
    return merged
