#!/usr/bin/env python3
"""Phase 3 stub: features aligned with Kelchen, Ritter & Webber (WP 24-20 / FEDS 2025-3).

Construct institution-year predictors from panel.parquet. Do not fit models here.

Core constructs from the Fed working paper (section on covariates):
- Enrollment trajectory: level, YoY change, 10% decline vs 5-year high,
  3 consecutive years of 5%+ decline; UG share; full-time share (when available).
- Staffing contraction: total staff, YoY change, instructional share, FT share.
- Tuition dependence: tuition & fees / total revenue; tuition discount
  (institutional grants or allowances / gross tuition).
- Operating margins: (rev - exp) / rev; persistent negative margin
  (3 of last 5 years); 10% revenue decline vs 5-year high.
- Liquidity / leverage: days cash on hand (when cash is available), debt/assets,
  debt/EBIDA, endowment level and change. Urban finance currently ends 2017 —
  later years need a NCES IPEDS Finance backfill.
- Prior distress flags (via 02_crosswalk + FSA): failed financial-responsibility
  composite score, HCM2, 90/10 (for-profits).

Publics stay in the panel but features for the risk model are estimated on
private nonprofit and for-profit rows (in_risk_model_universe).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    print("04_features.py is a later-phase stub (not implemented).")
    print("Input: data/processed/panel.parquet")
    print("Planned output: data/processed/features.parquet")
    print("Blueprint: Philadelphia Fed WP 24-20 / FEDS 2025-3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
