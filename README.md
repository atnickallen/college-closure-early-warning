# College closure early-warning watch list

Reproducible Python pipeline that ranks U.S. **degree-granting** colleges by
**elevated-risk indicators** of closure or merger within 2–3 years.

**This is a watch list, not a verdict.** A high score means an institution-year
resembles historical closures and mergers on trailing observables. It is **not**
a determination that a college will close, lose accreditation, or fail Title IV.
Do not publish ranks as “predicted closures.”

The primary scored universe is **private nonprofit and for-profit** schools
(`in_risk_model_universe`). Public institutions almost never close; they stay in
the panel for context and are excluded from the published ranking.

v1 (PR #1) shipped the MVP. **v2** (this branch) closes the data-quality gaps
that were honestly documented as blocked or missing. Live numbers below are from
the 2026-09-11 retrain.

## Contents

1. [What this is](#what-this-is)
2. [Motivation and method](#motivation-and-method)
3. [Repo layout](#repo-layout)
4. [Pipeline stages](#pipeline-stages)
5. [Install](#install)
6. [Run](#run)
7. [Environment variables](#environment-variables)
8. [College Scorecard ingest](#college-scorecard-ingest)
9. [v2 runbook](#v2-runbook)
10. [Data sources](#data-sources-verified-live-vs-still-limited)
11. [Outputs](#outputs)
12. [College universe](#college-universe)
13. [Identifiers (OPEID 6 vs 8)](#identifiers-opeid-6-vs-8)
14. [Finance](#finance)
15. [Libraries & book collections (enrichment)](#libraries--book-collections-enrichment)
16. [Labels](#labels)
17. [Features](#features)
18. [Model](#model)
19. [How to read a watch-list row](#how-to-read-a-watch-list-row)
20. [Tests](#tests)
21. [Configure](#configure)
22. [v1 → v2 changelog](#v1--v2-changelog)
23. [Caveats / ethics](#caveats--ethics)
24. [Roadmap](#roadmap-remaining-data-gaps)
25. [Data policy](#data-policy)

---

## What this is

A **ranked watch list** of private nonprofit and for-profit colleges whose
trailing public numbers look like schools that later closed or merged.

| It is | It is not |
| --- | --- |
| A screening list of elevated-risk *indicators* | A prediction that any named college will close |
| Statistical resemblance to historical closures/mergers | An accreditation, Title IV, or financial-responsibility finding |
| Built only from public files that actually downloaded | Invented enrollment, finance, closure dates, or rare-book claims |
| Right-censored on years whose outcomes are not yet knowable | A live “failure forecast” for 2024–26 |

If you only open one artifact after a run, open
[`outputs/top50_report.html`](outputs/top50_report.html) and read the banner on
every card: *elevated-risk indicator, not a closure verdict.*

## Motivation and method

Closures and mergers tend to show up in public data *before* a campus vanishes
from IPEDS. The constructs follow Kelchen, Ritter & Webber,
[*Predicting College Closures and Financial Distress*](https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2024/wp24-20.pdf)
(Philadelphia Fed WP 24-20 / FEDS 2025-3):

| Signal | Why it matters | Feature(s) here |
| --- | --- | --- |
| Shrinking enrollment / FTE | Demand is the first thing to go | `enr_pct_chg_1y/5y/10y`, `enr_decline_5y_gt30`, `log_fte`, `fte_under_1000` |
| First-time / admissions softening | Pipeline dries up before headcount | `ftft_pct_chg_1y`, `admit_rate`, `yield_rate`, 5y changes |
| High tuition dependence | Little cushion if students leave | `tuition_dependence`, `high_tuition_dependence`, `discount_rate` |
| Thin or negative margins | Operating losses compound | `operating_margin`, `consec_neg_margin_yrs`, `unrestricted_na_to_exp` |
| Weak endowment | Less ability to ride out a dip | `endowment_per_fte` |
| Staff cuts | Often a last-resort cash move | `staff_pct_chg_*`, `student_staff_ratio` |
| FSA composite in the zone / failing | Official financial-responsibility flag | `composite_score`, `composite_fail`, `composite_zone`, `years_in_zone`, `composite_is_lagged` |
| Missing finance / composite | Publication lag *or* a school that stopped reporting | `miss_finance`, `miss_composite` (never zero-filled as health) |
| Regional HS-graduate decline | Demographic headwind (v2) | `hs_grad_pct_chg_5y` (WICHE) |

This repo turns those ideas into a **reproducible watch list**:

- Official public files only (Urban IPEDS, NCES complete-data zips, FSA
  workbooks that actually download, College Scorecard, WICHE).
- Trailing-window features only (no future leakage).
- Honest missingness instead of filling zeros that look like health.
- Current-list flags (HCM, Scorecard HCM2, accreditor/WARN/990) on evidence
  cards — **not** silent score hacks and **not** training features unless a
  lagged historical series exists.

## Repo layout

```
config.yaml                 # years, splits, source URLs, label toggles
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
src/college_closure/        # library (ids, ingest, features, model, report, …)
data/raw/                   # cached downloads (gitignored)
data/processed/             # Parquet extracts (gitignored)
data/external/              # WICHE derived CSV + curated-closure placeholder
outputs/                    # committed QA, watchlist, model card
tests/
```

| Library module | Role |
| --- | --- |
| `ids.py` | UNITID / OPEID6 / OPEID8 / EIN normalization (never pad a 6-digit root wrong) |
| `urban.py` / `ingest.py` / `filters.py` | Urban IPEDS downloads and universe filters |
| `nces_finance.py` | Post-2017 F1A/F2/F3 zips |
| `fsa.py` | Urban + data.ed.gov composites, HCM, Closed School, attempt log |
| `scorecard.py` | API (`DATA_GOV_API_KEY`) or official no-key ZIP |
| `wiche.py` | Knocking at the College Door HS-graduate series |
| `closures_extra.py` | Higher Ed Dive / BestColleges / curated CSV (unique name+state) |
| `panel.py` / `crosswalk.py` | UNITID×year panel, parent/child rollup, composite attach |
| `features.py` | Trailing windows; `MODEL_FEATURE_COLUMNS` |
| `labels.py` | Event years, horizons, right-censor |
| `model.py` | Temporal split, logistic + XGBoost, PR-AUC, recall@K, SHAP |
| `report.py` / `enrichment.py` / `libraries.py` | Watchlist, HTML cards, accreditor/WARN/990 flags, IPEDS Academic Libraries |
| `download.py` / `attempts.py` | HTTP with browser UA, cache, Wayback, attempt log |

`scripts/*.py` add `src/` to `sys.path`; you do not have to `pip install -e .`.

## Pipeline stages

```
01 ingest  →  02 crosswalk  →  03 panel  →  04 features
                                           →  05 labels  →  06 model  →  07 report
```

`python3 scripts/run_pipeline.py` runs that sequence. `--skip-ingest` starts at
02 when Urban Parquet already exists.

| Stage | Reads | Writes | Notes |
| --- | --- | --- | --- |
| `01_ingest.py` | Urban CSV / API (`config.yaml` `sources:`) | `data/processed/directory.parquet`, enrollment, FTE, finance, admissions, staffing | First machine only if cache is empty |
| `02_crosswalk.py` | Directory + NCES zips + FSA / Scorecard / WICHE / trackers + IPEDS Academic Libraries | `crosswalk.parquet`, `finance_nces.parquet`, `fsa_*.parquet`, `scorecard_operating.parquet`, `libraries.parquet` | Continues on 404; logs URLs in `outputs/fsa_ingest.md` |
| `03_panel.py` | Processed extracts | `panel.parquet`, `outputs/qa_panel.md` | Official composites without UNITID join on OPEID6×year |
| `04_features.py` | Panel (+ WICHE CSV) | `features.parquet` | Trailing windows only; winsorize 1st/99th |
| `05_labels.py` | Features + `directory_raw` + optional FSA/Scorecard/trackers | `labels.parquet`, `closure_events.parquet` | Right-censor last *h* years |
| `06_model.py` | Labels | `scored.parquet`, `outputs/model_metrics.json` | No shuffle; HCM not in the feature matrix |
| `07_report.py` | Scored + Scorecard + shortlist enrichment + Academic Libraries | `watchlist.csv`, `watchlist_nonprofit.csv`, `top50_report.html`, `libraries_top50.md`, `model_card.md` | Score year = latest right-censored year with published finance |

Features never include future values, current HCM lists, Scorecard investigation
flags, accreditor/WARN/990 hits, IPEDS library holdings, or the label columns themselves.

## Install

Python **3.11+** (developed on 3.12).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` includes pandas, pyarrow, requests, PyYAML, scikit-learn,
XGBoost, SHAP, openpyxl/xlrd, matplotlib, pytest.

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

Optional flags (also accepted by `run_pipeline.py` unless noted):

| Flag | Effect |
| --- | --- |
| `--skip-ingest` | Reuse `data/processed/directory.parquet` (pipeline only) |
| `--skip-nces` | Skip NCES finance zips |
| `--skip-fsa` | Skip Urban + official FSA composites / HCM / Closed School (**does not** skip Scorecard) |
| `--skip-scorecard` | Skip College Scorecard API and bulk ZIP |
| `--with-scorecard` | Explicit Scorecard on (this is the default). API if `DATA_GOV_API_KEY` is set, else official no-key ZIP |
| `--skip-wiche` | Skip WICHE Knocking workbook |
| `--skip-closures` | Skip Higher Ed Dive / BestColleges / curated CSV |
| `--skip-libraries` | Skip IPEDS Academic Libraries CSV (`02_crosswalk.py` / `07_report.py`) |
| `--skip-scrape` | `07_report.py` only: join AL counts without fetching public library pages |

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
query parameter and never writes it into parquet, logs, or `outputs/`. A literal
`scorecard.api_key` in `config.yaml` is ignored; only env-var *names* are allowed
(`scorecard.api_key_env`).

## College Scorecard ingest

Auto-detect: if `DATA_GOV_API_KEY` (or `SCORECARD_API_KEY`) is already in the
environment, `02_crosswalk.py` / `run_pipeline.py` use the official API
(`school.operating`, `school.ownership`, `school.under_investigation`, UNITID,
OPEID6/8). Otherwise they download the official no-key most-recent ZIP
(`CURROPER` / `HCM2`). `--with-scorecard` is the default; `--skip-scorecard`
turns it off.

Live API on a machine that already has the key (do not paste the key):

```bash
python3 scripts/02_crosswalk.py --skip-nces --skip-fsa --skip-wiche --skip-closures --with-scorecard
python3 scripts/05_labels.py
python3 scripts/07_report.py
```

Scorecard is a **current snapshot**: HCM2 / `under_investigation` and
`operating=0` are evidence-card flags and a CLOSEDAT label cross-check when a
valid year exists. They are **not** training features. Sentinel CLOSEDAT years
are rejected. Unit tests mock HTTP so CI never needs a key.

## v2 runbook

1. `pip install -r requirements.txt`
2. Optionally set `DATA_GOV_API_KEY` on a machine that already has a data.gov
   key (this build VM does not store one).
3. `python3 scripts/run_pipeline.py` (first machine) or `--skip-ingest` when
   Urban Parquet already exists.
4. `PYTHONPATH=src python3 -m pytest tests -q`
5. Read `outputs/fsa_ingest.md` for the HTTP **verified live vs still impossible**
   table (exact URLs and status codes).
6. Read `outputs/nces_finance_years.md` before trusting a later score year —
   never rank a year whose `miss_finance` is mostly unpublished NCES files.
7. Open `outputs/top50_report.html` and `outputs/model_card.md`. Treat ranks as
   a screen, not a story.

## Data sources (verified live vs still limited)

Numbers below are from the v2 agent run on **2026-09-11**. Re-runs rewrite
`outputs/fsa_ingest.md` if URLs move. Missing files are skipped, never invented.

| Source | Status | Coverage vs MVP |
| --- | --- | --- |
| Official FSA composites on **data.ed.gov** (AY 2006–07 through 2017–18 `.xls`) | **Live** (CKAN `ff51fef3-9d22-49a7-b34b-54329a290307`) | **40,969** official rows, fiscal years **2007–2018**. Merged with Urban: **74,122** rows, **2006–2018** (MVP was 37,589 / 2006–2016). Contemporaneous panel hits: **2,103** in 2017 and **1,464** in 2018 (MVP was 0 after 2016). |
| Urban Institute IPEDS extracts | **Live** | Directory 2004–2024; finance through 2017 |
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
| IPEDS Academic Libraries (Urban endpoint 45, 2013–2023) | **Live** CSV `colleges_ipeds_academic_libraries.csv` | Watch-list enrichment only (`lib_*`). Not a training feature. |

| Pipeline step | v2 result |
| --- | --- |
| Urban ingest | Directory 2004–2024; **92,257** panel rows |
| Parent/child rollup | **3,028** child rows inherited parent totals |
| Labels h=3 | **3,703** positives / 50,315 complete *risk-universe* rows (same IPEDS event set as MVP; trackers added no unique matches) |
| Model | XGBoost test **PR-AUC 0.179** vs naive composite 0.052 / 5y-decline 0.123; recall@50 **0.090** vs 0.009 / 0.045. **Beats both baselines**. Honest note: PR-AUC is slightly below MVP 0.190 after adding 2017–18 composites + WICHE — not a claimed improvement in rank quality. |
| Watch list | Score year **2022** (`miss_finance` 4.8%). Extra columns: Scorecard HCM2/operating, accreditor/WARN/990 flags |

Exact URLs and status codes: [`outputs/fsa_ingest.md`](outputs/fsa_ingest.md).

## Outputs

Committed under `outputs/` so a clone can be read without re-downloading Urban.

| File | What it is | How to use it |
| --- | --- | --- |
| [`outputs/watchlist.csv`](outputs/watchlist.csv) | Ranked private nonprofit / for-profit rows for the score year (up to 500), including `lib_*` columns | Sort is already by `risk_score` descending. Not a closure list. |
| [`outputs/watchlist_nonprofit.csv`](outputs/watchlist_nonprofit.csv) | Same ranking restricted to `inst_control == 2` (up to 250) | Use when the question is nonprofit-only. |
| [`outputs/top50_report.html`](outputs/top50_report.html) | Evidence cards: FTE, discount, margins, composite, HCM/Scorecard, enrichment, libraries, SHAP drivers | Open in a browser. Read the yellow banner first. |
| [`outputs/libraries_top50.md`](outputs/libraries_top50.md) | Unique / unknown library notes for the top-50 + nonprofit shortlist | Cultural/asset context, not a model feature. |
| [`outputs/libraries_top50.csv`](outputs/libraries_top50.csv) | Same shortlist as a join table (`lib_*` columns) | Spreadsheet view of holdings + notes. |
| [`outputs/model_card.md`](outputs/model_card.md) | Task, data, split, PR-AUC / recall@K, SHAP, caveats | The narrative companion to the metrics JSON. |
| [`outputs/model_metrics.json`](outputs/model_metrics.json) | Machine-readable split metrics and year-level baseline comparison | Check `beats_naive` before claiming the model won. |
| [`outputs/nces_finance_years.md`](outputs/nces_finance_years.md) | Which NCES F-year zips parsed | Why 2023–24 are not ranked. |
| [`outputs/fsa_ingest.md`](outputs/fsa_ingest.md) / [`outputs/fsa_attempts.json`](outputs/fsa_attempts.json) | HTTP table: URL, status, bytes | Verified live vs still impossible. |
| [`outputs/qa_counts.md`](outputs/qa_counts.md) / [`outputs/qa_panel.md`](outputs/qa_panel.md) | Universe counts and missingness by year | Catch a broken ingest before you trust ranks. |

`data/raw/` and `data/processed/` are gitignored (regenerate with the scripts).

### Score-year rule

The watch list is scored on the latest **right-censored** year whose
`miss_finance` is not dominated by unpublished NCES files (threshold: mean
`miss_finance` &lt; 50%). In this build that year is **2022**. Directory years
2023–2024 exist, but `F2324` / `F2425` standalone zips still 404, so ranking
those years would treat publication lag as a risk signal.

Right-censor means: if the label horizon is 3 years and the last complete
directory year is 2024, then 2022–2024 rows cannot yet be confirmed *negative*
(a 2022 school could still close in 2024–25). Those rows are scored, not used
as training labels.

## College universe

From the Urban IPEDS directory (`inst_control` is the portal name for CONTROL):

- `degree_granting == 1`
- `inst_control` in `{1 public, 2 private nonprofit, 3 for-profit}`
- Title IV participating when `title_iv_indicator` is reported (`1, 2, 4, 8`);
  missing Title IV is kept
- Drop `sector == 0` and name patterns such as “system office”

Live Urban directory (fall 2004–2024), after filters: **5,886** unique UNITID,
**92,257** institution-years, **3,887** in 2024. Details: `outputs/qa_counts.md`.

The **risk-model universe** is private nonprofit + for-profit only. Publics
remain in the panel so you can see their features; they are not in
`watchlist.csv`.

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

## Libraries & book collections (enrichment)

Watch-list evidence cards include an IPEDS **Academic Libraries** block plus a
best-effort public-web note. This is **cultural / asset-value context** for
schools already on the elevated-risk list — not a closure verdict and **not a
model training feature**. No lagged `lib_*` columns are in
`MODEL_FEATURE_COLUMNS`.

**Holdings (all watch-list rows that appear in AL):** Urban Institute Education
Data Portal endpoint 45,
`/api/v1/college-university/ipeds/academic-libraries/{year}/`, years
**2013–2023**. Bulk CSV (preferred):
`https://educationdata.urban.org/csv/ipeds/colleges_ipeds_academic_libraries.csv`
(the hyphenated `academic-libraries` filename 404s). Join is UNITID × year; for
score year 2022 we take the latest AL year **≤ 2022** when one exists, otherwise
the latest available year, and record `lib_year`. Expenditure fields are only
published for libraries with total expenditures above $100,000 (Urban/IPEDS
rule). Sentinels `-1/-2/-3` become unknown — never filled with zeros that look
like an empty collection.

Mapped columns: `lib_physical_books`, `lib_digital_items` (Urban
`total_electronic_collections`, or a sum of electronic books/media/serials when
that total is absent), `lib_expenditures`, `lib_fte` (librarians), plus
`lib_staff_fte`, `lib_source`, `lib_arl_member`.

**Unique notes (top 50 + ~25 nonprofit):** `src/college_closure/libraries.py`
fetches the directory `url_school`, then library / special-collections /
archives paths. HTML is cached under `data/raw/libraries/` (gitignored). The
extractor keeps **named** collections, archives, rare-book areas, or digital
repositories. If a page only says “we have special collections” with no name,
`lib_unique_flag` stays false. If nothing usable is found, the note is
**unknown** — not “no library.” Holdings counts are never invented from prose.

ARL membership is matched against the public Association of Research Libraries
member list when that page downloads; otherwise a small built-in snapshot is
used. Small watch-list campuses are almost never ARL members.

Re-run: `python3 scripts/02_crosswalk.py` (downloads the AL CSV) then
`python3 scripts/07_report.py`. Use `--skip-scrape` to refresh counts only.

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
- Scorecard `operating=0` is an evidence flag, **not** a fabricated event year.

This v2 run: **3,703** h=3 positives among 50,315 complete risk-universe rows
(same IPEDS event set as MVP; trackers added no unique matches).

## Features

Training columns (`MODEL_FEATURE_COLUMNS` in `src/college_closure/features.py`):

Enrollment / size: `log_fte`, `fte_under_1000`, `enr_pct_chg_1y`,
`enr_pct_chg_5y`, `enr_pct_chg_10y`, `enr_decline_5y_gt30`, `ftft_pct_chg_1y`.

Admissions: `admit_rate`, `yield_rate`, `admit_rate_chg_5y`, `yield_rate_chg_5y`.

Finance: `tuition_dependence`, `discount_rate`, `discount_rate_chg_5y`,
`operating_margin`, `operating_margin_chg_5y`, `consec_neg_margin_yrs`,
`endowment_per_fte`, `unrestricted_na_to_exp`, `high_tuition_dependence`,
`miss_finance`, `finance_from_parent`.

Staff: `staff_pct_chg_1y`, `staff_pct_chg_5y`, `student_staff_ratio`,
`student_staff_ratio_chg_1y`.

FSA composite (lagged): `composite_score`, `composite_fail`, `composite_zone`,
`years_in_zone`, `miss_composite`, `composite_is_lagged`.

Structure / demography: `is_four_year`, `religious`, `urban`, `rural`,
`inst_control`, `sector`, `hs_grad_pct_chg_5y`.

Percent changes use only *past* values at that institution. A 2013 1-year FTE
change uses 2012→2013, never 2014.

## Model

- Unit of analysis: institution-year (`unitid` × `year`).
- Outcome: `closed_or_merged_within_3_years` (h=2 is also built).
- Train on `in_risk_model_universe` rows with complete h=3 labels.
- Default split (**no shuffle**): train ≤2016, val 2017–2019, test 2020–2021.
- Models: L2 logistic regression + XGBoost. The published rank is XGBoost
  `risk_score`.
- Naive baselines: (a) last-known composite &lt; 1.0; (b) 5-year FTE decline &gt; 30%.
- HCM / Scorecard HCM2 / operating / accreditor / WARN / 990 are **not**
  training features.

Held-out **test** (n=4,799 institution-years, 223 positives):

| Model | PR-AUC | ROC-AUC | Recall@25 | Recall@50 | Recall@100 |
| --- | --- | --- | --- | --- | --- |
| XGBoost | **0.179** | 0.748 | 0.049 | **0.090** | 0.148 |
| Logistic | 0.114 | 0.778 | 0.009 | 0.013 | 0.013 |
| Naive: composite &lt; 1.0 | 0.052 | 0.529 | 0.000 | 0.009 | 0.054 |
| Naive: 5y FTE decline &gt; 30% | 0.123 | 0.737 | 0.009 | 0.045 | 0.090 |

XGBoost **beats both naive baselines** on the pooled test set and on each test
year (2020 and 2021). That is a screening-quality check, not evidence the watch
list is a reliable forecast for any named school.

Honest comparison to MVP: test PR-AUC **0.179** / recall@50 **0.090** vs MVP
0.190 / 0.099 after attaching official 2017–18 composites and WICHE. Documented,
not hidden, not claimed as better ranks.

Split sizes: train 37,855 (2,876 positives); val 7,661; test 4,799.

Top global SHAP drivers in this run:

| Feature | mean \|SHAP\| |
| --- | --- |
| `unrestricted_na_to_exp` | 0.883 |
| `composite_score` | 0.516 |
| `log_fte` | 0.428 |
| `endowment_per_fte` | 0.412 |
| `operating_margin` | 0.267 |
| `yield_rate` | 0.258 |
| `tuition_dependence` | 0.238 |
| `enr_pct_chg_1y` | 0.217 |
| `hs_grad_pct_chg_5y` | 0.178 |
| `admit_rate` | 0.160 |

Full tables: [`outputs/model_card.md`](outputs/model_card.md),
[`outputs/model_metrics.json`](outputs/model_metrics.json).

## How to read a watch-list row

`risk_score` is a model output on the score-year (2022) slice. Higher means
“looks more like historical positives on trailing features.” It is not a
probability you should quote as “X% chance of closure.”

On an evidence card, read in this order:

1. The banner (*not a verdict*).
2. FTE level and 1y/5y change, discount rate, operating margin, composite.
3. `miss_finance` — if finance is missing because NCES has not published that
   year, ignore the rank (the score-year rule is meant to prevent that).
4. HCM / Scorecard investigation and operating flags — **current snapshots**.
5. Enrichment (accreditor page mention, WARN name match, 990 EIN). These never
   change the score.
6. Libraries & collections — IPEDS holdings if reported, plus any named
   special-collection note. Missing ≠ no library; not a model feature.
7. SHAP drivers — which features pushed *this* row.

A school can rank high because it is small, tuition-dependent, and already in
the composite zone — the same pattern as many historical closures — and still
remain open for years. False positives are expected.

## Tests

```bash
PYTHONPATH=src python3 -m pytest tests -q
```

This revision: **36 passed** plus Academic Libraries join/HTML-extraction tests.

Covers universe filters, OPEID 6/8 (never pad a 6-digit root to 8 with leading
zeros), official composite attach without dropping missing UNITID, trailing-
window (no-leak) features, parent/child rollup, label horizon / right-censor /
merger toggle / sentinel CLOSEDAT, Scorecard API mapping (mocked HTTP, no live
key), HCM2 mapping, WICHE join, extra-closure unique-match rule, recall@K,
no HCM/Scorecard/enrichment/`lib_*` columns in `MODEL_FEATURE_COLUMNS`,
IPEDS Academic Libraries join/sentinels, and mocked HTML note extraction.

## Configure

`config.yaml` knobs:

| Key | Meaning |
| --- | --- |
| `years.start` / `years.end` | IPEDS fall-year window (`end: null` = latest Urban year) |
| `label_horizons` | Default `[2, 3]` |
| `labels.mergers_are_positive` | Default `true` |
| `labels.use_disappearance` | Default `false` |
| `model.train_end` / `val_years` / `test_years` | Temporal split |
| `nces.year_start` / `year_end` | Which F-year zips to try (including unpublished) |
| `fsa.*_urls` | Official workbook URLs (tried in order) |
| `scorecard.api_base` / `api_key_env` / `bulk_urls` | API vs ZIP |
| `wiche.path` / `wiche.url` | Knocking workbook |
| `closure_trackers.curated_csv` | Optional cited closure list |

FSA pages move; ingest tries several URLs and **continues** on failure.

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
| Docs | Short MVP README | This onboarding README |
| Model | Test PR-AUC 0.190 / recall@50 0.099 | Test PR-AUC **0.179** / recall@50 **0.090** — still beats naive; not claimed as better ranks |

## Caveats / ethics

- **IPEDS lag.** Recent finance and composite scores may be missing.
  Missingness is a feature, not filled with zeros that look like health.
- **Publics almost never close.** A high public score (if you compute one) is
  usually a category error — different process than a private shutdown.
- **False positives are expected.** Precision at 50 on the test set is low in
  absolute terms (recall@50 = 0.090). A high rank is an invitation to read the
  evidence card, not a journalistic claim.
- **Reputational harm is real.** Naming a college as “at risk of closure” can
  itself accelerate enrollment loss. Keep language as **elevated-risk
  indicators**. Do not publish ranks as predicted closures.
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
- IPEDS Academic Libraries cells are often missing for small / for-profit
  campuses; missing ≠ no library. Scraped special-collection notes are
  best-effort and may be stale after a closure. Holdings counts are never invented.
- For-profit chain collapses and public “closures” are different processes.

## Roadmap (remaining data gaps)

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

- Do not invent enrollment, finance, closure dates, library holdings, or rare-book claims.
- Do not invent institutions or metrics.
- Do not commit `data/raw/` or processed Parquet (see `.gitignore`).
- Do not commit API keys.
- Cite Urban + IPEDS: [Education Data Portal](https://educationdata.urban.org/documentation/),
  Urban Institute; NCES IPEDS complete data files; FSA Data Center / data.ed.gov
  when those files are used; College Scorecard; WICHE Knocking at the College Door;
  Kelchen, Ritter & Webber (Philadelphia Fed WP 24-20).
