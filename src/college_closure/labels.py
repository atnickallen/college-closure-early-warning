"""Closure / merger labels from IPEDS + optional FSA Closed School file."""

from __future__ import annotations

import logging

import pandas as pd

from college_closure.config import Settings
from college_closure.constants import INST_STATUS_CLOSED, INST_STATUS_MERGED
from college_closure.ids import add_id_keys

LOGGER = logging.getLogger(__name__)


def _year_from_closedat(series: pd.Series) -> pd.Series:
    dates = pd.to_datetime(series, errors="coerce")
    years = dates.dt.year
    # Also accept bare years like "2019" or "05/2018"
    as_str = series.astype("string")
    extracted = as_str.str.extract(r"(19|20)\d{2}", expand=False)
    # extract of (19|20) only gets prefix — do a full 4-digit extract
    extracted = as_str.str.extract(r"((?:19|20)\d{2})", expand=False)
    extracted_y = pd.to_numeric(extracted, errors="coerce")
    return years.where(years.notna(), extracted_y)


def institution_event_years(
    directory: pd.DataFrame,
    *,
    mergers_are_positive: bool,
    fsa_closed: pd.DataFrame | None = None,
    use_disappearance: bool = True,
) -> pd.DataFrame:
    """One row per UNITID with earliest observed closure/merger year."""
    work = add_id_keys(directory)
    work["unitid"] = pd.to_numeric(work["unitid"], errors="coerce")
    work["year"] = pd.to_numeric(work["year"], errors="coerce")
    rows = []

    def _num(col: str) -> pd.Series:
        if col not in work.columns:
            return pd.Series(pd.NA, index=work.index)
        return pd.to_numeric(work[col], errors="coerce")

    status = _num("inst_status")
    closedat = _year_from_closedat(work["date_closed"]) if "date_closed" in work.columns else pd.Series(pd.NA, index=work.index)
    deleted = _num("year_deleted")

    close_mask = status.isin(INST_STATUS_CLOSED)
    merge_mask = status.isin(INST_STATUS_MERGED) if mergers_are_positive else pd.Series(False, index=work.index)

    for unitid, grp in work.groupby("unitid"):
        event_year = pd.NA
        event_type = None
        source = None
        g_status = status.loc[grp.index]
        g_closedat = closedat.loc[grp.index]
        g_deleted = deleted.loc[grp.index]
        candidates = []
        if g_closedat.notna().any():
            candidates.append((int(g_closedat.min()), "closure", "ipeds_date_closed"))
        if g_status.isin(INST_STATUS_CLOSED).any():
            y = int(grp.loc[g_status.isin(INST_STATUS_CLOSED), "year"].min())
            candidates.append((y, "closure", "ipeds_inst_status"))
        if mergers_are_positive and g_status.isin(INST_STATUS_MERGED).any():
            y = int(grp.loc[g_status.isin(INST_STATUS_MERGED), "year"].min())
            candidates.append((y, "merger", "ipeds_inst_status"))
        if g_deleted.notna().any():
            yd = int(g_deleted.min())
            if 1900 < yd < 2100:
                candidates.append((yd, "closure", "ipeds_year_deleted"))
        if candidates:
            event_year, event_type, source = min(candidates, key=lambda t: t[0])
        rows.append(
            {
                "unitid": unitid,
                "opeid6": grp["opeid6"].replace("", pd.NA).dropna().iloc[0] if grp["opeid6"].replace("", pd.NA).notna().any() else "",
                "event_year": event_year,
                "event_type": event_type,
                "event_source": source,
                "first_year": int(grp["year"].min()),
                "last_year": int(grp["year"].max()),
            }
        )
    events = pd.DataFrame(rows)

    if fsa_closed is not None and not fsa_closed.empty and "opeid6" in fsa_closed.columns:
        fsa = fsa_closed.copy()
        fsa["opeid6"] = fsa["opeid6"].astype(str)
        fsa_min = fsa.groupby("opeid6")["closed_year"].min()
        events = events.merge(fsa_min.rename("fsa_closed_year"), on="opeid6", how="left")
        use_fsa = events["event_year"].isna() & events["fsa_closed_year"].notna()
        events.loc[use_fsa, "event_year"] = events.loc[use_fsa, "fsa_closed_year"]
        events.loc[use_fsa, "event_type"] = "closure"
        events.loc[use_fsa, "event_source"] = "fsa_closed_school"
        both = events["event_year"].notna() & events["fsa_closed_year"].notna()
        earlier = both & (events["fsa_closed_year"] < events["event_year"])
        events.loc[earlier, "event_year"] = events.loc[earlier, "fsa_closed_year"]
        events.loc[earlier, "event_source"] = "fsa_closed_school"

    panel_max = int(work["year"].max())
    if use_disappearance:
        # Require a 2-year gap vs the latest directory year so a one-year IPEDS
        # publication lag is not labeled as a closure. Prefer this only on
        # directory_raw (unfiltered) so filter changes are not events.
        gone = events["event_year"].isna() & (events["last_year"] <= panel_max - 2)
        events.loc[gone, "event_year"] = events.loc[gone, "last_year"] + 1
        events.loc[gone, "event_type"] = events.loc[gone, "event_type"].fillna("disappeared")
        events.loc[gone, "event_source"] = events.loc[gone, "event_source"].fillna("panel_disappearance")

    LOGGER.info(
        "Event years: %s institutions, %s with an event",
        len(events),
        int(events["event_year"].notna().sum()),
    )
    return events


def attach_labels(
    panel: pd.DataFrame,
    events: pd.DataFrame,
    horizons: list[int],
    last_complete_year: int,
) -> pd.DataFrame:
    out = panel.merge(events[["unitid", "event_year", "event_type", "event_source"]], on="unitid", how="left")
    for h in horizons:
        future = (out["event_year"].notna()) & (out["event_year"] > out["year"]) & (out["event_year"] <= out["year"] + h)
        col = f"closed_or_merged_within_{h}_years"
        out[col] = future.astype(int)
        # Right-censor: cannot confirm a negative if the horizon runs past observed data.
        incomplete = out["year"] + h > last_complete_year
        out.loc[incomplete, col] = pd.NA
        out[f"label_complete_h{h}"] = ~incomplete
    return out


def build_labels(settings: Settings, panel: pd.DataFrame | None = None) -> pd.DataFrame:
    processed = settings.processed_dir
    if panel is None:
        feat_path = processed / "features.parquet"
        panel = pd.read_parquet(feat_path if feat_path.exists() else processed / "panel.parquet")

    # Event detection on the unfiltered directory when available so a school
    # that exits the *filtered* universe is not auto-labeled closed.
    raw_path = processed / "directory_raw.parquet"
    dir_path = processed / "directory.parquet"
    if raw_path.exists():
        directory = pd.read_parquet(raw_path)
    elif dir_path.exists():
        directory = pd.read_parquet(dir_path)
    else:
        directory = panel

    cfg = settings.raw.get("labels") or {}
    mergers = bool(cfg.get("mergers_are_positive", True))
    use_disappear = bool(cfg.get("use_disappearance", False))
    horizons = list(settings.raw.get("label_horizons") or [settings.label_horizon_years])

    fsa_path = processed / "fsa_closed_school.parquet"
    fsa = pd.read_parquet(fsa_path) if fsa_path.exists() else pd.DataFrame()

    events = institution_event_years(
        directory,
        mergers_are_positive=mergers,
        fsa_closed=fsa if not fsa.empty else None,
        use_disappearance=use_disappear,
    )
    events.to_parquet(processed / "closure_events.parquet", index=False)

    last_complete = int(pd.to_numeric(directory["year"], errors="coerce").max())
    if not fsa.empty and "closed_year" in fsa.columns:
        last_complete = max(last_complete, int(fsa["closed_year"].max()))

    labeled = attach_labels(panel, events, horizons, last_complete)
    dest = processed / "labels.parquet"
    labeled.to_parquet(dest, index=False)
    h = int(settings.label_horizon_years)
    col = f"closed_or_merged_within_{h}_years"
    known = labeled[col].dropna()
    LOGGER.info(
        "Labels h=%s: %s positives / %s complete rows (last complete year %s) -> %s",
        h,
        int(known.sum()) if not known.empty else 0,
        int(known.shape[0]),
        last_complete,
        dest,
    )
    return labeled
