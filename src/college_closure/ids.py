"""UNITID / OPEID / EIN normalization and join keys."""

from __future__ import annotations

import re

import pandas as pd

_NON_DIGIT = re.compile(r"\D+")


def digits_only(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if pd.isna(value):
            return ""
        value = str(int(value)) if float(value) == int(value) else str(value)
    text = _NON_DIGIT.sub("", str(value).strip())
    return text


def normalize_opeid8(value) -> str:
    """8-digit OPEID (6-digit FSA root + 2-digit branch).

    FSA files often store only the 6-digit root. Padding a 6-digit value to 8
    with leading zeros would shift the root (002345 → 00002345). Six or fewer
    digits are treated as the root and suffixed with ``00`` (main campus).
    """
    text = digits_only(value)
    if not text or text in {"1", "2", "3"}:  # Urban sentinels sometimes leak in
        return ""
    if len(text) > 8:
        text = text[-8:]
    # IPEDS OPEIDs are 8 digits; pandas often stores 00234500 as int 234500.
    # Six digits ending in 00 are treated as that stripped 8-digit form.
    # Other 6-digit values (typical FSA root) become root + "00".
    if len(text) <= 5:
        return text.zfill(6) + "00"
    if len(text) == 6:
        if text.endswith("00"):
            return text.zfill(8)
        return text + "00"
    return text.zfill(8)


def opeid6(value) -> str:
    """FSA 6-digit root (first 6 of the 8-digit OPEID)."""
    eight = normalize_opeid8(value)
    return eight[:6] if eight else ""


def is_main_opeid8(value) -> bool:
    eight = normalize_opeid8(value)
    return bool(eight) and eight.endswith("00")


def normalize_ein(value) -> str:
    text = digits_only(value)
    if not text or text in {"1", "2", "3"}:
        return ""
    return text.zfill(9) if text else ""


def add_id_keys(df: pd.DataFrame) -> pd.DataFrame:
    """Add opeid8 / opeid6 / ein_norm on a copy."""
    out = df.copy()
    opeid_col = "opeid" if "opeid" in out.columns else None
    if opeid_col:
        out["opeid8"] = out[opeid_col].map(normalize_opeid8)
        out["opeid6"] = out["opeid8"].str[:6]
        out["opeid_is_main"] = out["opeid8"].str.endswith("00")
    else:
        out["opeid8"] = ""
        out["opeid6"] = ""
        out["opeid_is_main"] = False
    if "ein" in out.columns:
        out["ein_norm"] = out["ein"].map(normalize_ein)
    else:
        out["ein_norm"] = ""
    return out
