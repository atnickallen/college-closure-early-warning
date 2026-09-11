"""WICHE Knocking workbook → state-year HS graduate totals."""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from college_closure.wiche import parse_knocking_workbook


def test_parse_knocking_grand_total_by_state(tmp_path: Path):
    path = tmp_path / "knocking.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(
        [
            "Stabbr",
            "StateRegionUS",
            "ClassOf",
            "SchoolYear",
            "SchoolSector",
            "Grade",
            "RaceEthnicity",
            "Students",
            "ActualProjected",
        ]
    )
    rows = [
        ["CA", "California", "Class of 2018", "2017-2018", "Grand Total (public+private)", "High school graduates", "Total/any", 400000, "Reported/Actual"],
        ["CA", "California", "Class of 2018", "2017-2018", "Public (total, any)", "High school graduates", "Total/any", 350000, "Reported/Actual"],
        ["CA", "California", "Class of 2018", "2017-2018", "Grand Total (public+private)", "High school graduates", "White", 100000, "Reported/Actual"],
        ["_W", "West", "Class of 2018", "2017-2018", "Grand Total (public+private)", "High school graduates", "Total/any", 900000, "Reported/Actual"],
        ["NY", "New York", "Class of 2019", "2018-2019", "Grand Total (public+private)", "High school graduates", "Total/any", 180000, "Reported/Actual"],
    ]
    for r in rows:
        ws.append(r)
    wb.save(path)

    out = parse_knocking_workbook(path)
    assert set(out["state_abbr"]) == {"CA", "NY"}
    ca = out.loc[(out["state_abbr"] == "CA") & (out["year"] == 2018)].iloc[0]
    assert int(ca["hs_graduates"]) == 400000
    ny = out.loc[(out["state_abbr"] == "NY") & (out["year"] == 2019)].iloc[0]
    assert int(ny["hs_graduates"]) == 180000
