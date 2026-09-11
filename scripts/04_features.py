#!/usr/bin/env python3
"""Trailing-window features (no future leakage) from the institution-year panel."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.features import build_features  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build data/processed/features.parquet")
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = load_settings(args.config)
    feat = build_features(settings)
    print(f"features rows={len(feat):,} cols={feat.shape[1]} -> {settings.processed_dir / 'features.parquet'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
