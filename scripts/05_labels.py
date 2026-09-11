#!/usr/bin/env python3
"""Phase 3 stub: closure / merger labels.

Label (default horizon h=3 from config.yaml):

    closed_or_merged_within_h_years

Sources (do not invent dates):
1. IPEDS directory: inst_status (4 out of business, 7 closed in current year,
   3 combined with other institution), date_closed, year_deleted, newid (merger
   successor UNITID).
2. Federal Student Aid Closed School file (OPEID), joined via 02_crosswalk.
3. Optional: news / SHEEO lists as a validation overlay, not the primary label.

The Fed paper predicts closure within two years using a two-year lag of
covariates; this pipeline uses a configurable 3-year horizon to match the
2–3 year early-warning goal. Publics almost never close; they remain in the
panel for context but are excluded from model training.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    print("05_labels.py is a later-phase stub (not implemented).")
    print("Inputs: directory.parquet + FSA Closed School (via OPEID crosswalk)")
    print("Planned output: data/processed/labels.parquet")
    print("Label: closed_or_merged_within_h_years (h from config.yaml, default 3)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
