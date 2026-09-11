"""Best-effort shortlist enrichment: accreditor actions, WARN, ProPublica 990.

Flags only — never silent score hacks. Joins on EIN (990) or exact name+state.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

import pandas as pd
import requests

from college_closure.config import Settings
from college_closure.download import DEFAULT_HEADERS, download_file
from college_closure.ids import normalize_ein

LOGGER = logging.getLogger(__name__)

ACCREDITOR_PAGES = {
    "HLC": "https://www.hlcommission.org/accreditation/accredited-institutions/public-disclosure-notices/",
    "MSCHE": "https://www.msche.org/accreditation-actions/",
    "SACSCOC": "https://sacscoc.org/app/uploads/2025/01/AccreditationActions.pdf",
    "NECHE": "https://www.neche.org/public-statements/",
    "WSCUC": "https://www.wscuc.org/resources/commission-actions/",
    "NWCCU": "https://nwccu.org/accreditation/accredited-institutions/",
}

WARN_URLS = [
    "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn_report.xlsx",
    "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/WARN-Report.xlsx",
    "https://dol.ny.gov/system/files/documents/2026/09/warn.xlsx",
]


def _fetch_text(url: str, dest: Path, timeout: int = 25) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 200:
        return dest.read_text(encoding="utf-8", errors="replace")
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        if resp.status_code >= 400:
            LOGGER.info("Enrichment %s %s", resp.status_code, url)
            return ""
        dest.write_bytes(resp.content)
        return resp.text
    except Exception as exc:  # noqa: BLE001
        LOGGER.info("Enrichment fetch failed %s: %s", url, exc)
        return ""


def _norm_name(s) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()


def accreditor_flags(shortlist: pd.DataFrame, cache: Path) -> pd.Series:
    names = {_norm_name(n) for n in shortlist.get("inst_name", pd.Series(dtype=str)) if _norm_name(n)}
    hits: dict[str, list[str]] = {n: [] for n in names}
    for agency, url in ACCREDITOR_PAGES.items():
        text = _fetch_text(url, cache / f"accreditor_{agency.lower()}.html")
        if not text:
            continue
        plain = re.sub(r"<[^>]+>", " ", text).lower()
        for n in names:
            if len(n) >= 8 and n in plain:
                hits[n].append(agency)
    out = []
    for name in shortlist.get("inst_name", pd.Series(dtype=str)):
        key = _norm_name(name)
        agencies = hits.get(key) or []
        out.append(";".join(agencies) if agencies else "")
    return pd.Series(out, index=shortlist.index, dtype="string")


def warn_flags(shortlist: pd.DataFrame, cache: Path) -> pd.Series:
    names = {_norm_name(n) for n in shortlist.get("inst_name", pd.Series(dtype=str)) if len(_norm_name(n)) >= 8}
    found: set[str] = set()
    for url in WARN_URLS:
        dest = cache / url.rstrip("/").split("/")[-1]
        path = download_file(url, dest, timeout=(6, 20), max_retries=1, backoff=1.0, source="warn")
        if path is None:
            continue
        try:
            if path.suffix.lower() in {".xlsx", ".xls"}:
                tables = [pd.read_excel(path)]
            else:
                tables = [pd.read_csv(path, encoding="latin-1", low_memory=False)]
        except Exception as exc:  # noqa: BLE001
            LOGGER.info("WARN parse failed %s: %s", path, exc)
            continue
        blob = " ".join(
            tables[0].astype(str).apply(lambda s: " ".join(s.tolist()), axis=0).tolist()
        ).lower()
        for n in names:
            if n in blob:
                found.add(n)
    out = []
    for name in shortlist.get("inst_name", pd.Series(dtype=str)):
        out.append(bool(_norm_name(name) in found))
    return pd.Series(out, index=shortlist.index)


def propublica_990(shortlist: pd.DataFrame, cache: Path) -> pd.DataFrame:
    """EIN-verified Nonprofit Explorer lookup — skip rows without a 9-digit EIN."""
    cache.mkdir(parents=True, exist_ok=True)
    rows = []
    eins = shortlist.get("ein_norm") if "ein_norm" in shortlist.columns else shortlist.get("ein")
    if eins is None:
        return pd.DataFrame(index=shortlist.index)
    for idx, raw in eins.items():
        ein = normalize_ein(raw)
        rec = {
            "irs990_ein_verified": False,
            "irs990_revenue": pd.NA,
            "irs990_assets": pd.NA,
            "irs990_tax_period": pd.NA,
            "irs990_name": pd.NA,
        }
        if len(ein) != 9:
            rows.append(rec)
            continue
        dest = cache / f"990_{ein}.json"
        if dest.exists():
            payload = json.loads(dest.read_text(encoding="utf-8"))
        else:
            url = f"https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
            try:
                resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=20)
                if resp.status_code >= 400:
                    dest.write_text("{}", encoding="utf-8")
                    rows.append(rec)
                    continue
                dest.write_bytes(resp.content)
                payload = resp.json()
            except Exception as exc:  # noqa: BLE001
                LOGGER.info("990 lookup failed %s: %s", ein, exc)
                rows.append(rec)
                continue
        org = payload.get("organization") or {}
        filings = payload.get("filings_with_data") or []
        latest = filings[0] if filings else {}
        # Verify EIN came back as requested
        got = normalize_ein(org.get("ein") or ein)
        rec["irs990_ein_verified"] = got == ein and bool(org)
        rec["irs990_name"] = org.get("name")
        rec["irs990_revenue"] = latest.get("totrevenue")
        rec["irs990_assets"] = latest.get("totassetsend")
        rec["irs990_tax_period"] = latest.get("tax_prd") or org.get("latest_object_id")
        rows.append(rec)
    return pd.DataFrame(rows, index=shortlist.index)


def enrich_shortlist(settings: Settings, watch: pd.DataFrame) -> pd.DataFrame:
    if watch.empty:
        return watch
    cache = settings.raw_dir / "enrichment"
    out = watch.copy()
    LOGGER.info("Enriching %s shortlist rows (accreditor / WARN / 990)", len(out))
    out["accreditor_public_action"] = accreditor_flags(out, cache)
    out["warn_layoff_mention"] = warn_flags(out, cache)
    nonprofit = pd.to_numeric(out.get("inst_control"), errors="coerce") == 2
    if nonprofit.any():
        nine = propublica_990(out.loc[nonprofit], cache)
        for c in nine.columns:
            out[c] = pd.NA
            out.loc[nonprofit, c] = nine[c]
    else:
        out["irs990_ein_verified"] = False
        out["irs990_revenue"] = pd.NA
        out["irs990_assets"] = pd.NA
    notes = []
    for _, row in out.iterrows():
        bits = []
        if row.get("accreditor_public_action"):
            bits.append(f"accreditor page mention: {row['accreditor_public_action']}")
        if row.get("warn_layoff_mention"):
            bits.append("WARN file mention (name match)")
        if row.get("irs990_ein_verified"):
            bits.append("ProPublica 990 EIN verified")
        notes.append("; ".join(bits))
    out["enrichment_notes"] = notes
    dest = settings.processed_dir / "shortlist_enrichment.parquet"
    out.to_parquet(dest, index=False)
    return out
