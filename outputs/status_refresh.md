# Current-status refresh

Run date: 2026-10-06
Watch-list rows: 616
Residential own-campus schools in the main list: 50
The main list keeps schools that are still operating, have on-campus dorms, and have their own campus. Scores remain 2022 federal financial data.
Ranked rows walked to fill that list: 616
Curated rows with a disagreement flag: 14
Curated campus-sold rows: 9
Curated campus-listed rows: 0

## Sources this run

- Scorecard: Scorecard API skipped (no API key). Used local scorecard_operating.parquet (6273 rows).
- FSA closed-school list: FSA closed-school file not downloaded. Tried the Partner Connect page and the configured ClosedSchoolSearchFile URLs; none returned a spreadsheet.
- IPEDS directory: IPEDS directory via Urban API, years 2025–2021 newest first: 625 of 625 UNITIDs returned a row.

Campus sales and listings are curated only. College Scorecard, the FSA closed-school list, and IPEDS do not report real-estate sales or listings.

Appended 12 residential own-campus row(s) to `data/status/status_curated.csv`. Existing curated rows were not modified.
Disagreement text is a flag. It does not replace the curated status, buyer, date, or price.
