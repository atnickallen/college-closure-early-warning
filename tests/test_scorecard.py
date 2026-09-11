"""Scorecard CLOSEDAT sentinels must not become event years."""

from __future__ import annotations

import pandas as pd

from college_closure.scorecard import scorecard_closure_events


def test_scorecard_rejects_sentinel_closedat():
    sc = pd.DataFrame(
        {
            "unitid": [1, 2, 3, 4],
            "opeid6": ["001111", "002222", "003333", "004444"],
            "scorecard_closedat": [-2, 1, 99991231, 20210615],
        }
    )
    ev = scorecard_closure_events(sc)
    assert set(ev["unitid"]) == {4}
    assert int(ev.iloc[0]["event_year"]) == 2021


def test_scorecard_empty_without_closedat():
    sc = pd.DataFrame({"unitid": [1], "opeid6": ["001111"]})
    assert scorecard_closure_events(sc).empty
