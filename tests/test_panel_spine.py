"""Extract years attach even when the directory spine skipped that year."""

import pandas as pd

from college_closure.panel import expand_spine_with_extract_years


def test_finance_year_missing_from_directory_is_added_to_the_spine():
    spine = pd.DataFrame(
        [
            {
                "unitid": 148016,
                "year": 2025,
                "inst_name": "Principia College",
                "inst_control": 2,
                "in_risk_model_universe": True,
            }
        ]
    )
    keys = pd.DataFrame(
        [
            {"unitid": 148016, "year": 2023},
            {"unitid": 148016, "year": 2024},
            {"unitid": 999999, "year": 2023},
        ]
    )
    out = expand_spine_with_extract_years(spine, keys)
    years = set(out.loc[out["unitid"] == 148016, "year"].astype(int))
    assert years == {2023, 2024, 2025}
    assert 999999 not in set(out["unitid"])
    row_2023 = out.loc[(out["unitid"] == 148016) & (out["year"] == 2023)].iloc[0]
    assert row_2023["inst_name"] == "Principia College"
    assert int(row_2023["inst_control"]) == 2
