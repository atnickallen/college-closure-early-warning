"""Label horizon, right-censor, and merger toggle."""

from __future__ import annotations

import pandas as pd

from college_closure.labels import attach_labels, institution_event_years


def test_horizon_positive_only_in_window():
    directory = pd.DataFrame(
        [
            {"unitid": 1, "year": y, "opeid": "00234500", "inst_status": 1, "date_closed": None}
            for y in range(2015, 2025)
        ]
    )
    # Closure recorded in 2021
    directory.loc[directory["year"] == 2021, "inst_status"] = 4
    directory.loc[directory["year"] == 2021, "date_closed"] = "2021-06-01"
    events = institution_event_years(directory, mergers_are_positive=True, use_disappearance=False)
    assert int(events.iloc[0]["event_year"]) == 2021

    panel = pd.DataFrame({"unitid": [1] * 10, "year": list(range(2015, 2025))})
    labeled = attach_labels(panel, events, horizons=[2, 3], last_complete_year=2024)
    # year 2018: 2021 is within 3 years, not within 2
    row = labeled.loc[labeled["year"] == 2018].iloc[0]
    assert int(row["closed_or_merged_within_3_years"]) == 1
    assert int(row["closed_or_merged_within_2_years"]) == 0
    # year 2021: event is not strictly after the feature year
    row21 = labeled.loc[labeled["year"] == 2021].iloc[0]
    assert int(row21["closed_or_merged_within_3_years"]) == 0
    # year 2023: 2023+3 > 2024 → right-censored
    row23 = labeled.loc[labeled["year"] == 2023].iloc[0]
    assert pd.isna(row23["closed_or_merged_within_3_years"])
    assert bool(row23["label_complete_h3"]) is False
    # year 2021 is complete for h=3 (2021+3 <= 2024)
    assert bool(row21["label_complete_h3"]) is True


def test_merger_toggle():
    directory = pd.DataFrame(
        [
            {"unitid": 2, "year": 2018, "opeid": "00300000", "inst_status": 3, "date_closed": None},
            {"unitid": 2, "year": 2019, "opeid": "00300000", "inst_status": 3, "date_closed": None},
        ]
    )
    on = institution_event_years(directory, mergers_are_positive=True, use_disappearance=False)
    off = institution_event_years(directory, mergers_are_positive=False, use_disappearance=False)
    assert pd.notna(on.iloc[0]["event_year"])
    assert on.iloc[0]["event_type"] == "merger"
    assert pd.isna(off.iloc[0]["event_year"])


def test_sentinel_closedat_rejected():
    directory = pd.DataFrame(
        [
            {"unitid": 9, "year": 2018, "opeid": "00500000", "inst_status": 1, "date_closed": "-2"},
            {"unitid": 9, "year": 2019, "opeid": "00500000", "inst_status": 1, "date_closed": "3"},
        ]
    )
    events = institution_event_years(directory, mergers_are_positive=True, use_disappearance=False)
    assert pd.isna(events.iloc[0]["event_year"])


def test_extra_events_fill_missing_unitid():
    directory = pd.DataFrame(
        [{"unitid": 8, "year": y, "opeid": "00600000", "inst_status": 1} for y in range(2018, 2022)]
    )
    extra = pd.DataFrame([{"unitid": 8, "event_year": 2021, "event_type": "closure", "event_source": "tracker"}])
    events = institution_event_years(
        directory, mergers_are_positive=True, extra_events=extra, use_disappearance=False
    )
    assert int(events.iloc[0]["event_year"]) == 2021


def test_disappearance_requires_two_year_gap():
    directory = pd.DataFrame(
        [{"unitid": 3, "year": y, "opeid": "00400000", "inst_status": 1} for y in range(2018, 2024)]
    )
    # last year 2023, panel max 2023 → no 2-year gap
    events = institution_event_years(directory, mergers_are_positive=True, use_disappearance=True)
    assert pd.isna(events.iloc[0]["event_year"])

    directory2 = pd.DataFrame(
        [{"unitid": 3, "year": y, "opeid": "00400000", "inst_status": 1} for y in range(2018, 2022)]
    )
    directory2 = pd.concat(
        [directory2, pd.DataFrame([{"unitid": 99, "year": 2023, "opeid": "00999900", "inst_status": 1}])],
        ignore_index=True,
    )
    events2 = institution_event_years(directory2, mergers_are_positive=True, use_disappearance=True)
    row = events2.loc[events2["unitid"] == 3].iloc[0]
    assert int(row["event_year"]) == 2022
