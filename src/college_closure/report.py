"""Watchlist, top-50 evidence cards, and model card.

Language is deliberately non-verdict: these are elevated-risk indicators
on a watch list, not predictions that a college will close.
"""

from __future__ import annotations

import html
import json
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd

from college_closure.config import Settings
from college_closure.features import MODEL_FEATURE_COLUMNS
from college_closure.campus import (
    exclusion_reason,
    is_residential,
    is_small_housing,
    partition_acquisition,
)
from college_closure.status import (
    BANNER_SENTENCE,
    STATUS_CSS,
    _source_html,
    load_status_for_report,
    status_badge,
    status_block_html,
)
from college_closure.libraries import (
    LIB_WATCHLIST_COLS,
    distinctive_notes_html,
    enrich_watchlist_libraries,
    library_section_html,
    write_libraries_summary,
)

LOGGER = logging.getLogger(__name__)

WATCHLIST_COLS = [
    "unitid",
    "opeid8",
    "opeid6",
    "inst_name",
    "state_abbr",
    "year",
    "inst_control",
    "sector",
    "fte",
    "risk_score",
    "enr_pct_chg_5y",
    "enr_pct_chg_1y",
    "discount_rate",
    "operating_margin",
    "tuition_dependence",
    "composite_score",
    "composite_zone",
    "composite_fail",
    "miss_finance",
    "finance_from_parent",
    "year_finance",
    "year_enrollment",
    "year_fall_enrollment",
    "year_admissions",
    "year_staff",
    "year_directory",
    "year_composite",
    "hcm1_current",
    "hcm2_current",
    "hcm2_scorecard",
    "scorecard_operating",
    "scorecard_currently_operating",
    "scorecard_ownership",
    "scorecard_under_investigation",
    "accreditor_public_action",
    "warn_layoff_mention",
    "irs990_ein_verified",
    "irs990_revenue",
    "enrichment_notes",
    "label_complete_h3",
    "closed_or_merged_within_3_years",
    *LIB_WATCHLIST_COLS,
]


def _control_label(v) -> str:
    try:
        i = int(float(v))
    except (TypeError, ValueError):
        return "unknown"
    return {1: "public", 2: "private nonprofit", 3: "for-profit"}.get(i, str(i))


def _fmt(v, digits: int = 2, pct: bool = False) -> str:
    if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
        return "—"
    if isinstance(v, str):
        token = v.strip().lower()
        if token in {"", "nan", "none", "<na>"}:
            return "—"
        if token == "true":
            v = 1
        elif token == "false":
            v = 0
    try:
        if pd.isna(v):
            return "—"
    except (TypeError, ValueError):
        pass
    try:
        x = float(v)
    except (TypeError, ValueError):
        return html.escape(str(v))
    if pct:
        return f"{x * 100:.{digits}f}%"
    return f"{x:.{digits}f}"


def _row_shap_fallback(row: pd.Series, shap_global: list[dict], n: int = 6) -> list[dict]:
    out = []
    index = row.index if hasattr(row, "index") else []
    for item in shap_global[:n]:
        feat = item.get("feature")
        if not feat:
            continue
        entry = {"feature": feat, "mean_abs_shap": item.get("mean_abs_shap")}
        if feat in index and _text(row.get(feat)):
            entry["value"] = row.get(feat)
        out.append(entry)
    return out


def _evidence_card(row: pd.Series, shap_items: list[dict], rank: int) -> str:
    name = html.escape(str(row.get("inst_name") or f"UNITID {row.get('unitid')}"))
    state = html.escape(str(row.get("state_abbr") or "—"))
    sector = html.escape(_control_label(row.get("inst_control")))
    try:
        year = str(int(float(row.get("year"))))
    except (TypeError, ValueError):
        year = row.get("year") or "—"
    try:
        original_rank = str(int(float(row.get("watchlist_rank"))))
    except (TypeError, ValueError):
        original_rank = ""
    rank_bit = f" · watch-list rank {original_rank}" if original_rank else ""
    shap_rows = ""
    for s in shap_items:
        feat = html.escape(str(s.get("feature")))
        if _text(s.get("value")):
            shap_rows += f"<li><code>{feat}</code> ({_fmt(s.get('value'), 3)})</li>"
        else:
            shap_rows += f"<li><code>{feat}</code> (mean |SHAP| {_fmt(s.get('mean_abs_shap'), 3)})</li>"
    if not shap_rows:
        shap_rows = "<li>SHAP unavailable for this row</li>"

    def _flag(v) -> bool:
        if isinstance(v, str):
            token = v.strip().lower()
            if token in {"", "false", "no", "nan", "none"}:
                return False
            if token in {"true", "yes"}:
                return True
            try:
                return float(token) != 0
            except ValueError:
                return False
        try:
            if v is None or pd.isna(v):
                return False
            if isinstance(v, (int, float)) and float(v) == 0:
                return False
        except (TypeError, ValueError):
            return False
        return bool(v)

    hcm = []
    if _flag(row.get("hcm2_current")):
        hcm.append("HCM2 (FSA list)")
    if _flag(row.get("hcm1_current")):
        hcm.append("HCM1 (FSA list)")
    if _flag(row.get("hcm2_scorecard")) or _flag(row.get("scorecard_under_investigation")):
        hcm.append("Scorecard under_investigation / HCM2 (current snapshot)")
    hcm_txt = ", ".join(hcm) if hcm else "not on current HCM / Scorecard investigation flags (or lists unavailable)"
    op = row.get("auto_scorecard_operating")
    if op is None or (isinstance(op, str) and not op.strip()) or (isinstance(op, float) and pd.isna(op)):
        op = row.get("scorecard_operating")
    try:
        op_n = int(op) if op is not None and not pd.isna(op) else None
    except (TypeError, ValueError):
        op_n = None
    if op_n == 0:
        op_txt = "not currently operating (Scorecard snapshot — not a closure year)"
    elif op_n == 1:
        op_txt = "currently operating (Scorecard)"
    else:
        op_txt = "Scorecard operating unknown"
    enrich_bits = []
    if row.get("accreditor_public_action"):
        enrich_bits.append(f"accreditor page mention: {row.get('accreditor_public_action')}")
    if _flag(row.get("warn_layoff_mention")):
        enrich_bits.append("WARN layoff file name match")
    if _flag(row.get("irs990_ein_verified")):
        enrich_bits.append(f"990 EIN verified; revenue {_fmt(row.get('irs990_revenue'), 0)}")
    enrich_txt = "; ".join(enrich_bits) if enrich_bits else "no extra accreditor / WARN / 990 hit"

    return f"""
    <article class="card">
      <div class="card-head">
        {_campus_photo_html(row)}
        <div class="card-main">
      <h2>{rank}. {name}</h2>
      <p class="meta">{state} · {sector} · score year {year}{rank_bit} · UNITID {row.get("unitid")}</p>
      {_prior_rank_html(row)}
      <p class="score">Watch-list score: <strong>{_fmt(row.get("risk_score"), 3)}</strong>
      — elevated-risk indicator, not a closure verdict.</p>
      {_feature_years_html(row)}
      {status_block_html(row)}
      <table>
        <tr><th>FTE</th><td>{_fmt(row.get("fte"), 0)}</td>
            <th>FTE 5y %Δ</th><td>{_fmt(row.get("enr_pct_chg_5y"), 1, pct=True)}</td></tr>
        <tr><th>FTE 1y %Δ</th><td>{_fmt(row.get("enr_pct_chg_1y"), 1, pct=True)}</td>
            <th>First-time FY %Δ</th><td>{_fmt(row.get("ftft_pct_chg_1y"), 1, pct=True)}</td></tr>
        <tr><th>Discount rate</th><td>{_fmt(row.get("discount_rate"), 1, pct=True)}</td>
            <th>Tuition dependence</th><td>{_fmt(row.get("tuition_dependence"), 1, pct=True)}</td></tr>
        <tr><th>Operating margin</th><td>{_fmt(row.get("operating_margin"), 1, pct=True)}</td>
            <th>Consec. neg. margins</th><td>{_fmt(row.get("consec_neg_margin_yrs"), 0)}</td></tr>
        <tr><th>Composite score</th><td>{_fmt(row.get("composite_score"), 2)}</td>
            <th>Zone / failing</th><td>{_fmt(row.get("composite_zone"), 0)} / {_fmt(row.get("composite_fail"), 0)}</td></tr>
        <tr><th>Finance missing</th><td>{_fmt(row.get("miss_finance"), 0)}</td>
            <th>HCM / investigation</th><td>{html.escape(hcm_txt)}</td></tr>
        <tr><th>Scorecard operating</th><td>{html.escape(op_txt)}</td>
            <th>Enrichment flags</th><td>{html.escape(enrich_txt)}</td></tr>
      </table>
      <h3>Top drivers (SHAP / global importance)</h3>
      <ul>{shap_rows}</ul>
      {library_section_html(row)}
      <h3>Campus</h3>
      <table>
        <tr><th>Dorm capacity</th><td>{html.escape(_housing_text(row))}</td>
            <th>Acreage</th><td>{html.escape(_acreage_text(row))}</td></tr>
        <tr><th>Own campus</th><td>{html.escape(_own_campus_text(row))}</td>
            <th>Land source</th><td>{_source_html(_text(row.get("campus_source_url"))) or "—"}</td></tr>
        {_satellite_row(row)}
        {_campus_map_row(row)}
      </table>
      <p class="caveat">IPEDS and FSA series lag; missing finance is flagged rather than imputed as health.
      Publics rarely close; this card is in the private nonprofit / for-profit risk universe.
      Library holdings are enrichment context (what cultural/asset value might be at stake),
      not a training feature. Dorm capacity is the latest IPEDS year that reports housing
      as yes or no. Acreage is blank when the land source does not state a number.</p>
        </div>
      </div>
    </article>
    """


def _html_page(
    cards: str,
    n: int,
    score_year: int,
    caveats: str,
    intro: str = "",
    teachout: str = "",
    closed: str = "",
    excluded: str = "",
    depth: int | None = None,
    vintage_note: str = "",
    movement: str = "",
) -> str:
    if depth:
        depth_note = (
            f'<p class="depth">The main list is {n} still-operating '
            f"school{'s' if n != 1 else ''} with on-campus dorms and their own campus, "
            f"reached by walking the ranked watch list through rank {int(depth)}.</p>"
        )
    else:
        depth_note = ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>College closure early-warning watch list (top {n} still operating)</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 980px; margin: 2rem auto; padding: 0 1rem;
           color: #222; line-height: 1.45; }}
    h1 {{ font-size: 1.6rem; }}
    .cover-banner {{ margin: 0 0 1.2rem; }}
    .cover-banner img {{ width: 100%; height: auto; display: block; }}
    .banner {{ background: #fff6e5; border: 1px solid #e0c48a; padding: 0.8rem 1rem; }}
    .card {{ border: 1px solid #ddd; padding: 1rem 1.2rem; margin: 1.2rem 0; }}
    .card-head {{ display: flex; gap: 1rem; align-items: flex-start; flex-wrap: wrap; }}
    .card-main {{ flex: 1; min-width: 0; }}
    .campus-photo {{ margin: 0; flex: 0 0 220px; max-width: 400px; }}
    .campus-photo img {{ width: 100%; height: auto; display: block; }}
    .photo-credit {{ color: #555; font-size: 0.8rem; margin-top: 0.35rem; }}
    .placeholder {{ border: 1px dashed #bbb; min-height: 8rem; display: flex;
                   align-items: center; justify-content: center; color: #666; background: #fafafa; }}
    .placeholder p {{ margin: 0.6rem; text-align: center; }}
    .card h2 {{ margin-top: 0; font-size: 1.2rem; }}
    .meta, .caveat, .lib-context, .lib-note {{ color: #555; font-size: 0.95rem; }}
    .lib-note {{ margin-top: 0.4rem; }}
    table {{ border-collapse: collapse; width: 100%; margin: 0.6rem 0; }}
    th {{ text-align: left; width: 28%; color: #444; font-weight: 600; padding: 0.2rem 0.4rem; }}
    td {{ padding: 0.2rem 0.4rem; }}
    table.roster th {{ width: auto; vertical-align: top; }}
    table.roster td {{ vertical-align: top; }}
    code {{ font-size: 0.9rem; }}
    {STATUS_CSS}
  </style>
</head>
<body>
  <p class="cover-banner" align="center"><img src="../docs/cover.png" alt="College Closure Early Warning System" width="100%"></p>
  <h1>Watch list — top {n} residential campuses (score year {score_year})</h1>
  <div class="banner">
    <strong>Not a verdict.</strong> Ranked elevated-risk indicators from a statistical model
    trained on historical institution-year features. A high score means the school resembles
    past closures/mergers on trailing observables — not that it will close. Scores come from
    {score_year} federal financial data. The list is elevated-risk indicators, not closure
    predictions. The main list is the highest-ranked schools that are still operating,
    have on-campus dorms, and have their own campus grounds. Online-only schools,
    single-building branches, and hospital programs without a residential campus
    are listed at the bottom instead.
    The score year is the latest <em>right-censored</em> year with published IPEDS finance
    (later directory years are omitted because unpublished finance looks like pre-closure
    missingness). Composite scores lag; HCM is a current snapshot and was not used as a
    training feature. Library holdings and special-collection notes are
    <em>enrichment context</em> (IPEDS Academic Libraries + public library pages), not a
    model input.{BANNER_SENTENCE}
  </div>
  {depth_note}
  {vintage_note}
  {movement}
  {intro}
  {cards}
  {teachout}
  {closed}
  {excluded}
  <h2>Limitations</h2>
  <p>{html.escape(caveats)}</p>
</body>
</html>
"""


def _year_bit(value) -> str:
    try:
        if value is None or pd.isna(value):
            return ""
    except (TypeError, ValueError):
        return ""
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "<na>"}:
        return ""
    try:
        return str(int(float(text)))
    except (TypeError, ValueError):
        return ""


def _feature_years_html(row: pd.Series) -> str:
    bits = []
    for label, col in (
        ("finance", "year_finance"),
        ("enrollment", "year_enrollment"),
        ("fall enrollment", "year_fall_enrollment"),
        ("admissions", "year_admissions"),
        ("staff", "year_staff"),
        ("directory", "year_directory"),
    ):
        year = _year_bit(row.get(col))
        if year:
            bits.append(f"{label} {year}")
    if not bits:
        return ""
    return (
        '<p class="meta">Feature years: '
        + html.escape(", ".join(bits))
        + ". A blank source means that school had no reported value. "
        "Other features from the same source can use an earlier year when the complete year is missing.</p>"
    )


def _prior_rank_html(row: pd.Series) -> str:
    if "prior_residential_rank" not in row.index and "prior_residential_rank" not in getattr(row, "index", []):
        return ""
    year = _year_bit(row.get("prior_residential_rank"))
    if year:
        return f'<p class="meta">2022 residential rank {html.escape(year)}</p>'
    if "prior_residential_rank" in row.index:
        return '<p class="meta">New to the residential top 50 versus the 2022 list</p>'
    return ""


def movement_section_html(open_df: pd.DataFrame, baseline: pd.DataFrame) -> str:
    """Entered and left schools versus the frozen 2022 residential top 50."""
    if open_df is None or open_df.empty or baseline is None or baseline.empty:
        return ""
    if "unitid" not in open_df.columns or "unitid" not in baseline.columns:
        return ""
    old_rank: dict[int, int] = {}
    old_name: dict[int, tuple[str, str]] = {}
    for _, row in baseline.iterrows():
        try:
            uid = int(float(row.get("unitid")))
            rank = int(float(row.get("old_rank")))
        except (TypeError, ValueError):
            continue
        old_rank[uid] = rank
        old_name[uid] = (
            _text(row.get("inst_name")) or "—",
            _text(row.get("state_abbr")) or "—",
        )
    if not old_rank:
        return ""
    current: list[tuple[int, int, str, str]] = []
    for rank, (_, row) in enumerate(open_df.iterrows(), start=1):
        try:
            uid = int(float(row.get("unitid")))
        except (TypeError, ValueError):
            continue
        current.append(
            (
                rank,
                uid,
                _text(row.get("inst_name")) or old_name.get(uid, ("—", ""))[0],
                _text(row.get("state_abbr")) or "—",
            )
        )
    new_ids = {uid for _, uid, _, _ in current}
    entered = [item for item in current if item[1] not in old_rank]
    left = []
    for uid, rank in sorted(old_rank.items(), key=lambda pair: pair[1]):
        if uid not in new_ids:
            name, state = old_name.get(uid, ("—", "—"))
            left.append((rank, uid, name, state))

    def _rows(items: list[tuple], *, entered_side: bool) -> str:
        if not items:
            return "<p>None.</p>"
        body = []
        for rank, uid, name, state in items:
            if entered_side:
                cells = (
                    f"<td>{rank}</td><td>—</td>"
                )
            else:
                cells = f"<td>—</td><td>{rank}</td>"
            body.append(
                "<tr>"
                f"{cells}"
                f"<td>{html.escape(name)}</td>"
                f"<td>{html.escape(state)}</td>"
                f"<td>{uid}</td>"
                "</tr>"
            )
        return (
            '<table class="roster"><tr><th>New rank</th><th>2022 rank</th>'
            "<th>School</th><th>State</th><th>UNITID</th></tr>"
            + "".join(body)
            + "</table>"
        )

    return (
        "<h2>Compared with the 2022 residential top 50</h2>"
        f"<p>{len(entered)} entered and {len(left)} left the residential top 50 "
        "versus the list scored on 2022 federal data.</p>"
        "<h3>Entered</h3>"
        + _rows(entered, entered_side=True)
        + "<h3>Left</h3>"
        + _rows(left, entered_side=False)
    )


def vintage_note_html(meta: dict | None) -> str:
    """One paragraph naming the complete year used for each federal source."""
    if not meta:
        return ""
    sources = meta.get("sources") or {}
    bits = []
    for key, label in (
        ("finance", "finance"),
        ("fall_enrollment", "fall enrollment"),
        ("enrollment_fte", "enrollment FTE"),
        ("admissions", "admissions"),
        ("staff", "instructional staff"),
        ("directory", "directory"),
        ("academic_libraries", "academic libraries"),
    ):
        block = sources.get(key) or {}
        year = block.get("complete_year")
        if year:
            bits.append(f"{label} {int(year)}")
    scorecard = sources.get("scorecard") or {}
    file_name = str(scorecard.get("file") or "").strip()
    file_date = str(scorecard.get("file_date") or "").strip()
    if file_name or file_date:
        bits.append(f"College Scorecard {file_name} {file_date}".strip())
    if not bits and not meta.get("score_year"):
        return ""
    score_year = meta.get("score_year")
    lead = "Score year"
    if score_year:
        lead += f" {int(score_year)} is IPEDS {int(score_year)}-{int(score_year) + 1} finance"
    lead += "."
    detail = "; ".join(bits)
    return (
        f'<p class="meta">{html.escape(lead)} Complete years by source: {html.escape(detail)}. '
        "Each feature uses that source's complete year when the school reported it, "
        "and otherwise the latest earlier year with a value. The year used is stored "
        "with the score.</p>"
    )


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _baseline_frame(report_path) -> pd.DataFrame:
    path = Path(report_path).resolve().parent.parent / "data" / "campus" / "top50_2022_baseline.csv"
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path)
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    return frame


def _attach_prior_rank(frame: pd.DataFrame, baseline: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if baseline is None or baseline.empty or "unitid" not in out.columns:
        return out
    mapping = {}
    for _, row in baseline.iterrows():
        try:
            mapping[int(float(row.get("unitid")))] = int(float(row.get("old_rank")))
        except (TypeError, ValueError):
            continue
    out["prior_residential_rank"] = pd.to_numeric(out["unitid"], errors="coerce").map(
        lambda uid: mapping.get(int(uid)) if pd.notna(uid) and int(uid) in mapping else pd.NA
    )
    return out


def _satellite_anchor(row: pd.Series) -> str:
    from college_closure.campus import satellite_maps_url

    url = satellite_maps_url(row.get("lat"), row.get("lon"))
    if not url:
        return ""
    return f'<a href="{html.escape(url, quote=True)}">Satellite view</a>'


def _satellite_row(row: pd.Series) -> str:
    link = _satellite_anchor(row)
    if not link:
        return ""
    return f"<tr><th>Satellite view</th><td colspan=\"3\">{link}</td></tr>"


def _campus_map_anchor(row: pd.Series) -> str:
    url = _text(row.get("campus_map_url"))
    if not url:
        return ""
    return f'<a href="{html.escape(url, quote=True)}">Campus map</a>'


def _campus_map_row(row: pd.Series) -> str:
    link = _campus_map_anchor(row)
    if not link:
        return ""
    return f"<tr><th>Campus map</th><td colspan=\"3\">{link}</td></tr>"


def _campus_photo_html(row: pd.Series) -> str:
    name = html.escape(str(row.get("inst_name") or "this school"))
    url = _text(row.get("image_url"))
    if not url:
        return '<figure class="campus-photo placeholder"><p>No photo found</p></figure>'
    credit = _text(row.get("image_credit_url"))
    license_name = _text(row.get("image_license"))
    author = _text(row.get("image_author"))
    bits: list[str] = []
    if author:
        bits.append(html.escape(author))
    if credit:
        bits.append(f'<a href="{html.escape(credit, quote=True)}">Photo source</a>')
    if license_name:
        bits.append(html.escape(license_name))
    caption = ". ".join(bits) if bits else "Photo credit unavailable"
    return (
        '<figure class="campus-photo">'
        f'<img src="{html.escape(url, quote=True)}" alt="Campus of {name}" width="400" loading="lazy">'
        f'<figcaption class="photo-credit">{caption}</figcaption>'
        "</figure>"
    )


def _housing_text(row: pd.Series) -> str:
    from college_closure.campus import _num

    capacity = _num(row.get("dormitory_capacity"))
    year = _text(row.get("housing_year"))
    if not is_residential(row):
        if capacity is None:
            return "no on-campus dorms reported"
        return "no on-campus dorms reported"
    cap_txt = str(int(capacity)) if capacity == int(capacity) else str(capacity)
    small = " (small housing)" if is_small_housing(row) else ""
    year_bit = f", IPEDS IC {year}" if year else ""
    return f"{cap_txt}{small}{year_bit}"


def _acreage_text(row: pd.Series) -> str:
    raw = _text(row.get("acreage"))
    if not raw:
        return "not stated"
    return f"{raw} acres"


def _own_campus_text(row: pd.Series) -> str:
    own = _text(row.get("own_campus")).lower()
    if own == "yes":
        return "yes"
    if own == "no":
        return "no"
    if own == "unknown":
        return "unknown"
    return "not confirmed"


def _text(value) -> str:
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


def _sale_summary(row: pd.Series) -> str:
    parts: list[str] = []
    for key in ("status_detail", "sold_listed_details"):
        text = _text(row.get(key))
        if text and text not in parts:
            parts.append(text)
    buyer = _text(row.get("buyer_or_broker"))
    if buyer:
        parts.append(f"Buyer or broker: {buyer}")
    when = _text(row.get("event_date"))
    if when:
        parts.append(f"Date: {when}")
    price = _text(row.get("sale_price_published"))
    if price:
        parts.append(f"Published price: {price}")
    return " ".join(parts)


def _roster_status(row: pd.Series) -> str:
    from college_closure.status import CLOSED_BUCKET, operating_bucket

    badge = re.sub(r"<[^>]+>", "", status_badge(row)).strip() or _text(row.get("status")) or "—"
    if operating_bucket(row) != CLOSED_BUCKET:
        return badge
    lowered = badge.lower()
    if any(word in lowered for word in ("closed", "sold", "merged")):
        return badge
    bits: list[str] = []
    if _text(row.get("auto_scorecard_operating")) == "0":
        bits.append("College Scorecard school.operating is 0")
    closed_date = _text(row.get("auto_ipeds_date_closed"))
    ipeds = _text(row.get("auto_ipeds_status"))
    if closed_date:
        bits.append(f"IPEDS close date {closed_date}")
    elif ipeds:
        try:
            code = int(float(ipeds))
        except (TypeError, ValueError):
            code = None
        if code in {3, 4, 7}:
            bits.append(f"IPEDS inst_status {code}")
    if bits:
        return f"{badge}; excluded from the open list ({'; '.join(bits)})"
    return badge


def _roster_table(frame: pd.DataFrame, *, score_year: int) -> str:
    if frame is None or frame.empty:
        return "<p>None in the rows walked for this list.</p>"
    body = []
    for _, row in frame.iterrows():
        try:
            rank = str(int(float(row.get("watchlist_rank"))))
        except (TypeError, ValueError):
            rank = "—"
        badge = _roster_status(row)
        sources = _source_html(_text(row.get("source_url"))) or "—"
        satellite = _satellite_anchor(row) or "—"
        body.append(
            "<tr>"
            f"<td>{html.escape(rank)}</td>"
            f"<td>{html.escape(_text(row.get('inst_name')) or '—')}</td>"
            f"<td>{html.escape(_text(row.get('state_abbr')) or '—')}</td>"
            f"<td>{_fmt(row.get('risk_score'), 3)}</td>"
            f"<td>{html.escape(badge)}</td>"
            f"<td>{html.escape(_sale_summary(row) or '—')}</td>"
            f"<td>{sources}</td>"
            f"<td>{satellite}</td>"
            "</tr>"
        )
    return (
        "<table class=\"roster\">"
        "<tr><th>Original rank</th><th>School</th><th>State</th>"
        f"<th>{score_year} score</th><th>Status</th><th>Status / sale</th><th>Sources</th>"
        "<th>Satellite view</th></tr>"
        + "".join(body)
        + "</table>"
    )


def teachout_section_html(frame: pd.DataFrame, *, score_year: int) -> str:
    return (
        "<h2>Teach-out / not enrolling</h2>"
        "<p>These schools are not enrolling new students. They are not part of the "
        "still-operating top 50. A teach-out note is a sourced description of current "
        f"enrollment, not a prediction. The score is the {score_year} watch-list score.</p>"
        + _roster_table(frame, score_year=score_year)
    )


def excluded_section_html(frame: pd.DataFrame, *, score_year: int) -> str:
    """Schools walked for this list that are still operating but not a residential campus."""
    if frame is None or frame.empty:
        body = "<p>None in the rows walked for this list.</p>"
    else:
        rows = []
        for _, row in frame.iterrows():
            try:
                rank = str(int(float(row.get("watchlist_rank"))))
            except (TypeError, ValueError):
                rank = "—"
            reason = exclusion_reason(row) or "—"
            note = _text(row.get("campus_notes"))
            if note:
                reason = f"{reason}. {note}"
            rows.append(
                "<tr>"
                f"<td>{html.escape(rank)}</td>"
                f"<td>{html.escape(_text(row.get('inst_name')) or '—')}</td>"
                f"<td>{html.escape(_text(row.get('state_abbr')) or '—')}</td>"
                f"<td>{_fmt(row.get('risk_score'), 3)}</td>"
                f"<td>{html.escape(_housing_text(row))}</td>"
                f"<td>{html.escape(_acreage_text(row))}</td>"
                f"<td>{html.escape(reason)}</td>"
                f"<td>{_satellite_anchor(row) or '—'}</td>"
                "</tr>"
            )
        body = (
            "<table class=\"roster\">"
            "<tr><th>Original rank</th><th>School</th><th>State</th>"
            f"<th>{score_year} score</th><th>Dorm capacity</th><th>Acreage</th>"
            "<th>Why excluded</th><th>Satellite view</th></tr>"
            + "".join(rows)
            + "</table>"
        )
    return (
        "<h2>Excluded: no on-campus dorms or no standalone campus</h2>"
        "<p>These schools were still operating in the rows walked to fill the main list, "
        "but they are not a residential campus with its own grounds. A missing land row "
        "means the campus was not confirmed. Dorm capacity comes from the latest IPEDS "
        f"year that reports housing. The score is the {score_year} watch-list score.</p>"
        + body
    )


def closed_section_html(frame: pd.DataFrame, *, score_year: int) -> str:
    heading = (
        f"Closed or defunct since the {score_year} data"
        if score_year
        else "Closed or defunct since the 2022 data"
    )
    return (
        f"<h2>{heading}</h2>"
        "<p>These schools were ranked above the last still-operating school in the main list. "
        f"The score is the {score_year} watch-list score from federal financial data, not a "
        "prediction that the school would close. A campus or location that has closed "
        "(including a local campus of a multi-campus system such as DeVry or Strayer) is "
        "listed here even when a parent campus is still in the directory. Sale and listing "
        "details come from the curated file when a source recorded them.</p>"
        + _roster_table(frame, score_year=score_year)
    )


_REPORT_STATUS_COLS = (
    "unitid",
    "status",
    "status_badge",
    "status_detail",
    "property_disposition",
    "buyer_or_broker",
    "event_date",
    "sale_price_published",
    "sold_listed_details",
    "source_url",
    "checked_at",
    "disagreement",
    "auto_scorecard_operating",
    "auto_fsa_match",
    "auto_ipeds_year",
    "auto_ipeds_status",
    "auto_ipeds_date_closed",
    "auto_checked_at",
    "list_bucket",
    "housing_year",
    "oncampus_housing",
    "dormitory_capacity",
    "acreage",
    "own_campus",
    "campus_source_url",
    "campus_checked_at",
    "campus_notes",
    "image_url",
    "image_credit_url",
    "image_license",
    "image_author",
    "lat",
    "lon",
    "coord_source",
    "campus_map_url",
    "exclusion_reason",
)


def _with_status(ranked: pd.DataFrame, status: pd.DataFrame) -> pd.DataFrame:
    frame = ranked.copy()
    if "watchlist_rank" not in frame.columns:
        frame["watchlist_rank"] = range(1, len(frame) + 1)
    if status is None or status.empty or "unitid" not in status.columns:
        return frame
    cols = [c for c in _REPORT_STATUS_COLS if c in status.columns]
    if "unitid" not in cols:
        return frame
    extra = status[cols].copy()
    extra["unitid"] = pd.to_numeric(extra["unitid"], errors="coerce")
    frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    frame = frame.drop(columns=[c for c in cols if c != "unitid" and c in frame.columns])
    return frame.merge(extra.drop_duplicates("unitid"), on="unitid", how="left")


def write_operating_report(
    path,
    ranked: pd.DataFrame,
    status: pd.DataFrame,
    *,
    open_n: int = 50,
    score_year: int = 2022,
    caveats: str | None = None,
    intro: str = "",
    shap_global: list | None = None,
) -> dict[str, int]:
    """Write the residential-campus list plus teach-out, closed, and excluded sections."""
    merged = _with_status(ranked, status)
    baseline = _baseline_frame(path)
    merged = _attach_prior_rank(merged, baseline)
    open_df, excluded_df, teach_df, closed_df, depth = partition_acquisition(merged, open_n)
    if shap_global is None:
        metrics_path = path.parent / "model_metrics.json"
        shap_global = []
        if metrics_path.exists():
            try:
                shap_global = json.loads(metrics_path.read_text(encoding="utf-8")).get("shap_global") or []
            except (OSError, json.JSONDecodeError):
                shap_global = []
    cards = []
    for i, (_, row) in enumerate(open_df.iterrows(), start=1):
        cards.append(_evidence_card(row, _row_shap_fallback(row, shap_global), i))
    if caveats is None:
        caveats = (
            "Watch list only. Scores come from the score-year federal snapshot and are "
            "elevated-risk indicators, not closure predictions. IPEDS lag; official FSA "
            "composites currently end FY 2018; HCM / Scorecard HCM2 are current-list "
            "evidence and were not training features. The main list keeps schools that "
            "are still operating, report on-campus housing with a real dorm capacity, "
            "and have their own campus in the curated land file. Teach-out schools and "
            "closed, merged, or campus-sold schools are listed below the main list. "
            "Schools without dorms or without a confirmed standalone campus are listed "
            "after those. Library holdings are enrichment context, not a training feature. "
            "Missing library data is not evidence of no library. Unknown acreage is left "
            "blank rather than estimated."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        _html_page(
            "\n".join(cards),
            n=len(open_df),
            score_year=score_year,
            caveats=caveats,
            intro=intro,
            teachout=teachout_section_html(teach_df, score_year=score_year),
            closed=closed_section_html(closed_df, score_year=score_year),
            excluded=excluded_section_html(excluded_df, score_year=score_year),
            depth=depth,
            vintage_note=vintage_note_html(_load_json(Path(path).resolve().parent / "vintage_years.json")),
            movement=movement_section_html(open_df, baseline),
        ),
        encoding="utf-8",
    )
    return {
        "n_open": int(len(open_df)),
        "n_excluded": int(len(excluded_df)),
        "n_teachout": int(len(teach_df)),
        "n_closed": int(len(closed_df)),
        "depth": int(depth),
    }


def _vintage_md(metrics: dict) -> str:
    vintage = metrics.get("vintage") or {}
    sources = vintage.get("sources") or {}
    if not sources and not vintage.get("score_year"):
        return ""
    lines = [
        "",
        "## Current federal vintages",
        "",
        "The published score is one current row per school. Training rows stay contemporaneous "
        "(no future years mixed into the fit). Each feature uses the newest complete year of its "
        "source when that school reported it, and otherwise that school's latest earlier value. "
        "Per-feature years are in `outputs/feature_years.csv`.",
        "",
    ]
    for key, label in (
        ("finance", "IPEDS finance"),
        ("fall_enrollment", "IPEDS fall enrollment"),
        ("enrollment_fte", "IPEDS enrollment FTE"),
        ("admissions", "IPEDS admissions"),
        ("staff", "IPEDS instructional staff"),
        ("directory", "IPEDS directory"),
        ("academic_libraries", "IPEDS academic libraries"),
    ):
        year = (sources.get(key) or {}).get("complete_year")
        if year:
            lines.append(f"- {label}: **{int(year)}**")
    finance = sources.get("finance") or {}
    if finance.get("nces_zip_years"):
        lines.append(f"- NCES finance complete-data zips: {finance['nces_zip_years']}")
    scorecard = sources.get("scorecard") or {}
    if scorecard.get("file") or scorecard.get("file_date"):
        lines.append(
            f"- College Scorecard: `{scorecard.get('file') or 'bulk ZIP'}` "
            f"({scorecard.get('file_date') or 'most recent file'})"
        )
    return "\n".join(lines) + "\n"


def _model_card_md(metrics: dict, score_year: int, n_watch: int, beats_note: str) -> str:
    splits = metrics.get("splits", {})
    test = metrics.get("test", {})
    booster = metrics.get("booster", "model")
    boost = test.get(booster, {})
    logit = test.get("logit", {})
    shap = metrics.get("shap_global", [])
    shap_lines = "\n".join(
        f"- `{s.get('feature')}` (mean |SHAP| {s.get('mean_abs_shap'):.4f})"
        if isinstance(s.get("mean_abs_shap"), (int, float))
        else f"- `{s.get('feature')}`"
        for s in shap[:12]
    )
    naive_comp = test.get("naive_composite_lt_1", {})
    naive_enr = test.get("naive_enr_decline_5y_gt30", {})

    def _m(block: dict, key: str) -> str:
        v = block.get(key)
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return "n/a"
        return f"{v:.3f}" if isinstance(v, float) else str(v)

    unused = [c for c in MODEL_FEATURE_COLUMNS if c not in (metrics.get("features") or [])]
    unused_txt = ", ".join(f"`{c}`" for c in unused) if unused else "none"

    return f"""# Model card — college closure early-warning watch list

**This is a watch list of elevated-risk indicators, not a prediction that any
college will fail or close.** Rankings are statistical resemblance to historical
closures and mergers on trailing (no-leakage) features.

## Task

- Unit of analysis: institution-year (`unitid` × `year`)
- Outcome: `closed_or_merged_within_h_years` with h=3 (also constructed for h=2)
- Risk universe: private nonprofit and for-profit Title IV / degree-granting schools
- Publics remain in the panel for context but are not the primary scored universe
  (public closures are rare; a high public score should be read even more cautiously)

## Data

- Urban Institute Education Data Portal IPEDS extracts (directory, fall enrollment,
  enrollment FTE, admissions, staffing, and finance through the newest complete year)
- NCES IPEDS complete finance files (F1A / F2 / F3) for 2018–2022 backfill. Later
  standalone finance zips are not invented when they 404.
- Official FSA composite year workbooks from data.ed.gov (FY 2007–2018) plus
  Urban Institute FSA CSV (2006–2016). Official scores win on overlap.
- HCM and Closed School lists: ingested when a current Data Center file downloads;
  HCM is **current-only evidence** and is **not** a training feature
- College Scorecard: `DATA_GOV_API_KEY` / `SCORECARD_API_KEY` **or** the official
  no-key most-recent institution ZIP. API field `school.under_investigation` and
  ZIP column `HCM2` map to the same evidence flag; `CURROPER` is operating status.
- WICHE Knocking at the College Door 11th edition (state HS-graduate totals) when the workbook downloads
- Top-50 enrichment (flags only): accreditor public-action pages, WARN files, ProPublica 990 by EIN
- IPEDS Academic Libraries (Urban portal, 2013–2023): **watch-list enrichment only**
  (`lib_*` columns / evidence-card section). Not used as a training feature.

## Temporal split (no shuffle)

- Train: years ≤ {splits.get("train_end")}
- Validation: {splits.get("val_years")}
- Test: {splits.get("test_years")}
- Right-censored years (incomplete h-year window) are scored for the watch list
  and excluded from training metrics

Sizes: train n={splits.get("train_n")} (positives {splits.get("train_pos")});
val n={splits.get("val_n")}; test n={splits.get("test_n")}.

## Metrics (held-out test)

| Model | PR-AUC | ROC-AUC | Recall@25 | Recall@50 | Recall@100 | n | positives |
|-------|--------|---------|-----------|-----------|------------|---|-----------|
| {booster} | {_m(boost, "pr_auc")} | {_m(boost, "roc_auc")} | {_m(boost, "recall_at_25")} | {_m(boost, "recall_at_50")} | {_m(boost, "recall_at_100")} | {_m(boost, "n")} | {_m(boost, "positives")} |
| logistic | {_m(logit, "pr_auc")} | {_m(logit, "roc_auc")} | {_m(logit, "recall_at_25")} | {_m(logit, "recall_at_50")} | {_m(logit, "recall_at_100")} | {_m(logit, "n")} | {_m(logit, "positives")} |
| naive: composite < 1.0 | {_m(naive_comp, "pr_auc")} | {_m(naive_comp, "roc_auc")} | {_m(naive_comp, "recall_at_25")} | {_m(naive_comp, "recall_at_50")} | {_m(naive_comp, "recall_at_100")} | {_m(naive_comp, "n")} | {_m(naive_comp, "positives")} |
| naive: 5y enrollment decline > 30% | {_m(naive_enr, "pr_auc")} | {_m(naive_enr, "roc_auc")} | {_m(naive_enr, "recall_at_25")} | {_m(naive_enr, "recall_at_50")} | {_m(naive_enr, "recall_at_100")} | {_m(naive_enr, "n")} | {_m(naive_enr, "positives")} |

{beats_note}

Configured feature columns not present in this run: {unused_txt}.

## Top global drivers

{shap_lines or "_SHAP / importances unavailable_"}

## Watch list

- Score year: **{score_year}**
- Rows written: **{n_watch}**
- Files: `outputs/watchlist.csv`, `outputs/top50_report.html`, `outputs/libraries_top50.md`
{_vintage_md(metrics)}

## Caveats

- IPEDS publications lag; recent finance and composite scores may be missing
  (`miss_finance` is an explicit feature, not silently filled with zeros that
  look like health).
- Official FSA composites via data.ed.gov currently end in FY 2018; later years
  use the last observed score (lagged) plus `composite_is_lagged`.
- Parent/child finance: child campuses with $0/missing revenue inherit parent
  totals for ratio features and are flagged `finance_from_parent` so they are
  not scored as empty shells.
- OPEID: FSA files often use a 6-digit root; joins use OPEID6 and prefer the
  main `…00` branch when disambiguating. Six-digit values are *not* left-padded
  to 8 (that would shift the root).
- Mergers are treated as positive labels by default (config toggle).
- HCM1/HCM2 on the HTML cards are a **current snapshot** (if the list downloaded)
  and were excluded from model training to avoid temporal leakage.
- Accreditor / WARN / 990 flags on the top 50 are best-effort name or EIN matches
  and are **not** inputs to the model score.
- Library holdings (`lib_*`) and scraped special-collection notes are
  **enrichment context** on the evidence cards. They are not lagged training
  features and were not used to fit the model.
- Do not publish these ranks as “predicted closures.”
"""


def run_report(
    settings: Settings,
    *,
    skip_scrape: bool = False,
    skip_libraries: bool = False,
    cache_only: bool = False,
) -> dict:
    processed = settings.processed_dir
    out_dir = settings.outputs_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    scored_path = processed / "scored.parquet"
    watch_fallback = out_dir / "watchlist.csv"
    from_watchlist_only = False
    if scored_path.exists():
        scored = pd.read_parquet(scored_path)
    elif watch_fallback.exists():
        LOGGER.warning("scored.parquet missing; enriching committed watchlist.csv (ranks unchanged)")
        scored = pd.read_csv(watch_fallback)
        from_watchlist_only = True
    else:
        raise FileNotFoundError("scored.parquet missing — run scripts/06_model.py")
    metrics_path = processed / "model_metrics.json"
    if not metrics_path.exists():
        metrics_path = out_dir / "model_metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {}

    if from_watchlist_only:
        current = scored.copy()
        score_year = int(current["year"].max()) if "year" in current.columns else 2022
    else:
        if "label_complete_h3" in scored.columns:
            current = scored.loc[scored["label_complete_h3"] != True].copy()  # noqa: E712
        else:
            current = scored.iloc[0:0].copy()
        if current.empty:
            ymax = int(scored["year"].max())
            current = scored.loc[scored["year"] == ymax].copy()
            LOGGER.warning("No right-censored rows; scoring latest year %s", ymax)
        # Do not rank a year where finance is still unpublished for everyone —
        # miss_finance / NA ratios then look like pre-closure missingness.
        score_year = int(current["year"].max())
        if "miss_finance" in current.columns:
            rates = current.groupby("year")["miss_finance"].mean()
            usable = rates[rates < 0.50]
            if len(usable):
                score_year = int(usable.index.max())
                LOGGER.info(
                    "Primary watch-list year %s (latest right-censored year with finance; miss_finance=%.1f%%)",
                    score_year,
                    100 * float(usable.loc[score_year]),
                )
        current = current.loc[current["year"] == score_year].copy()
    current = current.sort_values("risk_score", ascending=False)

    hcm_path = processed / "fsa_hcm_current.parquet"
    if hcm_path.exists() and "opeid6" in current.columns:
        hcm = pd.read_parquet(hcm_path)
        if "opeid6" in hcm.columns:
            keep = [c for c in ("opeid6", "hcm1_current", "hcm2_current") if c in hcm.columns]
            current = current.merge(hcm[keep].drop_duplicates("opeid6"), on="opeid6", how="left")
    for c in ("hcm1_current", "hcm2_current"):
        if c not in current.columns:
            current[c] = pd.NA

    sc_path = processed / "scorecard_operating.parquet"
    if sc_path.exists():
        sc = pd.read_parquet(sc_path)
        if "unitid" in sc.columns and "unitid" in current.columns:
            keep_sc = [c for c in ("unitid", "scorecard_operating", "scorecard_currently_operating", "scorecard_ownership", "scorecard_under_investigation", "hcm2_scorecard") if c in sc.columns]
            current = current.merge(sc[keep_sc].drop_duplicates("unitid"), on="unitid", how="left")
        elif "opeid6" in sc.columns and "opeid6" in current.columns:
            keep_sc = [c for c in ("opeid6", "scorecard_operating", "scorecard_currently_operating", "scorecard_ownership", "scorecard_under_investigation", "hcm2_scorecard") if c in sc.columns]
            current = current.merge(sc[keep_sc].drop_duplicates("opeid6"), on="opeid6", how="left")
    if "hcm2_scorecard" in current.columns:
        current["hcm2_current"] = current["hcm2_current"].fillna(False) | current["hcm2_scorecard"].fillna(False)

    from college_closure.enrichment import enrich_shortlist

    cfg = (getattr(settings, "raw", None) or {}).get("libraries") or {}
    top_n = int(cfg.get("scrape_top_n", 50))
    nonprofit_n = int(cfg.get("scrape_nonprofit_n", 25))
    np_mask = pd.to_numeric(current.get("inst_control"), errors="coerce") == 2
    short = pd.concat([current.head(50), current.loc[np_mask].head(50)]).drop_duplicates("unitid")
    enriched = enrich_shortlist(settings, short)
    extra_cols = [
        c
        for c in (
            "accreditor_public_action",
            "warn_layoff_mention",
            "irs990_ein_verified",
            "irs990_revenue",
            "irs990_assets",
            "enrichment_notes",
        )
        if c in enriched.columns
    ]
    if extra_cols and "unitid" in enriched.columns:
        current = current.merge(enriched[["unitid", *extra_cols]].drop_duplicates("unitid"), on="unitid", how="left")

    current = current.sort_values("risk_score", ascending=False).reset_index(drop=True)
    nonprofit_ids = current.loc[
        pd.to_numeric(current.get("inst_control"), errors="coerce") == 2, "unitid"
    ]
    scrape_ids = list(current.head(top_n)["unitid"]) + list(nonprofit_ids.head(nonprofit_n))

    if not skip_libraries:
        current = enrich_watchlist_libraries(
            current,
            settings,
            score_year=score_year,
            scrape_ids=scrape_ids,
            skip_scrape=skip_scrape,
            cache_only=cache_only,
        )

    current = current.sort_values("risk_score", ascending=False).reset_index(drop=True)
    nonprofit_mask = pd.to_numeric(current.get("inst_control"), errors="coerce") == 2
    watch_cols = [c for c in WATCHLIST_COLS if c in current.columns]
    watch = current[watch_cols].head(500)
    watch.to_csv(out_dir / "watchlist.csv", index=False)
    nonprofit = current.loc[nonprofit_mask, watch_cols].head(250)
    if not nonprofit.empty:
        nonprofit.to_csv(out_dir / "watchlist_nonprofit.csv", index=False)

    shortlist = pd.concat(
        [current.head(top_n), current.loc[nonprofit_mask].head(nonprofit_n)],
        ignore_index=True,
    ).drop_duplicates("unitid")
    write_libraries_summary(shortlist, out_dir / "libraries_top50.md")
    shortlist_cols = [
        c
        for c in (
            "unitid",
            "inst_name",
            "state_abbr",
            "inst_control",
            "year",
            "risk_score",
            *LIB_WATCHLIST_COLS,
        )
        if c in shortlist.columns
    ]
    shortlist[shortlist_cols].to_csv(out_dir / "libraries_top50.csv", index=False)

    status_frame = load_status_for_report(settings)
    shap_global = metrics.get("shap_global") or []
    ranked = current.head(500).copy()
    ranked["watchlist_rank"] = range(1, len(ranked) + 1)

    beats = metrics.get("beats_naive") or {}
    if beats.get("any_test_year"):
        beats_note = (
            "On at least one held-out test year the main model beat a naive "
            "baseline on PR-AUC and/or recall@50. See `outputs/model_metrics.json` "
            "for year-level detail. Beating a baseline is not evidence the watch list "
            "is a reliable forecast for any named school."
        )
    else:
        beats_note = (
            "The main model did **not** clearly beat both naive baselines on a test "
            "year in this run (or positives were too few / composite scores were "
            "missing in the test window). Treat ranks as exploratory. Details are in "
            "`outputs/model_metrics.json`."
        )

    caveats = (
        "Watch list only. IPEDS lag; official FSA composites currently end FY 2018; "
        "NCES finance backfill covers published F-year zips only; HCM / Scorecard HCM2 "
        "are current-list evidence and were not training features; mergers count as "
        "positives by default; publics excluded from the primary ranking. Library "
        "holdings are IPEDS Academic Libraries enrichment (Urban 2013–2023); scraped "
        "special-collection notes are best-effort. Missing library data ≠ no library. "
        "Current-status badges are a later curated check plus federal operating flags, "
        "not a model output. Campus sales and listings are curated only."
    )
    report_counts = write_operating_report(
        out_dir / "top50_report.html",
        ranked,
        status_frame,
        open_n=top_n,
        score_year=score_year,
        caveats=caveats,
        intro=distinctive_notes_html(shortlist),
        shap_global=shap_global,
    )
    (out_dir / "model_card.md").write_text(
        _model_card_md(metrics, score_year, n_watch=len(watch), beats_note=beats_note),
        encoding="utf-8",
    )
    LOGGER.info(
        "Wrote watchlist.csv (%s), top50_report.html, libraries_top50.md, model_card.md",
        len(watch),
    )
    return {
        "score_year": score_year,
        "n_watch": len(watch),
        "n_cards": int(report_counts["n_open"]),
        "n_library_shortlist": int(len(shortlist)),
    }
