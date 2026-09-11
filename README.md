# College closure early-warning pipeline

Reproducible Python pipeline that ranks U.S. **degree-granting** colleges (not trade / cosmetology / certificate-only schools) by the probability of **closure or merger within 2–3 years**. This repository is **Milestones 1–2**: Urban Institute IPEDS ingest, a filtered college universe, and a UNITID×year panel. Modeling, labels, and the public watch list come later.

Methodological blueprint: Kelchen, Ritter & Webber, [*Predicting College Closures and Financial Distress*](https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2024/wp24-20.pdf) (Philadelphia Fed WP 24-20 / FEDS 2025-3). Features in later phases follow their findings: enrollment trajectory, tuition dependence, liquidity/leverage, operating margins, staffing contraction, and prior distress flags (FSA composite scores / HCM). **Public institutions almost never close**; they stay in the panel for context, but risk models train on private nonprofit and for-profit rows only.

This is a **watch list, not a verdict.** Predicted risk is not a determination that a college will close.

## What works today (Milestones 1–2)

| Script | Status | Role |
| --- | --- | --- |
| `scripts/01_ingest.py` | **Implemented** | Download/cache Urban IPEDS extracts; filter to colleges; write Parquet + `outputs/qa_counts.md` |
| `scripts/03_panel.py` | **Implemented** | One row per UNITID×year; left-join enrollment (+ finance / admissions / staffing); `data/processed/panel.parquet` + `outputs/qa_panel.md` |
| `scripts/02_crosswalk.py` | Stub | UNITID ↔ OPEID ↔ EIN (Phase 2) |
| `scripts/04_features.py` | Stub | Fed-blueprint features |
| `scripts/05_labels.py` | Stub | `closed_or_merged_within_h_years` from IPEDS + FSA Closed School |
| `scripts/06_model.py` | Stub | Logistic baseline + XGBoost, temporal validation, recall@K |
| `scripts/07_report.py` | Stub | Ranked watch list + top-50 evidence cards |

Every institution is keyed on **UNITID**. The IPEDS directory also carries **opeid** and **ein** for the Phase 2 crosswalk to FSA and Form 990 / NCCS.

## College universe

From the Urban IPEDS directory (`inst_control` is the portal name for IPEDS CONTROL):

- `degree_granting == 1`
- `inst_control` / `control` in `{1 public, 2 private nonprofit, 3 for-profit}`
- Title IV participating when `title_iv_indicator` is reported (`1, 2, 4, 8`); missing Title IV is kept
- Drop `sector == 0` (administrative / system offices)
- Drop non-degree institutional categories and name patterns such as “System Office”

Live ingest (Urban IPEDS directory, fall 2004–2024), after the filters above:

| | |
| --- | --- |
| Unique UNITID over the panel | **5,886** (~6,000 with for-profit entry/exit) |
| Institution-years | **92,257** |
| Peak year (2013) | **4,876** |
| Latest year (2024) | **3,887** |
| Private nonprofit 4-year | **1,542** (2024) to **1,651** (2015) |

Certificate-only / less-than-2-year trade schools are out. Single-year totals are below 6,000 because that figure is the **longitudinal** Title IV college count, not the 2024 cross-section. Full sector×year tables: [`outputs/qa_counts.md`](outputs/qa_counts.md).

## Install

Python 3.11+ (developed on 3.12).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`scripts/*.py` add `src/` to `sys.path`; you do not have to `pip install -e .`.

## Configure

Edit `config.yaml`:

- `years.start` / `years.end` — default **2004 → latest** advertised on the Urban [`api-endpoints`](https://educationdata.urban.org/api/v1/api-endpoints/) metadata (directory is currently through **2024**)
- `label_horizon_years: 3` — used later for labels
- `filters` — degree-granting, control, Title IV, system-office drop rules
- `urban.api_base` / `urban.csv_base` — Education Data Portal

## Run Milestone 1

```bash
python scripts/01_ingest.py --milestone1-only
```

This downloads the all-years directory CSV and fall-enrollment **totals** (Urban JSON API with `race=sex=ftpt=degree_seeking=class_level=99` for undergraduate / graduate / first-professional). Raw files cache under `data/raw/` (gitignored). Processed Parquet lands in `data/processed/`:

- `directory_raw.parquet` — unfiltered IPEDS directory in the year window
- `directory.parquet` — filtered college universe
- `fall_enrollment.parquet` — UNITID×year fall headcount (UG / graduate / total)

QA: [`outputs/qa_counts.md`](outputs/qa_counts.md) (committed; regenerate locally after ingest).

Re-runs use the on-disk cache. Delete `data/raw/ipeds/...` to force a re-download.

## Run Milestone 2

```bash
python scripts/01_ingest.py          # directory + enrollment + finance + admissions + staffing
python scripts/03_panel.py
```

Additional extracts (skipped with `--milestone1-only`):

| Source | Urban endpoint | How we pull it |
| --- | --- | --- |
| Finance | `ipeds/finance` | Bulk CSV `colleges_ipeds_finance.csv` |
| Admissions | `ipeds/admissions-enrollment` | Bulk CSV; keep `sex==99` totals |
| Instructional staff | `ipeds/salaries-instructional-staff` | API totals (`academic_rank=sex=contract_length=99`) |
| Noninstructional staff | `ipeds/salaries-noninstructional-staff` | API totals (`staff_category=99`) |
| FTE enrollment | `ipeds/enrollment-full-time-equivalent` | Bulk CSV `colleges_ipeds_enrollment-fte.csv` |

`scripts/03_panel.py` left-joins these onto the filtered directory and writes `data/processed/panel.parquet` (92,257 × 77) plus [`outputs/qa_panel.md`](outputs/qa_panel.md). Fall enrollment is ~99.8% complete; finance is populated through 2017 (~6% missing in 2016, 100% missing afterward — Urban gap); admissions is missing for open-admission schools (~50%); staffing is ~4–5% missing.

Subset ingest:

```bash
python scripts/01_ingest.py --sources directory,fall_enrollment,finance
```

## Why some pulls use the API instead of CSV

Verified against [Urban college docs](https://educationdata.urban.org/documentation/colleges.html) and [`api-downloads`](https://educationdata.urban.org/api/v1/api-downloads/):

- Directory CSV is ~110MB for **all years** — faster than paging ~20 API years.
- Yearly `colleges_ipeds_fall-enrollment-race_{year}.csv` files are ~110MB **each** because they include every race × sex × FT/PT × class-level cell. Filtered API totals are one page per year×level.
- Instructional-staff CSV is ~400MB of rank/sex/contract cells; the totals API is a few thousand rows per year.
- If a year or file is missing, ingest **logs the URL and continues**.

Known portal gap: Urban IPEDS **finance currently ends in 2017** (`api-endpoints` id 91). Later years will need a NCES IPEDS Finance backfill before modeling.

## Later phases (stubs only)

Documented in the script headers; **not implemented** in this launch.

1. **02_crosswalk** — UNITID↔OPEID↔EIN, FSA / Scorecard keys, parent/child campuses.
2. **04_features** — enrollment path, tuition dependence, margins, liquidity/leverage, staffing contraction, prior FSA flags (WP 24-20 covariate list).
3. **05_labels** — `closed_or_merged_within_h_years` from IPEDS `inst_status` / `date_closed` / `newid` plus the FSA Closed School file.
4. **06_model** — logistic baseline + XGBoost; temporal validation; recall@K vs federal composite scores.
5. **07_report** — ranked watch list and top-50 evidence cards, with the watch-list-not-verdict caveat.

## Tests

```bash
PYTHONPATH=src pytest tests -q
```

Filter tests use synthetic rows only — they do not call the network.

## Data policy

- Do not invent enrollment, finance, or closure dates.
- Do not commit `data/raw/` or processed Parquet (see `.gitignore`).
- Cite Urban + IPEDS when publishing: IPEDS via [Education Data Portal](https://educationdata.urban.org/documentation/), Urban Institute.

## Layout

```
config.yaml
requirements.txt
scripts/01_ingest.py … 07_report.py
src/college_closure/     # client, filters, ingest, panel, QA
data/raw/                # cached Urban CSVs / API extracts (gitignored)
data/processed/          # Parquet (gitignored)
outputs/                 # qa_counts.md, qa_panel.md
tests/
```
