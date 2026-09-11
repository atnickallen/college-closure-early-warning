#!/usr/bin/env python3
"""Closure/merger labels: closed_or_merged_within_h_years (h=2 and h=3)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.labels import build_labels  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Attach right-censored closure/merger labels")
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = load_settings(args.config)
    labeled = build_labels(settings)
    print(f"labels rows={len(labeled):,} -> {settings.processed_dir / 'labels.parquet'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
