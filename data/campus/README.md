# Campus land file

`campus_land.csv` is hand-maintained. The status checker reads it and does not
overwrite it. A school needs `own_campus` = `yes` plus IPEDS on-campus housing
to enter the residential top list.

| Column | Meaning |
| --- | --- |
| `unitid` | IPEDS UNITID |
| `acreage` | Acres stated by `source_url` for this campus. Blank when the source shows buildings and grounds but does not give a number. |
| `own_campus` | `yes`, `no`, or `unknown` |
| `source_url` | Page that supports the land decision |
| `checked_at` | Date the source was read (YYYY-MM-DD) |
| `image_url` | Hotlinked thumbnail, usually a 400px Wikimedia Commons file. Blank when no campus photo was found. |
| `image_credit_url` | Commons file page or other credit link |
| `image_license` | Short license name from Commons |
| `image_author` | Photographer or rights holder, when Commons states one |
| `notes` | Uncertainty, shared grounds, or which campus the acreage belongs to |

`housing_latest.csv` is the latest IPEDS Institutional Characteristics year, for
each watch-list UNITID, in which `oncampus_housing` is 0 or 1. It is not the
bulk IC extract. Sentinel codes -1, -2, and -3 are not stored as the latest
reported year. The status checker uses this snapshot when the network is
skipped and when the weekly job does not need to re-download the bulk file.

Photos are hotlinked. Seals, wordmarks, and logos are not used as campus photos.
The report shows "No photo found" when `image_url` is blank.
