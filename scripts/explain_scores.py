#!/usr/bin/env python3
"""Write score explanations for the residential top 50 and refresh the report."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings
from college_closure.explain import (
    build_score_explanations,
    write_explanation_outputs,
)
from college_closure.report import write_operating_report


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    settings = load_settings()
    frame, meta = build_score_explanations(settings)
    write_explanation_outputs(frame, meta, settings.outputs_dir)
    ranked = __import__("pandas").read_csv(settings.outputs_dir / "ranked_universe.csv")
    status = __import__("pandas").read_csv(settings.outputs_dir / "status_current.csv", dtype=str, keep_default_na=False)
    from college_closure.campus import extend_ranked_universe

    scored = __import__("pandas").read_parquet(settings.processed_dir / "scored.parquet")
    extended = extend_ranked_universe(ranked, scored)
    stats = write_operating_report(
        settings.outputs_dir / "top50_report.html",
        extended,
        status,
        open_n=50,
        score_year=2023,
    )
    logging.info("Report %s", stats)
    logging.info("Score gap vs refit max abs %s", meta.get("max_abs_score_gap"))
    logging.info("Artifacts %s", len(meta.get("artifacts") or []))
    for item in meta.get("artifacts") or []:
        logging.info("Artifact %s %s", item["residential_rank"], item["inst_name"])


if __name__ == "__main__":
    main()
