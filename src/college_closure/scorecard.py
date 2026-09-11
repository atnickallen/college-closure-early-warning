"""College Scorecard: API (optional key) or official no-key bulk ZIP."""

from __future__ import annotations

import io
import logging
import os
import zipfile
from pathlib import Path

import pandas as pd

from college_closure.config import Settings
from college_closure.download import download_first
from college_closure.ids import add_id_keys, opeid6

LOGGER = logging.getLogger(__name__)

# Official College Scorecard API field names (api.data.gov).
# school.under_investigation is the HCM2-style flag on the API;
# the most-recent bulk ZIP uses column HCM2 for the same construct.
KEEP_FIELDS = [
    "id",
    "ope6_id",
    "ope8_id",
    "school.name",
    "school.operating",
    "school.ownership",
    "school.under_investigation",
    "school.accreditor",
    "school.state",
    "school.city",
    "school.alias",
    "latest.student.size",
]


def scorecard_api_key() -> str:
    """Return DATA_GOV_API_KEY or SCORECARD_API_KEY. Never log the value."""
    return (os.environ.get("DATA_GOV_API_KEY") or os.environ.get("SCORECARD_API_KEY") or "").strip()

BULK_COL_MAP = {
    "UNITID": "unitid",
    "OPEID": "opeid",
    "OPEID6": "opeid6_raw",
    "INSTNM": "inst_name",
    "CITY": "city",
    "STABBR": "state_abbr",
    "CONTROL": "scorecard_ownership",
    "OPERATING": "scorecard_operating",
    "UNDER_INVESTIGATION": "scorecard_under_investigation",
    "HCM2": "scorecard_under_investigation",  # most-recent ZIP name for HCM2 flag
    "ACCREDAGENCY": "scorecard_accreditor",
    "CLOSEDAT": "scorecard_closedat",
    "CURROPER": "scorecard_operating",
}


def _guess_bulk_urls(settings: Settings) -> list[str]:
    cfg = settings.raw.get("scorecard") or {}
    urls = list(cfg.get("bulk_urls") or [])
    defaults = [
        "https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Institution_06102026.zip",
        "https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Institution_05192025.zip",
        "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Institution_06102026.zip",
        "https://ed-public-download.app.cloud.gov/downloads/Most-Recent-Cohorts-Institution_05192025.zip",
    ]
    for u in defaults:
        if u not in urls:
            urls.append(u)
    return urls


def _http_get(url: str, params: dict, timeout: int = 60):
    import requests

    return requests.get(url, params=params, timeout=timeout)


def ingest_scorecard_api(settings: Settings, *, http_get=None) -> pd.DataFrame:
    """Paginated College Scorecard API. Requires DATA_GOV_API_KEY / SCORECARD_API_KEY.

    ``http_get(url, params, timeout)`` is injectable for unit tests. The key is
    sent as the ``api_key`` query param and is never written to parquet or logs.
    """
    key = scorecard_api_key()
    if not key:
        return pd.DataFrame()
    cfg = settings.raw.get("scorecard") or {}
    base = str(cfg.get("api_base", "https://api.data.gov/ed/collegescorecard/v1/schools"))
    getter = http_get or _http_get
    try:
        rows = []
        page = 0
        total = None
        per_page = 100
        while page < 200:
            resp = getter(
                base,
                {
                    "api_key": key,
                    "fields": ",".join(KEEP_FIELDS),
                    "per_page": per_page,
                    "page": page,
                },
                60,
            )
            status = getattr(resp, "status_code", 0)
            if status >= 400:
                body = getattr(resp, "text", "")[:160]
                LOGGER.warning("Scorecard API HTTP %s on page %s: %s", status, page, body)
                break
            payload = resp.json() if hasattr(resp, "json") else {}
            results = payload.get("results") or []
            if not results:
                break
            rows.extend(results)
            meta = payload.get("metadata") or {}
            if total is None:
                try:
                    total = int(meta.get("total") or 0) or None
                except (TypeError, ValueError):
                    total = None
            try:
                per_page = int(meta.get("per_page") or per_page)
            except (TypeError, ValueError):
                pass
            LOGGER.info("Scorecard API page %s (%s rows so far)", page, len(rows))
            page += 1
            if total is not None and len(rows) >= total:
                break
        if not rows:
            return pd.DataFrame()
        frame = pd.json_normalize(rows)
        frame = frame.rename(
            columns={
                "id": "unitid",
                "ope6_id": "opeid6_raw",
                "ope8_id": "opeid",
                "school.name": "inst_name",
                "school.operating": "scorecard_operating",
                "school.ownership": "scorecard_ownership",
                "school.under_investigation": "scorecard_under_investigation",
                "school.accreditor": "scorecard_accreditor",
                "school.state": "state_abbr",
                "school.city": "city",
            }
        )
        return _finalize(frame, settings, source="api")
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Scorecard API fetch failed: %s", type(exc).__name__)
        return pd.DataFrame()


def ingest_scorecard_bulk(settings: Settings) -> pd.DataFrame:
    urls = _guess_bulk_urls(settings)
    path = download_first(
        urls,
        settings.raw_dir / "scorecard",
        "scorecard_institution.zip",
        timeout=(15, 180),
        max_retries=2,
        source="scorecard_bulk",
    )
    if path is None:
        LOGGER.info("Scorecard bulk ZIP not downloaded")
        return pd.DataFrame()
    try:
        with zipfile.ZipFile(path) as zf:
            names = [
                n
                for n in zf.namelist()
                if n.lower().endswith(".csv") and "__macosx" not in n.lower() and not Path(n).name.startswith("._")
            ]
            if not names:
                LOGGER.warning("Scorecard ZIP has no CSV: %s", zf.namelist()[:10])
                return pd.DataFrame()
            # Prefer the institution-level most-recent file
            names_sorted = sorted(
                names,
                key=lambda n: (
                    "field" in n.lower(),
                    "data_dictionary" in n.lower(),
                    0 if "institution" in n.lower() else 1,
                    -len(n),
                ),
            )
            raw = zf.read(names_sorted[0])
        df = pd.read_csv(io.BytesIO(raw), encoding="latin-1", low_memory=False)
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Scorecard ZIP parse failed: %s", exc)
        return pd.DataFrame()
    rename = {c: BULK_COL_MAP[c] for c in df.columns if c in BULK_COL_MAP}
    # also accept lowercase
    lower = {c.upper(): c for c in df.columns}
    for src, dest in BULK_COL_MAP.items():
        if dest not in rename.values() and src in lower:
            rename[lower[src]] = dest
    df = df.rename(columns=rename)
    return _finalize(df, settings, source="bulk_zip")


def _finalize(df: pd.DataFrame, settings: Settings, source: str) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    if "opeid" in out.columns:
        out = add_id_keys(out)
    elif "opeid6_raw" in out.columns:
        out["opeid6"] = out["opeid6_raw"].map(opeid6)
    if "unitid" in out.columns:
        out["unitid"] = pd.to_numeric(out["unitid"], errors="coerce")
    for c in ("scorecard_operating", "scorecard_under_investigation", "scorecard_ownership"):
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    # Official ED HCM2 / under-investigation flag (column HCM2 or UNDER_INVESTIGATION)
    if "scorecard_under_investigation" in out.columns:
        out["hcm2_scorecard"] = pd.to_numeric(out["scorecard_under_investigation"], errors="coerce") == 1
    else:
        out["hcm2_scorecard"] = False
    out["scorecard_source"] = source
    dest = settings.processed_dir / "scorecard_operating.parquet"
    keep = [
        c
        for c in (
            "unitid",
            "opeid",
            "opeid8",
            "opeid6",
            "inst_name",
            "city",
            "state_abbr",
            "scorecard_operating",
            "scorecard_currently_operating",
            "scorecard_ownership",
            "scorecard_under_investigation",
            "hcm2_scorecard",
            "scorecard_accreditor",
            "scorecard_closedat",
            "scorecard_source",
        )
        if c in out.columns
    ]
    slim = out[keep].drop_duplicates()
    slim.to_parquet(dest, index=False)
    LOGGER.info("Scorecard snapshot %s rows (%s) -> %s", len(slim), source, dest)
    return slim


def ingest_scorecard(settings: Settings, *, skip: bool = False, http_get=None) -> pd.DataFrame:
    """API if ``DATA_GOV_API_KEY`` is set; otherwise official no-key bulk ZIP.

    Never invent rows. ``skip=True`` (``--skip-scorecard``) writes nothing.
    """
    if skip:
        LOGGER.info("Scorecard ingest skipped")
        return pd.DataFrame()
    if scorecard_api_key():
        api = ingest_scorecard_api(settings, http_get=http_get)
        if not api.empty:
            return api
        LOGGER.warning("Scorecard API returned no rows; falling back to official bulk ZIP")
    else:
        LOGGER.info("DATA_GOV_API_KEY unset; trying official Scorecard bulk ZIP (no key)")
    return ingest_scorecard_bulk(settings)


def scorecard_closure_events(scorecard: pd.DataFrame) -> pd.DataFrame:
    """UNITID events from a valid Scorecard CLOSEDAT only — never sentinel years."""
    if scorecard is None or scorecard.empty or "unitid" not in scorecard.columns:
        return pd.DataFrame()
    if "scorecard_closedat" not in scorecard.columns:
        return pd.DataFrame()
    work = scorecard.copy()
    raw = work["scorecard_closedat"]
    # YYYYMMDD integers or ISO strings; reject -2/-1/1/2/3 and years outside 1980–2035
    as_str = raw.astype("string")
    as_str = as_str.replace({"-1": pd.NA, "-2": pd.NA, "-3": pd.NA, "1": pd.NA, "2": pd.NA, "3": pd.NA})
    dates = pd.to_datetime(as_str, errors="coerce")
    # integer YYYYMMDD
    nums = pd.to_numeric(raw, errors="coerce")
    yyyymmdd = nums.where((nums >= 19800101) & (nums <= 20351231))
    from_num = pd.to_datetime(yyyymmdd.astype("Int64").astype("string"), format="%Y%m%d", errors="coerce")
    dates = dates.where(dates.notna(), from_num)
    years = dates.dt.year
    extracted = as_str.str.extract(r"((?:19|20)\d{2})", expand=False)
    extracted_y = pd.to_numeric(extracted, errors="coerce")
    years = years.where(years.notna(), extracted_y)
    years = years.where((years >= 1980) & (years <= 2035))
    out = pd.DataFrame(
        {
            "unitid": pd.to_numeric(work["unitid"], errors="coerce"),
            "opeid6": work["opeid6"] if "opeid6" in work.columns else "",
            "event_year": years,
            "event_type": "closure",
            "event_source": "scorecard_closedat",
        }
    )
    return out.dropna(subset=["unitid", "event_year"])
