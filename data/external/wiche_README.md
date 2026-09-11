# WICHE Knocking at the College Door

Pipeline writes `wiche_hs_graduates.csv` (`state_abbr`, `year`, `hs_graduates`)
from the official 11th-edition workbook when that file downloads:

https://www.wiche.edu/wp-content/uploads/2024/12/Knocking-at-the-College-Door-11th-Edition-Projections-Dataset-12-11-2024.xlsx

Landing page: https://www.wiche.edu/knocking/data/

If the workbook is blocked, this directory keeps the placeholder path and the
feature `hs_grad_pct_chg_5y` stays missing (not zero-filled).
