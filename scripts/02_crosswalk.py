#!/usr/bin/env python3
"""Phase 2: UNITID↔OPEID↔EIN crosswalk, NCES finance backfill, FSA extracts."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.crosswalk import write_crosswalk  # noqa: E402
from college_closure.fsa import run_fsa_ingest  # noqa: E402
from college_closure.nces_finance import ingest_nces_finance  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build OPEID/EIN crosswalk, NCES finance backfill, and FSA extracts."
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--skip-nces", action="store_true")
    parser.add_argument("--skip-fsa", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = load_settings(args.config)

    xw = write_crosswalk(settings)
    print(f"crosswalk rows={len(xw):,} -> {settings.processed_dir / 'crosswalk.parquet'}")

    if not args.skip_nces:
        nces = ingest_nces_finance(settings)
        print(f"nces finance rows={len(nces):,} -> {settings.processed_dir / 'finance_nces.parquet'}")
    if not args.skip_fsa:
        fsa = run_fsa_ingest(settings)
        for key, frame in fsa.items():
            n = 0 if frame is None or frame.empty else len(frame)
            print(f"fsa {key} rows={n:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
