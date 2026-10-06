"""Find campus, camp, and plat maps for a property.

Uses the Firecrawl v2 search and map endpoints when FIRECRAWL_API_KEY is set.
Otherwise it searches DuckDuckGo Lite (robots.txt allows `/`) and reads map
links from the listing page and the organization's site. The API key is never
written to logs.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from html import unescape
from urllib.parse import unquote, urljoin, urlparse

from camp_listings.http import USER_AGENT, Client

FIRECRAWL_SEARCH = "https://api.firecrawl.dev/v2/search"
FIRECRAWL_MAP = "https://api.firecrawl.dev/v2/map"
DDG_LITE = "https://lite.duckduckgo.com/lite/"

_SKIP_HOSTS = ("google.com", "facebook.com", "instagram.com", "youtube.com")
_SKIP_PATH = ("sitemap.xml", "wp-sitemap", "robots.txt")


@dataclass
class MapHit:
    url: str
    map_type: str
    is_pdf: bool
    source: str

    def as_dict(self) -> dict:
        return {
            "url": self.url,
            "map_type": self.map_type,
            "is_pdf": self.is_pdf,
            "source": self.source,
        }


@dataclass
class MapSearch:
    hits: list[MapHit] = field(default_factory=list)
    image_url: str = ""
    notes: list[str] = field(default_factory=list)


def queries_for(name: str) -> list[str]:
    clean = " ".join((name or "").split())
    return [
        f'"{clean}" campus map filetype:pdf',
        f'"{clean}" site map pdf',
        f'"{clean}" camp map',
    ]


def classify_map(url: str, anchor: str = "") -> tuple[str, bool] | None:
    """Return (map_type, is_pdf) or None when the link is not a property map."""
    if not url or url.startswith(("mailto:", "javascript:", "#")):
        return None
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if any(skip in host for skip in _SKIP_HOSTS):
        return None
    path = unquote(parsed.path).lower()
    if any(token in path for token in _SKIP_PATH):
        return None
    blob = f"{path} {anchor}".lower()
    has_map = "map" in blob
    has_plat = "plat" in blob
    has_survey = "survey" in blob
    # A survey page is a map when it is a plat/PDF or the link also says map.
    # "interest-survey" and similar forms are not property maps.
    if has_survey and not (has_map or has_plat or path.endswith(".pdf")):
        has_survey = False
    has_om = bool(re.search(r"offering[-_ ]memorand", blob))
    if not (has_map or has_plat or has_survey or has_om):
        return None
    is_pdf = path.endswith(".pdf")
    if has_plat or has_survey:
        kind = "plat"
    elif re.search(r"offering[-_ ]memorand|\bom\b", blob):
        kind = "offering_memorandum"
    elif "campus" in blob and "map" in blob:
        kind = "campus_map"
    elif re.search(r"facilit", blob):
        kind = "facility_map"
    elif re.search(r"site[-_ ]?map|sitemap", blob):
        kind = "site_map"
    else:
        kind = "property_map"
    return kind, is_pdf


def links_from_html(html: str, base_url: str) -> tuple[list[tuple[str, str]], str]:
    image = ""
    meta = re.search(r'(?is)<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html or "")
    if not meta:
        meta = re.search(r'(?is)<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html or "")
    if meta:
        image = urljoin(base_url, unescape(meta.group(1).strip()))
    found: list[tuple[str, str]] = []
    for match in re.finditer(r'(?is)<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html or ""):
        href = unescape(match.group(1).strip())
        text = re.sub(r"(?is)<[^>]+>", " ", match.group(2))
        text = re.sub(r"\s+", " ", unescape(text)).strip()
        absolute = urljoin(base_url, href)
        found.append((absolute, text))
    return found, image


def _add(hits: list[MapHit], seen: set[str], url: str, anchor: str, source: str) -> None:
    classified = classify_map(url, anchor)
    if not classified:
        return
    kind, is_pdf = classified
    key = url.split("#")[0]
    if key in seen:
        return
    seen.add(key)
    hits.append(MapHit(url=key, map_type=kind, is_pdf=is_pdf, source=source))


def _ddg_results(html: str) -> list[tuple[str, str]]:
    """Return (url, link text) from a DuckDuckGo Lite results page."""
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for match in re.finditer(
        r'(?is)<a[^>]+href="[^"]*uddg=([^&"\']+)[^"]*"[^>]*>(.*?)</a>',
        html or "",
    ):
        url = unquote(match.group(1))
        text = re.sub(r"(?is)<[^>]+>", " ", match.group(2))
        text = re.sub(r"\s+", " ", unescape(text)).strip()
        if url.startswith("http") and url not in seen:
            seen.add(url)
            found.append((url, text))
    if found:
        return found
    for match in re.finditer(r"uddg=([^&\"']+)", html or ""):
        url = unquote(match.group(1))
        if url.startswith("http") and url not in seen:
            seen.add(url)
            found.append((url, ""))
    return found


def _firecrawl_post(client: Client, endpoint: str, payload: dict, key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request_url = endpoint
    # The key is a header only. Callers log status text, never this value.
    from urllib.request import Request

    request = Request(
        request_url,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    opener = client.opener
    try:
        if opener is None:
            from urllib.request import urlopen

            response = urlopen(request, timeout=client.timeout)
        else:
            try:
                response = opener(request, timeout=client.timeout)
            except TypeError:
                response = opener(request)
        with response:
            raw = response.read()
            status = int(getattr(response, "status", 200))
    except Exception as exc:
        code = getattr(exc, "code", "")
        raise RuntimeError(f"Firecrawl HTTP {code}".strip()) from None
    if status >= 400:
        raise RuntimeError(f"Firecrawl HTTP {status}")
    if isinstance(raw, str):
        text = raw
    else:
        text = raw.decode("utf-8", "replace")
    return json.loads(text)


def _urls_from_firecrawl_search(payload: dict) -> list[str]:
    data = payload.get("data") or {}
    web = data.get("web") or payload.get("web") or []
    urls = []
    for item in web:
        if isinstance(item, str) and item.startswith("http"):
            urls.append(item)
        elif isinstance(item, dict) and item.get("url"):
            urls.append(str(item["url"]))
    return urls


def _urls_from_firecrawl_map(payload: dict) -> list[str]:
    links = payload.get("links") or (payload.get("data") or {}).get("links") or []
    urls = []
    for item in links:
        if isinstance(item, str):
            urls.append(item)
        elif isinstance(item, dict) and item.get("url"):
            urls.append(str(item["url"]))
    return urls


def find_maps(
    name: str,
    *,
    client: Client | None = None,
    listing_url: str = "",
    org_url: str = "",
    api_key: str | None = None,
    search_queries: list[str] | None = None,
) -> MapSearch:
    client = client or Client()
    key = (api_key if api_key is not None else os.environ.get("FIRECRAWL_API_KEY", "")).strip()
    result = MapSearch()
    hits: list[MapHit] = []
    seen: set[str] = set()
    queries = search_queries if search_queries is not None else queries_for(name)

    if key:
        result.notes.append("Firecrawl search enabled")
        for query in queries:
            try:
                payload = _firecrawl_post(client, FIRECRAWL_SEARCH, {"query": query, "limit": 5, "country": "US"}, key)
            except RuntimeError as exc:
                result.notes.append(str(exc))
                continue
            for url in _urls_from_firecrawl_search(payload):
                _add(hits, seen, url, "", "firecrawl")
        for site in (listing_url, org_url):
            if not site:
                continue
            try:
                payload = _firecrawl_post(
                    client,
                    FIRECRAWL_MAP,
                    {"url": site, "search": "map", "limit": 25},
                    key,
                )
            except RuntimeError as exc:
                result.notes.append(str(exc))
                continue
            for url in _urls_from_firecrawl_map(payload):
                _add(hits, seen, url, "map", "firecrawl")
    else:
        result.notes.append("Firecrawl key not set; using DuckDuckGo Lite and page links")
        if client.robots_allowed(DDG_LITE):
            for query in queries:
                time.sleep(0.6)
                fetched = client.fetch(DDG_LITE + "?" + _query(query))
                if fetched.blocked:
                    result.notes.append(f"DuckDuckGo search skipped: {fetched.reason}")
                    break
                for url, anchor in _ddg_results(fetched.body):
                    _add(hits, seen, url, anchor, "duckduckgo")
        else:
            result.notes.append("DuckDuckGo Lite skipped: robots.txt disallows search")

    crawled: set[str] = set()
    for site in (listing_url, org_url):
        if not site or site in crawled:
            continue
        crawled.add(site)
        fetched = client.fetch(site)
        if fetched.blocked or not fetched.body:
            if fetched.blocked:
                result.notes.append(f"Map crawl skipped {site}: {fetched.reason}")
            continue
        anchors, image = links_from_html(fetched.body, fetched.final_url or site)
        if image and not result.image_url:
            result.image_url = image
        for url, text in anchors:
            _add(hits, seen, url, text, "page")
    result.hits = relevant_maps(hits, listing_url, name)[:8]
    if result.hits:
        primary = best_campus_map(result.hits)
        if primary and primary is not result.hits[0]:
            result.hits = [primary] + [hit for hit in result.hits if hit.url != primary.url]
    return result


def _query(query: str) -> str:
    from urllib.parse import urlencode

    return urlencode({"q": query})


def relevant_maps(hits: list[MapHit], listing_url: str = "", name: str = "") -> list[MapHit]:
    """Drop the listing page itself and unrelated search hits."""
    listing = listing_url.split("#")[0].rstrip("/")
    host_tokens = _name_tokens(name)
    kept: list[MapHit] = []
    for hit in hits:
        url = hit.url.split("#")[0]
        if listing and url.rstrip("/") == listing:
            continue
        host = urlparse(url).netloc.lower()
        if any(bad in host for bad in _IRRELEVANT_HOSTS):
            continue
        listing_host = urlparse(listing_url).netloc.lower().removeprefix("www.") if listing_url else ""
        hit_host = host.removeprefix("www.")
        same_site = bool(listing_host) and (hit_host == listing_host or hit_host.endswith("." + listing_host))
        path = urlparse(url).path.lower()
        named = any(token in host for token in host_tokens)
        if hit.is_pdf or "id.land" in host or same_site or named:
            kept.append(hit)
            continue
        if any(token in path for token in ("campus-map", "campus_map", "site-map", "plat", "survey")):
            kept.append(hit)
    return kept


_IRRELEVANT_HOSTS = (
    "mapquest.",
    "tripadvisor.",
    "reddit.",
    "pinterest.",
    "mapy.com",
    "trip.com",
    "alltrails.",
    "merchantcircle.",
)


def _name_tokens(name: str) -> set[str]:
    stop = {"camp", "lodge", "club", "island", "river", "creek", "springs", "farms", "ranch", "resort", "hunting", "duck"}
    return {token for token in re.findall(r"[a-z0-9]{6,}", (name or "").lower()) if token not in stop}


def best_campus_map(hits: list[MapHit]) -> MapHit | None:
    if not hits:
        return None

    def rank(hit: MapHit) -> tuple:
        type_rank = {
            "campus_map": 0,
            "facility_map": 1,
            "site_map": 2,
            "plat": 3,
            "offering_memorandum": 4,
            "property_map": 5,
        }.get(hit.map_type, 9)
        return (0 if hit.is_pdf else 1, type_rank)

    return sorted(hits, key=rank)[0]
