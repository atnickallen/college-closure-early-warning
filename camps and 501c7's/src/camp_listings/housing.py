"""Keep a listing only when the page states housing, and keep that sentence."""

from __future__ import annotations

import re

# Dorms, cabins, bunkhouses, lodges with beds, and residence halls.
_HOUSING = re.compile(
    r"(?i)("
    r"residence halls?|dormitor(?:y|ies)|dorms?|"
    r"student housing|residential buildings?|"
    r"bunk\s*houses?|bunkrooms?|bunks|"
    r"cabins?|"
    r"lodges?|"
    r"sleeps?\s+\+?\d+|"
    r"\d+\s+bedrooms?|"
    r"\d+\s+beds\b|"
    r"guest rooms?"
    r")"
)


def housing_snippet(text: str, limit: int = 320) -> str:
    """Return a short quote that shows the housing, or blank when there is none."""
    if not text:
        return ""
    collapsed = re.sub(r"\s+", " ", text).strip()
    match = _HOUSING.search(collapsed)
    if not match:
        return ""
    start = max(0, match.start() - 80)
    end = min(len(collapsed), match.end() + 140)
    snippet = collapsed[start:end].strip(" .,-;")
    if start > 0:
        snippet = "…" + snippet
    if end < len(collapsed):
        snippet = snippet + "…"
    return snippet[:limit]


def has_housing(text: str) -> bool:
    return bool(housing_snippet(text))
