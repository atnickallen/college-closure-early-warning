"""Column names shared by the curated file and the published listings."""

from __future__ import annotations

COLUMNS = (
    "listing_id",
    "name",
    "category",
    "status",
    "city",
    "state",
    "address",
    "price_text",
    "price_amount",
    "acreage",
    "beds",
    "cabin_count",
    "housing_evidence",
    "source_name",
    "source_url",
    "image_url",
    "image_credit",
    "lat",
    "lon",
    "listing_date",
    "checked_at",
    "notes",
    "eo_ein",
    "eo_name",
    "map_urls",
    "map_type",
    "map_is_pdf",
    "map_source",
    "origin",
)

CATEGORIES = ("college", "camp", "501c7")


def empty_row() -> dict[str, str]:
    return {column: "" for column in COLUMNS}


def as_row(raw: dict) -> dict[str, str]:
    row = empty_row()
    for key, value in raw.items():
        if key not in row or value is None:
            continue
        if isinstance(value, bool):
            row[key] = "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            row[key] = "|".join(str(item) for item in value if str(item).strip())
        else:
            row[key] = str(value).strip()
    return row
