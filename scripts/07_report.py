#!/usr/bin/env python3
"""Ranked watch list, top-50 evidence cards, and model card.

This is a watch list of elevated-risk indicators, not a closure verdict.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.report import run_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Write watchlist.csv, top50_report.html, model_card.md")
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = load_settings(args.config)
    info = run_report(settings)
    print(
        f"watchlist year={info['score_year']} rows={info['n_watch']} "
        f"cards={info['n_cards']} -> {settings.outputs_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
