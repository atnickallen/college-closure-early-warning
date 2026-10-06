"""Public listing sources. A blocked host is logged and does not stop the run."""

from __future__ import annotations

import re
from html import unescape
from urllib.parse import quote_plus
from xml.etree import ElementTree

from camp_listings.housing import housing_snippet
from camp_listings.http import Client
from camp_listings.schema import as_row

_NEWS = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"


def _text(html: str) -> str:
    html = re.sub(r"(?is)<(script|style)[\s\S]*?</\1>", " ", html or "")
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(text)).strip()


_STATE = r"A[LKZR]|C[AOT]|D[EC]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|PA|RI|S[CD]|T[NX]|UT|V[AT]|W[AIVY]"


def parse_summer_camp_hub(html: str, source_url: str, checked_at: str) -> list[dict]:
    """Pull the sale blurbs from the Summer Camp Hub roundup page."""
    text = _text(html)
    chunks = re.split(r"(Current Price:\s*\$[\d,]+)", text)
    built: list[dict] = []
    pending = ""
    for chunk in chunks:
        if not chunk.startswith("Current Price:"):
            pending = chunk
            continue
        price_match = re.search(r"\$[\d,]+", chunk)
        price = price_match.group(0) if price_match else ""
        window = pending[-900:]
        evidence = housing_snippet(window)
        pending = ""
        if not evidence or not price:
            continue
        address = ""
        address_match = re.search(r"Address:\s*(.+)$", window)
        if address_match:
            address = address_match.group(1).strip(" .")
        state = ""
        city = ""
        if address:
            pieces = [piece.strip() for piece in address.split(",")]
            if len(pieces) >= 2:
                city = pieces[-2]
                state_match = re.search(rf"\b({_STATE})\b", pieces[-1])
                if state_match:
                    state = state_match.group(1)
        if not state or not city:
            place = re.search(
                rf"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*),\s*({_STATE})\b",
                window[-240:],
            )
            if place:
                city = city or place.group(1)
                state = state or place.group(2)
        acres = ""
        acres_match = re.search(r"(\d[\d,]*)\s*acres", window, re.I)
        if acres_match:
            acres = acres_match.group(1).replace(",", "")
        name = city + " camp" if city else "Summer camp"
        amount = price.replace("$", "").replace(",", "")
        built.append(
            as_row(
                {
                    "name": name[:120],
                    "category": "camp",
                    "status": "for sale",
                    "city": city,
                    "state": state,
                    "address": address,
                    "price_text": price,
                    "price_amount": amount,
                    "acreage": acres,
                    "housing_evidence": evidence,
                    "source_name": "Summer Camp Hub",
                    "source_url": source_url,
                    "checked_at": checked_at,
                    "origin": "fetched",
                }
            )
        )
    return built


def parse_news_rss(xml_text: str) -> list[dict[str, str]]:
    """Headlines only. Google News item text is not copied into listings."""
    leads: list[dict[str, str]] = []
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
        return leads
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title or link:
            leads.append({"title": title, "link": link})
    return leads


def run_source(source: dict, client: Client, checked_at: str, log: list[str]) -> list[dict]:
    kind = source.get("kind") or "probe"
    name = source.get("id") or kind
    url = source.get("url") or ""
    if kind == "news":
        return _news(source, client, log)
    if not url:
        log.append(f"{name}: no URL configured")
        return []
    result = client.fetch(url)
    if result.blocked:
        log.append(f"{name}: blocked ({result.reason}) {url}")
        return []
    if kind == "summercamphub":
        rows = parse_summer_camp_hub(result.body, result.final_url or url, checked_at)
        log.append(f"{name}: parsed {len(rows)} housing listings from {url}")
        return rows
    evidence = housing_snippet(_text(result.body))
    if evidence:
        log.append(f"{name}: fetched {url}; housing text is present but this source has no row parser")
    else:
        log.append(f"{name}: fetched {url}; no housing listings in the HTML")
    return []


def _news(source: dict, client: Client, log: list[str]) -> list[dict]:
    queries = source.get("queries") or []
    for query in queries:
        url = _NEWS.format(query=quote_plus(query))
        result = client.fetch(url)
        if result.blocked:
            log.append(f"news: blocked ({result.reason}) for {query}")
            continue
        leads = parse_news_rss(result.body)
        log.append(f"news: {len(leads)} headlines for '{query}' (not copied into listings)")
        for lead in leads[:8]:
            title = lead["title"].replace("\n", " ")
            log.append(f"news lead: {title[:160]}")
    return []
