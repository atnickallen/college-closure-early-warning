#!/usr/bin/env python3
"""Milestone 1–2 ingest: Urban IPEDS directory, enrollment, finance, admissions, staffing."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.ingest import run_ingest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Download/cache Urban Institute IPEDS extracts and write filtered Parquet. "
            "Default pulls directory + fall enrollment (Milestone 1) and finance, "
            "admissions, and staffing (Milestone 2)."
        )
    )
    parser.add_argument("--config", type=Path, default=None, help="Path to config.yaml")
    parser.add_argument(
        "--sources",
        default=None,
        help="Comma-separated subset: directory,fall_enrollment,enrollment_fte,finance,admissions,instructional_staff,noninstructional_staff",
    )
    parser.add_argument(
        "--milestone1-only",
        action="store_true",
        help="Pull only directory + fall-enrollment (skip Milestone 2 extracts).",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = load_settings(args.config)
    if args.milestone1_only:
        sources = ["directory", "fall_enrollment"]
    elif args.sources:
        sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    else:
        sources = None
    run_ingest(settings, sources=sources)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
