"""Drop the same property when two sources describe it."""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def _norm(text: str) -> str:
    text = (text or "").lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def canonical_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url.strip())
    if not parsed.netloc:
        return ""
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parsed.query) if k.lower() not in {"utm_source", "utm_medium"}))
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((parsed.scheme.lower() or "https", parsed.netloc.lower(), path, "", query, ""))


def _index_url(url: str) -> bool:
    path = urlparse(url).path.rstrip("/").lower()
    return path.endswith("/listings") or path.endswith("summer-camps-for-sale") or path.endswith("/search")


def identity_keys(row: dict) -> list[str]:
    keys: list[str] = []
    url = canonical_url(row.get("source_url", ""))
    if url and not _index_url(url):
        keys.append("url:" + url)
    name = _norm(row.get("name", ""))
    state = _norm(row.get("state", ""))
    if name and state:
        keys.append(f"name:{name}|{state}")
    city = _norm(row.get("city", ""))
    price = re.sub(r"[^0-9.]", "", row.get("price_amount", "") or "")
    if city and state and price:
        keys.append(f"place:{state}|{city}|{price}")
    if not keys and name:
        keys.append("name:" + name)
    return keys


def dedupe(rows: list[dict]) -> list[dict]:
    """Keep the curated row when a fetched row describes the same property."""
    ordered = sorted(rows, key=lambda row: (0 if row.get("origin") == "curated" else 1, row.get("name", "")))
    seen: dict[str, dict] = {}
    kept: list[dict] = []
    for row in ordered:
        keys = identity_keys(row)
        prior = next((seen[key] for key in keys if key in seen), None)
        if prior is not None:
            _fill_blanks(prior, row)
            for key in keys:
                seen[key] = prior
            continue
        kept.append(row)
        for key in keys:
            seen[key] = row
    return kept


def _fill_blanks(prior: dict, extra: dict) -> None:
    for key, value in extra.items():
        if not str(prior.get(key, "")).strip() and str(value).strip():
            prior[key] = value
