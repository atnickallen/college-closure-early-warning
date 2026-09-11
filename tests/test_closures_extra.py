"""Tracker HTML parse + unique name+state directory match."""

from __future__ import annotations

import pandas as pd

from college_closure.closures_extra import _match_to_directory, parse_tracker_html


HTML = """
<html><body>
<ul>
<li>Example College of the Arts closed in 2023 after enrollment collapsed.</li>
<li>North Example University will merge with State U in 2022.</li>
<li>This sentence has no year and should be ignored.</li>
</ul>
</body></html>
"""


def test_parse_tracker_requires_year_and_verb():
    out = parse_tracker_html(HTML, "higher_ed_dive")
    assert not out.empty
    assert set(out["event_year"]) <= {2022, 2023}
    assert out["event_source"].eq("higher_ed_dive").all()
    types = set(out["event_type"])
    assert types <= {"closure", "merger"}
    assert "closure" in types


def test_match_requires_unique_name():
    events = pd.DataFrame(
        [
            {"inst_name": "Example College of the Arts", "state_abbr": "PA", "event_year": 2023, "event_type": "closure", "event_source": "t"},
            {"inst_name": "Ambiguous College", "state_abbr": "", "event_year": 2020, "event_type": "closure", "event_source": "t"},
        ]
    )
    directory = pd.DataFrame(
        [
            {"unitid": 10, "year": 2022, "inst_name": "Example College of the Arts", "state_abbr": "PA", "opeid": "00200000"},
            {"unitid": 20, "year": 2022, "inst_name": "Ambiguous College", "state_abbr": "OH", "opeid": "00300000"},
            {"unitid": 21, "year": 2022, "inst_name": "Ambiguous College", "state_abbr": "IN", "opeid": "00310000"},
        ]
    )
    matched = _match_to_directory(events, directory)
    assert len(matched) == 1
    assert int(matched.iloc[0]["unitid"]) == 10
