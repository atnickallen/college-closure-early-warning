"""Official FSA composite parse + OPEID 6/8 (no silent root shift)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from openpyxl import Workbook

from college_closure.fsa import parse_official_composite_workbook
from college_closure.ids import normalize_opeid8, opeid6


def test_official_workbook_skips_title_rows(tmp_path: Path):
    path = tmp_path / "ay17-18-composite-scores.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Master FY18"
    ws.append(["Composite Scores For Private Institutions FY ending 2018"])
    ws.append([])
    ws.append(["Item#", "OPE ID", "Institution Name", "State", "Composite Score for Institution's Fiscal Year Ending Between 07/01/2017 - 6/30/2018"])
    ws.append([1, "00884300", "Alaska Bible College", "AK", 1.5])
    ws.append([2, "002345", "Six Digit Root College", "MA", 0.8])
    wb.save(path)

    out = parse_official_composite_workbook(path, fallback_year=2018)
    assert len(out) == 2
    roots = set(out["opeid6"])
    assert "008843" in roots
    assert "002345" in roots
    # 6-digit FSA root must not become 00002345
    six = out.loc[out["opeid6"] == "002345"].iloc[0]
    assert six["opeid8"] == "00234500"
    assert float(six["composite_score"]) == 0.8
    assert int(six["year"]) == 2018


def test_attach_composite_uses_opeid6_when_unitid_missing():
    from college_closure.fsa import attach_composite

    panel = pd.DataFrame(
        {
            "unitid": [10, 11],
            "year": [2017, 2017],
            "opeid6": ["001003", "009999"],
            "opeid_is_main": [True, True],
            "opeid6_n_unitids": [1, 1],
        }
    )
    official = pd.DataFrame(
        {
            "unitid": [pd.NA, pd.NA],
            "year": [2017.0, 2017.0],
            "opeid6": ["001003", "001012"],
            "composite_score": [2.4, 1.1],
        }
    )
    out = attach_composite(panel, official)
    assert float(out.loc[out["unitid"] == 10, "composite_score"].iloc[0]) == 2.4
    assert pd.isna(out.loc[out["unitid"] == 11, "composite_score"].iloc[0])


def test_opeid6_from_official_eight_digit_matches_ids():
    assert opeid6("00884300") == "008843"
    assert normalize_opeid8("00884300") == "00884300"
    assert normalize_opeid8("884300") == "00884300"  # int-stripped 00884300
    assert opeid6(884300) == "008843"
