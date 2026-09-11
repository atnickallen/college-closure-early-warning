"""QA tables: sector×year counts and missingness flags."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from college_closure.constants import CONTROL_LABELS, SECTOR_LABELS


def counts_by_year_sector(directory: pd.DataFrame) -> pd.DataFrame:
    frame = directory.copy()
    if "sector_label" not in frame.columns:
        frame["sector_label"] = frame.get("sector", pd.Series(dtype="float")).map(SECTOR_LABELS)
    if "control_label" not in frame.columns:
        control = frame["inst_control"] if "inst_control" in frame.columns else frame.get("control")
        frame["control_label"] = control.map(CONTROL_LABELS)
    return (
        frame.groupby(["year", "sector", "sector_label", "control_label"], dropna=False)
        .agg(n_institutions=("unitid", "nunique"), n_rows=("unitid", "size"))
        .reset_index()
        .sort_values(["year", "sector"])
    )


def latest_year_snapshot(directory: pd.DataFrame) -> pd.DataFrame:
    if directory.empty:
        return directory
    latest = int(directory["year"].max())
    snap = directory[directory["year"] == latest]
    return (
        snap.groupby(["control_label", "sector_label"], dropna=False)
        .agg(n_institutions=("unitid", "nunique"))
        .reset_index()
        .sort_values("n_institutions", ascending=False)
    )


def missingness_table(panel: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    rows = []
    for year, chunk in panel.groupby("year"):
        row: dict[str, object] = {
            "year": int(year),
            "n_institutions": int(chunk["unitid"].nunique()),
        }
        if "control_label" in chunk.columns:
            for label in ("public", "private_nonprofit", "for_profit"):
                row[f"n_{label}"] = int((chunk["control_label"] == label).sum())
        for col in columns:
            if col not in chunk.columns:
                row[f"miss_{col}"] = None
                row[f"miss_{col}_pct"] = None
                continue
            miss = chunk[col].isna().mean()
            row[f"miss_{col}"] = int(chunk[col].isna().sum())
            row[f"miss_{col}_pct"] = round(float(miss) * 100, 1)
        rows.append(row)
    return pd.DataFrame(rows).sort_values("year")


def write_markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._\n"
    cols = list(df.columns)
    header = "| " + " | ".join(str(c) for c in cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    lines = [header, sep]
    for _, row in df.iterrows():
        cells = []
        for col in cols:
            val = row[col]
            if pd.isna(val):
                cells.append("")
            elif isinstance(val, float) and val == int(val):
                cells.append(str(int(val)))
            else:
                cells.append(str(val))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def write_qa_counts(
    path: Path,
    *,
    title: str,
    directory: pd.DataFrame,
    notes: list[str] | None = None,
    extra_sections: list[tuple[str, pd.DataFrame | str]] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts = counts_by_year_sector(directory)
    snapshot = latest_year_snapshot(directory)
    unique_ids = int(directory["unitid"].nunique()) if not directory.empty else 0
    year_min = int(directory["year"].min()) if not directory.empty else None
    year_max = int(directory["year"].max()) if not directory.empty else None
    nfp4 = 0
    if not directory.empty and year_max is not None:
        latest = directory[directory["year"] == year_max]
        nfp4 = int(
            latest.loc[
                (latest.get("sector") == 2)
                | (
                    (latest.get("inst_control") == 2)
                    & latest.get("is_four_year", False)
                ),
                "unitid",
            ].nunique()
        )

    parts = [
        f"# {title}",
        "",
        f"- Institution-years: **{len(directory):,}**",
        f"- Unique UNITID: **{unique_ids:,}**",
        f"- Year range: **{year_min}–{year_max}**",
        f"- Private nonprofit 4-year in latest year ({year_max}): **{nfp4:,}**",
        "",
        "Sector codes: 1 public 4-year, 2 private nonprofit 4-year, 3 for-profit 4-year, "
        "4 public 2-year, 5 private nonprofit 2-year, 6 for-profit 2-year, "
        "7–9 less-than-2-year. Administrative units (sector 0) are dropped.",
        "",
        "## Latest-year snapshot by control × sector",
        "",
        write_markdown_table(snapshot),
        "",
        "## Institutions per year × sector",
        "",
        write_markdown_table(counts),
    ]
    if notes:
        parts.extend(["", "## Notes", ""])
        parts.extend(f"- {note}" for note in notes)
        parts.append("")
    if extra_sections:
        for heading, body in extra_sections:
            parts.extend(["", f"## {heading}", ""])
            if isinstance(body, pd.DataFrame):
                parts.append(write_markdown_table(body))
            else:
                parts.append(body)
                parts.append("")
    path.write_text("\n".join(parts), encoding="utf-8")
