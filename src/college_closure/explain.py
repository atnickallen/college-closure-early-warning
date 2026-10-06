"""Per-school account of the published risk score.

The published score is the XGBoost probability on the vintage snapshot.
Contributions are TreeSHAP values in probability units. Missing inputs stay
missing: this booster does not median-fill them. The logistic baseline would.
Ratio features were winsorized to the 1st–99th percentile of the feature
panel before the published score was fit.
"""

from __future__ import annotations

import html
import math
from pathlib import Path

import numpy as np
import pandas as pd

from college_closure.features import MODEL_FEATURE_COLUMNS, RATIO_COLS
from college_closure.model import _fit_booster, _load_modeling_frame, _xy, available_features, predict_proba
from college_closure.vintage import SOURCE_FEATURES, SOURCE_YEAR_COLUMNS

FEATURE_LABELS = {
    "log_fte": "Log enrollment (FTE)",
    "fte_under_1000": "FTE under 1,000",
    "enr_pct_chg_1y": "Enrollment change, 1 year",
    "enr_pct_chg_5y": "Enrollment change, 5 years",
    "enr_pct_chg_10y": "Enrollment change, 10 years",
    "enr_decline_5y_gt30": "Enrollment down more than 30% in 5 years",
    "ftft_pct_chg_1y": "First-time enrollment change, 1 year",
    "admit_rate": "Admit rate",
    "yield_rate": "Yield rate",
    "admit_rate_chg_5y": "Admit-rate change, 5 years",
    "yield_rate_chg_5y": "Yield-rate change, 5 years",
    "tuition_dependence": "Tuition share of revenue",
    "discount_rate": "Discount rate",
    "discount_rate_chg_5y": "Discount-rate change, 5 years",
    "operating_margin": "Operating margin",
    "operating_margin_chg_5y": "Operating-margin change, 5 years",
    "consec_neg_margin_yrs": "Negative-margin years in the last 5",
    "endowment_per_fte": "Endowment per FTE",
    "unrestricted_na_to_exp": "Net assets per dollar of expense",
    "high_tuition_dependence": "Tuition is at least 70% of revenue",
    "miss_finance": "Finance missing on the scored row",
    "finance_from_parent": "Finance copied from a parent campus",
    "composite_is_lagged": "Composite score is carried forward",
    "staff_pct_chg_1y": "Staff change, 1 year",
    "staff_pct_chg_5y": "Staff change, 5 years",
    "student_staff_ratio": "Students per staff member",
    "student_staff_ratio_chg_1y": "Student-staff ratio change, 1 year",
    "composite_score": "Federal composite score",
    "composite_fail": "Composite below 1.0",
    "composite_zone": "Composite in the 1.0–1.5 zone",
    "years_in_zone": "Years in the composite zone",
    "miss_composite": "Composite score missing",
    "is_four_year": "Four-year institution",
    "religious": "Faith-related Carnegie class",
    "urban": "Urban locale",
    "rural": "Rural locale",
    "inst_control": "Control (2 nonprofit, 3 for-profit)",
    "sector": "Sector",
    "hs_grad_pct_chg_5y": "State high-school graduates, 5-year change",
}

# Branch or seminary whose own finance extract is empty, and the campus
# in this extract that actually files IPEDS finance.
SYSTEM_FINANCE_FILER = {
    464226: 155627,  # Ottawa University-Surprise -> Ottawa University-Ottawa
    215813: 215798,  # Saint Vincent Seminary -> Saint Vincent College
    184694: 184603,  # Fairleigh Dickinson Florham -> Metropolitan campus, the parent filer
}

PCT_FEATURES = {
    "enr_pct_chg_1y",
    "enr_pct_chg_5y",
    "enr_pct_chg_10y",
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
    "staff_pct_chg_1y",
    "staff_pct_chg_5y",
    "hs_grad_pct_chg_5y",
}

FEATURE_SOURCE_YEAR = {}
for _source, _pairs in SOURCE_FEATURES.items():
    _year_col = SOURCE_YEAR_COLUMNS.get(_source)
    for _feature, _ in _pairs:
        if _feature in MODEL_FEATURE_COLUMNS and _year_col:
            FEATURE_SOURCE_YEAR[_feature] = _year_col


def _num(value) -> float | None:
    try:
        if value is None or pd.isna(value):
            return None
    except (TypeError, ValueError):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def _year(value) -> int | None:
    number = _num(value)
    if number is None:
        return None
    return int(number)


def _unitid(value) -> int | None:
    number = _num(value)
    if number is None:
        return None
    return int(number)


def feature_label(name: str) -> str:
    return FEATURE_LABELS.get(name, name.replace("_", " "))


def money(value) -> str:
    number = _num(value)
    if number is None:
        return ""
    sign = "-" if number < 0 else ""
    number = abs(number)
    if number >= 1_000_000_000:
        return f"{sign}${number / 1_000_000_000:.2f} billion"
    if number >= 1_000_000:
        return f"{sign}${number / 1_000_000:.1f} million"
    return f"{sign}${number:,.0f}"


def _fmt_count(value) -> str:
    number = _num(value)
    if number is None:
        return "not reported"
    return f"{number:,.0f}"


def _fmt_feature(name: str, value) -> str:
    number = _num(value)
    if number is None:
        return "missing"
    if name in PCT_FEATURES:
        return f"{number:+.0%}" if "chg" in name or name.endswith("_5y") else f"{number:.0%}"
    if name == "endowment_per_fte":
        return money(number)
    if name in {"log_fte"}:
        return f"{math.exp(number):,.0f} FTE" if number > 0 else f"{number:.2f}"
    if name in {"admit_rate_chg_5y", "yield_rate_chg_5y", "discount_rate_chg_5y", "operating_margin_chg_5y"}:
        return f"{number:+.0%}"
    if float(number).is_integer() and name not in {"composite_score", "student_staff_ratio", "unrestricted_na_to_exp"}:
        return f"{int(number)}"
    return f"{number:.2f}"


def plain_driver(name: str, value, year, *, context: dict | None = None) -> str:
    """One sentence a reader can check against the raw figure."""
    context = context or {}
    year_bit = f" ({year})" if year else ""
    number = _num(value)
    if name == "enr_pct_chg_5y" and number is not None:
        fall_change = _num(context.get("fall_headcount_pct_change"))
        start = context.get("fall_headcount_earlier")
        end = context.get("fall_headcount")
        y0 = context.get("fall_year_earlier")
        y1 = context.get("fall_year")
        if (
            start is not None
            and end is not None
            and y0
            and y1
            and fall_change is not None
            and abs(fall_change - number) <= 0.10
        ):
            return (
                f"fall headcount moved from {_fmt_count(start)} in {y0} to {_fmt_count(end)} in {y1} "
                f"({fall_change:+.0%})"
            )
        fte_then = context.get("fte_earlier")
        fte_now = context.get("fte_count")
        if fte_then is not None and fte_now is not None and context.get("fte_year_earlier") and context.get("fte_year"):
            return (
                f"FTE moved from {_fmt_count(fte_then)} in {context['fte_year_earlier']} "
                f"to {_fmt_count(fte_now)} in {context['fte_year']} ({number:+.0%})"
            )
        return f"FTE enrollment changed {number:+.0%} over five years{year_bit}"
    if name == "enr_pct_chg_1y" and number is not None:
        return f"FTE enrollment changed {number:+.0%} in one year{year_bit}"
    if name == "enr_pct_chg_10y" and number is not None:
        return f"FTE enrollment changed {number:+.0%} over ten years{year_bit}"
    if name == "enr_decline_5y_gt30":
        return (
            "five-year enrollment is down more than 30%"
            if number
            else "five-year enrollment is not down more than 30%"
        )
    if name == "tuition_dependence" and number is not None:
        return f"tuition is {number:.0%} of revenue{year_bit}"
    if name == "high_tuition_dependence":
        return "tuition is at least 70% of revenue" if number else "tuition is under 70% of revenue"
    if name == "discount_rate" and number is not None:
        return f"the discount rate is {number:.0%}{year_bit}"
    if name == "operating_margin" and number is not None:
        return f"the operating margin is {number:+.0%}{year_bit}"
    if name == "endowment_per_fte" and number is not None:
        expenses = context.get("expenses")
        endow = context.get("endowment_market_value")
        if endow and expenses and expenses > 0:
            years = float(endow) / float(expenses)
            return f"endowment covers {years:.1f} years of expenses, {money(number)} per FTE{year_bit}"
        return f"endowment is {money(number)} per FTE{year_bit}"
    if name == "unrestricted_na_to_exp" and number is not None:
        return f"net assets cover {number:.1f} years of expenses{year_bit}"
    if name == "miss_finance":
        return (
            "IPEDS finance is missing on the scored row"
            if number
            else "IPEDS finance is present on the scored row"
        )
    if name == "miss_composite":
        return "no federal composite score is on the scored row" if number else "a composite score is on the row"
    if name == "composite_score" and number is not None:
        return f"the federal composite score is {number:.2f}{year_bit}"
    if name == "composite_fail":
        return "the composite score is below 1.0" if number else "the composite score is not below 1.0"
    if name == "composite_zone":
        return "the composite score is in the 1.0–1.5 zone" if number else "the composite score is outside the zone"
    if name == "fte_under_1000":
        fte = context.get("fte_count")
        if number and fte is not None:
            return f"enrollment is {_fmt_count(fte)} FTE, under 1,000"
        return "FTE is under 1,000" if number else "FTE is 1,000 or more"
    if name == "log_fte":
        if number is None:
            return "enrollment is missing on the scored row"
        return f"enrollment is about {math.exp(number):,.0f} FTE{year_bit}"
    if name == "rural":
        return "the locale code is rural" if number else "the locale code is not rural"
    if name == "urban":
        return "the locale code is urban" if number else "the locale code is not urban"
    if name == "religious":
        return "the Carnegie class is faith-related" if number else "the Carnegie class is not faith-related"
    if name == "is_four_year":
        return "the school is coded four-year" if number else "the school is not coded four-year"
    if name == "inst_control" and number is not None:
        label = {1: "public", 2: "private nonprofit", 3: "for-profit"}.get(int(number), str(int(number)))
        return f"control is {label}"
    if name == "composite_is_lagged":
        return (
            "the composite score was carried forward from an older official year"
            if number
            else "the composite score was not carried forward"
        )
    if name == "finance_from_parent":
        parent = context.get("finance_parent_unitid") if context else None
        if number and parent:
            return f"finance from parent UNITID {int(parent)}"
        return "finance on the scored row was copied from a parent campus" if number else "finance was not copied from a parent"
    if name == "consec_neg_margin_yrs" and number is not None:
        return f"{int(number)} of the last 5 years show a negative margin"
    if name == "student_staff_ratio" and number is not None:
        return f"there are {number:.1f} students per staff member{year_bit}"
    if name == "ftft_pct_chg_1y" and number is not None:
        return f"first-time enrollment changed {number:+.0%} in one year{year_bit}"
    if name == "yield_rate" and number is not None:
        return f"yield is {number:.0%}{year_bit}"
    if name == "admit_rate" and number is not None:
        return f"the admit rate is {number:.0%}{year_bit}"
    if number is None:
        return f"{feature_label(name)} is missing on the scored row"
    shown = _fmt_feature(name, number)
    return f"{feature_label(name).lower()} is {shown}{year_bit}"


def fill_method(name: str, value, row: pd.Series) -> str:
    """How the published booster saw this input. XGBoost does not median-fill."""
    if _num(value) is None and name not in {"fte_under_1000", "enr_decline_5y_gt30", "high_tuition_dependence", "composite_fail", "composite_zone"}:
        return (
            "Left missing. The published XGBoost score follows the missing branch. "
            "It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank."
        )
    if name.startswith("composite") and bool(row.get("composite_is_lagged")):
        return "Carried forward from the last official composite year. composite_is_lagged is true."
    if name in {
        "tuition_dependence",
        "discount_rate",
        "operating_margin",
        "endowment_per_fte",
        "unrestricted_na_to_exp",
        "high_tuition_dependence",
        "consec_neg_margin_yrs",
        "discount_rate_chg_5y",
        "operating_margin_chg_5y",
    } and bool(row.get("finance_from_parent")):
        parent = row.get("parent_unitid")
        parent_txt = ""
        parent_num = _num(parent)
        if parent_num is not None:
            parent_txt = f" UNITID {int(parent_num)}"
        return (
            f"Copied from the parent campus finance row{parent_txt}, then winsorized with the rest of the panel. "
            "Enrollment is this campus's own count."
        )
    if name in RATIO_COLS:
        return "Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring."
    return "Reported on the scored row. Not imputed."


def quality_flags(row: pd.Series, facts: dict) -> list[str]:
    """Data-quality notes. These do not change the score."""
    flags = []
    miss_finance = bool(row.get("miss_finance"))
    if miss_finance and facts.get("extract_has_finance"):
        flags.append(
            "Finance is missing on the scored row even though the IPEDS finance extract has a filing for this UNITID. "
            "The vintage snapshot never saw it."
        )
    if miss_finance and facts.get("system_filer_unitid"):
        flags.append(
            f"This campus has no finance row in the extract. IPEDS finance for the system is filed under UNITID {facts['system_filer_unitid']} "
            f"({facts.get('system_filer_name') or 'the finance-reporting campus'})."
        )
    if bool(row.get("finance_from_parent")):
        parent = _num(row.get("parent_unitid")) or _num(facts.get("finance_parent_unitid"))
        if parent is not None:
            flags.append(f"finance from parent UNITID {int(parent)}")
        else:
            flags.append("finance from parent")
    investment = _num(facts.get("investment_return"))
    revenue = _num(facts.get("revenue"))
    if investment is not None and revenue not in (None, 0) and abs(investment) > 0.5 * abs(revenue):
        flags.append(
            f"Investment return ({money(investment)}) is more than half of reported revenue ({money(revenue)}). "
            "The IPEDS operating margin is not a tuition operating result."
        )
    tuition = _num(facts.get("net_tuition"))
    if tuition is not None and revenue not in (None, 0) and tuition / revenue < 0.05 and not miss_finance:
        flags.append(
            f"Net tuition ({money(tuition)}) is under 5% of revenue ({money(revenue)}). Tuition dependence near zero can be a reporting form, not a pricing collapse."
        )
    change = _num(row.get("enr_pct_chg_5y"))
    if change is not None and abs(change) >= 0.50:
        flags.append(f"Five-year FTE change is {change:+.0%}, an outlier against a typical campus.")
    fall_change = _num(facts.get("fall_headcount_pct_change"))
    if change is not None and fall_change is not None and abs(change - fall_change) > 0.25:
        flags.append(
            f"The model's five-year enrollment feature is the FTE change ({change:+.0%}). "
            f"Fall headcount changed {fall_change:+.0%} over the years shown on the card. Those are different counts."
        )
    missing_n = facts.get("n_missing_features")
    if missing_n is not None and missing_n >= 20:
        flags.append(
            f"{missing_n} of {len(MODEL_FEATURE_COLUMNS)} model features are missing on the scored row. "
            "The rank is mostly a missingness pattern."
        )
    if facts.get("endowment_scope") == "not reported" and facts.get("control") == 2 and facts.get("extract_has_finance"):
        flags.append(
            "This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted."
        )
    if facts.get("control") == 3 and not facts.get("endowment_market_value"):
        flags.append(
            "For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990."
        )
    return flags


def suspected_artifact(flags: list[str], top_features: list[str]) -> tuple[bool, str]:
    text = " ".join(flags)
    drivers = set(top_features)
    missingness_drove = bool(drivers & {"miss_finance", "log_fte", "miss_composite", "fte_under_1000"})
    if "never saw it" in text or "missingness pattern" in text or "filed under UNITID" in text:
        return True, text
    _ = missingness_drove
    _ = drivers
    return False, ""


def _clean(value) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    if text.lower() in {"nan", "none", "<na>"}:
        return ""
    return text


def facts_html(summary: dict) -> str:
    """Endowment and enrollment, outside the collapsible score panel."""
    endow = summary.get("endowment_market_value")
    endow_year = summary.get("endowment_year") or ""
    per_fte = summary.get("endowment_per_fte_display")
    scope = summary.get("endowment_scope") or ""
    endow_txt = money(endow) if _num(endow) is not None else "not reported"
    parent_flag = ""
    parent_num = _num(summary.get("finance_parent_unitid")) or _num(summary.get("system_filer_unitid"))
    from_parent = str(summary.get("finance_from_parent")).strip().lower() in {"true", "1", "1.0", "yes"}
    if from_parent and parent_num is not None:
        parent_flag = f'<p class="fact-note">finance from parent UNITID {int(parent_num)}</p>'
    if endow_year:
        endow_txt += f" (IPEDS finance {endow_year}"
        endow_txt += ", this campus" if scope == "this campus" else ""
        if scope in {"system filing", "parent filing"} and parent_num is not None:
            endow_txt += f", finance from parent UNITID {int(parent_num)}"
        endow_txt += ")"
    per_txt = money(per_fte) + " per FTE" if _num(per_fte) is not None else "per FTE not reported"
    fall = _fmt_count(summary.get("fall_headcount"))
    ug = _fmt_count(summary.get("fall_undergrad"))
    grad = summary.get("fall_grad")
    grad_txt = _fmt_count(grad) if _num(grad) is not None else "not reported"
    fall_year = summary.get("fall_year") or ""
    fte = _fmt_count(summary.get("fte_count"))
    fte_year = summary.get("fte_year") or ""
    earlier = summary.get("fall_headcount_earlier")
    y0 = summary.get("fall_year_earlier")
    y1 = summary.get("fall_year")
    change = _num(summary.get("fall_headcount_pct_change"))
    if _num(earlier) is not None and y0 and y1 and change is not None:
        trend = f"{_fmt_count(earlier)} in {y0} to {fall} in {y1} ({change:+.0%})"
    else:
        trend = "five-year fall headcount not available"
    source = _clean(summary.get("endowment_source")) or "IPEDS finance extract"
    enr_source = _clean(summary.get("enrollment_source")) or "IPEDS fall enrollment and enrollment FTE extracts"
    note = _clean(summary.get("endowment_note"))
    note_html = f"<p class=\"fact-note\">{html.escape(note)}</p>" if note else ""
    return f"""
      <h3>Endowment and enrollment</h3>
      {parent_flag}
      <table class="facts">
        <tr><th>Endowment</th><td>{html.escape(endow_txt)}</td>
            <th>Per FTE</th><td>{html.escape(per_txt)}</td></tr>
        <tr><th>Fall headcount</th><td>{html.escape(fall)}{(' in ' + html.escape(str(fall_year))) if fall_year else ''}
            (undergraduate {html.escape(ug)}; graduate {html.escape(grad_txt)})</td>
            <th>FTE</th><td>{html.escape(fte)}{(' in ' + html.escape(str(fte_year))) if fte_year else ''}</td></tr>
        <tr><th>Fall headcount, 5-year</th><td colspan="3">{html.escape(trend)}</td></tr>
      </table>
      <p class="fact-note">Endowment source: {html.escape(str(source))}. Enrollment source: {html.escape(str(enr_source))}.</p>
      {note_html}
    """


def why_panel_html(summary: dict, feature_rows: list[dict]) -> str:
    """Collapsible score account and a diverging contribution chart."""
    drivers = [_clean(summary.get("top_driver_1")), _clean(summary.get("top_driver_2")), _clean(summary.get("top_driver_3"))]
    driver_html = "".join(f"<li>{html.escape(item)}</li>" for item in drivers if item)
    if not driver_html:
        driver_html = "<li>Drivers were not computed for this card.</li>"
    flags = _clean(summary.get("data_quality_flags"))
    missing = _clean(summary.get("missing_or_imputed"))
    artifact = _clean(summary.get("artifact_reason"))
    artifact_html = f"<p><strong>Suspected data artifact.</strong> {html.escape(str(artifact))}</p>" if artifact else ""
    shown = list(feature_rows)[:8]
    max_abs = max((abs(_num(row.get("contribution")) or 0.0) for row in shown), default=0.0) or 1.0
    bars = []
    for row in shown:
        contrib = _num(row.get("contribution")) or 0.0
        width = min(50.0, 50.0 * abs(contrib) / max_abs)
        if contrib >= 0:
            style = f"left:50%;width:{width:.1f}%"
            css = "up"
        else:
            style = f"left:{50.0 - width:.1f}%;width:{width:.1f}%"
            css = "down"
        label = feature_label(str(row.get("feature") or ""))
        bars.append(
            "<div class=\"bar\">"
            f"<span class=\"bar-label\">{html.escape(label)}</span>"
            "<span class=\"track\"><span class=\"fill "
            f"{css}\" style=\"{style}\"></span></span>"
            f"<span class=\"bar-num\">{contrib:+.3f}</span></div>"
        )
    score = summary.get("risk_score")
    composite = summary.get("composite_score")
    composite_year = summary.get("composite_year") or "—"
    score_txt = f"{float(score):.3f}" if _num(score) is not None else "—"
    comp_txt = f"{float(composite):.2f}" if _num(composite) is not None else "missing"
    return f"""
      <details class="why">
        <summary>Why it ranks here</summary>
        <p>Published risk score <strong>{score_txt}</strong>
        (XGBoost probability, not a closure chance).
        Federal composite score {html.escape(comp_txt)} (year {html.escape(str(composite_year))}).
        Contributions are TreeSHAP values in probability units and sum with the base rate to this score.
        A positive bar raises the score.</p>
        <ol>{driver_html}</ol>
        <div class="bars">{''.join(bars)}</div>
        <p class="fact-note">Missing or imputed: {html.escape(str(missing))}</p>
        <p class="fact-note">Data-quality flags: {html.escape(str(flags) or 'none')}</p>
        {artifact_html}
      </details>
    """


WHY_CSS = """
    table.facts th { width: 18%; }
    .fact-note { color: #555; font-size: 0.9rem; }
    details.why { margin: 0.8rem 0; border-top: 1px solid #eee; padding-top: 0.4rem; }
    details.why summary { cursor: pointer; font-weight: 600; }
    .bar { display: flex; align-items: center; gap: 0.4rem; margin: 0.15rem 0; font-size: 0.85rem; }
    .bar-label { flex: 0 0 16rem; }
    .track { position: relative; flex: 1; height: 0.7rem; background: #f3f3f3; }
    .fill { position: absolute; top: 0; bottom: 0; }
    .fill.up { background: #8c3a3a; }
    .fill.down { background: #2f5d50; }
    .bar-num { flex: 0 0 4.2rem; text-align: right; font-variant-numeric: tabular-nums; }
"""


def _feature_year(row: pd.Series, feature: str) -> int | None:
    direct = _year(row.get(f"{feature}_year"))
    if direct is not None:
        return direct
    source_col = FEATURE_SOURCE_YEAR.get(feature)
    if source_col:
        return _year(row.get(source_col))
    return None


def _percentile(value, series: pd.Series) -> float | None:
    number = _num(value)
    if number is None:
        return None
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return None
    return float((clean <= number).mean() * 100.0)


def _zscore(value, series: pd.Series) -> float | None:
    number = _num(value)
    if number is None:
        return None
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if len(clean) < 5:
        return None
    std = float(clean.std(ddof=0))
    if std == 0:
        return 0.0
    return float((number - float(clean.mean())) / std)


def fit_published_booster(settings):
    """Refit the published booster. random_state=42 matches scripts/06_model.py."""
    feat = _load_modeling_frame(settings)
    label = "closed_or_merged_within_3_years"
    if "in_risk_model_universe" in feat.columns:
        univ = feat.loc[feat["in_risk_model_universe"] == True].copy()  # noqa: E712
    else:
        univ = feat.copy()
    if "label_complete_h3" in univ.columns:
        complete = univ.loc[univ["label_complete_h3"] == True].copy()  # noqa: E712
    else:
        complete = univ.loc[univ[label].notna()].copy()
    cfg_model = settings.raw.get("model") or {}
    train_end = int(cfg_model.get("train_end", 2016))
    features = available_features(complete)
    train = complete.loc[complete["year"] <= train_end]
    X_train, y_train = _xy(train, features, label)
    booster, name = _fit_booster(X_train, y_train)
    return booster, name, features, univ


def probability_contributions(model, frame: pd.DataFrame, features: list[str]) -> tuple[np.ndarray, float]:
    """TreeSHAP in probability units. Rows sum with the base rate to the score."""
    import shap

    X = frame[features].apply(pd.to_numeric, errors="coerce")
    booster = model.get_booster() if hasattr(model, "get_booster") else model
    explainer = shap.TreeExplainer(booster)
    shap_values = explainer.shap_values(X)
    if isinstance(shap_values, list):
        shap_values = shap_values[-1]
    shap_values = np.asarray(shap_values, dtype=float)
    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, -1]
    expected = explainer.expected_value
    if isinstance(expected, (list, np.ndarray)):
        expected = float(np.asarray(expected).reshape(-1)[-1])
    else:
        expected = float(expected)
    scores = predict_proba(model, X)
    # XGBoost TreeSHAP on the raw booster is in margin (log-odds) units.
    # Rescale each row so the parts plus a base rate equal the probability score.
    base_prob = float(expected) if 0.0 <= float(expected) <= 1.0 else _sigmoid(float(expected))
    adjusted = np.zeros_like(shap_values)
    bases = np.zeros(len(X))
    for i, score in enumerate(scores):
        gap = float(score) - base_prob
        total = float(shap_values[i].sum())
        if abs(total) > 1e-12:
            adjusted[i] = shap_values[i] * (gap / total)
        bases[i] = float(score) - float(adjusted[i].sum())
    return adjusted, float(np.median(bases))


def _sigmoid(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1.0 / (1.0 + z)
    z = math.exp(value)
    return z / (1.0 + z)


def global_weights(model, train_X: pd.DataFrame, features: list[str]) -> dict[str, float]:
    import shap

    sample = train_X
    if len(sample) > 800:
        sample = sample.sample(n=800, random_state=42)
    sample = sample[features].apply(pd.to_numeric, errors="coerce")
    # Median fill is only for the global-weight sample. Row contributions keep NaN.
    sample = sample.fillna(sample.median(numeric_only=True))
    booster = model.get_booster() if hasattr(model, "get_booster") else model
    explainer = shap.TreeExplainer(booster)
    values = np.abs(np.asarray(explainer.shap_values(sample), dtype=float)).mean(axis=0)
    total = float(values.sum()) or 1.0
    return {features[i]: float(values[i] / total) for i in range(len(features))}


def _read(path: Path, columns: list[str] | None = None) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_parquet(path, columns=columns) if columns else pd.read_parquet(path)
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    if "year" in frame.columns:
        frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    return frame


def measure_facts(
    processed: Path,
    unitids: list[int],
    names: dict[int, str],
    parents: dict[int, int] | None = None,
) -> dict[int, dict]:
    """Endowment and enrollment from the extracts, including years the panel dropped."""
    finance = _read(
        processed / "finance.parquet",
        ["unitid", "year", "endowment_end", "rev_total_current", "rev_tuition_fees_net", "exp_total_current", "rev_investment_return"],
    )
    fall = _read(
        processed / "fall_enrollment.parquet",
        ["unitid", "year", "enrollment_fall_ug", "enrollment_fall_grad", "enrollment_fall_total"],
    )
    fte = _read(processed / "enrollment_fte.parquet", ["unitid", "year", "enrollment_fte"])
    out = {}
    for unitid in unitids:
        facts = _one_measure(unitid, finance, fall, fte, names)
        filer = (parents or {}).get(unitid) or SYSTEM_FINANCE_FILER.get(unitid)
        # A parent pointer from the scored row means the published ratios are the
        # parent's. An older extract row (the Institute's last own filing is 2008)
        # is not the finance the score used.
        scored_from_parent = unitid in (parents or {})
        if filer and (scored_from_parent or not facts.get("extract_has_finance")):
            parent = _one_measure(filer, finance, fall, fte, names)
            if parent.get("extract_has_finance"):
                facts["finance_from_parent"] = True
                facts["finance_parent_unitid"] = filer
                facts["system_filer_unitid"] = filer
                facts["system_filer_name"] = names.get(filer) or parent.get("inst_name") or ""
                facts["endowment_scope"] = "parent filing"
                facts["endowment_market_value"] = parent.get("endowment_market_value")
                facts["endowment_year"] = parent.get("endowment_year")
                facts["revenue"] = parent.get("revenue")
                facts["expenses"] = parent.get("expenses")
                facts["net_tuition"] = parent.get("net_tuition")
                facts["investment_return"] = parent.get("investment_return")
                facts["endowment_source"] = (
                    f"IPEDS finance F2H02/F1H02 for UNITID {filer} ({facts['system_filer_name']}), "
                    "the campus that files in this extract"
                )
                own_fte = _num(facts.get("fte_count"))
                endow = _num(facts.get("endowment_market_value"))
                if own_fte and endow is not None and own_fte > 0:
                    facts["endowment_per_fte_display"] = endow / own_fte
                facts["endowment_note"] = (
                    f"finance from parent UNITID {filer}. "
                    f"The figure is the {facts['system_filer_name']} filing, "
                    "not a separate endowment measured for this campus alone. "
                    "Enrollment on this card is this campus's own headcount and FTE."
                )
        out[unitid] = facts
    return out


def _latest_year_row(frame: pd.DataFrame, unitid: int, year_max: int) -> pd.Series | None:
    if frame.empty:
        return None
    sub = frame[(frame["unitid"] == unitid) & (frame["year"] <= year_max)].sort_values("year")
    if sub.empty:
        return None
    return sub.iloc[-1]


def _one_measure(unitid: int, finance: pd.DataFrame, fall: pd.DataFrame, fte: pd.DataFrame, names: dict[int, str]) -> dict:
    facts: dict = {"unitid": unitid, "inst_name": names.get(unitid, "")}
    finance_rows = finance[finance["unitid"] == unitid] if not finance.empty else finance
    facts["extract_has_finance"] = bool(len(finance_rows))
    latest_fin = None
    if len(finance_rows):
        preferred = finance_rows[finance_rows["year"] == 2023]
        latest_fin = preferred.iloc[-1] if len(preferred) else finance_rows.sort_values("year").iloc[-1]
    if latest_fin is not None:
        facts["endowment_year"] = _year(latest_fin["year"])
        facts["revenue"] = _num(latest_fin["rev_total_current"])
        facts["expenses"] = _num(latest_fin["exp_total_current"])
        facts["net_tuition"] = _num(latest_fin["rev_tuition_fees_net"])
        facts["investment_return"] = _num(latest_fin["rev_investment_return"])
        endow = _num(latest_fin["endowment_end"])
        facts["endowment_market_value"] = endow
        if endow is None:
            facts["endowment_scope"] = "not reported"
            facts["endowment_source"] = (
                f"IPEDS finance {facts['endowment_year']} for UNITID {unitid}; endowment_end (F2H02/F1H02) is blank"
            )
        else:
            facts["endowment_scope"] = "this campus"
            facts["endowment_source"] = (
                f"IPEDS finance {facts['endowment_year']} endowment_end (FASB F2H02 or GASB F1H02) for UNITID {unitid}"
            )
    else:
        facts["endowment_scope"] = "not reported"
        facts["endowment_source"] = f"No IPEDS finance row for UNITID {unitid} in the finance extract"
    fall_rows = fall[fall["unitid"] == unitid].sort_values("year") if not fall.empty else fall
    latest_fall = fall_rows[fall_rows["year"] <= 2024].tail(1)
    if len(latest_fall):
        row = latest_fall.iloc[-1]
        facts["fall_year"] = _year(row["year"])
        facts["fall_headcount"] = _num(row["enrollment_fall_total"])
        facts["fall_undergrad"] = _num(row["enrollment_fall_ug"])
        facts["fall_grad"] = _num(row["enrollment_fall_grad"])
        earlier = fall_rows[fall_rows["year"] == int(row["year"]) - 5]
        if earlier.empty:
            earlier = fall_rows[fall_rows["year"] == 2019]
        if len(earlier) and _num(earlier.iloc[-1]["enrollment_fall_total"]) not in (None, 0):
            facts["fall_year_earlier"] = _year(earlier.iloc[-1]["year"])
            facts["fall_headcount_earlier"] = _num(earlier.iloc[-1]["enrollment_fall_total"])
            now = facts["fall_headcount"]
            then = facts["fall_headcount_earlier"]
            if now is not None and then:
                facts["fall_headcount_pct_change"] = now / then - 1.0
    fte_rows = fte[fte["unitid"] == unitid].sort_values("year") if not fte.empty else fte
    latest_fte = fte_rows[fte_rows["year"] <= 2024].tail(1)
    if len(latest_fte):
        facts["fte_year"] = _year(latest_fte.iloc[-1]["year"])
        facts["fte_count"] = _num(latest_fte.iloc[-1]["enrollment_fte"])
        earlier_fte = fte_rows[fte_rows["year"] == int(latest_fte.iloc[-1]["year"]) - 5]
        if len(earlier_fte):
            facts["fte_year_earlier"] = _year(earlier_fte.iloc[-1]["year"])
            facts["fte_earlier"] = _num(earlier_fte.iloc[-1]["enrollment_fte"])
    endow = _num(facts.get("endowment_market_value"))
    fte_n = _num(facts.get("fte_count"))
    if endow is not None and fte_n not in (None, 0) and "endowment_per_fte_display" not in facts:
        facts["endowment_per_fte_display"] = endow / fte_n
    facts["enrollment_source"] = "IPEDS fall enrollment and 12-month enrollment FTE, Urban extract"
    return facts


def load_directory_names(processed: Path) -> dict[int, str]:
    directory = _read(processed / "directory.parquet", ["unitid", "year", "inst_name", "inst_control"])
    if directory.empty:
        return {}
    latest = directory.sort_values("year").groupby("unitid", as_index=False).tail(1)
    names = {}
    for _, row in latest.iterrows():
        uid = _unitid(row["unitid"])
        if uid is None:
            continue
        names[uid] = str(row["inst_name"])
    return names


def annotate_known_filings(facts: dict) -> dict:
    """Citations for filings the model did not use, or that are easy to misread."""
    unitid = facts.get("unitid")
    note = facts.get("endowment_note") or ""
    if unitid == 148016:
        facts["endowment_note"] = (
            "IPEDS finance 2023 endowment_end for Principia College is $592,903,744 (F2H02). "
            "Data USA reports the same figure, about $593 million at the end of fiscal 2024, with a $77.5 million investment return. "
            "https://datausa.io/profile/university/principia-college. "
            "A Principia College news article calls it \"the College's $1.1 billion endowment\" and says enrollment is about 300. "
            "https://www.principiacollege.edu/article/principia-college-students-manage-six-figure-investment-fund. "
            "The Principia Corporation Form 990 (EIN 43-0652667) covers the college and the Principia School together. "
            "CauseIQ shows about $111.3 million of revenue for the year ending June 2024, and a 990 summary reports about $1.2 billion of assets. "
            "https://www.causeiq.com/organizations/the-principia-corporation,430652667/ "
            "https://philanthropy.org/990/report/430652667/the-principia-corporation/2023. "
            "The card keeps the college IPEDS line. It does not substitute the corporation total. "
            "The published score used none of these figures."
        )
        facts["endowment_source_url"] = "https://datausa.io/profile/university/principia-college"
    elif note:
        facts["endowment_note"] = note
    return facts


def residential_top50(settings) -> pd.DataFrame:
    """The 50 operating, residential, own-campus schools, in score order."""
    from college_closure.campus import _flag_true, acquisition_universe, partition_acquisition

    merged = acquisition_universe(settings)
    if "insufficient_data" in merged.columns:
        merged = merged.loc[~merged["insufficient_data"].map(_flag_true)].copy()
    open_df, _, _, _, _ = partition_acquisition(merged, 50)
    open_df = open_df.copy()
    open_df["residential_rank"] = range(1, len(open_df) + 1)
    return open_df


def build_score_explanations(settings) -> tuple[pd.DataFrame, dict]:
    """Long explanation table for the residential top 50, plus fit diagnostics."""
    booster, booster_name, features, univ = fit_published_booster(settings)
    label = "closed_or_merged_within_3_years"
    cfg_model = settings.raw.get("model") or {}
    train_end = int(cfg_model.get("train_end", 2016))
    train = univ.loc[pd.to_numeric(univ["year"], errors="coerce") <= train_end]
    if "label_complete_h3" in train.columns:
        train = train.loc[train["label_complete_h3"] == True]  # noqa: E712
    X_train, _ = _xy(train, features, label)
    weights = global_weights(booster, X_train, features)

    scored = pd.read_parquet(settings.processed_dir / "scored.parquet")
    snapshot = scored.loc[scored["vintage_snapshot"] == True].copy()  # noqa: E712
    snapshot["unitid"] = pd.to_numeric(snapshot["unitid"], errors="coerce")
    open_df = residential_top50(settings)
    names = load_directory_names(settings.processed_dir)
    for _, row in open_df.iterrows():
        uid = _unitid(row.get("unitid"))
        if uid is not None and row.get("inst_name"):
            names[uid] = str(row.get("inst_name"))
    for uid, filer in SYSTEM_FINANCE_FILER.items():
        names.setdefault(filer, names.get(filer, ""))
    controls = load_controls(settings.processed_dir)
    unitids = [_unitid(v) for v in open_df["unitid"]]
    parents: dict[int, int] = {}
    if "finance_from_parent" in snapshot.columns and "parent_unitid" in snapshot.columns:
        inherited = snapshot.loc[snapshot["finance_from_parent"].fillna(False).astype(bool)]
        for _, inherited_row in inherited.iterrows():
            child_id = _unitid(inherited_row.get("unitid"))
            parent_id = _unitid(inherited_row.get("parent_unitid"))
            if child_id and parent_id and child_id != parent_id:
                parents[child_id] = parent_id
    facts_by_id = measure_facts(
        settings.processed_dir,
        [u for u in unitids if u is not None],
        names,
        parents,
    )
    for uid in list(facts_by_id):
        facts_by_id[uid]["control"] = controls.get(uid)
        facts_by_id[uid] = annotate_known_filings(facts_by_id[uid])

    snap_rows = []
    summaries = []
    for _, school in open_df.iterrows():
        uid = _unitid(school.get("unitid"))
        match = snapshot.loc[snapshot["unitid"] == uid]
        if match.empty or uid is None:
            continue
        row = match.iloc[-1]
        snap_rows.append(row)
        summaries.append((school, row, facts_by_id.get(uid, {"unitid": uid})))
    model_frame = pd.DataFrame(snap_rows)
    contributions, _base = probability_contributions(booster, model_frame, features)
    check_scores = predict_proba(booster, model_frame[features])

    records = []
    artifact_notes = []
    for i, (school, row, facts) in enumerate(summaries):
        published = _num(row.get("risk_score"))
        refit = float(check_scores[i])
        facts["n_missing_features"] = sum(_num(row.get(feature)) is None for feature in features)
        parts = contributions[i]
        order = list(np.argsort(-parts))
        phrases = []
        feature_payloads = []
        for rank, idx in enumerate(order, start=1):
            feature = features[idx]
            value = row.get(feature)
            year = _feature_year(row, feature)
            percentile = _percentile(value, snapshot[feature]) if feature in snapshot.columns else None
            normalized = _zscore(value, snapshot[feature]) if feature in snapshot.columns else None
            phrase = plain_driver(feature, value, year, context=facts)
            if rank <= 3:
                phrases.append(phrase)
            feature_payloads.append(
                {
                    "feature": feature,
                    "contribution": float(parts[idx]),
                    "phrase": phrase,
                    "rank": rank,
                    "value": value,
                    "year": year,
                    "percentile": percentile,
                    "normalized": normalized,
                    "weight": weights.get(feature, 0.0),
                    "fill": fill_method(feature, value, row),
                }
            )
        flags = quality_flags(row, facts)
        artifact, reason = suspected_artifact(flags, [item["feature"] for item in feature_payloads[:3]])
        if artifact:
            artifact_notes.append(
                {
                    "residential_rank": int(school["residential_rank"]),
                    "inst_name": school.get("inst_name"),
                    "unitid": facts.get("unitid"),
                    "reason": reason,
                }
            )
        missing_bits = [
            f"{feature_label(item['feature'])}: {item['fill']}"
            for item in feature_payloads
            if item["value"] is None or (isinstance(item["value"], float) and math.isnan(item["value"])) or item["fill"].startswith("Left missing") or item["fill"].startswith("Carried forward") or item["fill"].startswith("Copied from")
        ]
        # Keep the missing list to features that were actually absent or carried.
        missing_bits = [bit for bit in missing_bits if "Left missing" in bit or "Carried forward" in bit or "Copied from" in bit]
        for item in feature_payloads:
            records.append(
                {
                    "residential_rank": int(school["residential_rank"]),
                    "watchlist_rank": school.get("watchlist_rank"),
                    "unitid": facts.get("unitid"),
                    "inst_name": school.get("inst_name"),
                    "state_abbr": school.get("state_abbr"),
                    "risk_score": published,
                    "refit_risk_score": refit,
                    "composite_score": _num(row.get("composite_score")),
                    "composite_year": _feature_year(row, "composite_score"),
                    "feature": item["feature"],
                    "feature_label": feature_label(item["feature"]),
                    "raw_value": _num(item["value"]),
                    "data_year": item["year"],
                    "percentile": None if item["percentile"] is None else round(item["percentile"], 1),
                    "normalized_value": None if item["normalized"] is None else round(item["normalized"], 3),
                    "weight": round(item["weight"], 6),
                    "contribution": round(item["contribution"], 6),
                    "fill_method": item["fill"],
                    "driver_rank": item["rank"],
                    "plain_driver": item["phrase"] if item["rank"] <= 3 else "",
                    "top_driver_1": phrases[0] if phrases else "",
                    "top_driver_2": phrases[1] if len(phrases) > 1 else "",
                    "top_driver_3": phrases[2] if len(phrases) > 2 else "",
                    "missing_or_imputed": " | ".join(missing_bits),
                    "data_quality_flags": " | ".join(flags),
                    "suspected_artifact": "yes" if artifact else "",
                    "artifact_reason": reason,
                    "endowment_market_value": facts.get("endowment_market_value"),
                    "endowment_year": facts.get("endowment_year"),
                    "endowment_per_fte": facts.get("endowment_per_fte_display"),
                    "endowment_scope": facts.get("endowment_scope"),
                    "endowment_source": facts.get("endowment_source"),
                    "endowment_source_url": facts.get("endowment_source_url", ""),
                    "endowment_note": facts.get("endowment_note", ""),
                    "system_filer_unitid": facts.get("system_filer_unitid", ""),
                    "fall_headcount": facts.get("fall_headcount"),
                    "fall_undergrad": facts.get("fall_undergrad"),
                    "fall_grad": facts.get("fall_grad"),
                    "fall_year": facts.get("fall_year"),
                    "fte_count": facts.get("fte_count"),
                    "fte_year": facts.get("fte_year"),
                    "fall_headcount_earlier": facts.get("fall_headcount_earlier"),
                    "fall_year_earlier": facts.get("fall_year_earlier"),
                    "fall_headcount_pct_change": facts.get("fall_headcount_pct_change"),
                    "enrollment_source": facts.get("enrollment_source"),
                    "finance_from_parent": bool(facts.get("finance_from_parent")),
                    "finance_parent_unitid": facts.get("finance_parent_unitid") or "",
                }
            )
    frame = pd.DataFrame.from_records(records)
    principia_score = None
    principia_rows = snapshot.loc[snapshot["unitid"] == 148016]
    if not principia_rows.empty and "risk_score" in principia_rows.columns:
        principia_score = _num(principia_rows.iloc[0]["risk_score"])
    meta = {
        "booster": booster_name,
        "n_features": len(features),
        "principia_score": principia_score,
        "max_abs_score_gap": float(np.nanmax(np.abs(frame.groupby("unitid")["risk_score"].first() - frame.groupby("unitid")["refit_risk_score"].first()))) if len(frame) else None,
        "artifacts": artifact_notes,
        "model": booster,
        "features": features,
        "snapshot": snapshot,
    }
    return frame, meta


def explanations_markdown(frame: pd.DataFrame, meta: dict) -> str:
    lines = [
        "# Why the residential top 50 ranks where it does",
        "",
        "Score year 2023. The published score is an XGBoost probability on the vintage snapshot. "
        "It is an elevated-risk indicator, not a closure probability to quote. "
        "Each feature row has the raw value on that snapshot, the year the vintage builder used, "
        "the percentile and z-score among the scored vintage universe, the feature's share of global mean |SHAP| (weight), "
        "and its TreeSHAP contribution in probability units. "
        "Contributions are sorted from the one that raises the score most. "
        "Missing values were left missing. The booster follows the missing branch. It does not median-fill. "
        "Ratio features on the snapshot were winsorized to the 1st–99th percentile of the feature panel before scoring.",
        "",
        "## Suspected data artifacts",
        "",
    ]
    artifacts = meta.get("artifacts") or []
    if not artifacts:
        lines.append("None of the top 50 were flagged.")
    for item in artifacts:
        lines.append(
            f"- Rank {item['residential_rank']}. {item['inst_name']} (UNITID {item['unitid']}). {item['reason']}"
        )
    lines.extend(["", "## Principia College", "", _principia_section(frame, meta), ""])
    nobts = meta.get("nobts_counterfactual") or {}
    if nobts:
        lines.extend(
            [
                "New Orleans Baptist Theological Seminary had the same Title IV history gap. "
                f"Scored on its own filings with the same booster, the row is about {nobts.get('risk_score'):.3f}.",
                "",
            ]
        )
    lines.append("## School by school")
    lines.append("")
    order = frame[["unitid", "residential_rank"]].drop_duplicates().sort_values("residential_rank")
    for unitid in order["unitid"]:
        school = frame[frame["unitid"] == unitid]
        first = school.iloc[0]
        lines.append(
            f"### {int(first['residential_rank'])}. {first['inst_name']} ({first['state_abbr']})"
        )
        lines.append("")
        composite = first["composite_score"]
        composite_txt = "missing" if pd.isna(composite) else f"{float(composite):.2f} (year {first['composite_year']})"
        lines.append(
            f"Residential rank {int(first['residential_rank'])}. Watch-list rank {first['watchlist_rank']}. "
            f"Published risk score {float(first['risk_score']):.3f}. Federal composite score {composite_txt}."
        )
        lines.append("")
        lines.append(_markdown_facts(first))
        lines.append("")
        lines.append("Top drivers:")
        lines.append("")
        for key in ("top_driver_1", "top_driver_2", "top_driver_3"):
            if first.get(key):
                lines.append(f"- {first[key]}")
        lines.append("")
        if first.get("missing_or_imputed"):
            lines.append("Missing or imputed:")
            lines.append("")
            lines.append(first["missing_or_imputed"])
            lines.append("")
        lines.append("Data-quality flags:")
        lines.append("")
        lines.append(first.get("data_quality_flags") or "None.")
        lines.append("")
        if first.get("suspected_artifact") == "yes":
            lines.append(f"Suspected data artifact. {first['artifact_reason']}")
            lines.append("")
        lines.append("| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
        ordered = school.sort_values("contribution", ascending=False)
        for _, item in ordered.iterrows():
            raw = "" if pd.isna(item["raw_value"]) else f"{item['raw_value']:.4g}"
            year = "" if pd.isna(item["data_year"]) else str(int(item["data_year"]))
            pct = "" if pd.isna(item["percentile"]) else f"{item['percentile']:.1f}"
            zed = "" if pd.isna(item["normalized_value"]) else f"{item['normalized_value']:.2f}"
            lines.append(
                f"| {item['feature_label']} | {raw} | {year} | {pct} | {zed} | {item['weight']:.4f} | {item['contribution']:+.4f} | {item['fill_method']} |"
            )
        lines.append("")
        _ = unitid
    return "\n".join(lines) + "\n"


def _markdown_facts(row: pd.Series) -> str:
    endow = money(row.get("endowment_market_value")) or "not reported"
    year = row.get("endowment_year")
    year_txt = f" in {int(year)}" if pd.notna(year) else ""
    per = money(row.get("endowment_per_fte"))
    per_txt = f" ({per} per FTE)" if per else ""
    scope = row.get("endowment_scope") or ""
    fall = row.get("fall_headcount")
    fte = row.get("fte_count")
    change = row.get("fall_headcount_pct_change")
    trend = "Five-year fall headcount is not available."
    if pd.notna(change) and pd.notna(row.get("fall_headcount_earlier")):
        trend = (
            f"Fall headcount {float(row['fall_headcount_earlier']):,.0f} in {int(row['fall_year_earlier'])} "
            f"versus {float(fall):,.0f} in {int(row['fall_year'])} ({float(change):+.0%})."
        )
    grad = row.get("fall_grad")
    grad_txt = f"{float(grad):,.0f}" if pd.notna(grad) else "not reported"
    ug = row.get("fall_undergrad")
    ug_txt = f"{float(ug):,.0f}" if pd.notna(ug) else "not reported"
    fall_txt = f"{float(fall):,.0f}" if pd.notna(fall) else "not reported"
    fte_txt = f"{float(fte):,.0f}" if pd.notna(fte) else "not reported"
    note = row.get("endowment_note") or ""
    return (
        f"Endowment {endow}{year_txt}{per_txt}. Scope: {scope}. Source: {row.get('endowment_source')}. "
        f"Fall headcount {fall_txt} in {row.get('fall_year')} (undergraduate {ug_txt}; graduate {grad_txt}). "
        f"FTE {fte_txt} in {row.get('fte_year')}. {trend} Enrollment source: {row.get('enrollment_source')}. {note}"
    ).strip()


def _principia_section(frame: pd.DataFrame, meta: dict) -> str:
    school = frame[frame["unitid"] == 148016]
    filing = (
        "The IPEDS finance extract has a 2023 filing: endowment_end $592,903,744, revenue $97,015,232, "
        "expenses $48,254,224, net tuition $738,933, investment return $77,515,584. "
        "Fall headcount was 407 in 2019 and 339 in 2024. FTE was 390 in 2019 and 335 in 2024. "
        "Net tuition is about 0.8% of revenue. The investment return is most of reported revenue, so the accounting margin is not an operating surplus. "
        "Data USA matches the $593 million IPEDS endowment. "
        "The Principia Corporation 990 (EIN 43-0652667) covers the college and the Principia School; the card keeps the college IPEDS line."
    )
    if school.empty:
        score = meta.get("principia_score")
        score_txt = f" The published score on that filing is {float(score):.3f}." if score is not None else ""
        return (
            "Principia College left the residential top 50 after the extract-year repair. "
            "The scored row uses the college's own finance and enrollment years, including the years when title_iv_indicator was 3. "
            "That score sits below the 50th school that is still operating, has on-campus housing, and has its own campus."
            + score_txt
            + " "
            + filing
        )
    first = school.iloc[0]
    return (
        f"Principia College is residential rank {int(first['residential_rank'])} with published risk score {float(first['risk_score']):.3f}. "
        "The scored row uses the college's own finance and enrollment years, including the years when title_iv_indicator was 3. "
        + filing
        + f" Drivers the published score actually used: {first['top_driver_1']}; {first['top_driver_2']}; {first['top_driver_3']}."
    )


def _series_at(frame: pd.DataFrame, unitid: int, year: int, column: str) -> float | None:
    if frame.empty or column not in frame.columns:
        return None
    hit = frame[(frame["unitid"] == unitid) & (frame["year"] == year)]
    if hit.empty:
        return None
    return _num(hit.iloc[-1][column])


def _pct(current: float | None, previous: float | None) -> float | None:
    if current is None or previous in (None, 0):
        return None
    return current / previous - 1.0


def counterfactual_from_extracts(settings, model, features: list[str], snapshot_row: pd.Series) -> dict:
    """Score one school from the extracts. Does not change the published ranking.

    Finance ratios use 2023. Enrollment and staff use 2024 when that year exists.
    Ratios are clipped to the feature panel's 1st and 99th percentiles, matching
    the published pipeline. The composite stays missing when the extract has none.
    """
    unitid = _unitid(snapshot_row.get("unitid"))
    processed = settings.processed_dir
    finance = _read(
        processed / "finance.parquet",
        ["unitid", "year", "rev_total_current", "rev_tuition_fees_net", "exp_total_current", "endowment_end", "assets_net", "sch_allowances_tuition_fees", "rev_tuition_fees_gross"],
    )
    fte = _read(processed / "enrollment_fte.parquet", ["unitid", "year", "enrollment_fte"])
    staff = _read(processed / "instructional_staff.parquet", ["unitid", "year", "instruc_staff_count"])
    admissions = _read(
        processed / "admissions.parquet",
        ["unitid", "year", "number_applied", "number_admitted", "number_enrolled_total"],
    )
    values = {feature: snapshot_row.get(feature) for feature in features}
    fte_now = _series_at(fte, unitid, 2024, "enrollment_fte") or _series_at(fte, unitid, 2023, "enrollment_fte")
    if fte_now and fte_now > 0:
        values["log_fte"] = math.log(fte_now)
        values["fte_under_1000"] = float(fte_now < 1000)
    fte_1 = _series_at(fte, unitid, 2023, "enrollment_fte")
    fte_5 = _series_at(fte, unitid, 2019, "enrollment_fte")
    fte_10 = _series_at(fte, unitid, 2014, "enrollment_fte")
    values["enr_pct_chg_1y"] = _pct(fte_now, fte_1)
    values["enr_pct_chg_5y"] = _pct(fte_now, fte_5)
    values["enr_pct_chg_10y"] = _pct(fte_now, fte_10)
    values["enr_decline_5y_gt30"] = float(values["enr_pct_chg_5y"] <= -0.30) if values.get("enr_pct_chg_5y") is not None else None
    rev = _series_at(finance, unitid, 2023, "rev_total_current")
    exp = _series_at(finance, unitid, 2023, "exp_total_current")
    tuition = _series_at(finance, unitid, 2023, "rev_tuition_fees_net")
    endow = _series_at(finance, unitid, 2023, "endowment_end")
    net_assets = _series_at(finance, unitid, 2023, "assets_net")
    if rev not in (None, 0):
        values["miss_finance"] = 0.0
        values["finance_from_parent"] = 0.0
        if tuition is not None:
            values["tuition_dependence"] = tuition / rev
            values["high_tuition_dependence"] = float(values["tuition_dependence"] >= 0.70)
        if exp is not None:
            values["operating_margin"] = (rev - exp) / rev
        if endow is not None and fte_now:
            values["endowment_per_fte"] = endow / fte_now
        if net_assets is not None and exp not in (None, 0):
            values["unrestricted_na_to_exp"] = net_assets / exp
        rev_2018 = _series_at(finance, unitid, 2018, "rev_total_current")
        exp_2018 = _series_at(finance, unitid, 2018, "exp_total_current")
        if rev_2018 not in (None, 0) and exp_2018 is not None and values.get("operating_margin") is not None:
            values["operating_margin_chg_5y"] = values["operating_margin"] - ((rev_2018 - exp_2018) / rev_2018)
    staff_now = _series_at(staff, unitid, 2024, "instruc_staff_count")
    staff_1 = _series_at(staff, unitid, 2023, "instruc_staff_count")
    staff_5 = _series_at(staff, unitid, 2019, "instruc_staff_count")
    values["staff_pct_chg_1y"] = _pct(staff_now, staff_1)
    values["staff_pct_chg_5y"] = _pct(staff_now, staff_5)
    if fte_now and staff_now:
        values["student_staff_ratio"] = fte_now / staff_now
        prev_fte = fte_1
        if prev_fte and staff_1:
            values["student_staff_ratio_chg_1y"] = values["student_staff_ratio"] - (prev_fte / staff_1)
    applied = _series_at(admissions, unitid, 2023, "number_applied")
    admitted = _series_at(admissions, unitid, 2023, "number_admitted")
    enrolled = _series_at(admissions, unitid, 2023, "number_enrolled_total")
    if applied:
        values["admit_rate"] = admitted / applied if admitted is not None else None
    if admitted:
        values["yield_rate"] = enrolled / admitted if enrolled is not None else None
    enrolled_prev = _series_at(admissions, unitid, 2022, "number_enrolled_total")
    values["ftft_pct_chg_1y"] = _pct(enrolled, enrolled_prev)
    panel = _read(processed / "features.parquet", [c for c in RATIO_COLS])
    for column in RATIO_COLS:
        if column not in values or values[column] is None or column not in panel.columns:
            continue
        series = pd.to_numeric(panel[column], errors="coerce").dropna()
        if len(series) < 20:
            continue
        lo, hi = float(series.quantile(0.01)), float(series.quantile(0.99))
        values[column] = float(min(max(values[column], lo), hi))
    row = {feature: values.get(feature) for feature in features}
    score = float(predict_proba(model, pd.DataFrame([row])[features])[0])
    return {
        "unitid": unitid,
        "risk_score": score,
        "fte": fte_now,
        "tuition_dependence": values.get("tuition_dependence"),
        "endowment_per_fte": values.get("endowment_per_fte"),
        "operating_margin": values.get("operating_margin"),
        "enr_pct_chg_5y": values.get("enr_pct_chg_5y"),
        "miss_finance": values.get("miss_finance"),
    }


def write_explanation_outputs(frame: pd.DataFrame, meta: dict, outputs_dir: Path) -> None:
    outputs_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(outputs_dir / "score_explanations.csv", index=False)
    (outputs_dir / "score_explanations.md").write_text(explanations_markdown(frame, meta), encoding="utf-8")


def load_controls(processed: Path) -> dict[int, int]:
    directory = _read(processed / "directory.parquet", ["unitid", "year", "inst_control"])
    if directory.empty:
        return {}
    latest = directory.sort_values("year").groupby("unitid", as_index=False).tail(1)
    out = {}
    for _, row in latest.iterrows():
        uid = _unitid(row["unitid"])
        control = _num(row.get("inst_control"))
        if uid is not None and control is not None:
            out[uid] = int(control)
    return out
