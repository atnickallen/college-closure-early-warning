# Current-status refresh

Run date: 2026-10-05
Watch-list rows: 93
Still-operating schools in the main list: 50
Ranked rows walked to fill that list: 93
Curated rows with a disagreement flag: 4
Curated campus-sold rows: 7
Curated campus-listed rows: 0

## Sources this run

- Scorecard: Scorecard skipped: DATA_GOV_API_KEY / SCORECARD_API_KEY is unset, and data/processed/scorecard_operating.parquet is not present.
- FSA closed-school list: FSA closed-school file not downloaded. Tried the Partner Connect page and the configured ClosedSchoolSearchFile URLs; none returned a spreadsheet.
- IPEDS directory: IPEDS directory via Urban API, years 2025–2021 newest first: 100 of 100 UNITIDs returned a row.

Campus sales and listings are curated only. College Scorecard, the FSA closed-school list, and IPEDS do not report real-estate sales or listings.

Appended 34 still-operating row(s) to `data/status/status_curated.csv`. Existing curated rows were not modified.
Disagreement text is a flag. It does not replace the curated status, buyer, date, or price.
