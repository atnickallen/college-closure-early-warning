"""Build a UNITID × year panel from directory rows plus each extract's own years."""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

import pandas as pd

from college_closure.config import Settings
from college_closure.constants import DIRECTORY_PANEL_COLUMNS, TITLE_IV_PARTICIPATING
from college_closure.crosswalk import (
    apply_parent_child_finance_rollup,
    attach_parent_links,
    build_crosswalk,
    links_from_finance,
    links_from_flags,
)
from college_closure.download import download_file
from college_closure.filters import filter_college_universe
from college_closure.fsa import attach_composite
from college_closure.ids import add_id_keys
from college_closure.nces_finance import merge_urban_and_nces
from college_closure.qa import missingness_table, write_qa_counts

LOGGER = logging.getLogger(__name__)

EXTRACT_KEY_FILES = (
    "fall_enrollment.parquet",
    "enrollment_fte.parquet",
    "finance.parquet",
    "admissions.parquet",
    "instructional_staff.parquet",
    "noninstructional_staff.parquet",
)


def _read_optional(path) -> pd.DataFrame:
    if path.exists():
        frame = pd.read_parquet(path)
        LOGGER.info("Loaded %s (%s rows)", path.name, len(frame))
        return frame
    LOGGER.info("Optional extract missing: %s", path)
    return pd.DataFrame()


def _ensure_unitid_year(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out["unitid"] = pd.to_numeric(out["unitid"], errors="coerce")
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    return out.dropna(subset=["unitid", "year"])


def collect_extract_keys(processed: Path) -> pd.DataFrame:
    """UNITID × year keys present on finance, FTE, fall enrollment, admissions, or staff."""
    frames = []
    for name in EXTRACT_KEY_FILES:
        path = processed / name
        if not path.exists():
            continue
        frame = pd.read_parquet(path, columns=["unitid", "year"])
        frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=["unitid", "year"])
    keys = pd.concat(frames, ignore_index=True)
    return _ensure_unitid_year(keys).drop_duplicates(["unitid", "year"])


def expand_spine_with_extract_years(spine: pd.DataFrame, keys: pd.DataFrame) -> pd.DataFrame:
    """Add extract years that the directory spine does not already have.

    Directory attributes for an extract-only year come from that UNITID's
    nearest directory year. The year column stays the extract year, so a later
    left join attaches that year's finance or enrollment.
    """
    if spine is None or spine.empty or keys is None or keys.empty:
        return spine
    base = spine.copy()
    base["unitid"] = pd.to_numeric(base["unitid"], errors="coerce")
    base["year"] = pd.to_numeric(base["year"], errors="coerce")
    base = base.dropna(subset=["unitid", "year"]).drop_duplicates(["unitid", "year"])
    base["unitid"] = base["unitid"].astype("int64")
    base["year"] = base["year"].astype("int64")
    wanted = _ensure_unitid_year(keys).drop_duplicates(["unitid", "year"])
    wanted["unitid"] = wanted["unitid"].astype("int64")
    wanted["year"] = wanted["year"].astype("int64")
    eligible = set(base["unitid"].tolist())
    wanted = wanted.loc[wanted["unitid"].isin(eligible)]
    have = base[["unitid", "year"]]
    missing = wanted.merge(have, on=["unitid", "year"], how="left", indicator=True)
    missing = missing.loc[missing["_merge"] == "left_only", ["unitid", "year"]]
    if missing.empty:
        return base
    lookup = base.rename(columns={"year": "dir_year"})
    cross = missing.merge(lookup, on="unitid", how="inner")
    cross["gap"] = (cross["year"] - cross["dir_year"]).abs()
    filled = (
        cross.sort_values(["gap", "dir_year"])
        .groupby(["unitid", "year"], as_index=False)
        .head(1)
        .drop(columns=["gap", "dir_year"])
    )
    out = pd.concat([base, filled], ignore_index=True)
    LOGGER.info("Extract-year spine added %s UNITID×year rows", len(filled))
    return out.drop_duplicates(["unitid", "year"], keep="first")


def _directory_spine(settings: Settings) -> pd.DataFrame:
    """College-universe directory rows, including Title IV code 3.

    Code 3 is non-participating (Grove City, and Principia's history). Those
    schools still file IPEDS finance. The participating-code flag stays false
    for code 3; only the spine keeps the row. Code 5 and other non-participating
    codes stay out. Public code-3 academies stay in the panel and out of the
    risk model because control is public.
    """
    processed = settings.processed_dir
    filters = dict(settings.filters)
    codes = {int(code) for code in filters.get("title_iv_participating", list(TITLE_IV_PARTICIPATING))}
    codes.add(3)
    filters["title_iv_participating"] = sorted(codes)
    raw_path = processed / "directory_raw.parquet"
    if raw_path.exists():
        raw = pd.read_parquet(raw_path)
        directory = filter_college_universe(raw, filters)
    else:
        directory = pd.read_parquet(processed / "directory.parquet")
    directory = _ensure_unitid_year(directory)
    if directory.empty:
        raise RuntimeError("Directory spine is empty; run scripts/01_ingest.py first")
    keep_dir = [c for c in DIRECTORY_PANEL_COLUMNS if c in directory.columns]
    return directory[keep_dir].drop_duplicates(subset=["unitid", "year"])


def _flag_csv(settings: Settings, year: int) -> Path | None:
    dest_dir = settings.raw_dir / "ipeds" / "flags"
    dest_dir.mkdir(parents=True, exist_ok=True)
    csv_path = dest_dir / f"Flags{year}.csv"
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return csv_path
    url = f"https://nces.ed.gov/ipeds/datacenter/data/FLAGS{year}.zip"
    zip_path = dest_dir / f"FLAGS{year}.zip"
    saved = download_file(url, zip_path, timeout=(10, 60), max_retries=2, source="nces-flags")
    if saved is None:
        return None
    try:
        with zipfile.ZipFile(saved) as zf:
            name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
            csv_path.write_bytes(zf.read(name))
    except (OSError, zipfile.BadZipFile, StopIteration) as exc:
        LOGGER.warning("Could not read FLAGS%s: %s", year, exc)
        return None
    return csv_path


def load_parent_links(settings: Settings, finance: pd.DataFrame) -> pd.DataFrame:
    """Historical finance child rows plus IPEDS FLAGS PRCH_F / IDX_F links."""
    frames = [links_from_finance(finance)]
    for year in range(2015, 2026):
        path = _flag_csv(settings, year)
        if path is None:
            continue
        try:
            flags = pd.read_csv(path, usecols=lambda c: str(c).upper() in {"UNITID", "PRCH_F", "IDX_F"}, low_memory=False)
        except ValueError:
            flags = pd.read_csv(path, low_memory=False)
        frames.append(links_from_flags(flags, year))
    frames = [frame for frame in frames if frame is not None and not frame.empty]
    if not frames:
        return pd.DataFrame(columns=["unitid", "year", "parent_child_flag", "parent_unitid"])
    return pd.concat(frames, ignore_index=True)


def build_panel(settings: Settings) -> pd.DataFrame:
    processed = settings.processed_dir
    panel = expand_spine_with_extract_years(_directory_spine(settings), collect_extract_keys(processed))

    enrollment = _ensure_unitid_year(_read_optional(processed / "fall_enrollment.parquet"))
    if not enrollment.empty:
        enroll_cols = [
            c
            for c in (
                "unitid",
                "year",
                "enrollment_fall_ug",
                "enrollment_fall_grad",
                "enrollment_fall_total",
            )
            if c in enrollment.columns
        ]
        panel = panel.merge(enrollment[enroll_cols], on=["unitid", "year"], how="left")

    fte = _ensure_unitid_year(_read_optional(processed / "enrollment_fte.parquet"))
    if not fte.empty:
        fte_cols = [c for c in ("unitid", "year", "enrollment_fte", "enrollment_fte_ug", "enrollment_fte_grad") if c in fte.columns]
        panel = panel.merge(fte[fte_cols], on=["unitid", "year"], how="left")

    finance = _ensure_unitid_year(_read_optional(processed / "finance.parquet"))
    nces = _ensure_unitid_year(_read_optional(processed / "finance_nces.parquet"))
    if not nces.empty:
        finance = merge_urban_and_nces(finance, nces)
        LOGGER.info("Finance after NCES merge: %s rows, years %s–%s", len(finance), int(finance["year"].min()), int(finance["year"].max()))
    if not finance.empty:
        finance_cols = [c for c in finance.columns if c in {"unitid", "year"} or c not in panel.columns]
        panel = panel.merge(finance[finance_cols], on=["unitid", "year"], how="left")
        panel = attach_parent_links(panel, load_parent_links(settings, finance))
        panel = apply_parent_child_finance_rollup(panel)

    admissions = _ensure_unitid_year(_read_optional(processed / "admissions.parquet"))
    if not admissions.empty:
        adm_cols = [c for c in admissions.columns if c in {"unitid", "year"} or c not in panel.columns]
        panel = panel.merge(admissions[adm_cols], on=["unitid", "year"], how="left")

    instr = _ensure_unitid_year(_read_optional(processed / "instructional_staff.parquet"))
    if not instr.empty:
        panel = panel.merge(instr, on=["unitid", "year"], how="left")

    noninstr = _ensure_unitid_year(_read_optional(processed / "noninstructional_staff.parquet"))
    if not noninstr.empty:
        rename = {}
        if "salary_outlays" in noninstr.columns and "salary_outlays" in panel.columns:
            rename["salary_outlays"] = "noninstruc_salary_outlays"
        panel = panel.merge(noninstr.rename(columns=rename), on=["unitid", "year"], how="left")

    if "instruc_staff_count" in panel.columns or "noninstruc_staff_count" in panel.columns:
        instr_c = pd.to_numeric(panel.get("instruc_staff_count"), errors="coerce")
        non_c = pd.to_numeric(panel.get("noninstruc_staff_count"), errors="coerce")
        panel["staff_total"] = instr_c.fillna(0) + non_c.fillna(0)
        panel.loc[instr_c.isna() & non_c.isna(), "staff_total"] = pd.NA

    panel["miss_enrollment"] = (
        panel["enrollment_fall_total"].isna() if "enrollment_fall_total" in panel.columns else True
    )
    panel["miss_finance"] = panel["rev_total_current"].isna() if "rev_total_current" in panel.columns else True
    panel["miss_admissions"] = panel["number_applied"].isna() if "number_applied" in panel.columns else True
    panel["miss_staff"] = (
        panel["instruc_staff_count"].isna() if "instruc_staff_count" in panel.columns else True
    )

    panel = add_id_keys(panel)
    xw = build_crosswalk(panel)
    extra_xw = [c for c in ("opeid8", "opeid6", "opeid_is_main", "ein_norm", "opeid6_n_unitids") if c in xw.columns]
    if extra_xw:
        panel = panel.drop(columns=[c for c in extra_xw if c in panel.columns], errors="ignore")
        panel = panel.merge(xw[["unitid", "year", *extra_xw]], on=["unitid", "year"], how="left")

    composite = _read_optional(processed / "fsa_composite.parquet")
    if not composite.empty:
        composite = composite.copy()
        if "unitid" in composite.columns:
            composite["unitid"] = pd.to_numeric(composite["unitid"], errors="coerce")
        composite["year"] = pd.to_numeric(composite.get("year"), errors="coerce")
        composite = composite.dropna(subset=["year"])
        if "composite_score" in panel.columns:
            panel = panel.drop(columns=["composite_score"])
        panel = attach_composite(panel, composite)

    panel = panel.sort_values(["unitid", "year"]).reset_index(drop=True)
    out_path = processed / "panel.parquet"
    panel.to_parquet(out_path, index=False)
    LOGGER.info("Panel %s rows × %s cols -> %s", len(panel), panel.shape[1], out_path)

    miss_cols = [
        c
        for c in (
            "enrollment_fall_total",
            "enrollment_fte",
            "rev_total_current",
            "rev_tuition_fees_net",
            "assets",
            "number_applied",
            "instruc_staff_count",
            "noninstruc_staff_count",
        )
        if c in panel.columns
    ]
    miss = missingness_table(panel, miss_cols)
    write_qa_counts(
        settings.outputs_dir / "qa_panel.md",
        title="QA: institution × year panel",
        directory=panel,
        notes=[
            "The spine keeps Title IV code 3 colleges and each UNITID's finance, FTE, fall enrollment, admissions, and staff years.",
            "Publics remain in the panel; in_risk_model_universe=True for private nonprofit and for-profit.",
            "Urban finance is the complete finance year; NCES F1A/F2/F3 zips fill 2018–2022.",
            "Child campuses with no finance row inherit the parent filer's ratios (finance_from_parent) from PCF/IDX_F. Enrollment stays the campus's own.",
            "Composite scores join on UNITID×year, then unambiguous OPEID6×year (main campus if shared).",
        ],
        extra_sections=[("Missingness by year", miss)],
    )
    LOGGER.info("Wrote %s", settings.outputs_dir / "qa_panel.md")
    return panel
