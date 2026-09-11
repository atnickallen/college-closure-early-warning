#!/usr/bin/env python3
"""Milestone 2: one row per institution × year (directory left-joined to extracts)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.panel import build_panel  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build data/processed/panel.parquet from ingested Parquet extracts."
    )
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = load_settings(args.config)
    panel = build_panel(settings)
    print(f"panel rows={len(panel):,} cols={panel.shape[1]} -> {settings.processed_dir / 'panel.parquet'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
