"""Unit tests for universe filters and year parsing (no network)."""

from __future__ import annotations

import pandas as pd

from college_closure.filters import add_directory_labels, filter_college_universe
from college_closure.urban import parse_years_available


FILTERS = {
    "degree_granting": 1,
    "control": [1, 2, 3],
    "title_iv_participating": [1, 2, 4, 8],
    "drop_admin_sector": 0,
    "drop_nondegree_inst_category": [5, 6],
    "drop_name_patterns": ["system office", "central office"],
}


def _row(**overrides):
    base = {
        "unitid": 100001,
        "year": 2022,
        "inst_name": "Example College",
        "degree_granting": 1,
        "inst_control": 2,
        "title_iv_indicator": 1,
        "sector": 2,
        "institution_level": 4,
        "inst_category": 2,
        "primarily_postsecondary": 1,
    }
    base.update(overrides)
    return base


def test_parse_years_available_en_dash_and_html():
    assert parse_years_available("1980, 1984–2024")[:3] == [1980, 1984, 1985]
    assert parse_years_available("1980, 1984–2024")[-1] == 2024
    assert parse_years_available("1984&ndash;2024")[0] == 1984
    assert 1999 in parse_years_available("1991, 1993, 1995, 1997, and 1999–2024")


def test_keeps_degree_granting_title_iv_college():
    df = pd.DataFrame([_row()])
    out = filter_college_universe(df, FILTERS)
    assert len(out) == 1
    assert bool(out.iloc[0]["in_risk_model_universe"]) is True
    assert out.iloc[0]["control_label"] == "private_nonprofit"


def test_drops_certificate_only_and_system_office():
    df = pd.DataFrame(
        [
            _row(unitid=1, degree_granting=0, inst_name="Aveda Institute"),
            _row(unitid=2, sector=0, inst_name="State University System Office"),
            _row(unitid=3, inst_category=6, inst_name="Trade Certificate School"),
            _row(unitid=4, inst_name="Keep Me College"),
        ]
    )
    out = filter_college_universe(df, FILTERS)
    assert set(out["unitid"]) == {4}


def test_title_iv_missing_is_kept():
    df = pd.DataFrame(
        [
            _row(unitid=10, title_iv_indicator=-1),
            _row(unitid=11, title_iv_indicator=5),  # not participating
        ]
    )
    out = filter_college_universe(df, FILTERS)
    assert set(out["unitid"]) == {10}


def test_publics_stay_but_are_flagged_out_of_risk_model():
    df = pd.DataFrame([_row(unitid=20, inst_control=1, sector=1)])
    out = filter_college_universe(df, FILTERS)
    assert len(out) == 1
    assert bool(out.iloc[0]["in_risk_model_universe"]) is False
    labeled = add_directory_labels(df)
    assert labeled.iloc[0]["control_label"] == "public"
    assert bool(labeled.iloc[0]["is_four_year"]) is True
