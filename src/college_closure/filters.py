"""Filter the IPEDS directory to actual degree-granting colleges."""

from __future__ import annotations

import logging
import re
from typing import Any

import pandas as pd

from college_closure.constants import (
    CONTROL_LABELS,
    SECTOR_LABELS,
    SENTINEL_VALUES,
    TITLE_IV_PARTICIPATING,
)

LOGGER = logging.getLogger(__name__)

SYSTEM_OFFICE_RE = re.compile(
    r"system office|system administration|central office|"
    r"administrative office|administrative unit",
    re.IGNORECASE,
)


def _series_or_empty(df: pd.DataFrame, *names: str) -> pd.Series:
    for name in names:
        if name in df.columns:
            return df[name]
    return pd.Series(pd.NA, index=df.index)


def add_directory_labels(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "inst_control" in out.columns and "control" not in out.columns:
        out["control"] = out["inst_control"]
    elif "control" in out.columns and "inst_control" not in out.columns:
        out["inst_control"] = out["control"]
    control = _series_or_empty(out, "inst_control", "control")
    out["control"] = control
    out["inst_control"] = control
    out["control_label"] = control.map(CONTROL_LABELS)
    sector = _series_or_empty(out, "sector")
    out["sector_label"] = sector.map(SECTOR_LABELS)
    inst_level = pd.to_numeric(_series_or_empty(out, "institution_level"), errors="coerce")
    out["is_four_year"] = (sector.isin([1, 2, 3])) | (inst_level == 4)
    title_iv = pd.to_numeric(_series_or_empty(out, "title_iv_indicator"), errors="coerce")
    out["title_iv_participating"] = title_iv.isin(TITLE_IV_PARTICIPATING)
    # Publics almost never close; keep them in the panel, flag the modeling universe.
    out["in_risk_model_universe"] = out["inst_control"].isin([2, 3])
    return out


def filter_college_universe(df: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
    """Keep degree-granting Title IV colleges; drop system offices / non-colleges.

    Title IV is applied only when ``title_iv_indicator`` is reported (not a
    sentinel). Missing Title IV is kept, per "where available".
    """
    work = add_directory_labels(df)
    n0 = len(work)

    degree_granting = pd.to_numeric(
        _series_or_empty(work, "degree_granting"), errors="coerce"
    )
    keep = degree_granting == int(filters.get("degree_granting", 1))

    control = pd.to_numeric(_series_or_empty(work, "inst_control", "control"), errors="coerce")
    allowed_control = set(filters.get("control", [1, 2, 3]))
    keep &= control.isin(allowed_control)

    title_iv = pd.to_numeric(_series_or_empty(work, "title_iv_indicator"), errors="coerce")
    participating = set(filters.get("title_iv_participating", list(TITLE_IV_PARTICIPATING)))
    title_iv_known = title_iv.notna() & ~title_iv.isin(SENTINEL_VALUES)
    keep &= ~title_iv_known | title_iv.isin(participating)

    admin_sector = filters.get("drop_admin_sector", 0)
    sector = pd.to_numeric(_series_or_empty(work, "sector"), errors="coerce")
    if admin_sector is not None and "sector" in work.columns:
        keep &= sector != admin_sector

    drop_categories = set(filters.get("drop_nondegree_inst_category") or [])
    if drop_categories and "inst_category" in work.columns:
        category = pd.to_numeric(work["inst_category"], errors="coerce")
        keep &= ~category.isin(drop_categories)

    if "primarily_postsecondary" in work.columns:
        pps = pd.to_numeric(work["primarily_postsecondary"], errors="coerce")
        known_pps = pps.notna() & ~pps.isin(SENTINEL_VALUES)
        keep &= ~known_pps | (pps == 1)

    names = _series_or_empty(work, "inst_name").astype("string")
    patterns = filters.get("drop_name_patterns") or []
    if patterns:
        combined = "|".join(re.escape(p) for p in patterns)
        name_hit = names.str.contains(combined, case=False, na=False, regex=True)
        keep &= ~name_hit
    else:
        keep &= ~names.str.contains(SYSTEM_OFFICE_RE, na=False)

    filtered = work.loc[keep].copy()
    LOGGER.info(
        "College universe filter: %s -> %s rows (dropped %s)",
        n0,
        len(filtered),
        n0 - len(filtered),
    )
    return filtered


def replace_sentinels(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Replace Urban/IPEDS -1/-2/-3 codes with NA on measure columns."""
    out = df.copy()
    cols = columns or [c for c in out.columns if c not in {"unitid", "year", "opeid", "ein"}]
    for col in cols:
        if col not in out.columns:
            continue
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].mask(out[col].isin(SENTINEL_VALUES))
    return out
