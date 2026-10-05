#!/usr/bin/env python3
"""Refresh current status for the top of the watch list.

Curated campus sales and listings are kept. Federal sources (Scorecard
operating flag, FSA closed-school list, IPEDS directory status) only flag
disagreements. Scorecard is skipped when DATA_GOV_API_KEY is unset.

This is a watch list of elevated-risk indicators, not a closure prediction.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.status import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
