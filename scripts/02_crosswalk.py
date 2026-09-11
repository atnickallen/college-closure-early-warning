#!/usr/bin/env python3
"""Phase 2 stub: UNITID ↔ OPEID ↔ EIN crosswalk.

IPEDS reports most surveys at UNITID. Federal Student Aid (closed-school
notifications, Heightened Cash Monitoring, financial-responsibility composite
scores) is keyed on OPEID (8-digit, sometimes OPEID6). IRS Form 990 / NCCS
nonprofit finances use EIN. The IPEDS directory already carries opeid and ein
on each UNITID×year row; later phases will:

1. Build a longitudinal crosswalk from data/processed/directory.parquet
   (unitid, year, opeid, ein, newid for mergers).
2. Attach FSA PEPS / Closed School and College Scorecard OPEID6 keys.
3. Resolve parent/child campus reporting (finance parent_unitid).
4. Persist data/processed/crosswalk.parquet for label construction.

Do not invent mappings. Re-run after 01_ingest.py has a directory extract.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    print("02_crosswalk.py is a Phase 2 stub.")
    print("Inputs: data/processed/directory.parquet (unitid, opeid, ein, newid)")
    print("Planned output: data/processed/crosswalk.parquet")
    print("See README.md → Later phases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
