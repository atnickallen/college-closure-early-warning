"""IRS Exempt Organizations Business Master File, subsection 07 only.

The four regional CSVs are public. This module streams them, keeps subsection
code 7, and writes a compact cache. The raw files are not stored in git.
"""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path

from camp_listings.http import Client

REGION_URLS = (
    "https://www.irs.gov/pub/irs-soi/eo1.csv",
    "https://www.irs.gov/pub/irs-soi/eo2.csv",
    "https://www.irs.gov/pub/irs-soi/eo3.csv",
    "https://www.irs.gov/pub/irs-soi/eo4.csv",
)

_STOP = {
    "the", "and", "of", "inc", "llc", "co", "company", "club", "association",
    "assn", "a", "for", "at", "in", "on",
}


def _norm(text: str) -> str:
    text = (text or "").upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _tokens(text: str) -> set[str]:
    return {token for token in _norm(text).lower().split() if len(token) > 2 and token not in _STOP}


def is_subsection_07(value: str) -> bool:
    text = (value or "").strip()
    if not text or not text.isdigit():
        return False
    return int(text) == 7


def filter_bmf_text(text: str) -> list[dict[str, str]]:
    """Keep EIN, name, city, and state for subsection 07 rows."""
    sample = text.lstrip("\ufeff")
    reader = csv.DictReader(io.StringIO(sample))
    if not reader.fieldnames:
        return []
    fields = {name.upper(): name for name in reader.fieldnames}
    needed = ("EIN", "NAME", "CITY", "STATE", "SUBSECTION")
    if any(key not in fields for key in needed):
        return []
    kept: list[dict[str, str]] = []
    for row in reader:
        if not is_subsection_07(row.get(fields["SUBSECTION"], "")):
            continue
        kept.append(
            {
                "ein": (row.get(fields["EIN"]) or "").strip(),
                "name": (row.get(fields["NAME"]) or "").strip(),
                "city": (row.get(fields["CITY"]) or "").strip(),
                "state": (row.get(fields["STATE"]) or "").strip().upper(),
            }
        )
    return kept


def load_or_download(cache_path: Path, client: Client, log: list[str]) -> list[dict[str, str]]:
    if cache_path.exists() and cache_path.stat().st_size > 0:
        with cache_path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    rows: list[dict[str, str]] = []
    for url in REGION_URLS:
        result = client.fetch(url)
        if result.blocked or result.status != 200 or "EIN" not in result.body[:500]:
            log.append(f"EO BMF {url} skipped: {result.reason or 'unexpected body'}")
            continue
        part = filter_bmf_text(result.body)
        log.append(f"EO BMF {url}: {len(part)} subsection 07 rows")
        rows.extend(part)
    if rows:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["ein", "name", "city", "state"])
            writer.writeheader()
            writer.writerows(rows)
    return rows


def match_club(rows: list[dict[str, str]], name: str, city: str, state: str) -> dict[str, str] | None:
    """Match a listing to one 501(c)(7) row. Ambiguous hits stay unmatched."""
    state_code = (state or "").strip().upper()
    if len(state_code) != 2:
        return None
    want = _tokens(name)
    if len(want) < 2:
        return None
    city_norm = _norm(city)
    hits: list[dict[str, str]] = []
    for row in rows:
        if (row.get("state") or "").upper() != state_code:
            continue
        have = _tokens(row.get("name", ""))
        if not want <= have:
            continue
        row_city = _norm(row.get("city", ""))
        if city_norm and row_city and city_norm != row_city:
            continue
        hits.append(row)
    if len(hits) == 1:
        return hits[0]
    return None
