#!/usr/bin/env python3
"""Logistic baseline + XGBoost, temporal validation, recall@K, SHAP."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from college_closure.config import load_settings  # noqa: E402
from college_closure.model import run_model  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit temporal models and score the risk universe")
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = load_settings(args.config)
    metrics = run_model(settings)
    test = metrics.get("test", {})
    booster = metrics.get("booster", "")
    block = test.get(booster, {})
    print(
        f"model={booster} test PR-AUC={block.get('pr_auc')} "
        f"recall@50={block.get('recall_at_50')} beats_naive={metrics.get('beats_naive', {}).get('any_test_year')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
