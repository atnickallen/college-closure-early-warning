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


def test_scorecard_operating_zero_is_not_a_closure_year():
    """operating=0 is an evidence flag, not a label year."""
    sc = pd.DataFrame(
        {
            "unitid": [5],
            "opeid6": ["005555"],
            "scorecard_operating": [0],
            "scorecard_currently_operating": [False],
        }
    )
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
    assert bool(out.iloc[0]["scorecard_currently_operating"]) is True
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


def test_scorecard_api_paginates_until_total(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "unit-test-key-do-not-use")
    pages = []

    def fake_get(url, params, timeout=60):
        pages.append(params["page"])
        page = params["page"]
        return _Resp(
            {
                "metadata": {"page": page, "per_page": 1, "total": 2},
                "results": [
                    {
                        "id": 100 + page,
                        "ope6_id": 2345,
                        "ope8_id": 234500,
                        "school": {
                            "name": f"College {page}",
                            "operating": 0 if page else 1,
                            "ownership": 3,
                            "under_investigation": 0,
                            "state": "OH",
                            "city": "Cleveland",
                        },
                    }
                ],
            }
        )

    settings = SimpleNamespace(raw={}, processed_dir=tmp_path, raw_dir=tmp_path, root=tmp_path)
    out = ingest_scorecard_api(settings, http_get=fake_get)
    assert pages == [0, 1]
    assert len(out) == 2
    assert set(out["unitid"].astype(int)) == {100, 101}
    assert set(out["opeid6"]) == {"002345"}
    closed = out.loc[out["unitid"] == 101].iloc[0]
    assert int(closed["scorecard_operating"]) == 0
    assert bool(closed["scorecard_currently_operating"]) is False


def test_ingest_scorecard_prefers_api_when_key_set(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_GOV_API_KEY", "unit-test-key-do-not-use")

    def fake_get(url, params, timeout=60):
        return _Resp(
            {
                "metadata": {"page": 0, "per_page": 100, "total": 1},
                "results": [
                    {
                        "id": 1,
                        "ope6_id": "001003",
                        "ope8_id": "00100300",
                        "school.name": "API College",
                        "school.operating": 1,
                        "school.ownership": 2,
                        "school.under_investigation": 0,
                    }
                ],
            }
        )

    settings = SimpleNamespace(raw={}, processed_dir=tmp_path, raw_dir=tmp_path, root=tmp_path)
    out = ingest_scorecard(settings, http_get=fake_get)
    assert len(out) == 1
    assert out.iloc[0]["scorecard_source"] == "api"
    assert out.iloc[0]["inst_name"] == "API College"


def test_config_literal_key_is_ignored(tmp_path, monkeypatch):
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    monkeypatch.delenv("SCORECARD_API_KEY", raising=False)
    settings = SimpleNamespace(
        raw={"scorecard": {"api_key": "should-never-be-read", "key": "also-ignored"}},
        processed_dir=tmp_path,
        raw_dir=tmp_path,
        root=tmp_path,
    )
    assert scorecard_api_key(settings) == ""


def test_config_api_key_env_name(monkeypatch):
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    monkeypatch.delenv("SCORECARD_API_KEY", raising=False)
    monkeypatch.setenv("CUSTOM_SCORECARD_ENV", "from-named-env")
    settings = SimpleNamespace(raw={"scorecard": {"api_key_env": "CUSTOM_SCORECARD_ENV"}})
    assert scorecard_api_key(settings) == "from-named-env"
