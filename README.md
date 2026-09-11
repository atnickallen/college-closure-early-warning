# College closure early-warning pipeline

Reproducible Python pipeline that ranks U.S. **degree-granting** colleges by
**elevated-risk indicators** of closure or merger within 2–3 years.

**This is a watch list, not a verdict.** A high score means an institution-year
resembles historical closures/mergers on trailing observables. It is **not** a
determination that a college will close, lose accreditation, or fail.

Methodological blueprint: Kelchen, Ritter & Webber,
[*Predicting College Closures and Financial Distress*](https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2024/wp24-20.pdf)
(Philadelphia Fed WP 24-20 / FEDS 2025-3). Features follow their constructs:
enrollment trajectory, tuition dependence, operating margins, staffing, and
lagged FSA financial-responsibility signals. **Public institutions almost never
close**; they stay in the panel for context. The risk model trains and ranks
**private nonprofit and for-profit** rows (`in_risk_model_universe`).

## Pipeline

| Script | Role |
| --- | --- |
| `scripts/01_ingest.py` | Urban IPEDS directory, enrollment, FTE, finance (through 2017), admissions, staffing |
| `scripts/02_crosswalk.py` | UNITID ↔ OPEID8 ↔ OPEID6 ↔ EIN; NCES finance backfill; FSA composite / HCM / Closed School |
| `scripts/03_panel.py` | UNITID×year panel, parent/child finance rollup, composite join |
| `scripts/04_features.py` | Trailing-window features only (no future leakage); winsorize 1st/99th |
| `scripts/05_labels.py` | `closed_or_merged_within_h_years` for h=2 and h=3; right-censor last h years |
| `scripts/06_model.py` | Logistic baseline + XGBoost; temporal split; PR-AUC + recall@K; SHAP |
| `scripts/07_report.py` | `outputs/watchlist.csv`, `outputs/top50_report.html`, `outputs/model_card.md` |
| `scripts/run_pipeline.py` | Runs 01 (optional) through 07 |

## Install

Python 3.11+ (developed on 3.12).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`scripts/*.py` add `src/` to `sys.path`; you do not have to `pip install -e .`.

## Run

End-to-end (reuses cached Urban extracts if present):

```bash
python3 scripts/run_pipeline.py --skip-ingest
```

First time on a new machine (downloads Urban CSVs/API extracts):

```bash
python3 scripts/run_pipeline.py
```

Step by step:

```bash
python3 scripts/01_ingest.py          # skip if data/processed/directory.parquet exists
python3 scripts/02_crosswalk.py       # NCES zips + FSA files; logs and continues on 404
python3 scripts/03_panel.py
python3 scripts/04_features.py
python3 scripts/05_labels.py
python3 scripts/06_model.py
python3 scripts/07_report.py
```

Optional flags: `02_crosswalk.py --skip-nces` / `--skip-fsa`.

College Scorecard is used only when `DATA_GOV_API_KEY` or `SCORECARD_API_KEY`
is set. WICHE high-school graduate trends are used only if
`data/external/wiche_hs_graduates.csv` exists (`state_abbr`, `year`, `hs_graduates`).

## Outputs (committed)

| File | Contents |
| --- | --- |
| [`outputs/watchlist.csv`](outputs/watchlist.csv) | Ranked private nonprofit / for-profit scores for the latest right-censored year |
| [`outputs/top50_report.html`](outputs/top50_report.html) | Evidence cards (FTE trend, discount, margins, composite, HCM, top drivers) |
| [`outputs/model_card.md`](outputs/model_card.md) | Metrics, recall@K, caveats |
| [`outputs/model_metrics.json`](outputs/model_metrics.json) | Machine-readable split metrics and baseline comparison |
| [`outputs/nces_finance_years.md`](outputs/nces_finance_years.md) | Which NCES F-year zips parsed |
| [`outputs/fsa_ingest.md`](outputs/fsa_ingest.md) | Which FSA files downloaded vs skipped |
| [`outputs/qa_counts.md`](outputs/qa_counts.md) / [`outputs/qa_panel.md`](outputs/qa_panel.md) | Universe / panel QA |

`data/raw/` and `data/processed/` are gitignored (regenerate with the scripts).

## College universe

From the Urban IPEDS directory (`inst_control` is the portal name for CONTROL):

- `degree_granting == 1`
- `inst_control` in `{1 public, 2 private nonprofit, 3 for-profit}`
- Title IV participating when `title_iv_indicator` is reported (`1, 2, 4, 8`); missing Title IV is kept
- Drop `sector == 0` and name patterns such as “system office”

Live Urban directory (fall 2004–2024), after filters: **5,886** unique UNITID,
**92,257** institution-years, **3,887** in 2024. Details: `outputs/qa_counts.md`.

## Identifiers (OPEID 6 vs 8)

- IPEDS OPEID is 8 digits: **6-digit FSA root + 2-digit branch** (`…00` = main).
- FSA files often store only the 6-digit root. We do **not** left-pad a 6-digit
  value to 8 (that would turn `002345` into `00002345`).
- Joins: exact UNITID×year when possible; else OPEID6, preferring the main
  campus when several UNITIDs share a root (`opeid6_n_unitids`).

## Finance

- Urban `colleges_ipeds_finance.csv` ends in **2017**.
- NCES complete-data zips `F{yy}{yy+1}_{F1A|F2|F3}.zip` backfill later years
  (e.g. `F1819_F2.zip` = FY 2018). `F2324_*` was not published as of this build.
- Child campuses with $0 / missing revenue **inherit parent totals** and are
  flagged `finance_from_parent`. Parents are not dropped or double-summed.

## Labels

- Positives: IPEDS `inst_status` ∈ {4, 7} (closed), {3} merger if
  `labels.mergers_are_positive` (default true), `date_closed` / `year_deleted`,
  and FSA Closed School (OPEID6 + year) when that file downloads.
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
- Naive baselines: (a) last-known composite &lt; 1.0; (b) 5-year FTE decline &gt; 30%.
- HCM is **not** a training feature (current list only, shown on evidence cards).
- Metrics and SHAP: `outputs/model_card.md`.

## Tests

```bash
PYTHONPATH=src python3 -m pytest tests -q
```

Covers universe filters, OPEID 6/8, trailing-window (no-leak) features,
parent/child rollup, label horizon / right-censor / merger toggle, recall@K.

## Configure

`config.yaml`: year window, label horizons, temporal split, Urban / NCES / FSA
URLs. FSA pages move; ingest tries several URLs and **continues** on failure.

## Known limitations

- IPEDS publications lag; recent finance and composite scores may be missing.
  Missingness is a feature (`miss_finance`, `miss_composite`), not filled with
  zeros that look like health.
- Urban composite scores historically end in 2016. Later years use the last
  observed score (lagged) plus `composite_is_lagged`.
- Official FSA HCM / Closed School / composite workbooks are downloaded when a
  current file URL works. JavaScript Data Center pages are not scraped as data.
- College Scorecard and WICHE are optional.
- Accreditor actions, WARN notices, and IRS 990s are **not** ingested
  (TODO — do not treat the watch list as a complete diligence file).
- For-profit chain collapses and public “closures” are different processes;
  publics are excluded from the primary ranking.
- Do not publish ranks as “predicted closures.”

## Data policy

- Do not invent enrollment, finance, or closure dates.
- Do not commit `data/raw/` or processed Parquet (see `.gitignore`).
- Cite Urban + IPEDS: [Education Data Portal](https://educationdata.urban.org/documentation/), Urban Institute;
  NCES IPEDS complete data files; FSA Data Center when those files are used.

## Layout

```
config.yaml
requirements.txt
scripts/01_ingest.py … 07_report.py  run_pipeline.py
src/college_closure/
data/raw/            # cached downloads (gitignored)
data/processed/      # Parquet (gitignored)
outputs/             # QA, watchlist, model card (committed)
tests/
```
