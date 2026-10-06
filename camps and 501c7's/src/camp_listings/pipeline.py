"""Merge the curated seed, live fetches, IRS tags, and map links."""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from urllib.parse import urlencode

import yaml

from camp_listings.dedupe import dedupe
from camp_listings.eo_bmf import load_or_download, match_club
from camp_listings.housing import housing_snippet
from camp_listings.http import Client
from camp_listings.maps import find_maps
from camp_listings.report import satellite_maps_url, write_outputs
from camp_listings.schema import COLUMNS, as_row
from camp_listings.sources import run_source

ROOT_MARKERS = ("config.yaml", "data", "src")


def feature_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "config.yaml").exists() and (candidate / "src" / "camp_listings").exists():
            return candidate
    raise FileNotFoundError("camps feature root not found")


def load_curated(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        rows = []
        for raw in csv.DictReader(handle):
            row = as_row(raw)
            row["origin"] = row.get("origin") or "curated"
            rows.append(row)
        return rows


def _geocode(client: Client, row: dict) -> str:
    if (row.get("lat") or "").strip() and (row.get("lon") or "").strip():
        return ""
    query = ", ".join(part for part in (row.get("address"), row.get("city"), row.get("state"), "USA") if part)
    if not query.strip(", "):
        return ""
    url = "https://nominatim.openstreetmap.org/search?" + urlencode({"q": query, "format": "json", "limit": "1"})
    if not client.robots_allowed(url):
        return "robots"
    result = client.fetch(url)
    time.sleep(1.1)
    if result.blocked or result.status != 200:
        return result.reason or "failed"
    try:
        payload = json.loads(result.body)
    except json.JSONDecodeError:
        return "invalid json"
    if not payload:
        return ""
    row["lat"] = str(payload[0].get("lat") or "")
    row["lon"] = str(payload[0].get("lon") or "")
    return ""


def _apply_maps(client: Client, row: dict, log: list[str]) -> None:
    found = find_maps(
        row.get("name", ""),
        client=client,
        listing_url=row.get("source_url", ""),
        search_queries=None,
    )
    for note in found.notes:
        if "failed" in note.lower() or "skipped" in note.lower():
            log.append(f"maps {row.get('listing_id') or row.get('name')}: {note}")
            break
    if found.image_url and not row.get("image_url"):
        row["image_url"] = found.image_url
        row["image_credit"] = row.get("image_credit") or row.get("source_name") or "Listing page"
    if not found.hits:
        return
    primary = found.hits[0]
    row["map_urls"] = "|".join(hit.url for hit in found.hits)
    row["map_type"] = primary.map_type
    row["map_is_pdf"] = "true" if primary.is_pdf else "false"
    row["map_source"] = primary.source
    row["maps"] = [hit.as_dict() for hit in found.hits]


def run(root: Path | None = None, *, skip_network: bool = False, geocode: bool = True) -> list[dict]:
    root = root or feature_root()
    config = yaml.safe_load((root / "config.yaml").read_text(encoding="utf-8")) or {}
    checked_at = str(config.get("checked_at") or "")
    log: list[str] = []
    curated_path = root / (config.get("curated_csv") or "data/curated_listings.csv")
    curated = load_curated(curated_path)
    log.append(f"Curated rows: {len(curated)}")
    fetched: list[dict] = []
    eo_rows: list[dict] = []
    client = Client()
    if skip_network:
        log.append("Network fetches skipped")
    else:
        for source in config.get("sources") or []:
            try:
                fetched.extend(run_source(source, client, checked_at, log))
            except Exception as exc:
                log.append(f"{source.get('id', 'source')}: failed ({exc.__class__.__name__})")
        cache = root / "data" / "cache" / "eo_bmf_subsection_07.csv"
        try:
            eo_rows = load_or_download(cache, client, log)
        except Exception as exc:
            eo_rows = []
            log.append(f"EO BMF failed ({exc.__class__.__name__})")
        log.append(f"EO BMF subsection 07 rows loaded: {len(eo_rows)}")
    else_rows = curated + fetched
    kept: list[dict] = []
    for row in else_rows:
        evidence = row.get("housing_evidence") or housing_snippet(row.get("notes", ""))
        if not evidence:
            log.append(f"Dropped {row.get('name') or row.get('source_url')}: no housing evidence")
            continue
        row["housing_evidence"] = evidence
        if not row.get("listing_id"):
            row["listing_id"] = _slug(row)
        kept.append(row)
    rows = dedupe(kept)
    curated_prices = {row.get("price_amount", "") for row in rows if row.get("origin") == "curated" and row.get("price_amount")}
    rows = [
        row
        for row in rows
        if row.get("origin") == "curated" or row.get("price_amount", "") not in curated_prices
    ]
    if not skip_network:
        for row in rows:
            if row.get("category") != "501c7" or row.get("eo_ein"):
                continue
            hit = match_club(eo_rows, row.get("name", ""), row.get("city", ""), row.get("state", ""))
            if hit:
                row["eo_ein"] = hit.get("ein", "")
                row["eo_name"] = hit.get("name", "")
                log.append(f"EO match {row['name']}: {row['eo_ein']} {row['eo_name']}")
        for row in rows:
            try:
                _apply_maps(client, row, log)
            except Exception as exc:
                log.append(f"maps {row.get('name')}: failed ({exc.__class__.__name__})")
            if geocode:
                try:
                    reason = _geocode(client, row)
                except Exception as exc:
                    log.append(f"geocode {row.get('name')}: failed ({exc.__class__.__name__})")
                    reason = ""
                if reason == "robots":
                    log.append("Geocoding skipped: Nominatim robots.txt disallows /search. Coordinates are kept only when a listing page stated them.")
                    geocode = False
    for row in rows:
        row["satellite_url"] = satellite_maps_url(row.get("lat", ""), row.get("lon", ""))
    rows.sort(key=lambda row: (row.get("category", ""), row.get("state", ""), row.get("name", "")))
    counts = {cat: sum(1 for row in rows if row.get("category") == cat) for cat in ("college", "camp", "501c7")}
    log.append(
        f"Published {len(rows)} listings "
        f"({counts['college']} college, {counts['camp']} camp, {counts['501c7']} 501c7)"
    )
    write_outputs(root / "outputs", rows, log)
    return rows


def _slug(row: dict) -> str:
    raw = "-".join(part for part in (row.get("name", ""), row.get("state", "")) if part)
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in raw)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")[:80]


def read_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
