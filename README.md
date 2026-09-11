# College closure early-warning pipeline

Reproducible Python pipeline that ranks U.S. **degree-granting** colleges by
**elevated-risk indicators** of closure or merger within 2–3 years.

**This is a watch list, not a verdict.** A high score means an institution-year
resembles historical closures and mergers on trailing observables. It is **not**
a determination that a college will close, lose accreditation, or fail Title IV.
Do not publish ranks as “predicted closures.”

The primary scored universe is **private nonprofit and for-profit** schools
(`in_risk_model_universe`). Public institutions almost never close; they stay in
the panel for context and are excluded from the published ranking.

## Why this exists

Closures and mergers cluster around a small set of public signals that show up
*before* a campus disappears from IPEDS: shrinking enrollment, high tuition
dependence, thin or negative operating margins, weak or missing financial-
responsibility composites, and (sometimes) a regional high-school graduate
decline. Those constructs come from Kelchen, Ritter & Webber,
[*Predicting College Closures and Financial Distress*](https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2024/wp24-20.pdf)
(Philadelphia Fed WP 24-20 / FEDS 2025-3).

This repo turns those ideas into a **reproducible watch list**:

- Official public files only (Urban IPEDS, NCES complete-data zips, FSA
  workbooks that actually download, College Scorecard, WICHE).
- Trailing-window features only (no future leakage).
- Honest missingness (`miss_finance`, `miss_composite`) instead of filling zeros
  that look like health.
- Current-list flags (HCM, Scorecard HCM2, accreditor/WARN/990) on evidence
  cards — **not** silent score hacks and **not** training features unless a
  lagged historical series exists.

v1 (PR #1) shipped the MVP. **v2** closes the data-quality gaps that were
honestly documented as blocked or missing.

## Repo layout

```
config.yaml                 # years, splits, source URLs
requirements.txt
scripts/
  01_ingest.py              # Urban IPEDS extracts
  02_crosswalk.py           # NCES finance, FSA, Scorecard, WICHE, trackers
  03_panel.py               # UNITID×year panel + composite join
  04_features.py            # trailing-window features
  05_labels.py              # h=2 / h=3 labels, right-censor
  06_model.py               # logistic + XGBoost, temporal split
  07_report.py              # watchlist + HTML cards + model card
  run_pipeline.py           # 01 (optional) through 07
src/college_closure/        # library code
data/raw/                   # cached downloads (gitignored)
data/processed/             # Parquet (gitignored)
data/external/              # WICHE derived CSV + curated-closure placeholder
outputs/                    # committed QA, watchlist, model card
tests/
```

## Pipeline stages

| Script | Role |
| --- | --- |
| `01_ingest.py` | Urban IPEDS directory, enrollment, FTE, finance (through 2017), admissions, staffing |
| `02_crosswalk.py` | UNITID ↔ OPEID8 ↔ OPEID6 ↔ EIN; NCES finance; FSA + Scorecard + WICHE + closure trackers |
| `03_panel.py` | UNITID×year panel, parent/child finance rollup, lagged composite join |
| `04_features.py` | Trailing-window features only; winsorize 1st/99th |
| `05_labels.py` | `closed_or_merged_within_h_years` for h=2 and h=3; right-censor last h years |
| `06_model.py` | Logistic baseline + XGBoost; temporal split; PR-AUC + recall@K; SHAP |
| `07_report.py` | `outputs/watchlist.csv`, `top50_report.html`, `model_card.md` |
| `run_pipeline.py` | Orchestrates 01–07 |

Features never include future values, current HCM lists, Scorecard investigation
flags, accreditor/WARN/990 hits, or the label columns themselves.

## Install

Python 3.11+ (developed on 3.12).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`scripts/*.py` add `src/` to `sys.path`; you do not have to `pip install -e .`.

## Run

End-to-end, reusing cached Urban extracts:

```bash
python3 scripts/run_pipeline.py --skip-ingest
```

First time on a new machine (downloads Urban CSVs / API extracts):

```bash
python3 scripts/run_pipeline.py
```

Step by step:

```bash
python3 scripts/01_ingest.py
python3 scripts/02_crosswalk.py
python3 scripts/03_panel.py
python3 scripts/04_features.py
python3 scripts/05_labels.py
python3 scripts/06_model.py
python3 scripts/07_report.py
```

Optional flags (also accepted by `run_pipeline.py`):

| Flag | Effect |
| --- | --- |
| `--skip-ingest` | Reuse `data/processed/directory.parquet` (pipeline only) |
| `--skip-nces` | Skip NCES finance zips |
| `--skip-fsa` | Skip Urban + official FSA composites / HCM / Closed School |
| `--skip-scorecard` | Skip College Scorecard API and bulk ZIP |
| `--with-scorecard` | Explicit Scorecard on (this is the default). API if `DATA_GOV_API_KEY` is set, else official no-key ZIP. With `--skip-fsa`, still runs Scorecard alone. |
| `--skip-wiche` | Skip WICHE Knocking workbook |
| `--skip-closures` | Skip Higher Ed Dive / BestColleges / curated CSV |

Tests:

```bash
PYTHONPATH=src python3 -m pytest tests -q
```

## Environment variables

| Variable | Effect |
| --- | --- |
| `DATA_GOV_API_KEY` | College Scorecard API (`api.data.gov`). Preferred when set. |
| `SCORECARD_API_KEY` | Alias for the same key. |

If neither is set, ingest uses the official no-key most-recent institution ZIP
from `ed-public-download.scorecard.network`. Urban, NCES, WICHE, and data.ed.gov
composites do not need a key.

**Do not commit API keys.** The Scorecard client sends the key as the `api_key`
query parameter and never writes it into parquet, logs, or `outputs/`.

## v2 runbook

1. `pip install -r requirements.txt`
2. Optionally `export DATA_GOV_API_KEY=…` on a machine that has a data.gov key
   (this VM does not store one).
3. `python3 scripts/run_pipeline.py` (first machine) or `--skip-ingest` when
   Urban Parquet already exists.
4. `PYTHONPATH=src python3 -m pytest tests -q`
5. Read `outputs/fsa_ingest.md` for the HTTP **verified live vs still impossible**
   table (exact URLs and status codes).
6. Read `outputs/nces_finance_years.md` before trusting a later score year —
   never rank a year whose `miss_finance` is mostly unpublished NCES files.

## Data sources (verified live vs still limited)

Numbers below are from the v2 agent run on **2026-09-11**. Re-runs will rewrite
`outputs/fsa_ingest.md` if URLs move.

| Source | Status | Coverage vs MVP |
| --- | --- | --- |
| Official FSA composites on **data.ed.gov** (AY 2006–07 through 2017–18 `.xls`) | **Live** (CKAN `ff51fef3-9d22-49a7-b34b-54329a290307`) | **40,969** official rows, fiscal years **2007–2018**. Merged with Urban: **74,122** rows, **2006–2018** (MVP was 37,589 / 2006–2016). Contemporaneous panel hits: **2,103** in 2017 and **1,464** in 2018 (MVP was 0 after 2016). |
| Urban FSA composite CSV | **Live** | 37,589 rows, 2006–2016 (unchanged) |
| College Scorecard most-recent institution ZIP (no API key) | **Live** (`Most-Recent-Cohorts-Institution_06102026.zip`) | **6,273** institutions; **16** HCM2 flags; **30** `CURROPER=0`. Most-recent file has no `CLOSEDAT`. |
| College Scorecard API (`DATA_GOV_API_KEY`) | Implemented; key not present on this VM | Same fields (`school.operating`, `school.ownership`, `school.under_investigation`, UNITID / OPEID). Mocked in `tests/test_scorecard.py`. |
| WICHE Knocking 11th edition workbook | **Live** | **1,683** state-years (2009–2041); `hs_grad_pct_chg_5y` on the panel when `state_abbr` is present |
| NCES `F1819`–`F2223` finance zips | **Live** | **29,613** rows, **2018–2022** (same as MVP) |
| NCES `F2324_*` / `F2425_*` complete-data zips | **404** (tried `_Data_Stata`, `_P`, `_RV`, `_rev`) | Score year stays **2022** — 2023–24 are publication-lag `miss_finance` |
| studentaid.gov JS Data Center HCM / post-2018 composites | Direct `.xlsx` timeout/404 | Scorecard `HCM2` used as current evidence flag only |
| Partner Connect Closed School `.xls` | Dated URLs 404 | Labels remain IPEDS `inst_status` / `date_closed` |
| Higher Ed Dive / BestColleges trackers | BestColleges HTML cached (3 regex rows); no unique name+state matches | **0** extra label events. Placeholder: `data/external/closures_curated.csv` |
| Accreditor public-action pages | HLC 403; SACSCOC/NECHE/WSCUC/NWCCU 404 | Flags empty unless a page hits |
| CA WARN xlsx | **Live** (EDD) | Name-match flags on the shortlist only |
| ProPublica 990 | **Live** by EIN | Nonprofit shortlist only; no fuzzy name join |

| Step | v2 result |
| --- | --- |
| Urban ingest | Directory 2004–2024; **92,257** panel rows |
| Parent/child rollup | **3,028** child rows inherited parent totals |
| Labels h=3 | **3,703** positives / 50,315 complete *risk-universe* rows (same IPEDS event set as MVP; trackers added no unique matches) |
| Model | XGBoost test **PR-AUC 0.179** vs naive composite 0.052 / 5y-decline 0.123; recall@50 **0.090** vs 0.009 / 0.045. **Beats both baselines**. Honest note: PR-AUC is slightly below MVP 0.190 after adding 2017–18 composites + WICHE — not a claimed improvement in rank quality. |
| Watch list | Score year **2022** (`miss_finance` 4.8%). Extra columns: Scorecard HCM2/operating, accreditor/WARN/990 flags |

Exact URLs and status codes: [`outputs/fsa_ingest.md`](outputs/fsa_ingest.md).

## Outputs (committed)

| File | What it is |
| --- | --- |
| [`outputs/watchlist.csv`](outputs/watchlist.csv) | Ranked private nonprofit / for-profit scores for the latest right-censored year that still has published finance (not a closure prediction) |
| [`outputs/watchlist_nonprofit.csv`](outputs/watchlist_nonprofit.csv) | Same ranking restricted to private nonprofits |
| [`outputs/top50_report.html`](outputs/top50_report.html) | Evidence cards: FTE trend, discount, margins, composite, HCM/Scorecard flags, enrichment, top drivers |
| [`outputs/model_card.md`](outputs/model_card.md) | Task, data, temporal split, PR-AUC / recall@K, SHAP, caveats |
| [`outputs/model_metrics.json`](outputs/model_metrics.json) | Machine-readable split metrics and baseline comparison |
| [`outputs/nces_finance_years.md`](outputs/nces_finance_years.md) | Which NCES F-year zips parsed; why later years are not ranked |
| [`outputs/fsa_ingest.md`](outputs/fsa_ingest.md) | Which FSA / Scorecard files downloaded vs skipped (HTTP table) |
| [`outputs/qa_counts.md`](outputs/qa_counts.md) / [`outputs/qa_panel.md`](outputs/qa_panel.md) | Universe / panel QA |

`data/raw/` and `data/processed/` are gitignored (regenerate with the scripts).

### Score-year rule

The watch list is scored on the latest **right-censored** year whose
`miss_finance` is not dominated by unpublished NCES files (threshold: mean
`miss_finance` &lt; 50%). In this build that year is **2022**. Directory years
2023–2024 exist, but `F2324` / `F2425` standalone zips still 404, so ranking
those years would treat publication lag as a risk signal.

## College universe

From the Urban IPEDS directory (`inst_control` is the portal name for CONTROL):

- `degree_granting == 1`
- `inst_control` in `{1 public, 2 private nonprofit, 3 for-profit}`
- Title IV participating when `title_iv_indicator` is reported (`1, 2, 4, 8`);
  missing Title IV is kept
- Drop `sector == 0` and name patterns such as “system office”

Live Urban directory (fall 2004–2024), after filters: **5,886** unique UNITID,
**92,257** institution-years, **3,887** in 2024. Details: `outputs/qa_counts.md`.

## Identifiers (OPEID 6 vs 8)

- IPEDS OPEID is 8 digits: **6-digit FSA root + 2-digit branch** (`…00` = main).
- FSA files often store only the 6-digit root. We do **not** left-pad a 6-digit
  value to 8 (that would turn `002345` into `00002345`). Six-digit roots become
  `root + "00"` via `ids.normalize_opeid8`.
- Pandas often stores `00234500` as int `234500`. That stripped form is restored
  to `00234500`, not treated as a 6-digit root.
- Joins: exact UNITID×year when possible; else OPEID6, preferring the main
  campus when several UNITIDs share a root (`opeid6_n_unitids`).
- Official data.ed.gov composite rows often have **no UNITID**. The panel join
  keeps those rows and attaches on OPEID6×year (this was a v2 bugfix: dropping
  null UNITID silently discarded all 2017–18 official scores).

## Finance

- Urban `colleges_ipeds_finance.csv` ends in **2017**.
- NCES complete-data zips `F{yy}{yy+1}_{F1A|F2|F3}.zip` backfill later years
  (e.g. `F1819_F2.zip` = FY 2018). `F2324_*` was not published as a standalone
  zip as of this build.
- Child campuses with $0 / missing revenue **inherit parent totals** and are
  flagged `finance_from_parent`. Parents are not dropped or double-summed.

## Labels

- Positives: IPEDS `inst_status` ∈ {4, 7} (closed), {3} merger if
  `labels.mergers_are_positive` (default true), `date_closed` / `year_deleted`,
  FSA Closed School (OPEID6 + year) when that file downloads, unique name+state
  matches from Higher Ed Dive / BestColleges / `data/external/closures_curated.csv`,
  and Scorecard `CLOSEDAT` only when the year is in 1980–2035 (sentinels `-2`,
  `-1`, `1`, `2`, `3` rejected).
- Events are taken from `directory_raw.parquet` (unfiltered) so leaving the
  *filtered* universe is not treated as a closure.
- Panel-disappearance labels are **off** by default (`use_disappearance: false`).
- `closed_or_merged_within_h_years` is 1 if the event year is in `(year, year+h]`.
- Rows with `year + h > last_complete_year` are right-censored (training
  excludes them; they are the watch-list scoring set).

## Model

- Train on `in_risk_model_universe` rows with complete h=3 labels.
- Default split: train ≤2016, val 2017–2019, test 2020–2021 (no shuffle).
  Years without complete labels are dropped from the split.
- Boosters: logistic regression + XGBoost. The published rank uses XGBoost
  `risk_score`.
- Naive baselines: (a) last-known composite &lt; 1.0; (b) 5-year FTE decline &gt; 30%.
- HCM / Scorecard HCM2 / operating / accreditor / WARN / 990 are **not**
  training features (current lists only; shown on evidence cards).
- Metrics and SHAP: `outputs/model_card.md`. This v2 test set:
  **PR-AUC 0.179**, recall@50 **0.090**, n=4,799, 223 positives. Beats both
  naive baselines. Slightly below MVP 0.190 / 0.099 after attaching official
  2017–18 composites and WICHE — documented, not hidden.
- Top SHAP drivers in this run include `unrestricted_na_to_exp`,
  `composite_score`, `log_fte`, `endowment_per_fte`, `operating_margin`, and
  WICHE `hs_grad_pct_chg_5y`.

## Tests

```bash
PYTHONPATH=src python3 -m pytest tests -q
```

Covers universe filters, OPEID 6/8 (never pad a 6-digit root to 8 with leading
zeros), official composite attach without dropping missing UNITID, trailing-
window (no-leak) features, parent/child rollup, label horizon / right-censor /
merger toggle / sentinel CLOSEDAT, Scorecard API mapping (mocked HTTP, no live
key), HCM2 mapping, WICHE join, extra-closure unique-match rule, recall@K.

## Configure

`config.yaml`: year window, label horizons, temporal split, Urban / NCES / FSA /
Scorecard / WICHE URLs. FSA pages move; ingest tries several URLs and
**continues** on failure. Missing files are skipped, never invented.

## v1 → v2 changelog

| Area | v1 (MVP) | v2 |
| --- | --- | --- |
| FSA composites | Urban CSV only, through 2016 | Urban + official data.ed.gov workbooks through FY **2018** (40,969 official rows) |
| Composite join | Dropped official rows with null UNITID | Keep those rows; join on OPEID6×year |
| HCM | Official workbook (blocked) | Still blocked; Scorecard `HCM2` / API `under_investigation` as **evidence only** |
| Closed School | Partner Connect `.xls` (404) | Still 404; IPEDS labels + tracker/curated hooks |
| NCES finance | `F1819`–`F2223` | Same live years; `F2324`/`F2425`/`F2526` tried with suffix variants, still 404 |
| Scorecard | Not ingested | API (`DATA_GOV_API_KEY`) or official no-key ZIP; `--with-scorecard` / `--skip-scorecard` |
| WICHE | Absent | 11th-edition workbook → `hs_grad_pct_chg_5y` |
| Trackers | Absent | Higher Ed Dive / BestColleges / curated CSV; unique name+state only |
| Top-50 flags | Composite + HCM if present | + Scorecard operating/HCM2, accreditor, WARN, ProPublica 990 by EIN |
| HTTP audit | Light | `outputs/fsa_ingest.md` + `fsa_attempts.json` |
| Model | Test PR-AUC 0.190 / recall@50 0.099 | Test PR-AUC **0.179** / recall@50 **0.090** — still beats naive; not claimed as better ranks |

## Caveats / ethics

- IPEDS publications lag. Recent finance and composite scores may be missing.
  Missingness is a feature, not filled with zeros that look like health.
- Official FSA composites via data.ed.gov currently end in FY **2018**. Later
  years use last observed score + `composite_is_lagged`. Post-2018 FSA
  workbooks are JS Data Center only (attempted; not ingested).
- `F2324` / `F2425` standalone zips are still 404. Score year stays 2022.
- Official HCM workbook and Closed School weekly `.xls` remain blocked.
- Extra closure trackers added 0 unique name+state matches this run.
- College Scorecard most-recent ZIP uses `HCM2` / `CURROPER`, not
  `UNDER_INVESTIGATION` / `OPERATING`. The API uses the latter names.
- Accreditor / WARN / 990 flags are best-effort on the top-50 / nonprofit
  shortlist only (exact name or verified EIN). They never change the model score.
- For-profit chain collapses and public “closures” are different processes.
  Publics are excluded from the primary ranking.
- False positives are expected. A high rank is an invitation to read the
  evidence card, not a journalistic claim.
- Reputational harm is real. Keep language as **elevated-risk indicators**.
- Do not publish ranks as “predicted closures.”

## Known remaining limits (roadmap)

- Official FSA HCM1/HCM2 workbook and weekly Closed School `.xls` (JS Data
  Center / Partner Connect). Try again when a stable direct file exists.
- Post-2018 official composite workbooks (same JS Data Center).
- NCES `F2324` / `F2425` standalone complete-data zips — raise the score year
  only when `miss_finance` is no longer mostly publication lag.
- Higher Ed Dive / BestColleges structured tables (current regex is conservative;
  unique directory matches only). Prefer filling `data/external/closures_curated.csv`
  from a cited list over fuzzy matching.
- Accreditor action pages (several 403/404). Cache whatever HTML/CSV is public.
- Additional state WARN files beyond CA (NY URL in config is best-effort).
- Live Scorecard API ingest on a machine that has `DATA_GOV_API_KEY` (code path
  is ready; this VM does not store a key).

## Data policy

- Do not invent enrollment, finance, or closure dates.
- Do not invent institutions or metrics.
- Do not commit `data/raw/` or processed Parquet (see `.gitignore`).
- Do not commit API keys.
- Cite Urban + IPEDS: [Education Data Portal](https://educationdata.urban.org/documentation/),
  Urban Institute; NCES IPEDS complete data files; FSA Data Center / data.ed.gov
  when those files are used; College Scorecard; WICHE Knocking at the College Door.
