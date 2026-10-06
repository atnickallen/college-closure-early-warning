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
| `image_url` | Hotlinked thumbnail. Commons files use a 400px `Special:FilePath` URL. A school-site image is used when Commons has no photo of this campus. Blank when no campus photo was found. |
| `image_credit_url` | Commons file page, or the school page the image came from |
| `image_license` | Short license name from Commons, or a note that the image is from the institution website |
| `image_author` | Photographer or rights holder, when the source states one |
| `notes` | Uncertainty, shared grounds, or which campus the acreage belongs to |
| `lat` | Campus latitude. IPEDS HD `LATITUDE` unless `coord_source` says the pin was moved. |
| `lon` | Campus longitude. IPEDS HD `LONGITUD` unless `coord_source` says the pin was moved. |
| `coord_source` | Where the pin came from. IPEDS points that sit on an admin office or a former campus are adjusted onto the campus. |

`housing_latest.csv` is the latest IPEDS Institutional Characteristics year, for
each watch-list UNITID, in which `oncampus_housing` is 0 or 1. It is not the
bulk IC extract. Sentinel codes -1, -2, and -3 are not stored as the latest
reported year. The status checker uses this snapshot when the network is
skipped and when the weekly job does not need to re-download the bulk file.

Photos are hotlinked. Seals, wordmarks, and logos are not used as campus photos.
The report shows "No photo found" when `image_url` is blank.

When `lat` and `lon` are filled, the report links "Satellite view" to a Google
Maps satellite image centered on that point (zoom 17). The same link is shown
on the closed and excluded tables when those schools have coordinates.
