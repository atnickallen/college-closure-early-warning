"""Current-status check for the watch list.

The watch list is scored on lagged federal data (score year 2022 in this
build). This module records what has happened since: still operating, not
enrolling, closed, merged/acquired, campus sold, or campus listed for sale.

Curated rows in ``data/status/status_curated.csv`` are the record for campus
sales and listings. College Scorecard, the FSA closed-school list, and IPEDS
directory status do not report real-estate transactions. The automated refresh
may flag a disagreement. It does not overwrite curated sale, listing, buyer,
date, or price fields. It may append a still-operating row for a school that
newly enters the open top 50, with the federal source and ``checked_at``.

Nothing here is a closure prediction. A badge is a sourced note about what
has already happened, or a blank when there is no source.
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import logging
import re
from datetime import date
from pathlib import Path
from typing import Any, Callable

import pandas as pd
import requests

from college_closure.config import Settings, load_settings
from college_closure.constants import INST_STATUS_CLOSED, INST_STATUS_MERGED
from college_closure.download import DEFAULT_HEADERS, download_first
from college_closure.fsa import _discover_closed_school_urls, _guess_col, _read_tabular
from college_closure.ids import digits_only
from college_closure.scorecard import fetch_operating_by_unitids, scorecard_api_key

LOGGER = logging.getLogger(__name__)

CHECKED_AT_SEED = "2026-10-05"

STATUS_OPEN = "operating"
STATUS_NOT_ENROLLING = "not_enrolling"
STATUS_CLOSED = "closed"
STATUS_MERGED = "merged_acquired"

PROP_SOLD = "sold"
PROP_LISTED = "listed"
PROP_NONE = "no_sale_found"
PROP_NA = "not_applicable"
PROP_INSTITUTIONAL = "institutional_sale"

CURATED_COLUMNS = (
    "unitid",
    "opeid6",
    "opeid8",
    "watchlist_rank",
    "inst_name",
    "state_abbr",
    "status",
    "status_detail",
    "property_disposition",
    "buyer_or_broker",
    "event_date",
    "sale_price_published",
    "sold_listed_details",
    "source_url",
    "checked_at",
    "library_notes",
)

CURATED_LOCK_COLUMNS = (
    "status",
    "status_detail",
    "property_disposition",
    "buyer_or_broker",
    "event_date",
    "sale_price_published",
    "sold_listed_details",
    "source_url",
    "checked_at",
    "library_notes",
)

OUTPUT_COLUMNS = [
    "watchlist_rank",
    "unitid",
    "opeid6",
    "opeid8",
    "inst_name",
    "state_abbr",
    "status",
    "status_badge",
    "status_detail",
    "property_disposition",
    "buyer_or_broker",
    "event_date",
    "sale_price_published",
    "sold_listed_details",
    "source_url",
    "checked_at",
    "property_source",
    "auto_checked_at",
    "auto_signal",
    "auto_scorecard_operating",
    "auto_fsa_match",
    "auto_fsa_closed_date",
    "auto_fsa_name",
    "auto_ipeds_year",
    "auto_ipeds_status",
    "auto_ipeds_date_closed",
    "auto_ipeds_absent_after",
    "auto_sources",
    "disagreement",
    "library_notes",
]

SALE_LISTING_NOTE = (
    "Campus sales and listings are curated only. College Scorecard, the FSA "
    "closed-school list, and IPEDS do not report real-estate sales or listings."
)

_STOPWORDS = {
    "the",
    "of",
    "and",
    "at",
    "for",
    "a",
    "an",
    "de",
    "la",
}

_STATUS_BLOCK_RE = re.compile(r"\n?[ \t]*<div class=\"status-block\">.*?</div>", re.S)
_CARD_RE = re.compile(r"<article class=\"card\">.*?</article>", re.S)
_UNITID_RE = re.compile(r"UNITID\s+(\d+)")
_YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def curated_path(settings: Settings) -> Path:
    cfg = (settings.raw.get("status") or {}) if settings.raw else {}
    rel = cfg.get("curated_csv") or "data/status/status_curated.csv"
    return settings.root / rel


def _id_digits(value: Any) -> str:
    text = _blank(value)
    if re.fullmatch(r"\d+\.0+", text):
        text = text.split(".", 1)[0]
    return digits_only(text)


def _blank(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    if text.lower() in {"nan", "none", "<na>", "nat"}:
        return ""
    return text


def _canon8(value: Any) -> str:
    digits = digits_only(value)
    if not digits:
        return ""
    if len(digits) > 8:
        digits = digits[-8:]
    return digits.zfill(8)


def _canon6_from_root(value: Any) -> str:
    digits = digits_only(value)
    if not digits:
        return ""
    if len(digits) >= 8:
        return digits[-8:-2]
    if len(digits) == 7:
        return digits.zfill(8)[:6]
    return digits.zfill(6)


def name_tokens(value: Any) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", _blank(value).lower())
    return {t for t in tokens if t not in _STOPWORDS and len(t) > 1}


def campus_name_match(school_name: Any, closed_name: Any) -> bool:
    """True when the closed-school name is at least as specific as the watch-list name.

    A parent-system name that drops the campus token does not match. That keeps
    a shared OPEID6 from marking every branch closed.
    """
    school = name_tokens(school_name)
    closed = name_tokens(closed_name)
    if not school or not closed:
        return False
    return school.issubset(closed)


def _norm_name_key(name: Any, state: Any) -> str:
    tokens = re.findall(r"[a-z0-9]+", _blank(name).lower())
    return " ".join(tokens) + "|" + _blank(state).upper()


def load_curated(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Curated status file missing: {path}")
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    frame.columns = [str(c).strip() for c in frame.columns]
    for col in frame.columns:
        frame[col] = frame[col].map(_blank)
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    return frame


def load_watchlist(path: Path, top_n: int) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    frame.columns = [str(c).strip() for c in frame.columns]
    if top_n > 0:
        frame = frame.head(top_n).copy()
    frame = frame.reset_index(drop=True)
    frame["watchlist_rank"] = frame.index + 1
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    return frame


def _expected_federal(status: str) -> str:
    """What a federal operating flag should look like, given the curated code.

    ``open_or_merged`` accepts an operating flag or an IPEDS merger code.
    Sales and listings are not part of this expectation.
    """
    if status in {STATUS_OPEN, STATUS_NOT_ENROLLING}:
        return "operating"
    if status == STATUS_CLOSED:
        return "closed"
    if status == STATUS_MERGED:
        return "open_or_merged"
    return ""


def _ipeds_bucket(status_code: str, closed_date: str) -> str:
    if closed_date:
        return "closed"
    if not status_code:
        return ""
    try:
        code = int(float(status_code))
    except (TypeError, ValueError):
        return ""
    if code in INST_STATUS_CLOSED:
        return "closed"
    if code in INST_STATUS_MERGED:
        return "merged"
    if code == 1:
        return "operating"
    return ""


def fsa_match_level(school_opeid8: Any, school_opeid6: Any, raw_opeid: Any) -> str:
    """Return ``opeid8``, ``opeid6``, or ``''`` for one closed-school OPEID cell."""
    raw = digits_only(raw_opeid)
    if not raw:
        return ""
    school8 = _canon8(school_opeid8)
    school6 = _canon6_from_root(school_opeid6)
    if len(raw) >= 7 and raw.zfill(8) == school8:
        return "opeid8"
    if len(raw) == 6 and raw.endswith("00") and raw.zfill(8) == school8:
        return "opeid8"
    if len(raw) == 6 and not raw.endswith("00") and raw.zfill(8) == school8:
        return "opeid8"
    if len(raw) <= 6 and raw.zfill(6) == school6:
        return "opeid6"
    if len(raw) >= 7 and raw.zfill(8)[:6] == school6:
        return "opeid6"
    if len(raw) == 6 and raw.endswith("00") and raw.zfill(8)[:6] == school6 and raw.zfill(8) != school8:
        return "opeid6"
    return ""


def match_fsa_row(school: pd.Series, closed: pd.DataFrame) -> dict[str, str]:
    """Match one watch-list campus to the closed-school file.

    UNITID or OPEID8 is a campus hit. OPEID6 alone is a campus hit only when
    the closed-school name covers this campus name. A shared root with no
    name match is recorded as ``opeid6_only`` and is not a closure signal.
    """
    empty = {"auto_fsa_match": "", "auto_fsa_closed_date": "", "auto_fsa_name": ""}
    if closed is None or closed.empty:
        return empty
    unitid = _id_digits(school.get("unitid"))
    if unitid and "unitid" in closed.columns:
        same = closed[closed["unitid"].map(_id_digits) == unitid]
        if not same.empty:
            hit = same.iloc[0]
            return {
                "auto_fsa_match": "unitid",
                "auto_fsa_closed_date": _blank(hit.get("closed_date")),
                "auto_fsa_name": _blank(hit.get("closed_name")),
            }
    best_level = ""
    best_row = None
    rank = {"": 0, "opeid6_only": 1, "name": 2, "opeid8": 3, "unitid": 4}
    for _, row in closed.iterrows():
        level = fsa_match_level(school.get("opeid8"), school.get("opeid6"), row.get("opeid_raw"))
        if level == "opeid6" and campus_name_match(school.get("inst_name"), row.get("closed_name")):
            level = "name"
        elif level == "opeid6":
            level = "opeid6_only"
        if rank.get(level, 0) > rank.get(best_level, 0):
            best_level = level
            best_row = row
    if best_row is None or not best_level:
        return empty
    return {
        "auto_fsa_match": best_level,
        "auto_fsa_closed_date": _blank(best_row.get("closed_date")) if best_level != "opeid6_only" else "",
        "auto_fsa_name": _blank(best_row.get("closed_name")),
    }


def _parse_ipeds_date(value: Any) -> str:
    text = _blank(value)
    if not text or text in {"-1", "-2", "-3", "0"}:
        return ""
    try:
        num = float(text)
        if num in {-1, -2, -3, 0, 1, 2, 3}:
            return ""
    except ValueError:
        pass
    parsed = pd.to_datetime(text, errors="coerce")
    if pd.notna(parsed):
        year = int(parsed.year)
        if 1980 <= year <= 2035:
            if parsed.month == 1 and parsed.day == 1 and re.fullmatch(r"(?:19|20)\d{2}", text):
                return str(year)
            return parsed.strftime("%Y-%m-%d")
    match = _YEAR_RE.search(text)
    if not match:
        return ""
    year = int(match.group(0))
    if 1980 <= year <= 2035:
        return match.group(0)
    return ""


def _ipeds_for_unit(ipeds: pd.DataFrame, unitid: Any) -> dict[str, str]:
    empty = {
        "auto_ipeds_year": "",
        "auto_ipeds_status": "",
        "auto_ipeds_date_closed": "",
        "auto_ipeds_absent_after": "",
    }
    if ipeds is None or ipeds.empty or "unitid" not in ipeds.columns:
        return empty
    uid = pd.to_numeric(pd.Series([unitid]), errors="coerce").iloc[0]
    rows = ipeds[pd.to_numeric(ipeds["unitid"], errors="coerce") == uid]
    if rows.empty:
        return empty
    work = rows.copy()
    work["_year"] = pd.to_numeric(work.get("year"), errors="coerce")
    work = work.sort_values("_year", ascending=False)
    hit = work.iloc[0]
    status = _blank(hit.get("inst_status"))
    if status.endswith(".0"):
        status = status[:-2]
    try:
        code = int(float(status)) if status else None
    except (TypeError, ValueError):
        code = None
    if code in {-1, -2, -3}:
        status = ""
    return {
        "auto_ipeds_year": _blank(hit.get("year")).split(".")[0],
        "auto_ipeds_status": status,
        "auto_ipeds_date_closed": _parse_ipeds_date(hit.get("date_closed")),
        "auto_ipeds_absent_after": _blank(hit.get("ipeds_absent_after")),
    }


def _scorecard_value(scorecard: pd.DataFrame | None, unitid: Any) -> str:
    if scorecard is None or scorecard.empty or "unitid" not in scorecard.columns:
        return ""
    col = "scorecard_operating" if "scorecard_operating" in scorecard.columns else None
    if col is None and "auto_scorecard_operating" in scorecard.columns:
        col = "auto_scorecard_operating"
    if col is None:
        return ""
    uid = pd.to_numeric(pd.Series([unitid]), errors="coerce").iloc[0]
    rows = scorecard[pd.to_numeric(scorecard["unitid"], errors="coerce") == uid]
    if rows.empty:
        return ""
    raw = rows.iloc[0][col]
    text = _blank(raw).lower()
    if text in {"1", "1.0", "true", "yes"}:
        return "1"
    if text in {"0", "0.0", "false", "no"}:
        return "0"
    return ""


def sale_year_label(event_date: Any) -> str:
    years: list[str] = []
    for match in _YEAR_RE.findall(_blank(event_date)):
        if match not in years:
            years.append(match)
    if not years:
        return ""
    if len(years) == 1:
        return years[0]
    if len(years) == 2 and abs(int(years[1]) - int(years[0])) <= 2:
        first, second = sorted(years, key=int)
        return f"{first}–{second}"
    return years[0]


def status_badge(row: pd.Series | dict[str, Any]) -> str:
    """Short label from curated fields only. Blank when status is blank."""
    getter = row.get if hasattr(row, "get") else lambda k, d=None: row[k] if k in row else d  # type: ignore[index]
    status = _blank(getter("status"))
    prop = _blank(getter("property_disposition"))
    buyer = _blank(getter("buyer_or_broker"))
    when = sale_year_label(getter("event_date"))
    parts: list[str] = []
    labels = {
        STATUS_OPEN: "Open",
        STATUS_NOT_ENROLLING: "Open, not enrolling",
        STATUS_CLOSED: "Closed",
        STATUS_MERGED: "Acquired",
    }
    if status in labels:
        label = labels[status]
        if status == STATUS_MERGED and buyer and "unpublished" not in buyer.lower():
            label = f"Acquired by {buyer}"
        parts.append(label)
    elif status:
        parts.append(status)
    if prop == PROP_SOLD:
        bit = "Campus sold"
        if when:
            bit += f" {when}"
        if buyer and "unpublished" not in buyer.lower():
            bit += f" to {buyer}"
        parts.append(bit)
    elif prop == PROP_LISTED:
        bit = "Campus listed for sale"
        if buyer:
            bit += f" ({buyer})"
        parts.append(bit)
    if not parts:
        return ""
    # Acquired + campus sold would be two clauses; institutional sales are not campus sales.
    return " · ".join(parts)


def _disagreement(
    *,
    status: str,
    scorecard_operating: str,
    fsa_match: str,
    ipeds_bucket: str,
    ipeds_status: str,
    ipeds_year: str,
    ipeds_absent_after: str = "",
) -> str:
    expected = _expected_federal(status)
    if not expected:
        return ""
    problems: list[str] = []
    fsa_campus = fsa_match in {"unitid", "opeid8", "name"}
    ipeds_bits = []
    if ipeds_status:
        ipeds_bits.append(f"inst_status {ipeds_status}")
    if ipeds_year:
        ipeds_bits.append(ipeds_year)
    ipeds_where = " ".join(ipeds_bits)
    if ipeds_absent_after:
        later_years = sorted({int(part) for part in ipeds_absent_after.split(",") if part.strip().isdigit()})
        if later_years:
            later = ", ".join(str(year) for year in later_years)
            ipeds_where = f"{ipeds_where}; no directory row in {later}".strip("; ")

    if expected == "operating":
        if scorecard_operating == "0":
            problems.append("Scorecard school.operating is 0")
        if fsa_campus:
            problems.append("FSA closed-school list matches this campus")
        if ipeds_bucket == "closed":
            problems.append(f"IPEDS shows closed ({ipeds_where})".replace(" ()", ""))
        if ipeds_bucket == "merged":
            problems.append(f"IPEDS shows merged ({ipeds_where})".replace(" ()", ""))
    elif expected == "closed":
        if scorecard_operating == "1":
            problems.append("Scorecard school.operating is 1")
        if ipeds_bucket == "operating":
            problems.append(f"IPEDS shows operating ({ipeds_where})".replace(" ()", ""))
    elif expected == "open_or_merged":
        if scorecard_operating == "0":
            problems.append("Scorecard school.operating is 0")
        if fsa_campus:
            problems.append("FSA closed-school list matches this campus")
        if ipeds_bucket == "closed":
            problems.append(f"IPEDS shows closed ({ipeds_where})".replace(" ()", ""))
    if not problems:
        return ""
    return "Automated check differs from the curated note: " + "; ".join(problems)


def _auto_signal(scorecard_operating: str, fsa_match: str, ipeds_bucket: str) -> str:
    fsa_campus = fsa_match in {"unitid", "opeid8", "name"}
    closed = scorecard_operating == "0" or fsa_campus or ipeds_bucket == "closed"
    opened = scorecard_operating == "1" or ipeds_bucket == "operating"
    merged = ipeds_bucket == "merged"
    if closed and opened:
        return "mixed"
    if closed:
        return "closed"
    if merged and opened:
        return "mixed"
    if merged:
        return "merged"
    if opened:
        return "operating"
    return "unknown"


def _auto_sources(scorecard_operating: str, fsa_match: str, ipeds_year: str) -> str:
    sources: list[str] = []
    if scorecard_operating:
        sources.append("scorecard")
    if fsa_match:
        sources.append("fsa_closed_school")
    if ipeds_year:
        sources.append("ipeds")
    return ";".join(sources)


def build_status_table(
    watch: pd.DataFrame,
    curated: pd.DataFrame,
    *,
    scorecard: pd.DataFrame | None = None,
    fsa_closed: pd.DataFrame | None = None,
    ipeds: pd.DataFrame | None = None,
    auto_checked_at: str = "",
) -> pd.DataFrame:
    """Left-join the watch list to curated status and attach automated signals.

    Curated sale, listing, buyer, date, price, narrative, and source columns
    are copied as-is. Automated frames cannot fill them.
    """
    curated_by_id: dict[int, pd.Series] = {}
    curated_by_name: dict[str, pd.Series] = {}
    if curated is not None and not curated.empty:
        for _, row in curated.iterrows():
            uid = pd.to_numeric(pd.Series([row.get("unitid")]), errors="coerce").iloc[0]
            if pd.notna(uid):
                curated_by_id[int(uid)] = row
            key = _norm_name_key(row.get("inst_name"), row.get("state_abbr"))
            if key.strip("|"):
                curated_by_name.setdefault(key, row)

    rows: list[dict[str, Any]] = []
    for _, school in watch.iterrows():
        uid_num = pd.to_numeric(pd.Series([school.get("unitid")]), errors="coerce").iloc[0]
        curated_row = None
        if pd.notna(uid_num) and int(uid_num) in curated_by_id:
            curated_row = curated_by_id[int(uid_num)]
        else:
            curated_row = curated_by_name.get(_norm_name_key(school.get("inst_name"), school.get("state_abbr")))
        rec: dict[str, Any] = {
            "watchlist_rank": _blank(school.get("watchlist_rank")),
            "unitid": "" if pd.isna(uid_num) else str(int(uid_num)),
            "opeid6": _blank(school.get("opeid6")),
            "opeid8": _blank(school.get("opeid8")),
            "inst_name": _blank(school.get("inst_name")),
            "state_abbr": _blank(school.get("state_abbr")),
        }
        for col in CURATED_LOCK_COLUMNS:
            rec[col] = _blank(curated_row.get(col)) if curated_row is not None else ""
        # Identity stays with the watch list even if the curated name drifts.
        if not rec["inst_name"]:
            rec["inst_name"] = _blank(school.get("inst_name"))
        if not rec["state_abbr"]:
            rec["state_abbr"] = _blank(school.get("state_abbr"))
        fsa = match_fsa_row(school, fsa_closed if fsa_closed is not None else pd.DataFrame())
        ip = _ipeds_for_unit(ipeds if ipeds is not None else pd.DataFrame(), uid_num)
        sc = _scorecard_value(scorecard, uid_num)
        rec.update(fsa)
        rec.update(ip)
        rec["auto_scorecard_operating"] = sc
        rec["auto_checked_at"] = auto_checked_at
        bucket = _ipeds_bucket(ip["auto_ipeds_status"], ip["auto_ipeds_date_closed"])
        rec["auto_signal"] = _auto_signal(sc, fsa["auto_fsa_match"], bucket)
        rec["auto_sources"] = _auto_sources(sc, fsa["auto_fsa_match"], ip["auto_ipeds_year"])
        rec["disagreement"] = _disagreement(
            status=rec["status"],
            scorecard_operating=sc,
            fsa_match=fsa["auto_fsa_match"],
            ipeds_bucket=bucket,
            ipeds_status=ip["auto_ipeds_status"],
            ipeds_year=ip["auto_ipeds_year"],
            ipeds_absent_after=ip["auto_ipeds_absent_after"],
        )
        rec["status_badge"] = status_badge(rec)
        rec["property_source"] = "curated" if curated_row is not None else ""
        rows.append(rec)
    out = pd.DataFrame(rows)
    for col in OUTPUT_COLUMNS:
        if col not in out.columns:
            out[col] = ""
    return out[OUTPUT_COLUMNS]


def normalize_closed_school_frame(raw: pd.DataFrame) -> pd.DataFrame:
    """Map a closed-school table onto opeid_raw / closed_name / closed_date / unitid."""
    if raw is None or raw.empty:
        return pd.DataFrame(columns=["opeid_raw", "closed_name", "closed_date", "unitid"])
    frame = raw.copy()
    frame.columns = [str(c).strip() for c in frame.columns]
    opeid_col = _guess_col(frame, ["opeid", "ope_id", "ope id", "opecode"])
    name_col = _guess_col(frame, ["school", "institution", "name"])
    date_col = _guess_col(frame, ["close_date", "closedate", "date_closed", "closure", "closed"])
    unit_col = _guess_col(frame, ["unitid", "unit_id", "unit id"])
    if opeid_col is None and not any(k in " ".join(frame.columns).lower() for k in ("ope", "school", "name")):
        detected = _detect_header_frame(frame)
        if detected is not None:
            return normalize_closed_school_frame(detected)
    if opeid_col is None:
        LOGGER.warning("Closed-school table has no OPEID column: %s", list(frame.columns)[:12])
        return pd.DataFrame(columns=["opeid_raw", "closed_name", "closed_date", "unitid"])
    out = pd.DataFrame(
        {
            "opeid_raw": frame[opeid_col].map(_blank),
            "closed_name": frame[name_col].map(_blank) if name_col else "",
            "closed_date": frame[date_col].map(_blank) if date_col else "",
            "unitid": frame[unit_col].map(_blank) if unit_col else "",
        }
    )
    out = out[out["opeid_raw"] != ""]
    return out.reset_index(drop=True)


def _detect_header_frame(raw: pd.DataFrame) -> pd.DataFrame | None:
    """Find a header row when a spreadsheet title sits above the column names."""
    preview = raw.head(25).fillna("")
    for idx, row in preview.iterrows():
        cells = [str(v).strip().lower() for v in row.tolist()]
        joined = " ".join(cells)
        if "ope" in joined and ("name" in joined or "school" in joined or "close" in joined):
            header = [str(v).strip() or f"col_{i}" for i, v in enumerate(row.tolist())]
            body = raw.loc[raw.index > idx].copy()
            body.columns = header
            return body
    return None


def read_closed_school_file(path: Path) -> pd.DataFrame:
    raw = _read_tabular(path)
    detected = _detect_header_frame(raw)
    if detected is not None:
        raw = detected
    return normalize_closed_school_frame(raw)


def fetch_fsa_closed_schools(settings: Settings) -> tuple[pd.DataFrame, str]:
    """Download the FSA closed-school search file if a public URL still works.

    Returns an empty frame and a plain note when every URL fails. Does not
    invent closure rows.
    """
    cfg = settings.raw.get("fsa") or {}
    urls: list[str] = []
    for extra in (
        "https://fsapartners.ed.gov/sites/default/files/2026-10/ClosedSchoolSearchFile.xls",
        "https://fsapartners.ed.gov/sites/default/files/2026-10/ClosedSchoolSearchFile.xlsx",
    ):
        urls.append(extra)
    for extra in _discover_closed_school_urls():
        if extra not in urls:
            urls.append(extra)
    for extra in cfg.get("closed_school_urls") or []:
        if extra not in urls:
            urls.append(extra)
    path = download_first(
        urls,
        settings.raw_dir / "status",
        "closed_school",
        timeout=(8, 25),
        max_retries=1,
        source="status_closed_school",
    )
    if path is None:
        return pd.DataFrame(), (
            "FSA closed-school file not downloaded. Tried the Partner Connect page "
            "and the configured ClosedSchoolSearchFile URLs; none returned a spreadsheet."
        )
    frame = read_closed_school_file(path)
    if frame.empty:
        return frame, f"FSA file downloaded ({path.name}) but no OPEID column was found."
    return frame, f"FSA closed-school file {path.name}: {len(frame)} rows with an OPEID."


def _ipeds_cache_path(settings: Settings) -> Path:
    return settings.raw_dir / "status" / "ipeds_directory_cache.json"


def fetch_ipeds_directory(
    unitids: list[int],
    *,
    get_json: Callable[[int, int], tuple[int, dict | None]] | None = None,
    years: list[int] | None = None,
    cache_path: Path | None = None,
) -> tuple[pd.DataFrame, str]:
    """Latest Urban IPEDS directory row per UNITID (inst_status, date_closed).

    Years are tried newest first. A missing later year is not treated as a
    closure; the newest year that actually has a row is kept. ``get_json``
    returns ``(status_code, payload)`` and is injectable for tests.
    """
    import json

    years = list(years or [2025, 2024, 2023, 2022, 2021])
    cache: dict[str, Any] = {}
    if cache_path and cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cache = {}

    def _default_get(year: int, unitid: int) -> tuple[int, dict | None]:
        url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/directory/{year}/"
        try:
            resp = requests.get(
                url,
                params={"unitid": unitid},
                headers=DEFAULT_HEADERS,
                timeout=25,
            )
        except requests.RequestException as exc:
            LOGGER.info("IPEDS directory request failed %s %s: %s", year, unitid, exc)
            return 0, None
        if resp.status_code >= 400:
            return resp.status_code, None
        try:
            payload = resp.json()
        except ValueError:
            return resp.status_code, None
        return resp.status_code, payload if isinstance(payload, dict) else None

    getter = get_json or _default_get
    dead_years: set[int] = set()
    rows: list[dict[str, Any]] = []
    hits = 0
    for unitid in unitids:
        found = None
        absent_after: list[str] = []
        for year in years:
            if year in dead_years:
                continue
            key = f"{year}:{unitid}"
            if key in cache:
                status_code = int(cache[key].get("status") or 0)
                payload = cache[key].get("payload")
            else:
                status_code, payload = getter(year, unitid)
                cache[key] = {"status": status_code, "payload": payload}
            if status_code == 404:
                dead_years.add(year)
                continue
            results = (payload or {}).get("results") if isinstance(payload, dict) else None
            if results:
                found = dict(results[0])
                found["year"] = found.get("year") or year
                found["ipeds_absent_after"] = ",".join(absent_after)
                break
            if status_code == 200:
                absent_after.append(str(year))
        if found:
            hits += 1
            rows.append(found)
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache), encoding="utf-8")
    note = (
        f"IPEDS directory via Urban API, years {years[0]}–{years[-1]} newest first: "
        f"{hits} of {len(unitids)} UNITIDs returned a row."
    )
    if not rows:
        note = (
            "IPEDS directory via Urban API returned no rows for this watch-list slice "
            f"(years tried: {', '.join(str(y) for y in years)})."
        )
    return pd.DataFrame(rows), note


def _load_local_scorecard(settings: Settings) -> pd.DataFrame:
    path = settings.processed_dir / "scorecard_operating.parquet"
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_parquet(path)
    except Exception as exc:  # noqa: BLE001
        LOGGER.info("Local Scorecard snapshot unreadable: %s", exc)
        return pd.DataFrame()


def collect_automated(
    settings: Settings,
    watch: pd.DataFrame,
    *,
    skip_network: bool = False,
    http_get=None,
    ipeds_get=None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, str]]:
    """Pull Scorecard, FSA, and IPEDS signals. Each source may come back empty."""
    notes: dict[str, str] = {}
    unitids = [
        int(v)
        for v in pd.to_numeric(watch.get("unitid"), errors="coerce").dropna().tolist()
    ]
    scorecard = pd.DataFrame()
    if skip_network:
        notes["scorecard"] = "Scorecard skipped (--skip-network)."
    elif not scorecard_api_key(settings):
        local = _load_local_scorecard(settings)
        if local.empty:
            notes["scorecard"] = (
                "Scorecard skipped: DATA_GOV_API_KEY / SCORECARD_API_KEY is unset, "
                "and data/processed/scorecard_operating.parquet is not present."
            )
        else:
            scorecard = local
            notes["scorecard"] = (
                f"Scorecard API skipped (no API key). Used local scorecard_operating.parquet "
                f"({len(local)} rows)."
            )
    else:
        scorecard = fetch_operating_by_unitids(settings, unitids, http_get=http_get)
        if scorecard.empty:
            local = _load_local_scorecard(settings)
            if not local.empty:
                scorecard = local
                notes["scorecard"] = (
                    "Scorecard API returned no rows. Used local scorecard_operating.parquet "
                    f"({len(local)} rows)."
                )
            else:
                notes["scorecard"] = "Scorecard API key is set, but the operating lookup returned no rows."
        else:
            notes["scorecard"] = f"Scorecard API school.operating for {len(scorecard)} UNITIDs."

    if skip_network:
        fsa = pd.DataFrame()
        notes["fsa"] = "FSA closed-school list skipped (--skip-network)."
        ipeds = pd.DataFrame()
        notes["ipeds"] = "IPEDS directory skipped (--skip-network)."
    else:
        fsa, notes["fsa"] = fetch_fsa_closed_schools(settings)
        ipeds, notes["ipeds"] = fetch_ipeds_directory(
            unitids,
            get_json=ipeds_get,
            cache_path=None if ipeds_get else _ipeds_cache_path(settings),
        )
    return scorecard, fsa, ipeds, notes


def badge_class(row: pd.Series | dict[str, Any]) -> str:
    getter = row.get
    prop = _blank(getter("property_disposition"))
    status = _blank(getter("status"))
    if prop == PROP_LISTED:
        return "badge-listed"
    if prop == PROP_SOLD:
        return "badge-sold"
    if status == STATUS_MERGED:
        return "badge-merged"
    if status == STATUS_NOT_ENROLLING:
        return "badge-enroll"
    if status == STATUS_CLOSED:
        return "badge-closed"
    if status == STATUS_OPEN:
        return "badge-open"
    return "badge-unknown"


def _source_html(source_url: str) -> str:
    parts = [p.strip() for p in re.split(r"\s*;\s*", _blank(source_url)) if p.strip()]
    if not parts:
        return ""
    rendered: list[str] = []
    for part in parts:
        match = re.search(r"https?://[^\s]+", part)
        if not match:
            rendered.append(html.escape(part))
            continue
        url = match.group(0).rstrip(").,")
        before = html.escape(part[: match.start()])
        after = html.escape(part[match.end() :])
        link = f'<a href="{html.escape(url, quote=True)}">{html.escape(url)}</a>'
        rendered.append(f"{before}{link}{after}")
    return "; ".join(rendered)


def status_block_html(row: pd.Series | dict[str, Any]) -> str:
    """Evidence-card fragment. Empty when there is no curated or badge text."""
    badge = _blank(row.get("status_badge")) or status_badge(row)
    detail = _blank(row.get("status_detail"))
    if not badge and not detail:
        return ""
    kind = badge_class(row)
    prop_sentence = _blank(row.get("sold_listed_details"))
    if prop_sentence and prop_sentence.lower().startswith("n/a"):
        prop_html = ""
    elif prop_sentence and prop_sentence != detail:
        prop_html = f'<p class="status-detail">{html.escape(prop_sentence)}</p>'
    else:
        prop_html = ""
    sale_bits: list[str] = []
    prop = _blank(row.get("property_disposition"))
    if prop in {PROP_SOLD, PROP_LISTED, PROP_INSTITUTIONAL}:
        buyer = _blank(row.get("buyer_or_broker"))
        when = _blank(row.get("event_date"))
        price = _blank(row.get("sale_price_published"))
        if buyer:
            sale_bits.append(f"Buyer / broker: {buyer}")
        if when:
            sale_bits.append(f"Date: {when}")
        if price:
            sale_bits.append(f"Published price: {price}")
    sale_html = f'<p class="status-sale">{html.escape(" · ".join(sale_bits))}</p>' if sale_bits else ""
    checked = _blank(row.get("checked_at"))
    sources = _source_html(_blank(row.get("source_url")))
    meta_bits = []
    if checked:
        meta_bits.append(f"Curated check {html.escape(checked)}")
    if sources:
        meta_bits.append(f"Sources: {sources}")
    meta_html = f'<p class="status-src">{" · ".join(meta_bits)}.</p>' if meta_bits else ""
    disagree = _blank(row.get("disagreement"))
    disagree_html = f'<p class="status-disagree">{html.escape(disagree)}</p>' if disagree else ""
    detail_html = f'<p class="status-detail">{html.escape(detail)}</p>' if detail else ""
    badge_html = f'<p><span class="badge {kind}">{html.escape(badge)}</span></p>' if badge else ""
    return (
        '<div class="status-block">'
        f"{badge_html}{detail_html}{prop_html}{sale_html}{meta_html}{disagree_html}"
        "</div>"
    )


STATUS_CSS = """
    .badge { display: inline-block; font-family: sans-serif; font-size: 0.82rem;
             letter-spacing: 0.01em; padding: 0.12rem 0.55rem; border-radius: 3px;
             border: 1px solid transparent; }
    .badge-open { background: #e7f6ec; border-color: #b7d7c2; }
    .badge-enroll { background: #eef3ff; border-color: #c5d2f2; }
    .badge-closed { background: #fde8e8; border-color: #e4b4b4; }
    .badge-sold { background: #fff3d6; border-color: #e0c48a; }
    .badge-listed { background: #fde8e8; border-color: #c45c5c; }
    .badge-merged { background: #f3e8ff; border-color: #d2b8ef; }
    .badge-unknown { background: #f4f4f4; border-color: #ddd; }
    .status-block { margin: 0.6rem 0 0.2rem; }
    .status-detail, .status-sale, .status-src { margin: 0.25rem 0; }
    .status-src { color: #555; font-size: 0.92rem; word-break: break-word; }
    .status-disagree { background: #fff6e5; border: 1px solid #e0c48a; padding: 0.35rem 0.55rem;
                       font-size: 0.92rem; }
"""

BANNER_SENTENCE = (
    " Current-status badges are a later check (curated notes plus federal operating flags). "
    "They are not part of the score and not closure predictions. Campus sales and for-sale "
    "listings come only from the curated file; College Scorecard, FSA, and IPEDS do not report them."
)

OPEN_BUCKET = "open"
TEACHOUT_BUCKET = "not_enrolling"
CLOSED_BUCKET = "closed"
UNKNOWN_BUCKET = "unknown"


def stamp_report_html(html_text: str, status: pd.DataFrame) -> str:
    """Insert or replace a status block on each evidence card, matched by UNITID."""
    by_id: dict[str, pd.Series] = {}
    if status is not None and not status.empty and "unitid" in status.columns:
        for _, row in status.iterrows():
            uid = _blank(row.get("unitid")).split(".")[0]
            if uid:
                by_id[uid] = row

    def _repl(match: re.Match[str]) -> str:
        card = match.group(0)
        found = _UNITID_RE.search(card)
        if not found or found.group(1) not in by_id:
            return card
        block = status_block_html(by_id[found.group(1)])
        if not block:
            return card
        if _STATUS_BLOCK_RE.search(card):
            return _STATUS_BLOCK_RE.sub("\n      " + block, card, count=1)
        needle = "not a closure verdict.</p>"
        idx = card.find(needle)
        if idx == -1:
            return card
        at = idx + len(needle)
        return card[:at] + "\n      " + block + card[at:]

    updated = _CARD_RE.sub(_repl, html_text)
    if ".status-block {" not in updated and "</style>" in updated:
        updated = updated.replace("</style>", STATUS_CSS + "\n  </style>", 1)
    anchor = "not a model input."
    if "Current-status badges" not in updated and anchor in updated:
        updated = updated.replace(anchor, anchor + BANNER_SENTENCE, 1)
    return updated


def operating_bucket(row: pd.Series | dict[str, Any]) -> str:
    """Place one ranked row: open, teach-out, closed, or unknown.

    A curated ``closed`` row or a recorded campus sale stays closed even when
    IPEDS or Scorecard still shows the parent system as operating (a closed
    DeVry or Strayer location, for example). A curated ``merged_acquired``
    row stays off the open list unless it is an ``institutional_sale`` that
    leaves the same school operating. IPEDS ``inst_status`` closed or
    merged, or a real close date, also counts as closed. ``not_enrolling``
    stays in the teach-out bucket unless IPEDS itself records a closure.
    """
    status = _blank(row.get("status"))
    prop = _blank(row.get("property_disposition"))
    ipeds = _ipeds_bucket(
        _blank(row.get("auto_ipeds_status")),
        _blank(row.get("auto_ipeds_date_closed")),
    )
    scorecard = _blank(row.get("auto_scorecard_operating"))
    federal_closed = ipeds in {"closed", "merged"} or scorecard == "0"
    if status == STATUS_CLOSED or prop == PROP_SOLD:
        return CLOSED_BUCKET
    if status == STATUS_MERGED and prop != PROP_INSTITUTIONAL:
        return CLOSED_BUCKET
    if status == STATUS_NOT_ENROLLING:
        if ipeds in {"closed", "merged"}:
            return CLOSED_BUCKET
        return TEACHOUT_BUCKET
    if federal_closed:
        return CLOSED_BUCKET
    if status in {STATUS_OPEN, STATUS_MERGED}:
        return OPEN_BUCKET
    if ipeds == "operating":
        return OPEN_BUCKET
    if scorecard == "1":
        return OPEN_BUCKET
    return UNKNOWN_BUCKET


def prefix_through_open(table: pd.DataFrame, open_n: int) -> pd.DataFrame:
    """Rows from rank 1 through the row that fills ``open_n`` still-operating schools."""
    if table.empty:
        return table.copy()
    if open_n <= 0:
        return table.iloc[0:0].copy()
    seen = 0
    cutoff = len(table)
    for i, (_, row) in enumerate(table.iterrows()):
        if operating_bucket(row) == OPEN_BUCKET:
            seen += 1
            if seen >= open_n:
                cutoff = i + 1
                break
    return table.iloc[:cutoff].copy()


def partition_operating(
    table: pd.DataFrame, open_n: int
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, int]:
    """Split the walked prefix into open, teach-out, and closed frames.

    The depth is the watch-list rank of the last row walked (the rank of the
    last still-operating school when the open list fills).
    """
    prefix = prefix_through_open(table, open_n)
    grouped: dict[str, list[pd.Series]] = {
        OPEN_BUCKET: [],
        TEACHOUT_BUCKET: [],
        CLOSED_BUCKET: [],
    }
    for _, row in prefix.iterrows():
        bucket = operating_bucket(row)
        if bucket in grouped:
            grouped[bucket].append(row)

    def _frame(rows: list[pd.Series]) -> pd.DataFrame:
        if not rows:
            return prefix.iloc[0:0].copy()
        return pd.DataFrame(rows)

    depth = 0
    if not prefix.empty and "watchlist_rank" in prefix.columns:
        try:
            depth = int(float(prefix.iloc[-1]["watchlist_rank"]))
        except (TypeError, ValueError):
            depth = int(len(prefix))
    return (
        _frame(grouped[OPEN_BUCKET]),
        _frame(grouped[TEACHOUT_BUCKET]),
        _frame(grouped[CLOSED_BUCKET]),
        depth,
    )


def _unitid_int(value: Any) -> int | None:
    try:
        if value is None or pd.isna(value):
            return None
    except (TypeError, ValueError):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def federal_operating_curated_fields(row: pd.Series | dict[str, Any], checked_at: str) -> dict[str, str]:
    """Curated-shaped note for a school IPEDS (and Scorecard, when used) shows as operating."""
    uid = _unitid_int(row.get("unitid"))
    uid_txt = "" if uid is None else str(uid)
    year = _blank(row.get("auto_ipeds_year"))
    if year:
        try:
            year = str(int(float(year)))
        except (TypeError, ValueError):
            pass
    code = _blank(row.get("auto_ipeds_status"))
    if code:
        try:
            code = str(int(float(code)))
        except (TypeError, ValueError):
            pass
    scorecard = _blank(row.get("auto_scorecard_operating"))
    bits: list[str] = []
    sources: list[str] = []
    if year:
        bits.append(f"IPEDS directory {year} inst_status {code or 'unknown'}")
        sources.append(
            "https://educationdata.urban.org/api/v1/college-university/ipeds/directory/"
            f"{year}/?unitid={uid_txt}"
        )
    if scorecard == "1":
        bits.append("College Scorecard school.operating is 1")
        sources.append(f"https://collegescorecard.ed.gov/school/?{uid_txt}")
    if not bits:
        bits.append("no newer closure flag in the federal operating check")
    rank = _blank(row.get("watchlist_rank"))
    try:
        rank = str(int(float(rank))) if rank else ""
    except (TypeError, ValueError):
        pass
    return {
        "unitid": uid_txt,
        "opeid6": _blank(row.get("opeid6")),
        "opeid8": _blank(row.get("opeid8")),
        "watchlist_rank": rank,
        "inst_name": _blank(row.get("inst_name")),
        "state_abbr": _blank(row.get("state_abbr")),
        "status": STATUS_OPEN,
        "status_detail": "Still operating (" + "; ".join(bits) + ").",
        "property_disposition": PROP_NA,
        "buyer_or_broker": "",
        "event_date": "",
        "sale_price_published": "",
        "sold_listed_details": "",
        "source_url": "; ".join(sources),
        "checked_at": checked_at,
        "library_notes": "",
    }


def append_curated_rows(path: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Append still-operating rows. Existing curated lines are left byte-for-byte."""
    if not rows or not path.exists():
        return []
    existing = load_curated(path)
    have: set[int] = set()
    if not existing.empty and "unitid" in existing.columns:
        have = {
            uid
            for uid in (_unitid_int(v) for v in existing["unitid"].tolist())
            if uid is not None
        }
    fresh: list[dict[str, str]] = []
    for row in rows:
        uid = _unitid_int(row.get("unitid"))
        if uid is None or uid in have:
            continue
        have.add(uid)
        fresh.append({col: _blank(row.get(col)) for col in CURATED_COLUMNS})
    if not fresh:
        return []
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        text += "\n"
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=list(CURATED_COLUMNS),
        lineterminator="\n",
        extrasaction="ignore",
    )
    for row in fresh:
        writer.writerow(row)
    path.write_text(text + buf.getvalue(), encoding="utf-8")
    return fresh


def apply_operating_notes(table: pd.DataFrame, notes_by_uid: dict[int, dict[str, str]]) -> pd.DataFrame:
    """Copy newly appended curated fields onto the status table. Other rows stay put."""
    if table.empty or not notes_by_uid:
        return table
    out = table.copy()
    fields = (
        "status",
        "status_detail",
        "property_disposition",
        "buyer_or_broker",
        "event_date",
        "sale_price_published",
        "sold_listed_details",
        "source_url",
        "checked_at",
    )
    for idx, row in out.iterrows():
        uid = _unitid_int(row.get("unitid"))
        note = notes_by_uid.get(uid) if uid is not None else None
        if not note:
            continue
        for col in fields:
            out.at[idx, col] = note.get(col, "")
        out.at[idx, "property_source"] = "curated"
        updated = out.loc[idx]
        out.at[idx, "disagreement"] = _disagreement(
            status=_blank(updated.get("status")),
            scorecard_operating=_blank(updated.get("auto_scorecard_operating")),
            fsa_match=_blank(updated.get("auto_fsa_match")),
            ipeds_bucket=_ipeds_bucket(
                _blank(updated.get("auto_ipeds_status")),
                _blank(updated.get("auto_ipeds_date_closed")),
            ),
            ipeds_status=_blank(updated.get("auto_ipeds_status")),
            ipeds_year=_blank(updated.get("auto_ipeds_year")),
            ipeds_absent_after=_blank(updated.get("auto_ipeds_absent_after")),
        )
        out.at[idx, "status_badge"] = status_badge(out.loc[idx])
    return out


def _scorecard_for_ids(
    settings: Settings,
    unitids: list[int],
    *,
    http_get=None,
) -> tuple[pd.DataFrame, str, bool]:
    """Scorecard operating flags for one slice.

    The third value is True when the API key is missing and the note is final
    (callers should not keep retrying).
    """
    if not scorecard_api_key(settings):
        local = _load_local_scorecard(settings)
        if local.empty:
            return (
                pd.DataFrame(),
                (
                    "Scorecard skipped: DATA_GOV_API_KEY / SCORECARD_API_KEY is unset, "
                    "and data/processed/scorecard_operating.parquet is not present."
                ),
                True,
            )
        return (
            local,
            (
                "Scorecard API skipped (no API key). Used local scorecard_operating.parquet "
                f"({len(local)} rows)."
            ),
            True,
        )
    got = fetch_operating_by_unitids(settings, unitids, http_get=http_get)
    return got, "", False


def _acquisition_status_detail(row: pd.Series) -> str:
    """Curated sentence for a school that enters the residential-campus list."""
    from college_closure.campus import _num, is_small_housing

    capacity = _num(row.get("dormitory_capacity"))
    year = _blank(row.get("housing_year"))
    if year:
        try:
            year = str(int(float(year)))
        except (TypeError, ValueError):
            pass
    acres = _blank(row.get("acreage"))
    bits = ["Still operating"]
    if capacity is not None and capacity > 0:
        cap_txt = str(int(capacity)) if capacity == int(capacity) else str(capacity)
        small = " (small housing)" if is_small_housing(row) else ""
        year_bit = f", IPEDS IC {year}" if year else ""
        bits.append(f"on-campus dorm capacity {cap_txt}{small}{year_bit}")
    if acres:
        bits.append(f"own campus, {acres} acres")
    else:
        bits.append("own campus; acreage not stated in the land source")
    note = _blank(row.get("campus_notes"))
    sentence = "; ".join(bits) + "."
    if note:
        sentence = f"{sentence} {note}"
    return sentence


def _walk_until_open(
    settings: Settings,
    watch: pd.DataFrame,
    curated: pd.DataFrame,
    *,
    open_n: int,
    checked_at: str,
    skip_network: bool,
    http_get=None,
    ipeds_get=None,
    housing: pd.DataFrame | None = None,
    land: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, dict[str, str]]:
    """Classify ranked rows until ``open_n`` are acquisition-ready residential campuses."""
    from college_closure.campus import acquisition_ready, attach_campus, prefix_through_acquisition

    def _ready_prefix(frame: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        joined = attach_campus(frame, housing, land)
        ready = int(sum(acquisition_ready(row) for _, row in joined.iterrows())) if not joined.empty else 0
        return joined, ready

    if skip_network or watch.empty:
        scorecard, fsa, ipeds, notes = collect_automated(
            settings,
            watch,
            skip_network=True,
            http_get=http_get,
            ipeds_get=ipeds_get,
        )
        table = build_status_table(
            watch,
            curated,
            scorecard=scorecard,
            fsa_closed=fsa,
            ipeds=ipeds,
            auto_checked_at=checked_at,
        )
        joined, _ready = _ready_prefix(table)
        return prefix_through_acquisition(joined, open_n), notes

    fsa, fsa_note = fetch_fsa_closed_schools(settings)
    parts: list[pd.DataFrame] = []
    sc_hits = 0
    sc_final_note = ""
    ip_hits = 0
    ip_tried = 0
    batch = 25
    cache_path = None if ipeds_get else _ipeds_cache_path(settings)
    for start in range(0, len(watch), batch):
        chunk = watch.iloc[start : start + batch]
        ids = [uid for uid in (_unitid_int(v) for v in chunk["unitid"].tolist()) if uid is not None]
        if sc_final_note:
            scorecard = pd.DataFrame()
            if "local scorecard_operating.parquet" in sc_final_note:
                scorecard, sc_final_note, _ = _scorecard_for_ids(settings, ids, http_get=http_get)
        else:
            scorecard, note, finished = _scorecard_for_ids(settings, ids, http_get=http_get)
            if finished:
                sc_final_note = note
            else:
                sc_hits += len(scorecard)
        ipeds, ip_note = fetch_ipeds_directory(ids, get_json=ipeds_get, cache_path=cache_path)
        if not ipeds.empty and "unitid" in ipeds.columns:
            ip_hits += int(pd.to_numeric(ipeds["unitid"], errors="coerce").nunique())
        ip_tried += len(ids)
        LOGGER.info("IPEDS walk batch rank %s–%s: %s", start + 1, start + len(chunk), ip_note)
        part = build_status_table(
            chunk,
            curated,
            scorecard=scorecard,
            fsa_closed=fsa,
            ipeds=ipeds,
            auto_checked_at=checked_at,
        )
        parts.append(part)
        combined = pd.concat(parts, ignore_index=True)
        joined, ready = _ready_prefix(combined)
        if ready >= open_n:
            table = prefix_through_acquisition(joined, open_n)
            break
    else:
        raw = pd.concat(parts, ignore_index=True) if parts else watch.iloc[0:0].copy()
        table, _ready = _ready_prefix(raw)

    if sc_final_note:
        scorecard_note = sc_final_note
    elif sc_hits:
        scorecard_note = f"College Scorecard school.operating returned {sc_hits} UNITID(s)."
    else:
        scorecard_note = "Scorecard API key is set, but the operating lookup returned no rows."
    notes = {
        "scorecard": scorecard_note,
        "fsa": fsa_note,
        "ipeds": (
            "IPEDS directory via Urban API, years 2025–2021 newest first: "
            f"{ip_hits} of {ip_tried} UNITIDs returned a row."
        ),
    }
    return table, notes


def refresh_markdown(
    notes: dict[str, str],
    table: pd.DataFrame,
    *,
    checked_at: str,
    top_n: int,
    open_count: int | None = None,
    depth: int | None = None,
    curated_note: str | None = None,
) -> str:
    disagree = 0
    if not table.empty and "disagreement" in table.columns:
        disagree = int(table["disagreement"].map(_blank).ne("").sum())
    sold = 0
    listed = 0
    if not table.empty and "property_disposition" in table.columns:
        sold = int(table["property_disposition"].eq(PROP_SOLD).sum())
        listed = int(table["property_disposition"].eq(PROP_LISTED).sum())
    lines = [
        "# Current-status refresh",
        "",
        f"Run date: {checked_at}",
        f"Watch-list rows: {top_n if table.empty else len(table)}",
    ]
    if open_count is not None:
        lines.append(f"Residential own-campus schools in the main list: {open_count}")
        lines.append(
            "The main list keeps schools that are still operating, have on-campus dorms, "
            "and have their own campus. Scores remain 2022 federal financial data."
        )
    if depth:
        lines.append(f"Ranked rows walked to fill that list: {depth}")
    lines.extend(
        [
            f"Curated rows with a disagreement flag: {disagree}",
            f"Curated campus-sold rows: {sold}",
            f"Curated campus-listed rows: {listed}",
            "",
            "## Sources this run",
            "",
            f"- Scorecard: {notes.get('scorecard', 'not run')}",
            f"- FSA closed-school list: {notes.get('fsa', 'not run')}",
            f"- IPEDS directory: {notes.get('ipeds', 'not run')}",
            "",
            SALE_LISTING_NOTE,
            "",
            curated_note
            or "The curated file `data/status/status_curated.csv` was not modified.",
            "Disagreement text is a flag. It does not replace the curated status, buyer, date, or price.",
            "",
        ]
    )
    return "\n".join(lines)


def write_status_outputs(
    settings: Settings,
    table: pd.DataFrame,
    notes: dict[str, str],
    *,
    checked_at: str,
    top_n: int,
    write_html: bool = True,
    open_count: int | None = None,
    depth: int | None = None,
    curated_note: str | None = None,
    watch: pd.DataFrame | None = None,
    open_n: int = 50,
) -> dict[str, str]:
    out_dir = settings.outputs_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "status_current.csv"
    table.to_csv(csv_path, index=False)
    md_path = out_dir / "status_refresh.md"
    md_path.write_text(
        refresh_markdown(
            notes,
            table,
            checked_at=checked_at,
            top_n=top_n,
            open_count=open_count,
            depth=depth,
            curated_note=curated_note,
        ),
        encoding="utf-8",
    )
    html_path = out_dir / "top50_report.html"
    if write_html and watch is not None:
        from college_closure.report import write_operating_report

        write_operating_report(
            html_path,
            watch,
            table,
            open_n=open_n,
            score_year=_score_year(watch),
        )
    return {"csv": str(csv_path), "markdown": str(md_path), "html": str(html_path)}


def _score_year(watch: pd.DataFrame) -> int:
    if watch is None or watch.empty or "year" not in watch.columns:
        return 2022
    try:
        return int(float(watch.iloc[0]["year"]))
    except (TypeError, ValueError):
        return 2022


def _opeid_lookup(watch: pd.DataFrame) -> dict[int, dict[str, str]]:
    out: dict[int, dict[str, str]] = {}
    if watch.empty or "unitid" not in watch.columns:
        return out
    for _, row in watch.iterrows():
        uid = _unitid_int(row.get("unitid"))
        if uid is None:
            continue
        out[uid] = {
            "opeid6": _blank(row.get("opeid6")),
            "opeid8": _blank(row.get("opeid8")),
        }
    return out


def run_status_check(
    settings: Settings,
    *,
    top_n: int = 0,
    open_n: int = 50,
    skip_network: bool = False,
    write_html: bool = True,
    watchlist: Path | None = None,
    auto_checked_at: str | None = None,
    http_get=None,
    ipeds_get=None,
    scorecard: pd.DataFrame | None = None,
    fsa_closed: pd.DataFrame | None = None,
    ipeds: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Walk the ranked list until ``open_n`` schools are residential own-campus and still operating.

    ``top_n`` limits how many ranked rows are scanned. ``0`` scans the whole
    watch list and, when ``data/processed/scored.parquet`` exists, rows past
    that list. Caller-supplied Scorecard, FSA, or IPEDS frames skip the network
    and classify only the scanned slice. Existing curated rows are not
    overwritten. Acquisition-ready schools missing from the curated file are
    appended, using the campus land source rather than an IPEDS directory URL.
    """
    from college_closure.campus import (
        acquisition_ready,
        attach_campus,
        campus_land_path,
        exclusion_reason,
        extend_ranked_universe,
        housing_snapshot_path,
        load_campus_land,
        load_housing_snapshot,
        partition_acquisition,
        prefix_through_acquisition,
    )

    checked = auto_checked_at or date.today().isoformat()
    watch_path = watchlist or (settings.outputs_dir / "watchlist.csv")
    watch = load_watchlist(watch_path, top_n)
    if top_n <= 0:
        scored_path = settings.processed_dir / "scored.parquet"
        scored = None
        if scored_path.exists():
            try:
                scored = pd.read_parquet(scored_path)
            except Exception as exc:  # noqa: BLE001
                LOGGER.info("scored.parquet unreadable: %s", exc)
                scored = None
        if scored is None or getattr(scored, "empty", True):
            from college_closure.campus import load_ranked_universe, ranked_universe_path

            scored = load_ranked_universe(ranked_universe_path(settings))
        watch = extend_ranked_universe(watch, scored)
    housing = load_housing_snapshot(housing_snapshot_path(settings))
    land = load_campus_land(campus_land_path(settings))
    curated_file = curated_path(settings)
    curated = load_curated(curated_file)
    injected = scorecard is not None or fsa_closed is not None or ipeds is not None
    if injected:
        notes = {
            "scorecard": "provided by caller" if scorecard is not None else "not provided",
            "fsa": "provided by caller" if fsa_closed is not None else "not provided",
            "ipeds": "provided by caller" if ipeds is not None else "not provided",
        }
        scorecard = scorecard if scorecard is not None else pd.DataFrame()
        fsa_closed = fsa_closed if fsa_closed is not None else pd.DataFrame()
        ipeds = ipeds if ipeds is not None else pd.DataFrame()
        table = build_status_table(
            watch,
            curated,
            scorecard=scorecard,
            fsa_closed=fsa_closed,
            ipeds=ipeds,
            auto_checked_at=checked,
        )
        table = prefix_through_acquisition(attach_campus(table, housing, land), open_n)
    else:
        table, notes = _walk_until_open(
            settings,
            watch,
            curated,
            open_n=open_n,
            checked_at=checked,
            skip_network=skip_network,
            http_get=http_get,
            ipeds_get=ipeds_get,
            housing=housing,
            land=land,
        )
    open_df, _excluded, _teach, _closed, depth = partition_acquisition(table, open_n)
    opeids = _opeid_lookup(watch)
    new_rows: list[dict[str, str]] = []
    for _, row in open_df.iterrows():
        payload = row.to_dict()
        uid = _unitid_int(row.get("unitid"))
        extra = opeids.get(uid) if uid is not None else None
        if extra:
            payload.setdefault("opeid6", extra.get("opeid6", ""))
            payload["opeid6"] = payload.get("opeid6") or extra.get("opeid6", "")
            payload["opeid8"] = payload.get("opeid8") or extra.get("opeid8", "")
        fields = federal_operating_curated_fields(payload, checked)
        campus_source = _blank(row.get("campus_source_url"))
        if not campus_source or "educationdata.urban.org" in campus_source:
            continue
        fields["source_url"] = campus_source
        fields["status_detail"] = _acquisition_status_detail(row)
        fields["property_disposition"] = PROP_NA
        fields["sale_price_published"] = ""
        new_rows.append(fields)
    appended = append_curated_rows(curated_file, new_rows) if curated_file.exists() else []
    if appended:
        table = apply_operating_notes(
            table,
            {_unitid_int(row["unitid"]): row for row in appended if _unitid_int(row["unitid"]) is not None},
        )
        curated_note = (
            f"Appended {len(appended)} residential own-campus row(s) to "
            "`data/status/status_curated.csv`. Existing curated rows were not modified."
        )
    else:
        curated_note = "The curated file `data/status/status_curated.csv` was not modified."
    if table.empty:
        table["list_bucket"] = pd.Series(dtype=str)
    else:
        table = table.copy()
        table["list_bucket"] = [operating_bucket(row) for _, row in table.iterrows()]
        table["exclusion_reason"] = [exclusion_reason(row) for _, row in table.iterrows()]
    open_df, _excluded, _teach, _closed, depth = partition_acquisition(table, open_n)
    write_status_outputs(
        settings,
        table,
        notes,
        checked_at=checked,
        top_n=len(table),
        write_html=write_html,
        open_count=int(len(open_df)),
        depth=depth,
        curated_note=curated_note,
        watch=watch,
        open_n=open_n,
    )
    return table


def load_status_for_report(settings: Settings) -> pd.DataFrame:
    """Status columns for evidence cards.

    Prefer the merged snapshot. If it has not been written yet, badge the
    curated file with no automated columns and no network calls.
    """
    snapshot = settings.outputs_dir / "status_current.csv"
    if snapshot.exists():
        frame = pd.read_csv(snapshot, dtype=str, keep_default_na=False)
        if "unitid" in frame.columns:
            frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
        return frame
    path = curated_path(settings)
    if not path.exists():
        return pd.DataFrame()
    curated = load_curated(path)
    empty_watch_cols = curated.copy()
    if "watchlist_rank" not in empty_watch_cols.columns:
        empty_watch_cols["watchlist_rank"] = ""
    return build_status_table(empty_watch_cols, curated, auto_checked_at="")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Walk the ranked watch list and refresh status for the still-operating top list. "
            "Curated sale and listing facts are kept; federal sources only flag disagreements. "
            "Schools that newly enter the open list are appended to the curated file."
        )
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Maximum ranked rows to scan (default: the whole watch list)",
    )
    parser.add_argument(
        "--open",
        type=int,
        default=None,
        help="How many still-operating schools to keep (default 50)",
    )
    parser.add_argument("--watchlist", type=Path, default=None)
    parser.add_argument("--skip-network", action="store_true", help="Use the curated file only")
    parser.add_argument("--no-html", action="store_true", help="Do not update outputs/top50_report.html")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = load_settings(args.config)
    cfg = settings.raw.get("status") or {}
    scan_n = args.top if args.top is not None else 0
    open_n = args.open if args.open is not None else int(cfg.get("open_n", cfg.get("top_n", 50)))
    table = run_status_check(
        settings,
        top_n=scan_n,
        open_n=open_n,
        skip_network=args.skip_network,
        write_html=not args.no_html,
        watchlist=args.watchlist,
    )
    flagged = int(table["disagreement"].map(_blank).ne("").sum()) if not table.empty else 0
    from college_closure.campus import acquisition_ready

    n_open = int(sum(acquisition_ready(row) for _, row in table.iterrows())) if not table.empty else 0
    depth = 0
    if not table.empty and "watchlist_rank" in table.columns:
        try:
            depth = int(float(table.iloc[-1]["watchlist_rank"]))
        except (TypeError, ValueError):
            depth = len(table)
    print(
        f"status rows={len(table)} open={n_open} depth={depth} disagreements={flagged} "
        f"-> {settings.outputs_dir / 'status_current.csv'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
