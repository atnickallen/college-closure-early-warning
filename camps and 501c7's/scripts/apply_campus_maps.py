#!/usr/bin/env python3
"""Fill campus_map_url for the 50 schools on the main watch-list cards."""

from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

FEATURE = Path(__file__).resolve().parents[1]
REPO = FEATURE.parents[0]
sys.path.insert(0, str(FEATURE / "src"))

from camp_listings.http import Client  # noqa: E402
from camp_listings.maps import (  # noqa: E402
    DDG_LITE,
    MapHit,
    _ddg_results,
    _query,
    best_campus_map,
    find_maps,
    queries_for,
)

# Generic words that show up in many school names and unrelated hosts.
_GENERIC = {
    "college",
    "university",
    "seminary",
    "institute",
    "school",
    "christian",
    "american",
    "national",
    "graduate",
    "campus",
    "international",
    "inter",
    "puerto",
    "north",
    "south",
    "mount",
    "saint",
    "bible",
    "baptist",
    "theological",
    "technology",
    "design",
    "studies",
    "main",
}

_BAD_HOSTS = (
    "academicjobs.",
    "all-maps.com",
    "communitycollegereview.",
    "wikipedia.org",
    "wikimedia.org",
    "squarespace-cdn.com",
    "illinoisworknet.",
    "niche.com",
    "usnews.com",
    "collegesimply.",
    "univstats.",
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "google.com",
    "goo.gl",
    "mapquest.",
)

_PROBE_PATHS = (
    "/campus-map",
    "/campus-map/",
    "/campusmap",
    "/maps",
    "/map",
    "/mapa",
    "/about/campus-map",
    "/about/maps",
    "/visit/campus-map",
    "/admissions/campus-map",
    "/student-life/campus-map",
    "/campus/map",
    "/campus-life/campus-map",
)


def main() -> int:
    report = (REPO / "outputs" / "top50_report.html").read_text(encoding="utf-8")
    main_html = report.split("Teach-out / not enrolling")[0]
    cards = re.findall(r"<h2>\d+\. ([^<]+)</h2>.*?UNITID (\d+)", main_html, re.S)
    land_path = REPO / "data" / "campus" / "campus_land.csv"
    with land_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    if "campus_map_url" not in fields:
        fields.append("campus_map_url")
    by_id = {row["unitid"]: row for row in rows}
    client = Client(timeout=12)
    # A set key means this run should query Firecrawl for every school.
    # An empty result leaves a map that was already stored.
    use_firecrawl = bool(os.environ.get("FIRECRAWL_API_KEY", "").strip())
    found = 0
    for name, unitid in cards:
        row = by_id.get(unitid)
        if row is None:
            continue
        existing = (row.get("campus_map_url") or "").strip()
        if _keep_existing(existing, name, use_firecrawl=use_firecrawl):
            found += 1
            print(f"{unitid} kept {existing}", flush=True)
            continue
        url = _find_campus_map(name, row, client, use_firecrawl=use_firecrawl)
        if url:
            row["campus_map_url"] = url
            found += 1
            print(f"{unitid} {url}", flush=True)
        elif existing and _stored_ok(existing):
            row["campus_map_url"] = existing
            found += 1
            print(f"{unitid} kept {existing}", flush=True)
        else:
            row["campus_map_url"] = ""
            print(f"{unitid} none", flush=True)
        _write_land(land_path, rows, fields)
    for row in rows:
        row.setdefault("campus_map_url", "")
    with land_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    _patch_report(by_id)
    print(f"Campus maps filled: {found} of {len(cards)}")
    return 0


def _write_land(path: Path, rows: list[dict], fields: list[str]) -> None:
    for row in rows:
        row.setdefault("campus_map_url", "")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _host(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def _bad_host(url: str) -> bool:
    host = _host(url)
    return any(bad in host for bad in _BAD_HOSTS)


# Campus names that show up in URLs. A map for one of these is the wrong
# campus when that word is not part of the school name.
_PLACE_WORDS = (
    "denver",
    "orlando",
    "florham",
    "metropolitan",
    "bayamon",
    "monterey",
    "surprise",
    "teaneck",
    "madison",
    "tampa",
    "online",
)


def _url_looks_like_map(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.lower()
    if host.startswith("map.") or host.startswith("maps."):
        return True
    if any(token in path for token in ("sitemap", "robots.txt", "style-guide")):
        return False
    if re.search(r"(campus|schematic|site|facility)[-_]?map", path):
        return True
    if "/maps-directions" in path or "/maps_directions" in path:
        return True
    if re.search(r"(?:^|/)(map|maps|mapa)(?:/|$)", path.rstrip("/")):
        return True
    file_path = path.split("?")[0]
    if file_path.endswith((".pdf", ".jpg", ".jpeg", ".png", ".gif", ".webp")) and re.search(r"map|plat|survey", file_path):
        return True
    return False


def _foreign_campus(url: str, name: str) -> bool:
    blob = url.lower()
    school = name.lower()
    return any(word in blob and word not in school for word in _PLACE_WORDS)


def _stored_ok(url: str) -> bool:
    return bool(url) and url.startswith("http") and not _bad_host(url) and _url_looks_like_map(url)


def _soft_missing(body: str) -> bool:
    title = re.search(r"(?is)<title>([^<]+)", body or "")
    text = (title.group(1) if title else "")[:180].lower()
    return "not found" in text or "404" in text or "page does not exist" in text


def _accept_fetched(url: str, fetched) -> str:
    if fetched.blocked or fetched.status != 200:
        return ""
    body = fetched.body or ""
    if len(body) < 400 or _soft_missing(body):
        return ""
    final = (fetched.final_url or url).split("#")[0]
    if _bad_host(final) or not _url_looks_like_map(final):
        return ""
    if urlparse(final).path.rstrip("/") in ("",) and not _host(final).startswith(("map.", "maps.")):
        return ""
    return final


def _wiki_site(client: Client, page_url: str) -> str:
    if "wikipedia.org" not in (page_url or ""):
        return ""
    fetched = client.fetch(page_url)
    body = fetched.body or ""
    match = re.search(
        r'class="infobox-label"[^>]*>\s*Website\s*</th>.*?<a[^>]+href="(https?://[^"]+)"',
        body,
        re.S,
    )
    if not match:
        return ""
    site = match.group(1)
    if _bad_host(site):
        return ""
    return f"https://{_host(site)}/"


def _org_from_search(client: Client, name: str) -> str:
    if not client.robots_allowed(DDG_LITE):
        return ""
    fetched = client.fetch(DDG_LITE + "?" + _query(f'"{name}"'))
    if fetched.blocked:
        return ""
    tokens = set(re.findall(r"[a-z0-9]{6,}", name.lower())) - _GENERIC
    for url, _anchor in _ddg_results(fetched.body):
        if _bad_host(url):
            continue
        host = _host(url)
        if any(token in host for token in tokens):
            return f"https://{host}/"
    return ""


def _probe(client: Client, origin: str, name: str) -> str:
    if not origin:
        return ""
    origin = origin.rstrip("/")
    candidates: list[str] = []
    for site in (origin + "/sitemap.xml", origin + "/sitemap_index.xml", origin + "/wp-sitemap.xml"):
        fetched = client.fetch(site)
        if fetched.blocked or not fetched.body:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", fetched.body, re.I)
        children = [item for item in locs if "sitemap" in item.lower()][:4]
        pages = [item for item in locs if "sitemap" not in item.lower()]
        for child in children:
            child_fetch = client.fetch(child)
            if child_fetch.body:
                pages.extend(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", child_fetch.body, re.I))
        candidates.extend(
            item for item in pages if _url_looks_like_map(item) and not _bad_host(item) and not _foreign_campus(item, name)
        )
        if candidates:
            break
    tokens = set(re.findall(r"[a-z0-9]{5,}", name.lower())) - _GENERIC
    candidates.sort(key=lambda url: (0 if any(token in url.lower() for token in tokens) else 1, _map_rank(url)))
    for loc in candidates[:6]:
        kept = _accept_fetched(loc, client.fetch(loc))
        if kept:
            return kept
    for path in _PROBE_PATHS:
        url = origin + path
        if _foreign_campus(url, name):
            continue
        kept = _accept_fetched(url, client.fetch(url))
        if kept and _foreign_campus(kept, name):
            continue
        if kept:
            return kept
    return ""


def _map_rank(url: str) -> tuple:
    path = urlparse(url).path.lower()
    specific = 0 if re.search(r"schematic-map|campus-map|campus_map|campusmap", path) else 1
    return (specific, 0 if path.endswith(".pdf") else 1, 0 if path.rstrip("/").endswith("/mapa") else 1, len(path))


def _maps_linked_from(client: Client, page_url: str, name: str) -> str:
    """Read map links from a campus page the land file already cites."""
    if not page_url.startswith("http") or _bad_host(page_url):
        return ""
    fetched = client.fetch(page_url)
    if fetched.blocked or not fetched.body:
        return ""
    from camp_listings.maps import links_from_html

    anchors, _image = links_from_html(fetched.body, fetched.final_url or page_url)
    found: list[str] = []
    for url, text in anchors:
        if _bad_host(url) or _foreign_campus(url, name):
            continue
        if _url_looks_like_map(url):
            found.append(url.split("#")[0])
            continue
        if "campus map" not in text.lower():
            continue
        kept = _accept_fetched(url, client.fetch(url))
        if kept and not _foreign_campus(kept, name):
            found.append(kept)
    if not found:
        return ""
    found.sort(key=lambda url: _pick_key(url, name))
    return found[0]


def _pick_key(url: str, name: str) -> tuple:
    school = name.lower()
    blob = url.lower()
    needed = [word for word in _PLACE_WORDS if word in school]
    missing = 1 if needed and not any(word in blob for word in needed) else 0
    return (missing, _map_rank(url))


def _prefer(name: str, *urls: str) -> str:
    choices = [url for url in urls if url]
    if not choices:
        return ""
    choices.sort(key=lambda url: _pick_key(url, name))
    return choices[0]


def _direct_from_row(row: dict) -> str:
    for key in ("image_credit_url", "source_url", "image_url"):
        url = (row.get(key) or "").strip()
        if _stored_ok(url):
            return url.split("#")[0]
    return ""


def _keep_existing(existing: str, name: str, *, use_firecrawl: bool) -> bool:
    if use_firecrawl or not existing:
        return False
    place_tokens = set(re.findall(r"[a-z0-9]{5,}", name.lower())) & set(_PLACE_WORDS)
    place_ok = not place_tokens or any(token in existing.lower() for token in place_tokens)
    return bool(_stored_ok(existing) and place_ok and not _foreign_campus(existing, name))


def _find_campus_map(name: str, row: dict, client: Client, *, use_firecrawl: bool = False) -> str:
    direct = _direct_from_row(row)
    if direct and not use_firecrawl:
        return direct
    linked = ""
    for key in ("source_url", "image_credit_url"):
        linked = _maps_linked_from(client, (row.get(key) or "").strip(), name)
        if linked:
            break
    org = _org_url(row)
    if not org:
        org = _wiki_site(client, row.get("source_url") or "")
    probed = _probe(client, org, name)
    best = _prefer(name, linked, probed)
    if best and not use_firecrawl:
        return best
    if not org:
        org = _org_from_search(client, name)
        probed = _probe(client, org, name)
        if probed and not use_firecrawl:
            return probed
    queries = queries_for(name) if use_firecrawl else [f'"{name}" campus map filetype:pdf', f'"{name}" campus map']
    result = find_maps(
        name,
        client=client,
        listing_url=org,
        org_url=org,
        search_queries=queries,
    )
    hit = _choose(result.hits, org, name)
    hit_url = hit.url if hit and _stored_ok(hit.url) else ""
    if use_firecrawl:
        return _prefer(name, hit_url, direct, linked, probed)
    return hit_url


def _choose(hits: list[MapHit], org: str, name: str) -> MapHit | None:
    """Keep a map on the school's site, or one whose host/path names the school."""
    org_host = ""
    if org:
        org_host = urlparse(org).netloc.lower().removeprefix("www.")
    tokens = set(re.findall(r"[a-z0-9]{6,}", name.lower())) - _GENERIC
    accepted: list[MapHit] = []
    for hit in hits:
        if not _stored_ok(hit.url) or _foreign_campus(hit.url, name):
            continue
        host = _host(hit.url)
        path = urlparse(hit.url).path.lower()
        same = bool(org_host) and (host == org_host or host.endswith("." + org_host))
        named_host = any(token in host for token in tokens)
        named_pdf = hit.is_pdf and any(token in path for token in tokens)
        if same or named_host or named_pdf:
            accepted.append(hit)
    return best_campus_map(accepted)


def _patch_report(by_id: dict) -> None:
    import html as html_lib
    path = REPO / "outputs" / "top50_report.html"
    text = path.read_text(encoding="utf-8")
    main, marker, rest = text.partition("Teach-out / not enrolling")
    main = re.sub(r"\n\s*<tr><th>Campus map</th>.*?</tr>", "", main)

    def insert(match: re.Match) -> str:
        unitid = match.group(1)
        url = (by_id.get(unitid, {}).get("campus_map_url") or "").strip()
        block = match.group(0)
        if not url or ">Campus map</a>" in block:
            return block
        href = html_lib.escape(url, quote=True)
        row = f'<tr><th>Campus map</th><td colspan="3"><a href="{href}">Campus map</a></td></tr>'
        return block + "\n        " + row

    main = re.sub(
        r'UNITID (\d+)</p>.*?<tr><th>Satellite view</th><td colspan="3">.*?</td></tr>',
        insert,
        main,
        flags=re.S,
    )
    path.write_text(main + marker + rest, encoding="utf-8")


def _org_url(row: dict) -> str:
    for key in ("source_url", "image_credit_url", "image_url"):
        url = (row.get(key) or "").strip()
        if not url.startswith("http"):
            continue
        host = url.split("/")[2].lower()
        if _bad_host(url):
            continue
        return f"https://{host}/"
    return ""


if __name__ == "__main__":
    raise SystemExit(main())
