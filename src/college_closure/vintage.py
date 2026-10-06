"""Current-year score snapshot from the newest complete federal vintage.

Training rows stay contemporaneous. The published watch list is one row per
school still in the panel at the finance score year. Each model feature is
taken from that source's newest complete year when the school reported it,
and otherwise from the latest earlier year with a value. The year used is
stored on ``{feature}_year``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

# (feature, availability column). None means any row in the preferred year
# counts, including a false or missing flag that is filled on every row.
ENROLLMENT_FEATURES: tuple[tuple[str, str | None], ...] = (
    ("log_fte", "fte"),
    ("fte_under_1000", "fte"),
    ("enr_pct_chg_1y", "enr_pct_chg_1y"),
    ("enr_pct_chg_5y", "enr_pct_chg_5y"),
    ("enr_pct_chg_10y", "enr_pct_chg_10y"),
    ("enr_decline_5y_gt30", "enr_pct_chg_5y"),
    ("fte", "fte"),
)
ADMISSIONS_FEATURES: tuple[tuple[str, str | None], ...] = (
    ("ftft_pct_chg_1y", "ftft_pct_chg_1y"),
    ("admit_rate", "admit_rate"),
    ("yield_rate", "yield_rate"),
    ("admit_rate_chg_5y", "admit_rate_chg_5y"),
    ("yield_rate_chg_5y", "yield_rate_chg_5y"),
)
FINANCE_FEATURES: tuple[tuple[str, str | None], ...] = (
    ("tuition_dependence", "tuition_dependence"),
    ("discount_rate", "discount_rate"),
    ("discount_rate_chg_5y", "discount_rate_chg_5y"),
    ("operating_margin", "operating_margin"),
    ("operating_margin_chg_5y", "operating_margin_chg_5y"),
    ("consec_neg_margin_yrs", "operating_margin"),
    ("endowment_per_fte", "endowment_per_fte"),
    ("unrestricted_na_to_exp", "unrestricted_na_to_exp"),
    ("high_tuition_dependence", "tuition_dependence"),
    ("miss_finance", None),
    ("finance_from_parent", None),
)
STAFF_FEATURES: tuple[tuple[str, str | None], ...] = (
    ("staff_pct_chg_1y", "staff_pct_chg_1y"),
    ("staff_pct_chg_5y", "staff_pct_chg_5y"),
    ("student_staff_ratio", "student_staff_ratio"),
    ("student_staff_ratio_chg_1y", "student_staff_ratio_chg_1y"),
)
DIRECTORY_FEATURES: tuple[tuple[str, str | None], ...] = (
    ("is_four_year", None),
    ("religious", None),
    ("urban", None),
    ("rural", None),
    ("inst_control", None),
    ("sector", None),
)
COMPOSITE_FEATURES: tuple[tuple[str, str | None], ...] = (
    ("composite_score", "composite_score"),
    ("composite_fail", "composite_score"),
    ("composite_zone", "composite_score"),
    ("composite_is_lagged", None),
    ("years_in_zone", None),
    ("miss_composite", None),
)
WICHE_FEATURES: tuple[tuple[str, str | None], ...] = (("hs_grad_pct_chg_5y", "hs_grad_pct_chg_5y"),)

SOURCE_FEATURES: dict[str, tuple[tuple[str, str | None], ...]] = {
    "enrollment": ENROLLMENT_FEATURES,
    "admissions": ADMISSIONS_FEATURES,
    "finance": FINANCE_FEATURES,
    "staff": STAFF_FEATURES,
    "directory": DIRECTORY_FEATURES,
    "composite": COMPOSITE_FEATURES,
    "wiche": WICHE_FEATURES,
}

SOURCE_ANCHORS = {
    "enrollment": "fte",
    "admissions": "admit_rate",
    "staff": "student_staff_ratio",
    "directory": "inst_name",
    "composite": "composite_score",
    "wiche": "hs_grad_pct_chg_5y",
    "fall_enrollment": "enrollment_fall_total",
}

SOURCE_YEAR_COLUMNS = {
    "finance": "year_finance",
    "enrollment": "year_enrollment",
    "admissions": "year_admissions",
    "staff": "year_staff",
    "directory": "year_directory",
    "composite": "year_composite",
    "wiche": "year_wiche",
    "fall_enrollment": "year_fall_enrollment",
}


def newest_complete_year(counts: pd.Series, *, min_ratio: float = 0.8, lookback: int = 5) -> int | None:
    """Newest year whose row count is close to the recent peak.

    A stub release (a handful of rows in a new year) is skipped. Counts are
    compared with the peak inside a short lookback so a long decline in the
    number of institutions does not mark a full recent file incomplete.
    """
    if counts is None or len(counts) == 0:
        return None
    counts = pd.to_numeric(counts, errors="coerce").dropna()
    counts.index = counts.index.astype(int)
    for year in sorted((int(y) for y in counts.index), reverse=True):
        window = counts[(counts.index >= year - lookback) & (counts.index <= year)]
        peak = float(window.max()) if len(window) else 0.0
        if peak > 0 and float(counts.loc[year]) >= min_ratio * peak:
            return int(year)
    return int(counts.idxmax())


def finance_complete_year(frame: pd.DataFrame) -> int | None:
    """Latest year whose finance is present for most schools.

    Matches the watch-list rule: a year with ``miss_finance`` at or above 50%
    is unpublished finance, not a score year.
    """
    if frame is None or frame.empty or "miss_finance" not in frame.columns or "year" not in frame.columns:
        return None
    work = frame.copy()
    work["year"] = pd.to_numeric(work["year"], errors="coerce")
    rates = work.groupby("year")["miss_finance"].mean()
    usable = rates[rates < 0.50]
    if usable.empty:
        return None
    return int(usable.index.max())


def _anchor_counts(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame.columns or "year" not in frame.columns:
        return pd.Series(dtype=float)
    work = frame.copy()
    work["year"] = pd.to_numeric(work["year"], errors="coerce")
    present = work[column].notna()
    return present.groupby(work["year"]).sum()


def detect_source_years(frame: pd.DataFrame) -> dict:
    """National complete year for each source on a feature panel."""
    finance_year = finance_complete_year(frame)
    sources: dict[str, dict] = {}
    if finance_year is not None:
        sources["finance"] = {"complete_year": int(finance_year)}
    for name, column in SOURCE_ANCHORS.items():
        counts = _anchor_counts(frame, column)
        year = newest_complete_year(counts)
        if year is not None:
            sources[name] = {"complete_year": int(year)}
    if "staff" not in sources:
        counts = _anchor_counts(frame, "staff_pct_chg_1y")
        year = newest_complete_year(counts)
        if year is not None:
            sources["staff"] = {"complete_year": int(year)}
    return {"score_year": finance_year, "sources": sources}


def _risk_pool(frame: pd.DataFrame) -> pd.DataFrame:
    work = frame.copy()
    work["unitid"] = pd.to_numeric(work["unitid"], errors="coerce")
    work["year"] = pd.to_numeric(work["year"], errors="coerce")
    work = work.dropna(subset=["unitid", "year"])
    work["unitid"] = work["unitid"].astype(int)
    work["year"] = work["year"].astype(int)
    if "in_risk_model_universe" in work.columns:
        pool = work.loc[work["in_risk_model_universe"] == True].copy()  # noqa: E712
    else:
        pool = work
    return pool.drop_duplicates(["unitid", "year"], keep="last")


def _choose_feature(
    pool: pd.DataFrame,
    feature: str,
    preferred: int | None,
    available: str | None,
) -> pd.DataFrame:
    if feature not in pool.columns:
        return pd.DataFrame(columns=["unitid", "value", "year"])
    mask = pd.Series(True, index=pool.index)
    gate = available if available and available in pool.columns else None
    if gate is not None:
        mask = pool[gate].notna()
    elif available and available not in pool.columns:
        mask = pool[feature].notna()
    sub = pool.loc[mask, ["unitid", "year", feature]]
    if preferred is None:
        hit = sub.iloc[0:0]
    else:
        hit = sub.loc[sub["year"] == int(preferred)]
    taken = set(hit["unitid"].tolist())
    rest = sub.loc[~sub["unitid"].isin(taken)]
    if not rest.empty:
        rest = rest.sort_values("year").groupby("unitid", as_index=False).tail(1)
    chosen = pd.concat([hit, rest], ignore_index=True).drop_duplicates("unitid", keep="first")
    return chosen.rename(columns={feature: "value"})


def _align_finance_year(snapshot: pd.DataFrame, pool: pd.DataFrame) -> pd.DataFrame:
    """Point the finance year at a year that actually reported finance.

    ``miss_finance`` is filled on every row, including later years where the
    survey is unpublished. The score should carry the latest reported finance
    ratios and mark finance missing only when no earlier year has them.
    """
    year_cols = [
        col
        for col in (
            "operating_margin_year",
            "tuition_dependence_year",
            "discount_rate_year",
            "unrestricted_na_to_exp_year",
            "endowment_per_fte_year",
        )
        if col in snapshot.columns
    ]
    if not year_cols:
        if "miss_finance_year" in snapshot.columns:
            snapshot["year_finance"] = snapshot["miss_finance_year"]
        return snapshot
    derived = snapshot[year_cols].bfill(axis=1).iloc[:, 0]
    if "miss_finance_year" in snapshot.columns:
        snapshot["year_finance"] = derived.where(derived.notna(), snapshot["miss_finance_year"])
    else:
        snapshot["year_finance"] = derived
    has_finance = derived.notna()
    if "miss_finance" in snapshot.columns:
        snapshot.loc[has_finance, "miss_finance"] = False
        snapshot.loc[~has_finance, "miss_finance"] = True
        snapshot["miss_finance_year"] = snapshot["year_finance"]
    if "finance_from_parent" in pool.columns and "miss_finance" in pool.columns:
        extra = ["finance_from_parent"]
        if "parent_unitid" in pool.columns:
            extra.append("parent_unitid")
        reported = pool.loc[~pool["miss_finance"].fillna(True).astype(bool), ["unitid", "year", *extra]]
        reported = reported.drop_duplicates(["unitid", "year"], keep="last")
        keys = snapshot.loc[has_finance, ["unitid", "year_finance"]].rename(columns={"year_finance": "year"})
        merged = keys.merge(reported, on=["unitid", "year"], how="left")
        parent = pd.Series(False, index=snapshot.index)
        parent.loc[has_finance] = merged["finance_from_parent"].fillna(False).astype(bool).to_numpy()
        snapshot["finance_from_parent"] = parent
        if "parent_unitid" in merged.columns:
            parent_ids = pd.Series(pd.NA, index=snapshot.index, dtype="Float64")
            parent_ids.loc[has_finance] = pd.to_numeric(merged["parent_unitid"], errors="coerce").to_numpy()
            snapshot["parent_unitid"] = parent_ids
        if "finance_from_parent_year" in snapshot.columns:
            snapshot.loc[has_finance, "finance_from_parent_year"] = snapshot.loc[has_finance, "year_finance"]
    if "miss_finance" in snapshot.columns:
        snapshot["insufficient_data"] = snapshot["miss_finance"].fillna(True).astype(bool)
    else:
        snapshot["insufficient_data"] = True
    return snapshot


def build_vintage_snapshot(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """One current row per risk-universe school, with per-feature years."""
    pool = _risk_pool(frame)
    meta = detect_source_years(pool)
    score_year = meta.get("score_year")
    if pool.empty or score_year is None:
        return pool.iloc[0:0].copy(), meta
    latest = pool.groupby("unitid")["year"].transform("max")
    pool = pool.loc[latest >= int(score_year)].copy()
    if pool.empty:
        return pool, meta
    sources = meta["sources"]
    directory_year = (sources.get("directory") or {}).get("complete_year")
    pool["_prefer_directory"] = pool["year"].eq(int(directory_year)) if directory_year is not None else False
    base = (
        pool.sort_values(["unitid", "_prefer_directory", "year"])
        .groupby("unitid", as_index=False)
        .tail(1)
        .drop(columns=["_prefer_directory"])
        .reset_index(drop=True)
    )
    snapshot = base.copy()
    snapshot["year_directory"] = snapshot["year"]
    snapshot["year"] = int(score_year)
    snapshot["label_complete_h3"] = False
    snapshot["vintage_snapshot"] = True
    ids = snapshot["unitid"]
    for source, features in SOURCE_FEATURES.items():
        preferred = (sources.get(source) or {}).get("complete_year")
        for feature, available in features:
            chosen = _choose_feature(pool, feature, preferred, available)
            if chosen.empty:
                continue
            values = chosen.set_index("unitid")["value"]
            years = chosen.set_index("unitid")["year"]
            snapshot[feature] = ids.map(values)
            snapshot[f"{feature}_year"] = ids.map(years)
    for dest, src in (
        ("year_enrollment", "log_fte_year"),
        ("year_admissions", "admit_rate_year"),
        ("year_staff", "student_staff_ratio_year"),
        ("year_composite", "composite_score_year"),
        ("year_wiche", "hs_grad_pct_chg_5y_year"),
    ):
        if src in snapshot.columns:
            snapshot[dest] = snapshot[src]
    snapshot = _align_finance_year(snapshot, pool)
    if "enrollment_fall_total" in pool.columns:
        preferred = (sources.get("fall_enrollment") or {}).get("complete_year")
        chosen = _choose_feature(pool, "enrollment_fall_total", preferred, "enrollment_fall_total")
        if not chosen.empty:
            years = chosen.set_index("unitid")["year"]
            snapshot["year_fall_enrollment"] = ids.map(years)
    meta["n_schools"] = int(len(snapshot))
    return snapshot.reset_index(drop=True), meta


def file_complete_year(path: Path) -> int | None:
    """Newest complete year in a processed parquet, by row count."""
    path = Path(path)
    if not path.exists():
        return None
    frame = pd.read_parquet(path, columns=["year"])
    counts = pd.to_numeric(frame["year"], errors="coerce").dropna().astype(int).value_counts()
    return newest_complete_year(counts)


def scorecard_bulk_label(raw_dir: Path) -> dict:
    """Identify the College Scorecard bulk ZIP on disk, without reading the key."""
    folder = Path(raw_dir) / "scorecard"
    if not folder.exists():
        return {}
    hits = sorted(folder.glob("Most-Recent-Cohorts-Institution_*.zip"))
    if not hits:
        hits = sorted(folder.glob("*.zip"))
    if not hits:
        return {}
    name = hits[-1].name
    digits = ""
    for token in name.replace(".zip", "").split("_"):
        if token.isdigit() and len(token) == 8:
            digits = token
    file_date = ""
    if digits:
        file_date = f"{digits[4:8]}-{digits[0:2]}-{digits[2:4]}"
    return {"file": name, "file_date": file_date}


def source_file_manifest(processed_dir: Path, raw_dir: Path) -> dict:
    """National file vintages used to describe the score, one year per source."""
    processed_dir = Path(processed_dir)
    files = {
        "finance": processed_dir / "finance.parquet",
        "fall_enrollment": processed_dir / "fall_enrollment.parquet",
        "enrollment_fte": processed_dir / "enrollment_fte.parquet",
        "admissions": processed_dir / "admissions.parquet",
        "staff": processed_dir / "instructional_staff.parquet",
        "directory": processed_dir / "directory.parquet",
        "academic_libraries": processed_dir / "libraries.parquet",
    }
    sources: dict[str, dict] = {}
    for name, path in files.items():
        year = file_complete_year(path)
        if year is not None:
            sources[name] = {"complete_year": int(year)}
    if "finance" in sources:
        sources["finance"]["nces_zip_years"] = "2018-2022"
        sources["finance"]["note"] = (
            "Urban IPEDS finance CSV is the complete finance year. "
            "NCES F1819–F2223 complete-data zips fill 2018–2022. "
            "Later NCES standalone zips are not in the panel."
        )
    scorecard = scorecard_bulk_label(raw_dir)
    if scorecard:
        sources["scorecard"] = scorecard
    return sources


def write_vintage_outputs(snapshot: pd.DataFrame, meta: dict, outputs_dir: Path) -> None:
    """Write the source-year manifest and the per-school feature years."""
    outputs_dir = Path(outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    payload = json.loads(json.dumps(meta, default=_json_default))
    (outputs_dir / "vintage_years.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if snapshot is None or snapshot.empty:
        return
    year_cols = [c for c in snapshot.columns if c == "year" or c.startswith("year_") or c.endswith("_year")]
    id_cols = [c for c in ("unitid", "inst_name", "state_abbr") if c in snapshot.columns]
    keep = id_cols + [c for c in year_cols if c not in id_cols]
    snapshot[keep].to_csv(outputs_dir / "feature_years.csv", index=False)


def _json_default(value):
    if isinstance(value, (pd.Timestamp,)):
        return str(value)
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except (ValueError, AttributeError):
            return str(value)
    return str(value)


def merge_file_manifest(meta: dict, manifest: dict) -> dict:
    """Prefer the feature-panel score year; fill source notes from files."""
    out = dict(meta)
    sources = dict(out.get("sources") or {})
    for name, block in manifest.items():
        current = dict(sources.get(name) or {})
        for key, value in block.items():
            current.setdefault(key, value)
        if "complete_year" in block and "complete_year" not in current:
            current["complete_year"] = block["complete_year"]
        sources[name] = current
    out["sources"] = sources
    return out
