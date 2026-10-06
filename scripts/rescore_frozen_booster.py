#!/usr/bin/env python3
"""Rebuild the panel from extract years and rescore with the existing booster.

The booster is fit on the pre-fix labels frame (train_end 2016, random_state=42).
Winsor bounds are the pre-fix feature-panel percentiles. Weights are not refit
on the expanded panel.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.explain import fit_published_booster  # noqa: E402
from college_closure.features import RATIO_COLS, build_features  # noqa: E402
from college_closure.model import publish_frozen_snapshot  # noqa: E402
from college_closure.panel import build_panel  # noqa: E402


def _bounds(frame: pd.DataFrame) -> dict[str, tuple[float, float]]:
    bounds = {}
    for column in RATIO_COLS:
        if column not in frame.columns:
            continue
        series = pd.to_numeric(frame[column], errors="coerce")
        if int(series.notna().sum()) < 20:
            continue
        bounds[column] = (float(series.quantile(0.01)), float(series.quantile(0.99)))
    return bounds


def _snapshot(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_parquet(path)
    if "vintage_snapshot" in frame.columns:
        frame = frame.loc[frame["vintage_snapshot"] == True].copy()  # noqa: E712
    return frame


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = load_settings()
    old = _snapshot(settings.processed_dir / "scored.parquet")
    old_features = pd.read_parquet(settings.processed_dir / "features.parquet")
    bounds = _bounds(old_features)
    logging.info("Fitting the existing booster on the pre-fix labels frame")
    booster, name, features, _univ = fit_published_booster(settings)
    logging.info("Booster %s on %s features", name, len(features))
    logging.info("Rebuilding the panel from extract years and parent-child flags")
    build_panel(settings)
    build_features(settings, winsor_bounds=bounds)
    snapshot = publish_frozen_snapshot(settings, booster, features)
    counts = _counts(old, snapshot)
    dest = settings.outputs_dir / "data_match_counts.json"
    dest.write_text(json.dumps(counts, indent=2), encoding="utf-8")
    logging.info("Counts %s", json.dumps(counts))
    return 0


def _counts(old: pd.DataFrame, new: pd.DataFrame) -> dict:
    def _ids(frame: pd.DataFrame) -> set[int]:
        if frame is None or frame.empty or "unitid" not in frame.columns:
            return set()
        return {int(v) for v in pd.to_numeric(frame["unitid"], errors="coerce").dropna().tolist()}

    old_ids = _ids(old)
    new_ids = _ids(new)
    old_miss = set()
    if not old.empty and "miss_finance" in old.columns:
        old_miss = _ids(old.loc[old["miss_finance"].fillna(True).astype(bool)])
    own = new.loc[~new["insufficient_data"].fillna(True).astype(bool) & ~new["finance_from_parent"].fillna(False).astype(bool)]
    inherited = new.loc[new["finance_from_parent"].fillna(False).astype(bool)]
    insufficient = new.loc[new["insufficient_data"].fillna(False).astype(bool)]
    gained_own = _ids(own) & (old_miss | (new_ids - old_ids))
    return {
        "old_snapshot_schools": len(old_ids),
        "new_snapshot_schools": len(new_ids),
        "newly_in_snapshot": len(new_ids - old_ids),
        "gained_own_finance": len(gained_own),
        "finance_from_parent": int(inherited["unitid"].nunique()) if not inherited.empty else 0,
        "insufficient_data": int(insufficient["unitid"].nunique()) if not insufficient.empty else 0,
        "gained_own_finance_unitids": sorted(gained_own),
        "finance_from_parent_unitids": sorted(_ids(inherited)),
    }


if __name__ == "__main__":
    raise SystemExit(main())
