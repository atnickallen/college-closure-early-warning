"""UNITID ↔ OPEID8 ↔ OPEID6 ↔ EIN longitudinal crosswalk + finance rollup."""

from __future__ import annotations

import logging

import pandas as pd

from college_closure.config import Settings
from college_closure.constants import (
    FINANCE_PANEL_COLUMNS,
    PARENT_CHILD_CHILD,
    PARENT_CHILD_PARENT,
    SENTINEL_VALUES,
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


def _real_parent_id(series: pd.Series) -> pd.Series:
    parent = pd.to_numeric(series, errors="coerce")
    return parent.where(parent.notna() & ~parent.isin(SENTINEL_VALUES) & (parent > 0))


def links_from_finance(finance: pd.DataFrame) -> pd.DataFrame:
    """Child → parent links already stored on IPEDS finance rows (PCF / parent UNITID)."""
    empty = pd.DataFrame(columns=["unitid", "year", "parent_child_flag", "parent_unitid"])
    if finance is None or finance.empty or "parent_unitid" not in finance.columns:
        return empty
    work = finance.copy()
    work["unitid"] = pd.to_numeric(work["unitid"], errors="coerce")
    work["year"] = pd.to_numeric(work["year"], errors="coerce")
    flag = pd.to_numeric(work.get("parent_child_flag"), errors="coerce")
    parent = _real_parent_id(work["parent_unitid"])
    child = flag.isin(PARENT_CHILD_CHILD) & parent.notna() & (parent != work["unitid"])
    out = work.loc[child, ["unitid", "year"]].copy()
    out["parent_child_flag"] = flag.loc[child].to_numpy()
    out["parent_unitid"] = parent.loc[child].to_numpy()
    return out.dropna(subset=["unitid", "year", "parent_unitid"])


def links_from_flags(flags: pd.DataFrame, year: int) -> pd.DataFrame:
    """Child → parent links from an IPEDS FLAGS file (PRCH_F / IDX_F).

    FLAGS names the finance parent-child indicator ``PRCH_F`` and the parent
    UNITID ``IDX_F``. ``PCF_F`` on that file is the allocation percent, not the
    parent id. Full children often have no finance row of their own; the flag
    file is what names their parent filer.
    """
    empty = pd.DataFrame(columns=["unitid", "year", "parent_child_flag", "parent_unitid"])
    if flags is None or flags.empty:
        return empty
    columns = {c.upper(): c for c in flags.columns}
    if "UNITID" not in columns or "IDX_F" not in columns or "PRCH_F" not in columns:
        return empty
    work = pd.DataFrame(
        {
            "unitid": pd.to_numeric(flags[columns["UNITID"]], errors="coerce"),
            "parent_child_flag": pd.to_numeric(flags[columns["PRCH_F"]], errors="coerce"),
            "parent_unitid": _real_parent_id(flags[columns["IDX_F"]]),
        }
    )
    child = work["parent_child_flag"].isin(PARENT_CHILD_CHILD) & work["parent_unitid"].notna()
    child &= work["parent_unitid"] != work["unitid"]
    out = work.loc[child].dropna(subset=["unitid"]).copy()
    out["year"] = int(year)
    return out[["unitid", "year", "parent_child_flag", "parent_unitid"]]


def attach_parent_links(panel: pd.DataFrame, links: pd.DataFrame) -> pd.DataFrame:
    """Fill a child campus's parent UNITID when its own finance row is missing.

    The latest link at or before the panel year wins. Enrollment columns are
    left untouched. A campus that already reports revenue keeps that revenue;
    the rollup only copies dollars onto missing or zero revenue.
    """
    if panel is None or panel.empty or links is None or links.empty:
        return panel
    out = panel.copy()
    out["unitid"] = pd.to_numeric(out["unitid"], errors="coerce")
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    link = links.copy()
    link["unitid"] = pd.to_numeric(link["unitid"], errors="coerce")
    link["year"] = pd.to_numeric(link["year"], errors="coerce")
    link["parent_unitid"] = _real_parent_id(link["parent_unitid"])
    link["parent_child_flag"] = pd.to_numeric(link.get("parent_child_flag"), errors="coerce")
    link = link.dropna(subset=["unitid", "year", "parent_unitid"])
    link = link.sort_values(["unitid", "year"]).drop_duplicates(["unitid", "year"], keep="last")
    if link.empty:
        return out
    if "parent_unitid" not in out.columns:
        out["parent_unitid"] = pd.NA
    if "parent_child_flag" not in out.columns:
        out["parent_child_flag"] = pd.NA
    right = link.rename(
        columns={"year": "link_year", "parent_unitid": "_link_parent", "parent_child_flag": "_link_flag"}
    )
    # Latest link with link_year <= panel year. A python merge_asof needs a
    # globally sorted key, so match inside each UNITID.
    pieces = []
    grouped_links = {int(uid): g for uid, g in right.groupby(right["unitid"].astype(int), sort=False)}
    for uid, rows in out.groupby(out["unitid"].astype("Int64"), sort=False):
        if pd.isna(uid) or int(uid) not in grouped_links:
            pieces.append(rows)
            continue
        g = grouped_links[int(uid)].sort_values("link_year")
        block = rows.sort_values("year")
        matched = pd.merge_asof(
            block,
            g[["link_year", "_link_parent", "_link_flag"]],
            left_on="year",
            right_on="link_year",
            direction="backward",
        )
        pieces.append(matched)
    merged = pd.concat(pieces, ignore_index=True)
    if "_link_parent" not in merged.columns:
        return out
    rev = (
        pd.to_numeric(merged["rev_total_current"], errors="coerce")
        if "rev_total_current" in merged.columns
        else pd.Series(pd.NA, index=merged.index)
    )
    need = rev.isna() | (rev == 0)
    existing = _real_parent_id(merged["parent_unitid"])
    unitid = pd.to_numeric(merged["unitid"], errors="coerce")
    missing_pointer = existing.isna() | (existing == unitid)
    take = need & missing_pointer & merged["_link_parent"].notna()
    merged.loc[take, "parent_unitid"] = merged.loc[take, "_link_parent"]
    merged.loc[take, "parent_child_flag"] = merged.loc[take, "_link_flag"]
    n = int(take.sum())
    if n:
        LOGGER.info("Attached IPEDS finance parent links on %s child rows", n)
    return merged.drop(columns=[c for c in ("link_year", "_link_parent", "_link_flag") if c in merged.columns])


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
