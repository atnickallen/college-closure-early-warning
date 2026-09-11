"""Features must use trailing windows only — no future values."""

from __future__ import annotations

import pandas as pd

from college_closure.config import load_settings
from college_closure.features import MODEL_FEATURE_COLUMNS, build_features
from college_closure.crosswalk import apply_parent_child_finance_rollup


def _settings(tmp_path):
    settings = load_settings()
    # Point processed/outputs at a temp dir without rewriting config.yaml
    object.__setattr__  # keep frozen dataclass; use a simple namespace
    class _S:
        raw = settings.raw
        root = settings.root
        processed_dir = tmp_path
        outputs_dir = tmp_path
        label_horizon_years = 3

    return _S()


def test_pct_change_ignores_future_fte(tmp_path):
    rows = []
    for year, fte in [(2010, 1000), (2011, 1100), (2012, 1200), (2013, 800), (2014, 5000)]:
        rows.append(
            {
                "unitid": 1,
                "year": year,
                "enrollment_fte": fte,
                "enrollment_fall_total": fte,
                "rev_total_current": 10_000_000,
                "exp_total_current": 9_000_000,
                "rev_tuition_fees_net": 4_000_000,
                "inst_control": 2,
                "sector": 2,
                "in_risk_model_universe": True,
                "is_four_year": True,
            }
        )
    panel = pd.DataFrame(rows)
    feat = build_features(_settings(tmp_path), panel)
    y2013 = feat.loc[feat["year"] == 2013].iloc[0]
    # 1y change at 2013 uses 2012 (1200 → 800), not 2014's spike
    expected = 800 / 1200 - 1
    assert abs(y2013["enr_pct_chg_1y"] - expected) < 1e-9
    # 5y change at 2013 has no 2008 baseline → NA, must not use 2014
    assert pd.isna(y2013["enr_pct_chg_5y"])


def test_training_features_exclude_hcm_and_future_labels():
    forbidden = {
        "hcm1",
        "hcm2",
        "hcm1_current",
        "hcm2_current",
        "hcm2_scorecard",
        "scorecard_under_investigation",
        "scorecard_operating",
        "scorecard_currently_operating",
        "scorecard_ownership",
        "accreditor_public_action",
        "warn_layoff_mention",
        "irs990_revenue",
        "enrichment_notes",
        "lib_physical_books",
        "lib_digital_items",
        "lib_expenditures",
        "lib_fte",
        "lib_special_collections_note",
        "lib_unique_flag",
        "lib_oclc_symbol",
        "lib_worldcat_registry_id",
        "lib_libraries_org_id",
        "closed_or_merged_within_2_years",
        "closed_or_merged_within_3_years",
        "event_year",
        "risk_score",
    }
    assert not (forbidden & set(MODEL_FEATURE_COLUMNS))


def test_parent_child_rollup_copies_parent_not_double_source():
    df = pd.DataFrame(
        [
            {
                "unitid": 10,
                "year": 2016,
                "parent_child_flag": 1,
                "parent_unitid": 10,
                "rev_total_current": 50_000_000,
                "exp_total_current": 40_000_000,
                "rev_tuition_fees_net": 20_000_000,
            },
            {
                "unitid": 11,
                "year": 2016,
                "parent_child_flag": 2,
                "parent_unitid": 10,
                "rev_total_current": 0,
                "exp_total_current": 0,
                "rev_tuition_fees_net": 0,
            },
        ]
    )
    out = apply_parent_child_finance_rollup(df)
    child = out.loc[out["unitid"] == 11].iloc[0]
    parent = out.loc[out["unitid"] == 10].iloc[0]
    assert child["rev_total_current"] == 50_000_000
    assert bool(child["finance_from_parent"]) is True
    assert parent["rev_total_current"] == 50_000_000
    assert bool(parent["finance_from_parent"]) is False
