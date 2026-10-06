#!/usr/bin/env python3
"""Refresh listings.csv, listings.json, and index.html."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from camp_listings.pipeline import run  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find camps, campuses, and 501(c)(7) clubs with housing that are for sale.")
    parser.add_argument("--skip-network", action="store_true", help="Use the curated CSV only")
    parser.add_argument("--no-geocode", action="store_true", help="Do not call Nominatim")
    args = parser.parse_args(argv)
    rows = run(ROOT, skip_network=args.skip_network, geocode=not args.no_geocode)
    print(f"Wrote {len(rows)} listings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
