"""Scorecard API client (mocked HTTP) and CLOSEDAT sentinel rejection."""

from __future__ import annotations

from types import SimpleNamespace

import pandas as pd

from college_closure.scorecard import (
    ingest_scorecard,
    ingest_scorecard_api,
    scorecard_api_key,
    scorecard_closure_events,
)


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


def test_scorecard_api_key_reads_data_gov(monkeypatch):
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    monkeypatch.delenv("SCORECARD_API_KEY", raising=False)
    assert scorecard_api_key() == ""
    monkeypatch.setenv("DATA_GOV_API_KEY", "  not-a-real-key  ")
    assert scorecard_api_key() == "not-a-real-key"


class _Resp:
    def __init__(self, payload, status=200):
        self.status_code = status
        self._payload = payload
        self.text = ""

    def json(self):
        return self._payload


def test_scorecard_api_maps_fields_and_does_not_store_key(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "unit-test-key-do-not-use")
    seen = {}

    def fake_get(url, params, timeout=60):
        seen["url"] = url
        seen["params"] = params
        return _Resp(
            {
                "metadata": {"page": 0, "per_page": 100, "total": 1},
                "results": [
                    {
                        "id": 166027,
                        "ope6_id": "002345",
                        "ope8_id": "00234500",
                        "school.name": "Example College",
                        "school.operating": 1,
                        "school.ownership": 2,
                        "school.under_investigation": 1,
                        "school.accreditor": "NECHE",
                        "school.state": "MA",
                        "school.city": "Boston",
                    }
                ],
            }
        )

    settings = SimpleNamespace(
        raw={"scorecard": {"api_base": "https://api.data.gov/ed/collegescorecard/v1/schools"}},
        processed_dir=tmp_path,
        raw_dir=tmp_path,
        root=tmp_path,
    )
    out = ingest_scorecard_api(settings, http_get=fake_get)
    assert len(out) == 1
    assert int(out.iloc[0]["unitid"]) == 166027
    assert out.iloc[0]["opeid6"] == "002345"
    assert bool(out.iloc[0]["hcm2_scorecard"]) is True
    assert int(out.iloc[0]["scorecard_under_investigation"]) == 1
    assert int(out.iloc[0]["scorecard_operating"]) == 1
    assert int(out.iloc[0]["scorecard_ownership"]) == 2
    assert out.iloc[0]["scorecard_source"] == "api"
    assert seen["params"]["api_key"] == "unit-test-key-do-not-use"
    assert "school.under_investigation" in seen["params"]["fields"]
    assert "school.operating" in seen["params"]["fields"]
    # Key must not land in the snapshot written for joins.
    written = pd.read_parquet(tmp_path / "scorecard_operating.parquet")
    blob = written.to_csv(index=False)
    assert "unit-test-key-do-not-use" not in blob
    assert "api_key" not in written.columns


def test_scorecard_api_empty_without_key(tmp_path, monkeypatch):
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    monkeypatch.delenv("SCORECARD_API_KEY", raising=False)

    def boom(*_a, **_k):
        raise AssertionError("HTTP must not run without a key")

    settings = SimpleNamespace(raw={}, processed_dir=tmp_path, raw_dir=tmp_path, root=tmp_path)
    assert ingest_scorecard_api(settings, http_get=boom).empty


def test_ingest_scorecard_skip_does_not_call_http(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "unit-test-key-do-not-use")

    def boom(*_a, **_k):
        raise AssertionError("skipped ingest must not call HTTP")

    settings = SimpleNamespace(raw={}, processed_dir=tmp_path, raw_dir=tmp_path, root=tmp_path)
    assert ingest_scorecard(settings, skip=True, http_get=boom).empty
