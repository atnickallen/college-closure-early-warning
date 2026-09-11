#!/usr/bin/env python3
"""Phase 4 stub: ranked watch list + top-50 evidence cards.

Outputs (later):
- outputs/watchlist.csv — UNITID, name, sector, predicted P(close/merge within h years),
  rank, key feature contributions, data-completeness flags.
- outputs/evidence_cards/ — short markdown cards for the top 50 with enrollment
  trajectory, tuition dependence, margins, liquidity/leverage, staffing, and
  prior FSA distress flags.

Caveat (must appear on every artifact): this is a watch list, not a verdict.
Predicted risk is not a determination that an institution will close or merge.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    print("07_report.py is a later-phase stub (not implemented).")
    print("Planned outputs: outputs/watchlist.csv and top-50 evidence cards.")
    print("Caveat: watch list, not a verdict.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
