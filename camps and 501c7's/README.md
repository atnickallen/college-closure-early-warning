# Camps, campuses, and 501(c)(7) clubs for sale

This folder is a standalone search for U.S. properties that are listed for sale
and that have housing: dorms or residence halls, cabins, bunkhouses, or a lodge
with beds. It does not import the college-closure package.

Three categories are kept:

- `college` — a campus or former campus
- `camp` — a summer camp, retreat, or camp-style lodge property
- `501c7` — a social club (country club, hunting or fishing club, yacht club, lodge) with overnight lodging

A row is published only when the source states that housing. The evidence
sentence is stored on the row. Prices, acreage, and bed counts are copied from
the page. A blank means the page did not state the number.

## Run

```bash
python3 "camps and 501c7's/scripts/run_listings.py"
python3 "camps and 501c7's/scripts/run_listings.py" --skip-network
```

`--skip-network` republishes `data/curated_listings.csv` and does not fetch.
A normal run merges that seed with the sources in `config.yaml`, tags a
501(c)(7) EIN only when the name and city match the IRS EO BMF subsection 07
extract, looks up maps, and geocodes rows that have no coordinates.

Outputs:

- `outputs/listings.csv`
- `outputs/listings.json`
- `outputs/index.html` — category tabs, state filter, price, acreage, beds, photo, map links, satellite link, last-checked date
- `outputs/fetch_log.md` — blocked hosts and empty pages

## Maps

`src/camp_listings/maps.py` looks up a campus map, site map, plat, or offering
memorandum for each property.

When `FIRECRAWL_API_KEY` is set it POSTs to
`https://api.firecrawl.dev/v2/search` and `https://api.firecrawl.dev/v2/map`.
The key is not written to the log. Without the key, the same queries go to
DuckDuckGo Lite (its robots.txt allows `/`) and the listing page is crawled
for PDF and “map” links.

The weekly job is `.github/workflows/camps-501c7-refresh.yml`. The schedule
and `workflow_dispatch` both run the listing finder and the top-50 campus map
finder. Each step receives `FIRECRAWL_API_KEY` from the repository secret.
The workflow does not print the secret. It pushes `camps-501c7-refresh`
(listing outputs, `data/campus/campus_land.csv`, and `outputs/top50_report.html`)
because Actions cannot always open a pull request.

The same finder fills campus maps for the 50 schools on the main watch-list
cards:

```bash
python3 "camps and 501c7's/scripts/apply_campus_maps.py"
```

It writes `campus_map_url` in `data/campus/campus_land.csv` and adds a Campus
map link on each card that has one. When the Firecrawl key is set, every
school is searched again. A school keeps its stored map when that search
returns nothing.

## Sources

Configured probes include LoopNet, Crexi, LandWatch, Lands of America, Ten-X,
the American Camp Association classifieds, Tranzon, Bid4Assets, and the
Christian Camp and Conference Association site. A 401, 403, 429, 503, or a
challenge page is logged and skipped. Summer Camp Hub is parsed when the HTML
is readable. Google News RSS headlines are logged as leads and are not copied
into the listing file.

The IRS Exempt Organizations Business Master File region files
(`eo1.csv` through `eo4.csv`) are streamed at run time and filtered to
subsection 07. The compact cache lives in `data/cache/` and is not committed.

## Tests

```bash
python3 -m pytest "camps and 501c7's/tests" -q
```
