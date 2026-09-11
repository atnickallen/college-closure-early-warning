"""UNITID ↔ OPEID8 ↔ OPEID6 ↔ EIN longitudinal crosswalk + finance rollup."""

from __future__ import annotations

import logging

import pandas as pd

from college_closure.config import Settings
from college_closure.constants import (
    FINANCE_PANEL_COLUMNS,
    PARENT_CHILD_CHILD,
    PARENT_CHILD_PARENT,
)
from college_closure.ids import add_id_keys

LOGGER = logging.getLogger(__name__)


def build_crosswalk(directory: pd.DataFrame) -> pd.DataFrame:
    """One row per UNITID×year with join keys and a preferred OPEID6 mapping.

    FSA often keys on the 6-digit root. Multiple UNITIDs can share an OPEID6
    (branch campuses). We keep every UNITID row and flag:
    - opeid_is_main (OPEID8 ends in 00)
    - opeid6_n_unitids (how many UNITIDs share the root that year)
    Join strategy for FSA: exact OPEID8 first, else OPEID6 restricted to the
    main campus when the root is shared.
    """
    if directory.empty:
        return directory
    work = add_id_keys(directory)
    keep = [
        c
        for c in (
            "unitid",
            "year",
            "inst_name",
            "opeid",
            "opeid8",
            "opeid6",
            "opeid_is_main",
            "ein",
            "ein_norm",
            "newid",
            "inst_control",
            "sector",
            "state_abbr",
            "inst_status",
            "date_closed",
        )
        if c in work.columns
    ]
    out = work[keep].drop_duplicates(subset=["unitid", "year"])
    if "opeid6" in out.columns:
        counts = (
            out.loc[out["opeid6"] != ""]
            .groupby(["year", "opeid6"])["unitid"]
            .nunique()
            .rename("opeid6_n_unitids")
            .reset_index()
        )
        out = out.merge(counts, on=["year", "opeid6"], how="left")
        out["opeid6_n_unitids"] = out["opeid6_n_unitids"].fillna(0).astype(int)
    LOGGER.info("Crosswalk %s UNITID×year rows", len(out))
    return out


def write_crosswalk(settings: Settings, directory: pd.DataFrame | None = None) -> pd.DataFrame:
    if directory is None:
        path = settings.processed_dir / "directory.parquet"
        directory = pd.read_parquet(path)
    xw = build_crosswalk(directory)
    dest = settings.processed_dir / "crosswalk.parquet"
    xw.to_parquet(dest, index=False)
    LOGGER.info("Wrote %s", dest)
    return xw


FINANCE_VALUE_COLS = [
    c
    for c in FINANCE_PANEL_COLUMNS
    if c not in {"parent_child_flag", "parent_unitid", "est_fte", "rep_fte", "calc_fte"}
]


def carry_parent_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill parent_unitid / parent_child_flag within UNITID (Urban ends 2017)."""
    out = df.sort_values(["unitid", "year"]).copy()
    for col in ("parent_unitid", "parent_child_flag"):
        if col in out.columns:
            out[col] = out.groupby("unitid", sort=False)[col].ffill()
    return out


def apply_parent_child_finance_rollup(df: pd.DataFrame) -> pd.DataFrame:
    """Copy parent finance onto child campuses with missing/$0 revenue.

    Children keep their own UNITID row (we do not drop them). Totals are
    inherited so ratio features are not $0 shells. ``finance_from_parent``
    marks the copy so we do not treat the child as an independent $0 reporter.
    Parent rows are unchanged — this is inheritance, not consolidation that
    would double-count parent+child as two full enterprises in the *source*
    data; both may still appear on a watch list and are flagged.
    """
    if df.empty:
        return df
    out = carry_parent_ids(df)
    if "finance_from_parent" not in out.columns:
        out["finance_from_parent"] = False
    else:
        out["finance_from_parent"] = out["finance_from_parent"].fillna(False).astype(bool)

    if "parent_unitid" not in out.columns:
        return out

    flag = pd.to_numeric(out.get("parent_child_flag"), errors="coerce") if "parent_child_flag" in out.columns else pd.Series(pd.NA, index=out.index)
    parent_id = pd.to_numeric(out["parent_unitid"], errors="coerce")
    unitid = pd.to_numeric(out["unitid"], errors="coerce")
    child = flag.isin(PARENT_CHILD_CHILD) | (parent_id.notna() & (parent_id != unitid))
    rev = pd.to_numeric(out["rev_total_current"], errors="coerce") if "rev_total_current" in out.columns else pd.Series(pd.NA, index=out.index)
    need = child & (rev.isna() | (rev == 0))
    if not bool(need.any()):
        return out

    value_cols = [c for c in FINANCE_VALUE_COLS if c in out.columns]
    if not value_cols:
        return out

    parents = out.loc[:, ["unitid", "year", *value_cols]].copy()
    parents["unitid"] = pd.to_numeric(parents["unitid"], errors="coerce")
    parents["year"] = pd.to_numeric(parents["year"], errors="coerce")
    rename = {c: f"_p_{c}" for c in value_cols}
    parents = parents.rename(columns={"unitid": "_parent_id", **rename})

    out["_parent_join"] = parent_id
    merged = out.merge(
        parents,
        left_on=["_parent_join", "year"],
        right_on=["_parent_id", "year"],
        how="left",
    )
    # merge can duplicate if parent keys collide; keep first
    merged = merged.drop_duplicates(subset=["unitid", "year"], keep="first")
    need_m = child.reindex(merged.index, fill_value=False)
    if "rev_total_current" in merged.columns:
        rev_m = pd.to_numeric(merged["rev_total_current"], errors="coerce")
        need_m = (
            (
                pd.to_numeric(merged.get("parent_child_flag"), errors="coerce").isin(PARENT_CHILD_CHILD)
                | (
                    pd.to_numeric(merged["_parent_join"], errors="coerce").notna()
                    & (pd.to_numeric(merged["_parent_join"], errors="coerce") != pd.to_numeric(merged["unitid"], errors="coerce"))
                )
            )
            & (rev_m.isna() | (rev_m == 0))
        )

    any_copied = pd.Series(False, index=merged.index)
    for col in value_cols:
        pcol = f"_p_{col}"
        if pcol not in merged.columns:
            continue
        cur = pd.to_numeric(merged[col], errors="coerce") if col in merged.columns else pd.Series(pd.NA, index=merged.index)
        take = need_m & merged[pcol].notna() & (cur.isna() | (cur == 0))
        merged.loc[take, col] = merged.loc[take, pcol]
        any_copied = any_copied | take
        merged = merged.drop(columns=[pcol])
    merged.loc[any_copied, "finance_from_parent"] = True
    drop_extra = [c for c in ("_parent_join", "_parent_id") if c in merged.columns]
    merged = merged.drop(columns=drop_extra)
    n = int(any_copied.sum())
    if n:
        LOGGER.info("Parent/child finance rollup: inherited parent totals on %s child rows", n)
    return merged
