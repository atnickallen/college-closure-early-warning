# FSA accountability ingest (v2)

Tried Urban FSA CSV, **data.ed.gov official year workbooks**, current FSA Data Center /
Partner Connect URLs, Wayback CDX (best-effort), and College Scorecard (API or bulk ZIP).
Missing files are skipped; they are **not** invented.

## Row counts this run

- **composite_urban**: 37,589 rows years 2006–2016
- **composite_official**: 40,969 rows years 2007–2018
- **composite**: 74,122 rows years 2006–2018
- **hcm**: not available this run
- **closed_school**: not available this run
- **scorecard**: 6,273 rows

## HTTP attempts (verified live vs still impossible)

| Status | OK | Bytes | Source | URL | Note |
| --- | --- | --- | --- | --- | --- |
| cache | yes | 1,210,575 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F1819_F1A.zip` | cached F1819_F1A.zip |
| cache | yes | 1,013,120 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F1819_F2.zip` | cached F1819_F2.zip |
| cache | yes | 466,858 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F1819_F3.zip` | cached F1819_F3.zip |
| cache | yes | 1,421,820 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F1920_F1A.zip` | cached F1920_F1A.zip |
| cache | yes | 1,144,147 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F1920_F2.zip` | cached F1920_F2.zip |
| cache | yes | 497,138 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F1920_F3.zip` | cached F1920_F3.zip |
| cache | yes | 1,420,852 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2021_F1A.zip` | cached F2021_F1A.zip |
| cache | yes | 1,147,312 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2021_F2.zip` | cached F2021_F2.zip |
| cache | yes | 479,497 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2021_F3.zip` | cached F2021_F3.zip |
| cache | yes | 1,431,839 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2122_F1A.zip` | cached F2122_F1A.zip |
| cache | yes | 1,139,868 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2122_F2.zip` | cached F2122_F2.zip |
| cache | yes | 466,096 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2122_F3.zip` | cached F2122_F3.zip |
| cache | yes | 711,679 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2223_F1A.zip` | cached F2223_F1A.zip |
| cache | yes | 560,124 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2223_F2.zip` | cached F2223_F2.zip |
| cache | yes | 228,105 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2223_F3.zip` | cached F2223_F3.zip |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F1A.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F1A_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F1A_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F1A_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F1A_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F2.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F2_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F2_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F2_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F2_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F3.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F3_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F3_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F3_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2324_F3_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F1A.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F1A_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F1A_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F1A_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F1A_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F2.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F2_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F2_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F2_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F2_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F3.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F3_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F3_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F3_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2425_F3_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F1A.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F1A_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F1A_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F1A_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F1A_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F2.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F2_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F2_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F2_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F2_rev.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F3.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F3_Data_Stata.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F3_P.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F3_RV.zip` |  |
| 404 | no | 0 | nces | `https://nces.ed.gov/ipeds/datacenter/data/F2526_F3_rev.zip` |  |
| cache | yes | 810,496 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/8f7ea82b-0f47-4a3d-a999-a2a0377bb3d9/download/ay17-18-composite-scores.xls` | cached ay17-18-composite-scores.xls |
| cache | yes | 1,040,384 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/54455fd6-0c25-40ab-8b2a-d95e343eeff7/download/ay16-17-composite-scores.xls` | cached ay16-17-composite-scores.xls |
| cache | yes | 857,600 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/9ac2022e-1033-4907-837a-e1b5c6fbf0c6/download/20152016compositescores.xls` | cached 20152016compositescores.xls |
| cache | yes | 673,792 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/c04c1fea-f4ad-4881-b8d1-c76ac1f45793/download/20142015compositescores.xls` | cached 20142015compositescores.xls |
| cache | yes | 683,520 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/24d7de6a-f3b3-4c33-8536-dd302a3d0d49/download/20132014compositescores.xls` | cached 20132014compositescores.xls |
| cache | yes | 678,912 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/a05ecde2-d0c1-48ee-8f02-9c34ca4b10f1/download/1213compositescores.xls` | cached 1213compositescores.xls |
| cache | yes | 677,888 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/020e80ac-c04a-4e93-867e-935e1320c043/download/1112compositescores.xls` | cached 1112compositescores.xls |
| cache | yes | 687,616 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/60dfc9bb-a0b5-4f1d-bbaf-0b0439047e12/download/1011compositescores.xls` | cached 1011compositescores.xls |
| cache | yes | 684,544 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/a0022964-8b7f-4e3d-92ed-e7ac8636173d/download/0910compositescores.xls` | cached 0910compositescores.xls |
| cache | yes | 676,352 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/4f949bd9-76ad-439c-960c-b610e6653f9f/download/0809compositescores.xls` | cached 0809compositescores.xls |
| cache | yes | 611,328 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/e66c0255-d77a-4059-98bc-e62ae972a976/download/0708compositescores.xls` | cached 0708compositescores.xls |
| cache | yes | 611,840 | data.ed.gov_composite | `https://data.ed.gov/dataset/ff51fef3-9d22-49a7-b34b-54329a290307/resource/329f11b4-06ac-4a7d-82c1-156c63435453/download/0607compositescores.xls` | cached 0607compositescores.xls |
| 404 | no | 0 | fsa_composite_workbook | `https://studentaid.gov/sites/default/files/fsawg/datacenter/library/CompositeScores.xlsx` |  |
| 404 | no | 0 | fsa_composite_workbook | `https://studentaid.gov/sites/default/files/CompositeScores.xlsx` |  |
| 404 | no | 0 | fsa_composite_workbook | `https://studentaid.gov/sites/default/files/financial-responsibility-composite-scores.xlsx` |  |
| 404 | no | 0 | hcm | `https://studentaid.gov/sites/default/files/fsawg/datacenter/library/hcm.xlsx` |  |
| 404 | no | 0 | hcm | `https://studentaid.gov/sites/g/files/dbyssus161/files/media/data/hcm.xlsx` |  |
| 404 | no | 0 | hcm | `https://studentaid.gov/sites/default/files/hcm.xlsx` |  |
| 404 | no | 0 | hcm | `https://www2.ed.gov/offices/OSFAP/PEPS/hcm.xlsx` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2026-09/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2026-08/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2026-01/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2025-12/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2025-09/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2025-01/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2024-12/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://fsapartners.ed.gov/sites/default/files/2024-01/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://studentaid.gov/sites/default/files/fsawg/datacenter/library/ClosedSchoolSearchFile.xls` |  |
| 404 | no | 0 | closed_school | `https://www2.ed.gov/offices/OSFAP/PEPS/docs/closedschoolsearchfile.xls` |  |
| cache | yes | 23,559,465 | scorecard_bulk | `https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Institution_06102026.zip` | cached Most-Recent-Cohorts-Institution_06102026.zip |

## Join rules

- OPEID: 6-digit FSA roots are **not** left-padded to 8 (that would shift the root).
  Six-digit values become `root + '00'` via `ids.normalize_opeid8`.
- Composites join UNITID×year first, then unambiguous OPEID6×year (main campus if shared).
- Official data.ed.gov files are preferred on overlap with Urban; Urban keeps 2006–2016 history.

HCM / Scorecard `UNDER_INVESTIGATION` are **current snapshots** and must not be used as
historical training features unless a lagged year-by-year series is present (it is not in this build).

College Scorecard API key absent; bulk ZIP path used when the official file downloaded.
