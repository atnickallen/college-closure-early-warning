"""Build a UNITID × year panel from directory + left-joined extracts."""

from __future__ import annotations

import logging

import pandas as pd

from college_closure.config import Settings
from college_closure.constants import DIRECTORY_PANEL_COLUMNS
from college_closure.qa import missingness_table, write_qa_counts

LOGGER = logging.getLogger(__name__)


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


def build_panel(settings: Settings) -> pd.DataFrame:
    processed = settings.processed_dir
    directory = _ensure_unitid_year(pd.read_parquet(processed / "directory.parquet"))
    if directory.empty:
        raise RuntimeError("data/processed/directory.parquet is empty; run scripts/01_ingest.py first")

    keep_dir = [c for c in DIRECTORY_PANEL_COLUMNS if c in directory.columns]
    panel = directory[keep_dir].drop_duplicates(subset=["unitid", "year"])

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
    if not finance.empty:
        finance_cols = [c for c in finance.columns if c in {"unitid", "year"} or c not in panel.columns]
        panel = panel.merge(finance[finance_cols], on=["unitid", "year"], how="left")

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
            "Panel is directory-left-joined to fall enrollment, FTE, finance, admissions, and staffing.",
            "Publics remain in the panel; in_risk_model_universe=True for private nonprofit and for-profit.",
            "Urban finance currently ends in 2017, so miss_finance is expected for later years.",
        ],
        extra_sections=[("Missingness by year", miss)],
    )
    LOGGER.info("Wrote %s", settings.outputs_dir / "qa_panel.md")
    return panel
