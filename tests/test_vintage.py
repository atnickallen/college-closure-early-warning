"""Newest-complete-year snapshot and the 2022 residential comparison."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from college_closure.campus import write_ranked_universe
from college_closure.report import movement_section_html, vintage_note_html
from college_closure.vintage import build_vintage_snapshot, finance_complete_year, newest_complete_year


def _panel() -> pd.DataFrame:
    rows = []
    for year in (2022, 2023, 2024):
        rows.append(
            {
                "unitid": 1,
                "year": year,
                "inst_name": "Alpha College",
                "state_abbr": "OH",
                "in_risk_model_universe": True,
                "inst_control": 2,
                "sector": 2,
                "is_four_year": True,
                "religious": False,
                "urban": True,
                "rural": False,
                "fte": 100 + year - 2022,
                "log_fte": 4.6,
                "fte_under_1000": True,
                "enr_pct_chg_1y": -0.01 * (year - 2021),
                "enr_pct_chg_5y": -0.2,
                "enr_pct_chg_10y": -0.3,
                "enr_decline_5y_gt30": False,
                "admit_rate": 0.5 if year < 2024 else None,
                "yield_rate": 0.4 if year < 2024 else None,
                "admit_rate_chg_5y": 0.01 if year < 2024 else None,
                "yield_rate_chg_5y": None,
                "ftft_pct_chg_1y": -0.05 if year < 2024 else None,
                "tuition_dependence": 0.8 if year == 2023 else (0.7 if year == 2022 else None),
                "discount_rate": 0.2 if year <= 2023 else None,
                "discount_rate_chg_5y": None,
                "operating_margin": -0.04 if year == 2023 else (-0.02 if year == 2022 else None),
                "operating_margin_chg_5y": None,
                "consec_neg_margin_yrs": 2 if year == 2023 else 1,
                "endowment_per_fte": 1000 if year <= 2023 else None,
                "unrestricted_na_to_exp": 0.3 if year <= 2023 else None,
                "high_tuition_dependence": True if year <= 2023 else False,
                "miss_finance": year == 2024,
                "finance_from_parent": False,
                "student_staff_ratio": 10 if year >= 2023 else 9,
                "student_staff_ratio_chg_1y": 0.1 if year >= 2023 else None,
                "staff_pct_chg_1y": -0.02 if year >= 2023 else None,
                "staff_pct_chg_5y": None,
                "composite_score": 1.2,
                "composite_fail": False,
                "composite_zone": True,
                "composite_is_lagged": True,
                "years_in_zone": 3,
                "miss_composite": False,
                "hs_grad_pct_chg_5y": -0.05,
                "label_complete_h3": False,
                "enrollment_fall_total": 120 if year >= 2023 else 110,
            }
        )
    # School 2 has finance only in 2021, and is still in the directory in 2024.
    for year, finance in ((2021, False), (2024, True)):
        rows.append(
            {
                "unitid": 2,
                "year": year,
                "inst_name": "Beta College",
                "state_abbr": "IN",
                "in_risk_model_universe": True,
                "inst_control": 3,
                "sector": 3,
                "is_four_year": False,
                "religious": False,
                "urban": False,
                "rural": True,
                "fte": 80 if year == 2024 else 90,
                "log_fte": 4.4,
                "fte_under_1000": True,
                "enr_pct_chg_1y": -0.1,
                "enr_pct_chg_5y": None,
                "enr_pct_chg_10y": None,
                "enr_decline_5y_gt30": False,
                "admit_rate": None,
                "yield_rate": None,
                "admit_rate_chg_5y": None,
                "yield_rate_chg_5y": None,
                "ftft_pct_chg_1y": None,
                "tuition_dependence": None if finance else 0.6,
                "discount_rate": None if finance else 0.1,
                "discount_rate_chg_5y": None,
                "operating_margin": None if finance else 0.01,
                "operating_margin_chg_5y": None,
                "consec_neg_margin_yrs": None if finance else 0,
                "endowment_per_fte": None,
                "unrestricted_na_to_exp": None if finance else 0.2,
                "high_tuition_dependence": False,
                "miss_finance": finance,
                "finance_from_parent": False,
                "student_staff_ratio": 8,
                "student_staff_ratio_chg_1y": None,
                "staff_pct_chg_1y": None,
                "staff_pct_chg_5y": None,
                "composite_score": 1.4,
                "composite_fail": False,
                "composite_zone": True,
                "composite_is_lagged": True,
                "years_in_zone": 1,
                "miss_composite": False,
                "hs_grad_pct_chg_5y": None,
                "label_complete_h3": False,
                "enrollment_fall_total": 80,
            }
        )
    # Ended before the finance score year.
    rows.append(
        {
            "unitid": 3,
            "year": 2021,
            "inst_name": "Gone College",
            "state_abbr": "MI",
            "in_risk_model_universe": True,
            "inst_control": 2,
            "fte": 50,
            "log_fte": 3.9,
            "miss_finance": False,
            "label_complete_h3": True,
            "inst_name": "Gone College",
        }
    )
    return pd.DataFrame(rows)


def test_finance_complete_year_skips_unpublished_finance():
    frame = _panel()
    assert finance_complete_year(frame) == 2023
    assert newest_complete_year(pd.Series({2022: 100, 2023: 98, 2024: 3})) == 2023


def test_snapshot_uses_newer_enrollment_and_records_finance_fallback():
    snapshot, meta = build_vintage_snapshot(_panel())
    assert meta["score_year"] == 2023
    assert set(snapshot["unitid"]) == {1, 2}
    alpha = snapshot.loc[snapshot["unitid"] == 1].iloc[0]
    assert int(alpha["year"]) == 2023
    assert int(alpha["year_enrollment"]) == 2024
    assert int(alpha["fte"]) == 102
    assert int(alpha["year_finance"]) == 2023
    assert float(alpha["operating_margin"]) == -0.04
    assert int(alpha["log_fte_year"]) == 2024
    assert bool(alpha["label_complete_h3"]) is False
    beta = snapshot.loc[snapshot["unitid"] == 2].iloc[0]
    assert int(beta["year_finance"]) == 2021
    assert int(beta["operating_margin_year"]) == 2021
    assert int(beta["year_enrollment"]) == 2024
    assert pd.isna(beta["admit_rate_year"]) or beta["admit_rate"] != beta["admit_rate"]


def test_ranked_universe_without_prefer_year_follows_finance():
    scored = pd.DataFrame(
        [
            {"unitid": 1, "year": 2022, "risk_score": 0.99, "inst_name": "Old", "label_complete_h3": False, "miss_finance": False},
            {"unitid": 1, "year": 2023, "risk_score": 0.4, "inst_name": "New", "label_complete_h3": False, "miss_finance": False},
            {"unitid": 2, "year": 2024, "risk_score": 0.95, "inst_name": "Gap", "label_complete_h3": False, "miss_finance": True},
        ]
    )
    dest = Path("/tmp/ranked_vintage.csv")
    n = write_ranked_universe(scored, dest, prefer_year=None)
    loaded = pd.read_csv(dest)
    assert n == 1
    assert int(loaded.iloc[0]["year"]) == 2023
    assert loaded.iloc[0]["inst_name"] == "New"


def test_movement_section_names_entered_and_left_schools():
    open_df = pd.DataFrame(
        [
            {"unitid": 10, "inst_name": "Stayed College", "state_abbr": "OH"},
            {"unitid": 11, "inst_name": "Entered College", "state_abbr": "TX"},
        ]
    )
    baseline = pd.DataFrame(
        [
            {"old_rank": 1, "unitid": 10, "inst_name": "Stayed College", "state_abbr": "OH"},
            {"old_rank": 2, "unitid": 12, "inst_name": "Left College", "state_abbr": "ME"},
        ]
    )
    html = movement_section_html(open_df, baseline)
    assert "Entered College" in html
    assert "Left College" in html
    assert "1 entered and 1 left" in html
    note = vintage_note_html(
        {
            "score_year": 2023,
            "sources": {
                "finance": {"complete_year": 2023},
                "fall_enrollment": {"complete_year": 2024},
                "enrollment_fte": {"complete_year": 2024},
                "admissions": {"complete_year": 2024},
                "staff": {"complete_year": 2024},
                "directory": {"complete_year": 2025},
                "scorecard": {"file": "Most-Recent-Cohorts-Institution_06102026.zip", "file_date": "2026-06-10"},
            },
        }
    )
    assert "2023-2024" in note
    assert "fall enrollment 2024" in note
    assert "2026-06-10" in note
