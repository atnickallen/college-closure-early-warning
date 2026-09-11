#!/usr/bin/env python3
"""Phase 2: UNITID↔OPEID↔EIN crosswalk, NCES finance backfill, FSA extracts."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.closures_extra import ingest_closure_trackers  # noqa: E402
from college_closure.config import load_settings  # noqa: E402
from college_closure.crosswalk import write_crosswalk  # noqa: E402
from college_closure.fsa import run_fsa_ingest  # noqa: E402
from college_closure.nces_finance import ingest_nces_finance  # noqa: E402
from college_closure.wiche import ingest_wiche  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build OPEID/EIN crosswalk, NCES finance backfill, and FSA extracts."
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--skip-nces", action="store_true")
    parser.add_argument("--skip-fsa", action="store_true")
    parser.add_argument("--skip-wiche", action="store_true")
    parser.add_argument("--skip-closures", action="store_true")
    parser.add_argument(
        "--skip-scorecard",
        action="store_true",
        help="Skip College Scorecard (API and bulk ZIP).",
    )
    parser.add_argument(
        "--with-scorecard",
        action="store_true",
        help="Use Scorecard (default). API if DATA_GOV_API_KEY is set, else official no-key ZIP.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = load_settings(args.config)

    xw = write_crosswalk(settings)
    print(f"crosswalk rows={len(xw):,} -> {settings.processed_dir / 'crosswalk.parquet'}")

    if not args.skip_nces:
        nces = ingest_nces_finance(settings)
        print(f"nces finance rows={len(nces):,} -> {settings.processed_dir / 'finance_nces.parquet'}")
    if args.with_scorecard and args.skip_scorecard:
        print("both --with-scorecard and --skip-scorecard set; skipping Scorecard")
    if not args.skip_fsa:
        fsa = run_fsa_ingest(settings, skip_scorecard=bool(args.skip_scorecard))
        for key, frame in fsa.items():
            n = 0 if frame is None or frame.empty else len(frame)
            print(f"fsa {key} rows={n:,}")
    elif not args.skip_scorecard:
        # Scorecard is independent of FSA workbooks: --skip-fsa still ingests it.
        from college_closure.scorecard import ingest_scorecard

        sc = ingest_scorecard(settings, skip=False)
        print(f"scorecard rows={0 if sc is None or sc.empty else len(sc):,}")
    if not args.skip_wiche:
        wiche = ingest_wiche(settings)
        print(f"wiche rows={0 if wiche is None or wiche.empty else len(wiche):,}")
    if not args.skip_closures:
        closures = ingest_closure_trackers(settings)
        print(f"closure_trackers matches={0 if closures is None or closures.empty else len(closures):,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
