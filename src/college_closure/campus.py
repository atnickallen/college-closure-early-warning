"""Residential campus gate for the acquisition watch list.

A school stays on the main list only when it is still operating, IPEDS
reports on-campus housing with a real dorm capacity, and the curated land
file says it has its own campus. Acreage may be blank when a source shows
buildings and grounds but does not state a number.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from college_closure.status import (
    CLOSED_BUCKET,
    OPEN_BUCKET,
    TEACHOUT_BUCKET,
    operating_bucket,
)

ACQUISITION = "acquisition"
EXCLUDED = "excluded"
SMALL_HOUSING_BELOW = 50
HOUSING_SENTINELS = {-1, -2, -3}

LAND_COLUMNS = (
    "unitid",
    "acreage",
    "own_campus",
    "source_url",
    "checked_at",
    "image_url",
    "image_credit_url",
    "image_license",
    "image_author",
    "notes",
    "lat",
    "lon",
    "coord_source",
    "campus_map_url",
)

HOUSING_COLUMNS = (
    "unitid",
    "housing_year",
    "oncampus_housing",
    "dormitory_capacity",
)


def _num(value) -> float | None:
    try:
        if value is None or pd.isna(value):
            return None
    except (TypeError, ValueError):
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "<na>"}:
        return None
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def _text(value) -> str:
    number = _num(value)
    if number is None and (value is None or (isinstance(value, float) and pd.isna(value))):
        return ""
    try:
        if value is None or pd.isna(value):
            return ""
    except (TypeError, ValueError):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "<na>"}:
        return ""
    return text


def housing_is_reported(value) -> bool:
    """True only for IPEDS oncampus_housing codes 0 and 1.

    -1, -2, and -3 are missing-data sentinels, not a yes or a no.
    """
    number = _num(value)
    return number in {0.0, 1.0}


def latest_reported_housing(frame: pd.DataFrame) -> pd.DataFrame:
    """Newest IC year per UNITID where on-campus housing is actually 0 or 1."""
    empty = pd.DataFrame(columns=list(HOUSING_COLUMNS))
    if frame is None or frame.empty or "unitid" not in frame.columns:
        return empty
    work = frame.copy()
    work["unitid"] = pd.to_numeric(work["unitid"], errors="coerce")
    work["year"] = pd.to_numeric(work.get("year"), errors="coerce")
    work["oncampus_housing"] = pd.to_numeric(work.get("oncampus_housing"), errors="coerce")
    work["dormitory_capacity"] = pd.to_numeric(work.get("dormitory_capacity"), errors="coerce")
    reported = work[work["oncampus_housing"].isin([0, 1])].dropna(subset=["unitid"])
    if reported.empty:
        return empty
    latest = reported.sort_values(["unitid", "year"]).groupby("unitid", as_index=False).tail(1)
    latest = latest.rename(columns={"year": "housing_year"})
    keep = [c for c in HOUSING_COLUMNS if c in latest.columns]
    return latest[keep].reset_index(drop=True)


def is_residential(row: pd.Series | dict) -> bool:
    """On-campus housing is 1 and dorm capacity is a positive count.

    Sentinel capacities (-1, -2, -3) are not beds.
    """
    housing = _num(row.get("oncampus_housing"))
    capacity = _num(row.get("dormitory_capacity"))
    if housing != 1:
        return False
    if capacity is None or capacity in HOUSING_SENTINELS:
        return False
    return capacity > 0


def is_small_housing(row: pd.Series | dict) -> bool:
    capacity = _num(row.get("dormitory_capacity"))
    if capacity is None or capacity in HOUSING_SENTINELS:
        return False
    return 0 < capacity < SMALL_HOUSING_BELOW


def own_campus_value(row: pd.Series | dict) -> str:
    return _text(row.get("own_campus")).lower()


def acquisition_ready(row: pd.Series | dict) -> bool:
    """Still operating, residential, and curated own_campus = yes."""
    if operating_bucket(row) != OPEN_BUCKET:
        return False
    if not is_residential(row):
        return False
    return own_campus_value(row) == "yes"


def exclusion_reason(row: pd.Series | dict) -> str:
    """Why an otherwise walked row is off the acquisition list.

    Closed and teach-out rows are not given an exclusion reason; those
    sections already explain them.
    """
    bucket = operating_bucket(row)
    if bucket != OPEN_BUCKET:
        return ""
    if not is_residential(row):
        return "no on-campus dorms"
    own = own_campus_value(row)
    if own == "no":
        return "no standalone campus"
    if own != "yes":
        return "campus not confirmed"
    return ""


def load_campus_land(path: Path | None) -> pd.DataFrame:
    if path is None or not Path(path).exists():
        return pd.DataFrame(columns=list(LAND_COLUMNS))
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    return frame


def load_housing_snapshot(path: Path | None) -> pd.DataFrame:
    if path is None or not Path(path).exists():
        return pd.DataFrame(columns=list(HOUSING_COLUMNS))
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if "unitid" in frame.columns:
        frame["unitid"] = pd.to_numeric(frame["unitid"], errors="coerce")
    return frame


def attach_campus(
    table: pd.DataFrame,
    housing: pd.DataFrame | None = None,
    land: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Join housing and land onto a status table without touching curated source_url."""
    if table is None or table.empty:
        return table.copy() if table is not None else pd.DataFrame()
    out = table.copy()
    out["unitid"] = pd.to_numeric(out["unitid"], errors="coerce")
    if housing is not None and not housing.empty and "unitid" in housing.columns:
        piece = housing.copy()
        piece["unitid"] = pd.to_numeric(piece["unitid"], errors="coerce")
        cols = [c for c in HOUSING_COLUMNS if c in piece.columns]
        out = out.drop(columns=[c for c in cols if c != "unitid" and c in out.columns], errors="ignore")
        out = out.merge(piece[cols].drop_duplicates("unitid"), on="unitid", how="left")
    if land is not None and not land.empty and "unitid" in land.columns:
        piece = land.copy()
        piece["unitid"] = pd.to_numeric(piece["unitid"], errors="coerce")
        rename = {
            "source_url": "campus_source_url",
            "checked_at": "campus_checked_at",
            "notes": "campus_notes",
        }
        piece = piece.rename(columns={k: v for k, v in rename.items() if k in piece.columns})
        keep = [
            c
            for c in (
                "unitid",
                "acreage",
                "own_campus",
                "campus_source_url",
                "campus_checked_at",
                "image_url",
                "image_credit_url",
                "image_license",
                "image_author",
                "campus_notes",
                "lat",
                "lon",
                "coord_source",
                "campus_map_url",
            )
            if c in piece.columns
        ]
        out = out.drop(columns=[c for c in keep if c != "unitid" and c in out.columns], errors="ignore")
        out = out.merge(piece[keep].drop_duplicates("unitid"), on="unitid", how="left")
    return out


def _frame(prefix: pd.DataFrame, rows: list[pd.Series]) -> pd.DataFrame:
    if not rows:
        return prefix.iloc[0:0].copy()
    return pd.DataFrame(rows)


def prefix_through_acquisition(table: pd.DataFrame, open_n: int) -> pd.DataFrame:
    """Rows from rank 1 through the row that fills ``open_n`` acquisition-ready schools.

    If the ranked frame runs out first, the whole frame is returned.
    """
    if table is None or table.empty:
        return table.copy() if table is not None else pd.DataFrame()
    if open_n <= 0:
        return table.iloc[0:0].copy()
    seen = 0
    cutoff = len(table)
    for i, (_, row) in enumerate(table.iterrows()):
        if acquisition_ready(row):
            seen += 1
            if seen >= open_n:
                cutoff = i + 1
                break
    return table.iloc[:cutoff].copy()


def partition_acquisition(
    table: pd.DataFrame, open_n: int
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, int]:
    """Split the walked prefix into acquisition, excluded, teach-out, and closed.

    Depth is the watch-list rank of the last row walked.
    """
    prefix = prefix_through_acquisition(table, open_n)
    grouped: dict[str, list[pd.Series]] = {
        ACQUISITION: [],
        EXCLUDED: [],
        TEACHOUT_BUCKET: [],
        CLOSED_BUCKET: [],
    }
    for _, row in prefix.iterrows():
        if acquisition_ready(row):
            grouped[ACQUISITION].append(row)
            continue
        bucket = operating_bucket(row)
        if bucket == TEACHOUT_BUCKET:
            grouped[TEACHOUT_BUCKET].append(row)
        elif bucket == CLOSED_BUCKET:
            grouped[CLOSED_BUCKET].append(row)
        elif bucket == OPEN_BUCKET:
            grouped[EXCLUDED].append(row)
    depth = 0
    if not prefix.empty and "watchlist_rank" in prefix.columns:
        try:
            depth = int(float(prefix.iloc[-1]["watchlist_rank"]))
        except (TypeError, ValueError):
            depth = int(len(prefix))
    return (
        _frame(prefix, grouped[ACQUISITION]),
        _frame(prefix, grouped[EXCLUDED]),
        _frame(prefix, grouped[TEACHOUT_BUCKET]),
        _frame(prefix, grouped[CLOSED_BUCKET]),
        depth,
    )


def extend_ranked_universe(watch: pd.DataFrame, scored: pd.DataFrame | None) -> pd.DataFrame:
    """Append later score-year rows after the watch list, in risk-score order.

    Ranks continue after the last watch-list rank. Schools already on the
    watch list are not repeated. A missing scored frame leaves the watch
    list unchanged.
    """
    if watch is None or watch.empty:
        return watch.copy() if watch is not None else pd.DataFrame()
    frame = watch.copy()
    if "watchlist_rank" not in frame.columns:
        frame["watchlist_rank"] = range(1, len(frame) + 1)
    if (
        scored is None
        or scored.empty
        or "unitid" not in scored.columns
        or "risk_score" not in scored.columns
    ):
        return frame
    extra = scored.copy()
    extra["unitid"] = pd.to_numeric(extra["unitid"], errors="coerce")
    have = {
        int(v)
        for v in pd.to_numeric(frame["unitid"], errors="coerce").dropna().tolist()
    }
    extra = extra[extra["unitid"].notna() & ~extra["unitid"].astype(int).isin(have)]
    if "year" in frame.columns and "year" in extra.columns and not frame.empty:
        try:
            year = int(float(frame.iloc[0]["year"]))
            extra = extra[pd.to_numeric(extra["year"], errors="coerce") == year]
        except (TypeError, ValueError):
            pass
    if extra.empty:
        return frame
    extra = extra.sort_values("risk_score", ascending=False)
    try:
        start = int(float(pd.to_numeric(frame["watchlist_rank"], errors="coerce").max())) + 1
    except (TypeError, ValueError):
        start = len(frame) + 1
    extra = extra.copy()
    extra["watchlist_rank"] = range(start, start + len(extra))
    return pd.concat([frame, extra], ignore_index=True)


def _coord_text(number: float) -> str:
    return f"{number:.6f}".rstrip("0").rstrip(".")


def satellite_maps_url(lat, lon) -> str:
    """Google Maps satellite view centered on a campus.

    Blank when either coordinate is missing. The link is the public Maps URL
    ``center=LAT,LON`` at zoom 17 on the satellite basemap.
    """
    lat_n = _num(lat)
    lon_n = _num(lon)
    if lat_n is None or lon_n is None:
        return ""
    if not (-90.0 <= lat_n <= 90.0 and -180.0 <= lon_n <= 180.0):
        return ""
    return (
        "https://www.google.com/maps/@?api=1&map_action=map"
        f"&center={_coord_text(lat_n)},{_coord_text(lon_n)}&zoom=17&basemap=satellite"
    )


def campus_land_path(settings) -> Path:
    cfg = (settings.raw.get("status") or {}) if settings is not None else {}
    rel = cfg.get("campus_land_csv") or "data/campus/campus_land.csv"
    return settings.root / rel


def housing_snapshot_path(settings) -> Path:
    cfg = (settings.raw.get("status") or {}) if settings is not None else {}
    rel = cfg.get("housing_csv") or "data/campus/housing_latest.csv"
    return settings.root / rel


def ranked_universe_path(settings) -> Path:
    cfg = (settings.raw.get("status") or {}) if settings is not None else {}
    rel = cfg.get("ranked_universe_csv") or "outputs/ranked_universe.csv"
    return settings.root / rel


def load_ranked_universe(path: Path) -> pd.DataFrame:
    """Score-year ranking committed for walks that continue past the top 500.

    An empty frame is returned when the file is missing. ``extend_ranked_universe``
    then leaves the watch list unchanged.
    """
    path = Path(path)
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path)
    for col in ("unitid", "year", "risk_score"):
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
    return frame


RANKED_EXPORT_COLUMNS = (
    "unitid",
    "opeid8",
    "opeid6",
    "opeid",
    "inst_name",
    "state_abbr",
    "city",
    "year",
    "inst_control",
    "sector",
    "fte",
    "risk_score",
    "enr_pct_chg_5y",
    "enr_pct_chg_1y",
    "ftft_pct_chg_1y",
    "discount_rate",
    "operating_margin",
    "tuition_dependence",
    "composite_score",
    "composite_zone",
    "composite_fail",
    "miss_finance",
    "finance_from_parent",
    "year_finance",
    "year_enrollment",
    "year_fall_enrollment",
    "year_admissions",
    "year_staff",
    "year_directory",
    "label_complete_h3",
    "closed_or_merged_within_3_years",
)


def write_ranked_universe(scored: pd.DataFrame, path: Path, *, prefer_year: int | None = None) -> int:
    """Write the score-year ranking that continues the watch list.

    ``prefer_year`` keeps the continuation on the same year as the committed
    watch list when that year is still in the scored panel.
    """
    current, score_year = select_score_year(scored)
    if prefer_year and not scored.empty and "year" in scored.columns:
        years = set(pd.to_numeric(scored["year"], errors="coerce").dropna().astype(int))
        if int(prefer_year) in years:
            held = scored
            if "label_complete_h3" in scored.columns:
                incomplete = scored.loc[scored["label_complete_h3"] != True]  # noqa: E712
                if int(prefer_year) in set(pd.to_numeric(incomplete["year"], errors="coerce").dropna().astype(int)):
                    held = incomplete
            current = held.loc[pd.to_numeric(held["year"], errors="coerce") == int(prefer_year)].copy()
            if "risk_score" in current.columns:
                current = current.sort_values("risk_score", ascending=False)
            current = current.reset_index(drop=True)
            score_year = int(prefer_year)
    if current.empty:
        return 0
    current = current.copy()
    current.insert(0, "universe_rank", range(1, len(current) + 1))
    cols = ["universe_rank", *[c for c in RANKED_EXPORT_COLUMNS if c in current.columns]]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    current[cols].to_csv(path, index=False)
    return len(current)


def select_score_year(scored: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Right-censored score year used for the published watch list.

    Matches the report: latest year whose finance is not missing for most
    schools, among years whose 3-year outcome is not yet complete.
    """
    if scored is None or scored.empty:
        return pd.DataFrame(), 0
    if "label_complete_h3" in scored.columns:
        current = scored.loc[scored["label_complete_h3"] != True].copy()  # noqa: E712
    else:
        current = scored.iloc[0:0].copy()
    if current.empty and "year" in scored.columns:
        ymax = int(pd.to_numeric(scored["year"], errors="coerce").max())
        current = scored.loc[pd.to_numeric(scored["year"], errors="coerce") == ymax].copy()
    if current.empty or "year" not in current.columns:
        return current, 0
    score_year = int(pd.to_numeric(current["year"], errors="coerce").max())
    if "miss_finance" in current.columns:
        rates = current.groupby("year")["miss_finance"].mean()
        usable = rates[rates < 0.50]
        if len(usable):
            score_year = int(usable.index.max())
    current = current.loc[pd.to_numeric(current["year"], errors="coerce") == score_year].copy()
    if "risk_score" in current.columns:
        current = current.sort_values("risk_score", ascending=False)
    return current.reset_index(drop=True), score_year
