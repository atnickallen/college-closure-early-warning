# Current status (curated)

`status_curated.csv` is the record of what happened to each watch-list school
after the score year. Edit rows in place. Git history is the version history.
`scripts/check_status.py` does not overwrite existing rows. When a school
further down the ranked watch list enters the still-operating top 50 and is
not already in this file, the checker appends a row with `status=operating`,
the IPEDS directory URL (and the College Scorecard school page when
`school.operating` was 1), and `checked_at`. It does not invent a sale price.

## Columns

| Column | What to put |
| --- | --- |
| `unitid` | IPEDS UNITID. This is the join key to `outputs/watchlist.csv`. |
| `opeid6`, `opeid8` | Copied from the watch list so a row can be checked against FSA. |
| `watchlist_rank` | Rank when the row was added. The checker re-ranks from the current watch list. |
| `inst_name`, `state_abbr` | Keep these even when `unitid` is filled in. |
| `status` | `operating`, `not_enrolling`, `closed`, or `merged_acquired`. |
| `status_detail` | Short sourced description. |
| `property_disposition` | `not_applicable`, `no_sale_found`, `sold`, `listed`, or `institutional_sale`. |
| `buyer_or_broker` | Who bought, listed, or auctioned. Blank if unknown. |
| `event_date` | Date or season as published. Do not invent a day. |
| `sale_price_published` | Only a price that appears in the source. Otherwise blank. |
| `sold_listed_details` | What was sold or listed, or that no sale/listing was found. |
| `source_url` | One or more URLs, separated by `; `. |
| `checked_at` | ISO date of the manual check (`YYYY-MM-DD`). |
| `library_notes` | Optional collection note from the same review. Not used in the badge. |

## What the checker will not fill in

Campus sales, listings, buyers, dates, and prices are not in College Scorecard,
the FSA closed-school list, or IPEDS. Leave `sale_price_published` blank when
the source does not state a price. The automated refresh flags a row when a
federal operating flag disagrees with `status`. It does not replace these columns.

`institutional_sale` is an ownership change of a school that is still operating
(a stock sale). It is not a closed-campus real-estate sale. Use
`sold` only for the campus property. Use `merged_acquired` without
`institutional_sale` when a merger ends the UNITID as its own school. That
row is left off the still-operating list. Web checks of schools that entered
the open list from a lagging IPEDS row belong in `source_url` and `checked_at`;
edit those rows in place.
