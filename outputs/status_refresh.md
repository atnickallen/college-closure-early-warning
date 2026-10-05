# Current-status refresh

Run date: 2026-10-05
Watch-list rows: 50
Curated rows with a disagreement flag: 5
Curated campus-sold rows: 7
Curated campus-listed rows: 0

## Sources this run

- Scorecard: Scorecard API school.operating for 20 UNITIDs.
- FSA closed-school list: FSA closed-school file not downloaded. Tried the Partner Connect page and the configured ClosedSchoolSearchFile URLs; none returned a spreadsheet.
- IPEDS directory: IPEDS directory via Urban API, years 2025–2021 newest first: 50 of 50 UNITIDs returned a row.

Campus sales and listings are curated only. College Scorecard, the FSA closed-school list, and IPEDS do not report real-estate sales or listings.

The curated file `data/status/status_curated.csv` was not modified.
Disagreement text is a flag. It does not replace the curated status, buyer, date, or price.
