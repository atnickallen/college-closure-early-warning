# Model card — college closure early-warning watch list

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
- IPEDS Academic Libraries (Urban portal, 2013–2023): **watch-list enrichment only**
  (`lib_*` columns / evidence-card section). Not used as a training feature.

## Temporal split (no shuffle)

- Train: years ≤ 2016
- Validation: [2017, 2018, 2019]
- Test: [2020, 2021]
- Right-censored years (incomplete h-year window) are scored for the watch list
  and excluded from training metrics

Sizes: train n=37855 (positives 2876);
val n=7661; test n=4799.

## Metrics (held-out test)

| Model | PR-AUC | ROC-AUC | Recall@25 | Recall@50 | Recall@100 | n | positives |
|-------|--------|---------|-----------|-----------|------------|---|-----------|
| xgboost | 0.179 | 0.748 | 0.049 | 0.090 | 0.148 | 4799 | 223 |
| logistic | 0.114 | 0.778 | 0.009 | 0.013 | 0.013 | 4799 | 223 |
| naive: composite < 1.0 | 0.052 | 0.529 | 0.000 | 0.009 | 0.054 | 4799 | 223 |
| naive: 5y enrollment decline > 30% | 0.123 | 0.737 | 0.009 | 0.045 | 0.090 | 4799 | 223 |

On at least one held-out test year the main model beat a naive baseline on PR-AUC and/or recall@50. See `outputs/model_metrics.json` for year-level detail. Beating a baseline is not evidence the watch list is a reliable forecast for any named school.

Configured feature columns not present in this run: none.

## Top global drivers

- `unrestricted_na_to_exp` (mean |SHAP| 0.8833)
- `composite_score` (mean |SHAP| 0.5162)
- `log_fte` (mean |SHAP| 0.4278)
- `endowment_per_fte` (mean |SHAP| 0.4115)
- `operating_margin` (mean |SHAP| 0.2667)
- `yield_rate` (mean |SHAP| 0.2584)
- `tuition_dependence` (mean |SHAP| 0.2384)
- `enr_pct_chg_1y` (mean |SHAP| 0.2173)
- `hs_grad_pct_chg_5y` (mean |SHAP| 0.1780)
- `admit_rate` (mean |SHAP| 0.1598)
- `student_staff_ratio` (mean |SHAP| 0.1516)
- `sector` (mean |SHAP| 0.1441)

## Watch list

- Score year: **2022**
- Rows written: **500**
- Files: `outputs/watchlist.csv`, `outputs/top50_report.html`, `outputs/libraries_top50.md`

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
