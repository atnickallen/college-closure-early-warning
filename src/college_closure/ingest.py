"""Download Urban IPEDS extracts and write filtered Parquet tables."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from college_closure.config import Settings
from college_closure.constants import FINANCE_PANEL_COLUMNS
from college_closure.filters import filter_college_universe, replace_sentinels
from college_closure.qa import write_qa_counts
from college_closure.urban import UrbanClient, read_csv_filtered

LOGGER = logging.getLogger(__name__)


def _write_parquet(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    LOGGER.info("Wrote %s rows × %s cols -> %s", len(df), df.shape[1], path)
    return path


def ingest_directory(settings: Settings, client: UrbanClient) -> pd.DataFrame:
    spec = settings.sources["directory"]
    dest = client.download_csv(spec["csv_file"], spec.get("csv_dir", "ipeds"))
    if dest is None:
        raise RuntimeError(
            "Required directory CSV missing. Tried "
            f"{settings.csv_base}/{spec.get('csv_dir', 'ipeds')}/{spec['csv_file']}"
        )
    years = client.resolve_year_range(spec.get("endpoint_id"))
    raw = read_csv_filtered(dest, year_min=min(years), year_max=max(years))
    if raw.empty:
        raise RuntimeError("Directory CSV downloaded but produced no rows in the configured year range.")
    if "unitid" not in raw.columns:
        raise RuntimeError(f"Directory extract missing unitid. Columns: {list(raw.columns)[:20]}")
    LOGGER.info("Directory raw rows %s years %s–%s", len(raw), raw["year"].min(), raw["year"].max())
    _write_parquet(raw, settings.processed_dir / "directory_raw.parquet")
    filtered = filter_college_universe(raw, settings.filters)
    _write_parquet(filtered, settings.processed_dir / "directory.parquet")
    return filtered


def ingest_fall_enrollment(settings: Settings, client: UrbanClient) -> pd.DataFrame:
    spec = settings.sources["fall_enrollment"]
    years = client.resolve_year_range(spec.get("endpoint_id"))
    available = set(client.years_for_endpoint(spec["endpoint_id"]))
    api_filters = spec.get("api_filters") or {}
    frames: list[pd.DataFrame] = []
    notes: list[str] = []

    for year in years:
        if available and year not in available:
            msg = f"fall-enrollment year {year} not in Urban years_available; skipping"
            LOGGER.warning(msg)
            notes.append(msg)
            continue
        year_frames: list[pd.DataFrame] = []
        for level in spec.get("levels") or ["undergraduate", "graduate"]:
            path = f"college-university/ipeds/fall-enrollment/{year}/{level}/race/sex"
            cache = f"fall_enrollment_{year}_{level}_totals"
            frame = client.fetch_api_pages(path, params=api_filters, cache_name=cache)
            if frame.empty:
                notes.append(f"No fall-enrollment rows for {year} {level}")
                continue
            year_frames.append(frame)
        if not year_frames:
            # Fallback: yearly race CSV, keep totals only
            csv_name = (spec.get("csv_pattern") or "").format(year=year)
            if csv_name:
                dest = client.download_csv(csv_name, spec.get("csv_dir", "ipeds"))
                if dest is not None:
                    csv_df = read_csv_filtered(dest, extra_equals=api_filters)
                    if not csv_df.empty:
                        year_frames.append(csv_df)
                    else:
                        notes.append(f"Yearly CSV {csv_name} had no total rows")
                else:
                    notes.append(
                        f"Tried API + CSV for fall-enrollment {year}: "
                        f"{settings.csv_base}/{spec.get('csv_dir', 'ipeds')}/{csv_name}"
                    )
        if year_frames:
            frames.append(pd.concat(year_frames, ignore_index=True))

    if not frames:
        LOGGER.error("Fall enrollment produced no rows")
        return pd.DataFrame()

    raw = pd.concat(frames, ignore_index=True)
    raw = replace_sentinels(raw, ["enrollment_fall"])
    wide = _reshape_fall_enrollment(raw)
    _write_parquet(wide, settings.processed_dir / "fall_enrollment.parquet")
    if notes:
        LOGGER.info("Fall-enrollment notes: %s", "; ".join(notes[:12]))
    return wide


def _reshape_fall_enrollment(raw: pd.DataFrame) -> pd.DataFrame:
    """One row per UNITID×year with UG / graduate / total fall headcount."""
    work = raw.copy()
    if "enrollment_fall" not in work.columns:
        # Some extracts use `enrollment`
        if "enrollment" in work.columns:
            work = work.rename(columns={"enrollment": "enrollment_fall"})
        else:
            LOGGER.warning("Fall enrollment extract missing enrollment_fall")
            return pd.DataFrame(columns=["unitid", "year"])

    # Prefer already-total rows; if ftpt etc. still vary, take the max total-like row.
    for col, total in (("ftpt", 99), ("sex", 99), ("race", 99), ("degree_seeking", 99), ("class_level", 99)):
        if col in work.columns:
            totals = work[work[col] == total]
            if not totals.empty:
                work = totals

    keys = ["unitid", "year"]
    work = (
        work.groupby(keys + (["level_of_study"] if "level_of_study" in work.columns else []), dropna=False)[
            "enrollment_fall"
        ]
        .max()
        .reset_index()
    )
    if "level_of_study" not in work.columns:
        work = work.rename(columns={"enrollment_fall": "enrollment_fall_total"})
        return work

    pivot = work.pivot_table(
        index=keys,
        columns="level_of_study",
        values="enrollment_fall",
        aggfunc="max",
    )
    pivot.columns = [f"level_{int(c)}" if pd.notna(c) else "level_na" for c in pivot.columns]
    out = pivot.reset_index()
    out["enrollment_fall_ug"] = out["level_1"] if "level_1" in out.columns else pd.NA
    out["enrollment_fall_grad"] = out["level_2"] if "level_2" in out.columns else pd.NA
    first_prof = out["level_3"] if "level_3" in out.columns else 0
    out["enrollment_fall_total"] = (
        pd.to_numeric(out["enrollment_fall_ug"], errors="coerce").fillna(0)
        + pd.to_numeric(out["enrollment_fall_grad"], errors="coerce").fillna(0)
        + pd.to_numeric(first_prof, errors="coerce").fillna(0)
    )
    keep = [
        "unitid",
        "year",
        "enrollment_fall_ug",
        "enrollment_fall_grad",
        "enrollment_fall_total",
    ]
    return out[keep]


def ingest_enrollment_fte(settings: Settings, client: UrbanClient) -> pd.DataFrame:
    spec = settings.sources["enrollment_fte"]
    dest = client.download_csv(spec["csv_file"], spec.get("csv_dir", "ipeds"))
    if dest is None:
        LOGGER.warning(
            "FTE CSV missing; tried %s/%s/%s",
            settings.csv_base,
            spec.get("csv_dir", "ipeds"),
            spec["csv_file"],
        )
        return pd.DataFrame()
    years = client.resolve_year_range(spec.get("endpoint_id"))
    raw = read_csv_filtered(dest, year_min=min(years), year_max=max(years))
    if raw.empty:
        return raw
    value_col = "est_fte" if "est_fte" in raw.columns else None
    if value_col is None:
        for candidate in ("rep_fte", "fte", "enrollment_fte"):
            if candidate in raw.columns:
                value_col = candidate
                break
    if value_col is None:
        LOGGER.warning("FTE extract has no est_fte/rep_fte columns: %s", list(raw.columns)[:20])
        return pd.DataFrame()
    raw = replace_sentinels(raw, [value_col, "credit_hours", "contact_hours"])
    if "level_of_study" in raw.columns:
        pivot = raw.pivot_table(
            index=["unitid", "year"],
            columns="level_of_study",
            values=value_col,
            aggfunc="max",
        )
        pivot.columns = [f"fte_level_{int(c)}" if pd.notna(c) else "fte_level_na" for c in pivot.columns]
        out = pivot.reset_index()
        out["enrollment_fte_ug"] = out["fte_level_1"] if "fte_level_1" in out.columns else pd.NA
        out["enrollment_fte_grad"] = out["fte_level_2"] if "fte_level_2" in out.columns else pd.NA
        out["enrollment_fte"] = pd.to_numeric(out["enrollment_fte_ug"], errors="coerce").fillna(0) + pd.to_numeric(
            out["enrollment_fte_grad"], errors="coerce"
        ).fillna(0)
        out = out[["unitid", "year", "enrollment_fte", "enrollment_fte_ug", "enrollment_fte_grad"]]
    else:
        out = raw.groupby(["unitid", "year"], as_index=False)[value_col].max()
        out = out.rename(columns={value_col: "enrollment_fte"})
    _write_parquet(out, settings.processed_dir / "enrollment_fte.parquet")
    return out


def ingest_finance(settings: Settings, client: UrbanClient) -> pd.DataFrame:
    spec = settings.sources["finance"]
    dest = client.download_csv(spec["csv_file"], spec.get("csv_dir", "ipeds"))
    if dest is None:
        LOGGER.warning(
            "Finance CSV missing; tried %s/%s/%s",
            settings.csv_base,
            spec.get("csv_dir", "ipeds"),
            spec["csv_file"],
        )
        return pd.DataFrame()
    years = client.resolve_year_range(spec.get("endpoint_id"))
    raw = read_csv_filtered(dest, year_min=min(years), year_max=max(years))
    if raw.empty:
        LOGGER.warning("Finance CSV had no rows in %s–%s", min(years), max(years))
        return raw
    keep = ["unitid", "year"] + [c for c in FINANCE_PANEL_COLUMNS if c in raw.columns]
    slim = replace_sentinels(raw[keep], [c for c in keep if c not in {"unitid", "year", "parent_unitid", "parent_child_flag"}])
    actual_max = int(slim["year"].max()) if not slim.empty else None
    if actual_max is not None and actual_max < max(years):
        LOGGER.warning(
            "Urban IPEDS finance currently ends in %s (requested through %s). "
            "This is a known portal gap vs NCES IPEDS Finance.",
            actual_max,
            max(years),
        )
    _write_parquet(slim, settings.processed_dir / "finance.parquet")
    return slim


def ingest_admissions(settings: Settings, client: UrbanClient) -> pd.DataFrame:
    spec = settings.sources["admissions"]
    dest = client.download_csv(spec["csv_file"], spec.get("csv_dir", "ipeds"))
    if dest is None:
        LOGGER.warning(
            "Admissions CSV missing; tried %s/%s/%s",
            settings.csv_base,
            spec.get("csv_dir", "ipeds"),
            spec["csv_file"],
        )
        return pd.DataFrame()
    years = client.resolve_year_range(spec.get("endpoint_id"))
    raw = read_csv_filtered(dest, year_min=min(years), year_max=max(years))
    if raw.empty:
        return raw
    measure_cols = [
        c
        for c in (
            "number_applied",
            "number_admitted",
            "number_enrolled_ft",
            "number_enrolled_pt",
            "number_enrolled_total",
        )
        if c in raw.columns
    ]
    raw = replace_sentinels(raw, measure_cols)
    if "sex" in raw.columns:
        totals = raw[raw["sex"] == 99]
        if totals.empty:
            totals = raw.groupby(["unitid", "year"], as_index=False)[measure_cols].sum(min_count=1)
        else:
            totals = totals[["unitid", "year"] + measure_cols]
    else:
        totals = raw[["unitid", "year"] + measure_cols]
    if "number_applied" in totals.columns and "number_admitted" in totals.columns:
        applied = pd.to_numeric(totals["number_applied"], errors="coerce")
        admitted = pd.to_numeric(totals["number_admitted"], errors="coerce")
        totals = totals.copy()
        totals["admit_rate"] = admitted / applied.replace({0: pd.NA})
    _write_parquet(totals, settings.processed_dir / "admissions.parquet")
    return totals


def ingest_staffing(settings: Settings, client: UrbanClient, key: str) -> pd.DataFrame:
    spec = settings.sources[key]
    years = client.resolve_year_range(spec.get("endpoint_id"))
    available = set(client.years_for_endpoint(spec["endpoint_id"]))
    frames: list[pd.DataFrame] = []
    for year in years:
        if available and year not in available:
            LOGGER.warning("%s year %s not in Urban years_available; skipping", key, year)
            continue
        path = f"college-university/ipeds/{spec['endpoint']}/{year}"
        frame = client.fetch_api_pages(
            path,
            params=spec.get("api_filters") or {},
            cache_name=f"{key}_{year}_totals",
        )
        # Pre-2012 instructional-staff files use contract_length in {5,6,7,8}, not 99.
        if frame.empty and key == "instructional_staff":
            relaxed = {"academic_rank": 99, "sex": 99}
            frame = client.fetch_api_pages(
                path,
                params=relaxed,
                cache_name=f"{key}_{year}_totals_relaxed",
            )
            if not frame.empty:
                LOGGER.info(
                    "Instructional staff %s: used academic_rank=99&sex=99 "
                    "(contract_length=99 not present in this year)",
                    year,
                )
        if frame.empty:
            LOGGER.warning("No %s rows for %s", key, year)
            continue
        frames.append(frame)
    if not frames:
        csv_file = spec.get("csv_file")
        if csv_file:
            dest = client.download_csv(csv_file, spec.get("csv_dir", "ipeds"))
            if dest is not None:
                frames.append(read_csv_filtered(dest, year_min=min(years), year_max=max(years)))
    if not frames:
        return pd.DataFrame()
    raw = pd.concat(frames, ignore_index=True)
    count_col = "instruc_staff_count" if "instruc_staff_count" in raw.columns else "noninstruc_staff_count"
    keep = ["unitid", "year"]
    if count_col in raw.columns:
        keep.append(count_col)
    if "salary_outlays" in raw.columns:
        keep.append("salary_outlays")
    slim = replace_sentinels(raw[keep], [c for c in keep if c not in {"unitid", "year"}])
    slim = slim.groupby(["unitid", "year"], as_index=False).max()
    _write_parquet(slim, settings.processed_dir / f"{key}.parquet")
    return slim


def run_ingest(
    settings: Settings,
    sources: list[str] | None = None,
) -> dict[str, pd.DataFrame]:
    client = UrbanClient(settings)
    wanted = sources or [
        "directory",
        "fall_enrollment",
        "enrollment_fte",
        "finance",
        "admissions",
        "instructional_staff",
        "noninstructional_staff",
    ]
    results: dict[str, pd.DataFrame] = {}
    notes: list[str] = []

    if "directory" in wanted:
        results["directory"] = ingest_directory(settings, client)
    else:
        path = settings.processed_dir / "directory.parquet"
        if path.exists():
            results["directory"] = pd.read_parquet(path)
        else:
            raise RuntimeError("directory is required; re-run with directory in --sources")

    if "fall_enrollment" in wanted:
        results["fall_enrollment"] = ingest_fall_enrollment(settings, client)
    if "enrollment_fte" in wanted:
        results["enrollment_fte"] = ingest_enrollment_fte(settings, client)
    if "finance" in wanted:
        results["finance"] = ingest_finance(settings, client)
        finance = results["finance"]
        if not finance.empty:
            notes.append(
                f"Finance years present: {int(finance['year'].min())}–{int(finance['year'].max())}. "
                "Urban portal finance currently ends in 2017 (api-endpoints id 91)."
            )
        else:
            notes.append(
                "Finance extract empty. URL tried: "
                f"{settings.csv_base}/ipeds/colleges_ipeds_finance.csv"
            )
    if "admissions" in wanted:
        results["admissions"] = ingest_admissions(settings, client)
    if "instructional_staff" in wanted:
        results["instructional_staff"] = ingest_staffing(settings, client, "instructional_staff")
    if "noninstructional_staff" in wanted:
        results["noninstructional_staff"] = ingest_staffing(settings, client, "noninstructional_staff")
    if "academic_libraries" in wanted:
        from college_closure.libraries import ingest_academic_libraries

        results["academic_libraries"] = ingest_academic_libraries(settings, client=client)

    directory = results["directory"]
    write_qa_counts(
        settings.outputs_dir / "qa_counts.md",
        title="QA: filtered college universe (IPEDS directory)",
        directory=directory,
        notes=notes
        + [
            "Every institution is keyed on UNITID. Directory also carries opeid and ein "
            "for the Phase 2 UNITID↔OPEID↔EIN crosswalk (see scripts/02_crosswalk.py).",
            "Public institutions (control=1) remain in the panel; "
            "in_risk_model_universe flags private nonprofit and for-profit rows.",
        ],
    )
    LOGGER.info("Wrote %s", settings.outputs_dir / "qa_counts.md")
    return results
