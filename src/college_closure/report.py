"""Watchlist, top-50 evidence cards, and model card.

Language is deliberately non-verdict: these are elevated-risk indicators
on a watch list, not predictions that a college will close.
"""

from __future__ import annotations

import html
import json
import logging

import numpy as np
import pandas as pd

from college_closure.config import Settings
from college_closure.features import MODEL_FEATURE_COLUMNS

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
]


def _control_label(v) -> str:
    try:
        i = int(v)
    except (TypeError, ValueError):
        return "unknown"
    return {1: "public", 2: "private nonprofit", 3: "for-profit"}.get(i, str(i))


def _fmt(v, digits: int = 2, pct: bool = False) -> str:
    if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
        return "—"
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
    for item in shap_global[:n]:
        feat = item.get("feature")
        if feat and feat in row.index:
            out.append({"feature": feat, "value": row.get(feat), "mean_abs_shap": item.get("mean_abs_shap")})
    return out


def _evidence_card(row: pd.Series, shap_items: list[dict], rank: int) -> str:
    name = html.escape(str(row.get("inst_name") or f"UNITID {row.get('unitid')}"))
    state = html.escape(str(row.get("state_abbr") or "—"))
    sector = html.escape(_control_label(row.get("inst_control")))
    year = row.get("year")
    shap_rows = ""
    for s in shap_items:
        feat = html.escape(str(s.get("feature")))
        extra = s.get("shap", s.get("value", s.get("mean_abs_shap")))
        shap_rows += f"<li><code>{feat}</code> ({_fmt(extra, 3)})</li>"
    if not shap_rows:
        shap_rows = "<li>SHAP unavailable for this row</li>"

    def _flag(v) -> bool:
        try:
            if v is None or pd.isna(v):
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
      <h2>{rank}. {name}</h2>
      <p class="meta">{state} · {sector} · score year {year} · UNITID {row.get("unitid")}</p>
      <p class="score">Watch-list score: <strong>{_fmt(row.get("risk_score"), 3)}</strong>
      — elevated-risk indicator, not a closure verdict.</p>
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
      <p class="caveat">IPEDS and FSA series lag; missing finance is flagged rather than imputed as health.
      Publics rarely close; this card is in the private nonprofit / for-profit risk universe.</p>
    </article>
    """


def _html_page(cards: str, n: int, score_year: int, caveats: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>College closure early-warning watch list (top {n})</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 920px; margin: 2rem auto; padding: 0 1rem;
           color: #222; line-height: 1.45; }}
    h1 {{ font-size: 1.6rem; }}
    .banner {{ background: #fff6e5; border: 1px solid #e0c48a; padding: 0.8rem 1rem; }}
    .card {{ border: 1px solid #ddd; padding: 1rem 1.2rem; margin: 1.2rem 0; }}
    .card h2 {{ margin-top: 0; font-size: 1.2rem; }}
    .meta, .caveat {{ color: #555; font-size: 0.95rem; }}
    table {{ border-collapse: collapse; width: 100%; margin: 0.6rem 0; }}
    th {{ text-align: left; width: 28%; color: #444; font-weight: 600; padding: 0.2rem 0.4rem; }}
    td {{ padding: 0.2rem 0.4rem; }}
    code {{ font-size: 0.9rem; }}
  </style>
</head>
<body>
  <h1>Watch list — top {n} (score year {score_year})</h1>
  <div class="banner">
    <strong>Not a verdict.</strong> Ranked elevated-risk indicators from a statistical model
    trained on historical institution-year features. A high score means the school resembles
    past closures/mergers on trailing observables — not that it will close. The score year
    is the latest <em>right-censored</em> year with published IPEDS finance (later directory
    years are omitted because unpublished finance looks like pre-closure missingness).
    Composite scores lag; HCM is a current snapshot and was not used as a training feature.
  </div>
  {cards}
  <h2>Limitations</h2>
  <p>{html.escape(caveats)}</p>
</body>
</html>
"""


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

- Urban Institute Education Data Portal IPEDS extracts (directory, enrollment, FTE,
  admissions, staffing, finance through 2017)
- NCES IPEDS complete finance files (F1A / F2 / F3) for post-2017 backfill
- Official FSA composite year workbooks from data.ed.gov (FY 2007–2018) plus
  Urban Institute FSA CSV (2006–2016). Official scores win on overlap.
- HCM and Closed School lists: ingested when a current Data Center file downloads;
  HCM is **current-only evidence** and is **not** a training feature
- College Scorecard: `DATA_GOV_API_KEY` / `SCORECARD_API_KEY` **or** the official
  no-key most-recent institution ZIP. API field `school.under_investigation` and
  ZIP column `HCM2` map to the same evidence flag; `CURROPER` is operating status.
- WICHE Knocking at the College Door 11th edition (state HS-graduate totals) when the workbook downloads
- Top-50 enrichment (flags only): accreditor public-action pages, WARN files, ProPublica 990 by EIN

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
- Files: `outputs/watchlist.csv`, `outputs/top50_report.html`

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
- Do not publish these ranks as “predicted closures.”
"""


def run_report(settings: Settings) -> dict:
    processed = settings.processed_dir
    out_dir = settings.outputs_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    scored_path = processed / "scored.parquet"
    if not scored_path.exists():
        raise FileNotFoundError("scored.parquet missing — run scripts/06_model.py")
    scored = pd.read_parquet(scored_path)
    metrics_path = processed / "model_metrics.json"
    if not metrics_path.exists():
        metrics_path = out_dir / "model_metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {}

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

    watch_cols = [c for c in WATCHLIST_COLS if c in current.columns]
    watch = current[watch_cols].head(500)
    watch.to_csv(out_dir / "watchlist.csv", index=False)
    nonprofit = current.loc[pd.to_numeric(current.get("inst_control"), errors="coerce") == 2, watch_cols].head(250)
    if not nonprofit.empty:
        nonprofit.to_csv(out_dir / "watchlist_nonprofit.csv", index=False)

    shap_global = metrics.get("shap_global") or []
    top_n = 50
    top = current.head(top_n)
    cards = []
    for i, (_, row) in enumerate(top.iterrows(), start=1):
        cards.append(_evidence_card(row, _row_shap_fallback(row, shap_global), i))

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
        "positives by default; publics excluded from the primary ranking."
    )
    (out_dir / "top50_report.html").write_text(
        _html_page("\n".join(cards), n=len(top), score_year=score_year, caveats=caveats),
        encoding="utf-8",
    )
    (out_dir / "model_card.md").write_text(
        _model_card_md(metrics, score_year, n_watch=len(watch), beats_note=beats_note),
        encoding="utf-8",
    )
    LOGGER.info("Wrote watchlist.csv (%s), top50_report.html, model_card.md", len(watch))
    return {"score_year": score_year, "n_watch": len(watch), "n_cards": int(len(top))}
