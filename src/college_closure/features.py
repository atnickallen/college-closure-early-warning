"""Institution-year features. Trailing windows only — no future leakage."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from college_closure.config import Settings
from college_closure.constants import FAITH_RELATED_CC_BASIC

LOGGER = logging.getLogger(__name__)

RATIO_COLS = [
    "tuition_dependence",
    "discount_rate",
    "operating_margin",
    "endowment_per_fte",
    "unrestricted_na_to_exp",
    "student_staff_ratio",
    "enr_pct_chg_1y",
    "enr_pct_chg_5y",
    "enr_pct_chg_10y",
    "fte_pct_chg_1y",
    "staff_pct_chg_1y",
    "staff_pct_chg_5y",
    "admit_rate",
    "yield_rate",
    "admit_rate_chg_5y",
    "yield_rate_chg_5y",
    "discount_rate_chg_5y",
    "operating_margin_chg_5y",
    "ftft_pct_chg_1y",
    "student_staff_ratio_chg_1y",
]


def _group_shift(df: pd.DataFrame, col: str, periods: int) -> pd.Series:
    return df.groupby("unitid", sort=False)[col].shift(periods)


def _pct_change_back(df: pd.DataFrame, col: str, years: int) -> pd.Series:
    lagged = _group_shift(df, col, years)
    current = pd.to_numeric(df[col], errors="coerce")
    lagged = pd.to_numeric(lagged, errors="coerce")
    return current / lagged.replace({0: np.nan}) - 1


def _winsorize(series: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() < 20:
        return s
    qlo, qhi = s.quantile(lo), s.quantile(hi)
    return s.clip(qlo, qhi)


def _consecutive_neg(df: pd.DataFrame, flag_col: str, window: int = 5) -> pd.Series:
    """Count of negative flags in the current year and prior window-1 years."""
    return (
        df.groupby("unitid", sort=False)[flag_col]
        .rolling(window, min_periods=1)
        .sum()
        .reset_index(level=0, drop=True)
    )


def build_features(settings: Settings, panel: pd.DataFrame | None = None) -> pd.DataFrame:
    processed = settings.processed_dir
    if panel is None:
        panel = pd.read_parquet(processed / "panel.parquet")
    df = panel.sort_values(["unitid", "year"]).copy()
    df["unitid"] = pd.to_numeric(df["unitid"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    def _num(col: str) -> pd.Series:
        if col not in df.columns:
            return pd.Series(np.nan, index=df.index)
        return pd.to_numeric(df[col], errors="coerce")

    fte = _num("enrollment_fte")
    if fte.isna().all() and "enrollment_fall_total" in df.columns:
        fte = _num("enrollment_fall_total")
    headcount = _num("enrollment_fall_total")
    df["fte"] = fte.where(fte.notna(), headcount)
    df["log_fte"] = np.log(df["fte"].where(df["fte"] > 0))
    df["fte_under_1000"] = (df["fte"] < 1000) & df["fte"].notna()

    for years, name in ((1, "enr_pct_chg_1y"), (5, "enr_pct_chg_5y"), (10, "enr_pct_chg_10y")):
        df[name] = _pct_change_back(df, "fte", years)
    df["fte_pct_chg_1y"] = df["enr_pct_chg_1y"]
    df["enr_decline_5y_gt30"] = df["enr_pct_chg_5y"] <= -0.30

    # First-time / yield from admissions (contemporaneous survey year)
    applied = _num("number_applied")
    admitted = _num("number_admitted")
    enrolled = _num("number_enrolled_total")
    df["admit_rate"] = admitted / applied.replace({0: np.nan})
    df["yield_rate"] = enrolled / admitted.replace({0: np.nan})
    df["ftft_enrolled"] = enrolled
    df["ftft_pct_chg_1y"] = _pct_change_back(df, "ftft_enrolled", 1)
    df["admit_rate_chg_5y"] = df["admit_rate"] - _group_shift(df, "admit_rate", 5)
    df["yield_rate_chg_5y"] = df["yield_rate"] - _group_shift(df, "yield_rate", 5)

    rev = _num("rev_total_current")
    exp = _num("exp_total_current")
    tuition = _num("rev_tuition_fees_net")
    if tuition.isna().all():
        tuition = _num("rev_tuition_fees_gross")
    allow = _num("sch_allowances_tuition_fees")
    inst_grants = _num("sch_grants_institutional")
    gross_tuition = _num("rev_tuition_fees_gross")
    endowment = _num("endowment_end")
    unrestricted = _num("assets_net")

    df["net_tuition"] = tuition
    df["tuition_dependence"] = tuition / rev.replace({0: np.nan})
    discount_num = allow.where(allow.notna(), inst_grants)
    discount_den = gross_tuition.where(gross_tuition.notna() & (gross_tuition > 0), tuition + discount_num.fillna(0))
    df["discount_rate"] = discount_num / discount_den.replace({0: np.nan})
    df["operating_margin"] = (rev - exp) / rev.replace({0: np.nan})
    df["neg_margin"] = df["operating_margin"] < 0
    df["consec_neg_margin_yrs"] = _consecutive_neg(df, "neg_margin", 5)
    df["endowment_per_fte"] = endowment / df["fte"].replace({0: np.nan})
    df["unrestricted_na_to_exp"] = unrestricted / exp.replace({0: np.nan})
    # Simple revenue concentration: tuition share (already tuition_dependence);
    # also flag high dependence.
    df["high_tuition_dependence"] = df["tuition_dependence"] >= 0.70
    df["discount_rate_chg_5y"] = df["discount_rate"] - _group_shift(df, "discount_rate", 5)
    df["operating_margin_chg_5y"] = df["operating_margin"] - _group_shift(df, "operating_margin", 5)
    df["miss_finance"] = rev.isna()
    if "finance_from_parent" in df.columns:
        df["finance_from_parent"] = df["finance_from_parent"].fillna(False).astype(bool)
    else:
        df["finance_from_parent"] = False

    staff = _num("staff_total")
    if staff.isna().all():
        staff = _num("instruc_staff_count")
    df["staff_fte"] = staff
    df["staff_pct_chg_1y"] = _pct_change_back(df, "staff_fte", 1)
    df["staff_pct_chg_5y"] = _pct_change_back(df, "staff_fte", 5)
    df["student_staff_ratio"] = df["fte"] / staff.replace({0: np.nan})
    df["student_staff_ratio_chg_1y"] = df["student_staff_ratio"] - _group_shift(df, "student_staff_ratio", 1)

    # Distress: composite is historical (Urban ~2006–2016, plus any official FSA
    # workbook years). Forward-fill within UNITID so later years carry the *last
    # observed* score (lagged — not a future value). Contemporaneous missingness
    # is kept as its own feature. HCM is current-only and is NOT a training feature.
    if "composite_score" not in df.columns:
        df["composite_score"] = pd.NA
    df["miss_composite"] = pd.to_numeric(df["composite_score"], errors="coerce").isna()
    df["composite_score"] = df.groupby("unitid", sort=False)["composite_score"].ffill()
    df["composite_is_lagged"] = df["miss_composite"] & pd.to_numeric(df["composite_score"], errors="coerce").notna()
    df["composite_fail"] = pd.to_numeric(df["composite_score"], errors="coerce") < 1.0
    df["composite_zone"] = (pd.to_numeric(df["composite_score"], errors="coerce") >= 1.0) & (
        pd.to_numeric(df["composite_score"], errors="coerce") < 1.5
    )
    df["years_in_zone"] = _consecutive_neg(df, "composite_zone", 5)

    faith = pd.Series(False, index=df.index)
    for col in ("cc_basic_2021", "cc_basic_2018", "cc_basic_2015"):
        if col in df.columns:
            faith = faith | pd.to_numeric(df[col], errors="coerce").isin(FAITH_RELATED_CC_BASIC)
    df["religious"] = faith
    locale = _num("urban_centric_locale")
    df["urban"] = locale.isin([1, 2, 11, 12, 13])
    df["rural"] = locale.isin([41, 42, 43, 7, 8])

    wiche_path = settings.root / str((settings.raw.get("wiche") or {}).get("path") or "data/external/wiche_hs_graduates.csv")
    if Path(wiche_path).exists() and "state_abbr" in df.columns:
        wiche = pd.read_csv(wiche_path)
        year_col = next((c for c in wiche.columns if c.lower() in {"year", "class_year"} or c.lower() == "year"), None)
        if year_col is None:
            year_col = next((c for c in wiche.columns if "year" in c.lower()), None)
        state_col = next((c for c in wiche.columns if c.lower() in {"state_abbr", "stabbr", "state"}), None)
        val_col = next((c for c in wiche.columns if c.lower() in {"hs_graduates", "students", "graduates"}), None)
        if year_col and state_col and val_col:
            wiche = wiche.rename(columns={year_col: "year", state_col: "state_abbr", val_col: "hs_graduates"})
            df = df.merge(wiche[["state_abbr", "year", "hs_graduates"]], on=["state_abbr", "year"], how="left")
            df["hs_grad_pct_chg_5y"] = _pct_change_back(df, "hs_graduates", 5)
        else:
            df["hs_grad_pct_chg_5y"] = pd.NA
    else:
        if not Path(wiche_path).exists():
            LOGGER.info("No WICHE CSV at %s; skipping state HS-grad trend", wiche_path)
        df["hs_grad_pct_chg_5y"] = pd.NA

    for col in RATIO_COLS:
        if col in df.columns:
            df[col] = _winsorize(df[col])

    dest = processed / "features.parquet"
    df.to_parquet(dest, index=False)
    LOGGER.info("Features %s rows × %s cols -> %s", len(df), df.shape[1], dest)
    return df


MODEL_FEATURE_COLUMNS = [
    "log_fte",
    "fte_under_1000",
    "enr_pct_chg_1y",
    "enr_pct_chg_5y",
    "enr_pct_chg_10y",
    "enr_decline_5y_gt30",
    "ftft_pct_chg_1y",
    "admit_rate",
    "yield_rate",
    "admit_rate_chg_5y",
    "yield_rate_chg_5y",
    "tuition_dependence",
    "discount_rate",
    "discount_rate_chg_5y",
    "operating_margin",
    "operating_margin_chg_5y",
    "consec_neg_margin_yrs",
    "endowment_per_fte",
    "unrestricted_na_to_exp",
    "high_tuition_dependence",
    "miss_finance",
    "finance_from_parent",
    "composite_is_lagged",
    "staff_pct_chg_1y",
    "staff_pct_chg_5y",
    "student_staff_ratio",
    "student_staff_ratio_chg_1y",
    "composite_score",
    "composite_fail",
    "composite_zone",
    "years_in_zone",
    "miss_composite",
    "is_four_year",
    "religious",
    "urban",
    "rural",
    "inst_control",
    "sector",
    "hs_grad_pct_chg_5y",
]
