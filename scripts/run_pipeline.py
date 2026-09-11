#!/usr/bin/env python3
"""Run the full pipeline: ingest (optional) → crosswalk/FSA/NCES → panel → features → labels → model → report."""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(script: str, extra: list[str] | None = None) -> None:
    cmd = [sys.executable, str(ROOT / "scripts" / script), *(extra or [])]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="End-to-end college-closure watch-list pipeline")
    parser.add_argument("--skip-ingest", action="store_true", help="Reuse existing Urban Parquet extracts")
    parser.add_argument("--skip-nces", action="store_true")
    parser.add_argument("--skip-fsa", action="store_true")
    parser.add_argument("--skip-wiche", action="store_true")
    parser.add_argument("--skip-closures", action="store_true")
    parser.add_argument("--skip-scorecard", action="store_true")
    parser.add_argument("--skip-libraries", action="store_true")
    parser.add_argument(
        "--with-scorecard",
        action="store_true",
        help="Use Scorecard (default). API if DATA_GOV_API_KEY is set, else official no-key ZIP.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    processed = ROOT / "data" / "processed"
    if not args.skip_ingest:
        _run("01_ingest.py")
    elif not (processed / "directory.parquet").exists():
        print("directory.parquet missing; running 01_ingest.py")
        _run("01_ingest.py")

    extra = []
    if args.skip_nces:
        extra.append("--skip-nces")
    if args.skip_fsa:
        extra.append("--skip-fsa")
    if args.skip_wiche:
        extra.append("--skip-wiche")
    if args.skip_closures:
        extra.append("--skip-closures")
    if args.skip_scorecard:
        extra.append("--skip-scorecard")
    if args.skip_libraries:
        extra.append("--skip-libraries")
    if args.with_scorecard:
        extra.append("--with-scorecard")
    _run("02_crosswalk.py", extra)
    _run("03_panel.py")
    _run("04_features.py")
    _run("05_labels.py")
    _run("06_model.py")
    _run("07_report.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
