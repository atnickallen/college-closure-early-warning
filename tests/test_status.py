"""Curated status merge: federal flags disagree, they do not overwrite sales."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from college_closure.config import Settings
from college_closure.scorecard import fetch_operating_by_unitids
from college_closure.status import (
    build_status_table,
    campus_name_match,
    fsa_match_level,
    load_curated,
    load_watchlist,
    normalize_closed_school_frame,
    run_status_check,
    sale_year_label,
    stamp_report_html,
    status_badge,
)

ROOT = Path(__file__).resolve().parents[1]


def _school(**kwargs) -> pd.DataFrame:
    base = {
        "watchlist_rank": 1,
        "unitid": 111,
        "opeid6": "9748",
        "opeid8": "974811",
        "inst_name": "Carrington College-Ontario",
        "state_abbr": "CA",
    }
    base.update(kwargs)
    return pd.DataFrame([base])


def _curated(**kwargs) -> pd.DataFrame:
    base = {
        "unitid": 111,
        "opeid6": "9748",
        "opeid8": "974811",
        "watchlist_rank": 1,
        "inst_name": "Carrington College-Ontario",
        "state_abbr": "CA",
        "status": "closed",
        "status_detail": "Closed (campus permanently closed Jan 8, 2024)",
        "property_disposition": "no_sale_found",
        "buyer_or_broker": "",
        "event_date": "2024-01-08",
        "sale_price_published": "",
        "sold_listed_details": "no sale/listing found",
        "source_url": "https://example.edu/closure",
        "checked_at": "2026-10-05",
        "library_notes": "",
    }
    base.update(kwargs)
    return pd.DataFrame([base])


def test_parent_opeid_does_not_close_a_different_campus():
    """A shared OPEID6 without the campus name is not a closure signal."""
    assert fsa_match_level("974811", "9748", "00974811") == "opeid8"
    assert fsa_match_level("974804", "9748", "00974811") == "opeid6"
    assert fsa_match_level("974811", "9748", "009748") == "opeid6"
    assert campus_name_match("Carrington College-Ontario", "CARRINGTON COLLEGE") is False
    assert campus_name_match("Carrington College-Ontario", "Carrington College-Ontario") is True

    watch = _school()
    curated = _curated(status="operating", property_disposition="not_applicable")
    fsa = pd.DataFrame(
        [
            {
                "opeid_raw": "009748",
                "closed_name": "CARRINGTON COLLEGE",
                "closed_date": "2024-01-08",
                "unitid": "",
            }
        ]
    )
    out = build_status_table(watch, curated, fsa_closed=fsa, auto_checked_at="2026-10-05")
    assert out.loc[0, "auto_fsa_match"] == "opeid6_only"
    assert out.loc[0, "disagreement"] == ""
    assert out.loc[0, "status"] == "operating"
    assert out.loc[0, "sale_price_published"] == ""


def test_opeid8_or_unitid_match_flags_an_open_curated_row():
    watch = _school(unitid=222, opeid8="00974811")
    curated = _curated(unitid=222, status="operating", property_disposition="not_applicable")
    fsa = pd.DataFrame(
        [
            {
                "opeid_raw": "00974811",
                "closed_name": "SOME OTHER LABEL",
                "closed_date": "2024-01-08",
                "unitid": "",
            }
        ]
    )
    out = build_status_table(watch, curated, fsa_closed=fsa)
    assert out.loc[0, "auto_fsa_match"] == "opeid8"
    assert "FSA closed-school list matches this campus" in out.loc[0, "disagreement"]
    assert out.loc[0, "status"] == "operating"
    assert out.loc[0, "buyer_or_broker"] == ""

    fsa_unit = pd.DataFrame(
        [
            {
                "opeid_raw": "00000000",
                "closed_name": "Unrelated",
                "closed_date": "2024-02-02",
                "unitid": "222",
            }
        ]
    )
    by_unit = build_status_table(watch, curated, fsa_closed=fsa_unit)
    assert by_unit.loc[0, "auto_fsa_match"] == "unitid"
    assert "FSA closed-school list matches this campus" in by_unit.loc[0, "disagreement"]


def test_scorecard_and_ipeds_disagreements_do_not_overwrite_sale_facts():
    watch = _school(unitid=115728, inst_name="Holy Names University", state_abbr="CA", opeid6="1183", opeid8="118300")
    curated = _curated(
        unitid=115728,
        inst_name="Holy Names University",
        state_abbr="CA",
        status="closed",
        property_disposition="sold",
        buyer_or_broker="BH Properties",
        event_date="2023-06 (sale)",
        sale_price_published="~$65 million",
        sold_listed_details="Sold to BH Properties Jun 2023 for ~$65 million (60 acres).",
        source_url="https://www.bhproperties.com/example",
    )
    scorecard = pd.DataFrame({"unitid": [115728], "scorecard_operating": [1]})
    ipeds = pd.DataFrame(
        {
            "unitid": [115728],
            "year": [2024],
            "inst_status": [1],
            "date_closed": [-2],
            "ipeds_absent_after": ["2025"],
        }
    )
    poisoned = scorecard.copy()
    poisoned["sale_price_published"] = "999"
    poisoned["buyer_or_broker"] = "Not A Buyer"
    out = build_status_table(watch, curated, scorecard=poisoned, ipeds=ipeds, auto_checked_at="2026-10-06")
    row = out.iloc[0]
    assert row["sale_price_published"] == "~$65 million"
    assert row["buyer_or_broker"] == "BH Properties"
    assert row["property_disposition"] == "sold"
    assert row["source_url"] == "https://www.bhproperties.com/example"
    assert row["property_source"] == "curated"
    assert "Scorecard school.operating is 1" in row["disagreement"]
    assert "IPEDS shows operating" in row["disagreement"]
    assert "no directory row in 2025" in row["disagreement"]
    assert row["status_badge"].startswith("Closed · Campus sold 2023 to BH Properties")
    assert "999" not in row["status_badge"]
    assert row["auto_signal"] == "operating"


def test_agreeing_closed_signals_are_not_flagged():
    watch = _school(unitid=10)
    curated = _curated(unitid=10, status="closed")
    scorecard = pd.DataFrame({"unitid": [10], "scorecard_operating": [0]})
    ipeds = pd.DataFrame(
        {"unitid": [10], "year": [2023], "inst_status": [4], "date_closed": ["05/15/2023"]}
    )
    out = build_status_table(watch, curated, scorecard=scorecard, ipeds=ipeds)
    assert out.loc[0, "disagreement"] == ""
    assert out.loc[0, "auto_ipeds_date_closed"] == "2023-05-15"
    assert out.loc[0, "auto_signal"] == "closed"
    assert out.loc[0, "status_badge"] == "Closed"


def test_mixed_federal_signals_flag_only_the_conflict():
    watch = _school(unitid=10)
    curated = _curated(unitid=10, status="closed")
    scorecard = pd.DataFrame({"unitid": [10], "scorecard_operating": [1]})
    ipeds = pd.DataFrame(
        {"unitid": [10], "year": [2023], "inst_status": [4], "date_closed": ["2023-05-15"]}
    )
    out = build_status_table(watch, curated, scorecard=scorecard, ipeds=ipeds)
    text = out.loc[0, "disagreement"]
    assert "Scorecard school.operating is 1" in text
    assert "IPEDS shows closed" not in text
    assert out.loc[0, "auto_signal"] == "mixed"
    assert out.loc[0, "status"] == "closed"


def test_missing_federal_rows_do_not_invent_a_disagreement():
    watch = _school(unitid=10, status="operating")
    curated = _curated(unitid=10, status="operating", property_disposition="not_applicable")
    out = build_status_table(
        watch,
        curated,
        scorecard=pd.DataFrame(columns=["unitid", "scorecard_operating"]),
        fsa_closed=pd.DataFrame(columns=["opeid_raw", "closed_name", "closed_date", "unitid"]),
        ipeds=pd.DataFrame(columns=["unitid", "year", "inst_status", "date_closed"]),
    )
    assert out.loc[0, "disagreement"] == ""
    assert out.loc[0, "auto_scorecard_operating"] == ""
    assert out.loc[0, "auto_signal"] == "unknown"
    assert out.loc[0, "status_badge"] == "Open"


def test_not_enrolling_accepts_an_operating_flag_and_rejects_a_closed_one():
    watch = _school(unitid=28, inst_name="San Joaquin Valley College-Fresno")
    curated = _curated(
        unitid=28,
        inst_name="San Joaquin Valley College-Fresno",
        status="not_enrolling",
        property_disposition="not_applicable",
        sold_listed_details="N/A — not a closed-campus sale",
    )
    open_sc = pd.DataFrame({"unitid": [28], "scorecard_operating": [1]})
    opened = build_status_table(watch, curated, scorecard=open_sc)
    assert opened.loc[0, "disagreement"] == ""
    assert opened.loc[0, "status_badge"] == "Open, not enrolling"

    closed_sc = pd.DataFrame({"unitid": [28], "scorecard_operating": [0]})
    closed = build_status_table(watch, curated, scorecard=closed_sc)
    assert "Scorecard school.operating is 0" in closed.loc[0, "disagreement"]
    assert closed.loc[0, "status"] == "not_enrolling"


def test_merged_acquired_accepts_operating_or_ipeds_merger():
    watch = _school(unitid=42, inst_name="St Louis College of Health Careers-Fenton", opeid6="23405", opeid8="2340500")
    curated = _curated(
        unitid=42,
        inst_name="St Louis College of Health Careers-Fenton",
        status="merged_acquired",
        property_disposition="institutional_sale",
        buyer_or_broker="Stepful, Inc.",
        event_date="2025-12-01 (ownership transfer)",
        sale_price_published="",
        sold_listed_details="Institutional stock-purchase sale to Stepful.",
    )
    ipeds_merged = pd.DataFrame({"unitid": [42], "year": [2024], "inst_status": [3], "date_closed": [-2]})
    merged = build_status_table(watch, curated, ipeds=ipeds_merged)
    assert merged.loc[0, "disagreement"] == ""
    assert merged.loc[0, "status_badge"] == "Acquired by Stepful, Inc."
    assert "Campus sold" not in merged.loc[0, "status_badge"]

    ipeds_closed = pd.DataFrame(
        {"unitid": [42], "year": [2024], "inst_status": [4], "date_closed": ["2024-01-01"]}
    )
    closed = build_status_table(watch, curated, ipeds=ipeds_closed)
    assert "IPEDS shows closed" in closed.loc[0, "disagreement"]
    assert closed.loc[0, "buyer_or_broker"] == "Stepful, Inc."
    assert closed.loc[0, "sale_price_published"] == ""


def test_listed_badge_and_unpublished_buyer():
    listed = status_badge(
        {
            "status": "closed",
            "property_disposition": "listed",
            "buyer_or_broker": "Example Broker",
            "event_date": "2026-03",
            "sale_price_published": "",
        }
    )
    assert listed == "Closed · Campus listed for sale (Example Broker)"

    auction = status_badge(
        {
            "status": "closed",
            "property_disposition": "sold",
            "buyer_or_broker": "Joe R. Pyle Auction & Realty; buyer unpublished",
            "event_date": "2024-09-19 (auction/sold)",
            "sale_price_published": "",
        }
    )
    assert auction == "Closed · Campus sold 2024"
    assert "unpublished" not in auction
    assert sale_year_label("2023–2024 (phased)") == "2023–2024"


def test_closed_school_header_row_is_detected_and_sentinel_dates_dropped():
    raw = pd.DataFrame(
        [
            ["Weekly closed school search", None, None],
            ["OPE ID", "School Name", "Date Closed"],
            ["00974811", "Carrington College-Ontario", "01/08/2024"],
            ["", "blank", "01/01/2020"],
        ]
    )
    out = normalize_closed_school_frame(raw)
    assert len(out) == 1
    assert out.loc[0, "opeid_raw"] == "00974811"
    assert out.loc[0, "closed_name"] == "Carrington College-Ontario"
    assert out.loc[0, "closed_date"] == "01/08/2024"


def test_stamp_html_is_idempotent_and_links_the_source():
    page = """<!DOCTYPE html><html><head><style>
    .card { border: 1px solid #ddd; }
    </style></head><body>
    <div class="banner">Library holdings are not a model input.</div>
    <article class="card">
      <h2>1. Example College</h2>
      <p class="meta">CA · for-profit · score year 2022 · UNITID 115728</p>
      <p class="score">Watch-list score: <strong>0.962</strong>
      — elevated-risk indicator, not a closure verdict.</p>
      <table><tr><th>FTE</th><td>1</td></tr></table>
    </article>
    </body></html>"""
    status = pd.DataFrame(
        [
            {
                "unitid": "115728",
                "status": "closed",
                "status_badge": "Closed · Campus sold 2023 to BH Properties",
                "status_detail": "Closed (final semester Spring 2023).",
                "property_disposition": "sold",
                "buyer_or_broker": "BH Properties",
                "event_date": "2023-06 (sale)",
                "sale_price_published": "~$65 million",
                "sold_listed_details": "Sold to BH Properties Jun 2023 for ~$65 million.",
                "source_url": "https://www.bhproperties.com/example; staff memo",
                "checked_at": "2026-10-05",
                "disagreement": "",
            }
        ]
    )
    once = stamp_report_html(page, status)
    twice = stamp_report_html(once, status)
    assert once == twice
    assert once.count('class="status-block"') == 1
    assert "Campus sold 2023 to BH Properties" in once
    assert 'href="https://www.bhproperties.com/example"' in once
    assert "Published price: ~$65 million" in once
    assert ".status-block {" in once
    assert "Current-status badges" in once
    assert "staff memo" in once


def test_scorecard_lookup_skips_without_a_key(monkeypatch):
    monkeypatch.delenv("DATA_GOV_API_KEY", raising=False)
    monkeypatch.delenv("SCORECARD_API_KEY", raising=False)
    called = {"n": 0}

    def getter(*_args, **_kwargs):
        called["n"] += 1
        raise AssertionError("HTTP should not run without a key")

    settings = Settings(raw={"scorecard": {}}, root=ROOT)
    out = fetch_operating_by_unitids(settings, [115728], http_get=getter)
    assert out.empty
    assert called["n"] == 0


def test_scorecard_lookup_maps_operating_and_does_not_require_parquet(monkeypatch, tmp_path):
    monkeypatch.setenv("DATA_GOV_API_KEY", "unit-test-key-do-not-use")

    class _Resp:
        status_code = 200
        text = ""

        def json(self):
            return {
                "results": [
                    {
                        "id": 481155,
                        "school.name": "Helms College",
                        "school.operating": 1,
                        "school.state": "GA",
                    }
                ]
            }

    seen = {}

    def getter(url, params, timeout=30):
        seen["params"] = params
        return _Resp()

    settings = Settings(raw={"scorecard": {}, "paths": {}}, root=tmp_path)
    out = fetch_operating_by_unitids(settings, [481155], http_get=getter)
    assert seen["params"]["api_key"] == "unit-test-key-do-not-use"
    assert int(out.iloc[0]["unitid"]) == 481155
    assert int(out.iloc[0]["scorecard_operating"]) == 1
    assert not (tmp_path / "data" / "processed" / "scorecard_operating.parquet").exists()


def test_seed_matches_watchlist_and_prices_are_quoted_from_the_note():
    curated = load_curated(ROOT / "data" / "status" / "status_curated.csv")
    watch = load_watchlist(ROOT / "outputs" / "watchlist.csv", 50)
    seed = curated.iloc[:50]
    assert len(seed) == 50
    assert seed["unitid"].astype(int).tolist() == watch["unitid"].astype(int).tolist()
    assert seed["inst_name"].tolist() == watch["inst_name"].tolist()
    assert seed["checked_at"].eq("2026-10-05").all()
    assert curated["source_url"].str.contains("http").all()
    extra = curated.iloc[50:]
    if not extra.empty:
        assert set(extra["status"]) <= {"operating", "not_enrolling", "closed", "merged_acquired"}
        assert extra["sale_price_published"].eq("").all()
        assert extra["checked_at"].str.match(r"\d{4}-\d{2}-\d{2}").all()
        assert extra["watchlist_rank"].astype(int).min() > 50
        assert extra["source_url"].str.contains("educationdata.urban.org").sum() == 0
    assert set(curated["status"]) <= {"operating", "not_enrolling", "closed", "merged_acquired"}
    assert set(curated["property_disposition"]) <= {
        "not_applicable",
        "no_sale_found",
        "sold",
        "listed",
        "institutional_sale",
    }
    for _, row in curated.iterrows():
        price = row["sale_price_published"]
        if price:
            assert price in (row["sold_listed_details"] + " " + row["status_detail"])
        if row["property_disposition"] == "sold":
            assert row["buyer_or_broker"]
            assert "http" in row["source_url"]
        if row["property_disposition"] == "listed":
            assert "http" in row["source_url"]
    by_rank = curated.set_index(curated["watchlist_rank"].astype(int))
    assert by_rank.loc[1, "status"] == "closed"
    assert by_rank.loc[1, "property_disposition"] == "no_sale_found"
    assert by_rank.loc[14, "status"] == "operating"
    assert by_rank.loc[29, "status"] == "not_enrolling"
    assert by_rank.loc[30, "property_disposition"] == "sold"
    assert by_rank.loc[30, "sale_price_published"] == "~$65 million"
    assert by_rank.loc[42, "status"] == "merged_acquired"
    assert by_rank.loc[42, "property_disposition"] == "institutional_sale"
    assert by_rank.loc[53, "status"] == "merged_acquired"
    assert by_rank.loc[64, "status"] == "closed"
    assert by_rank.loc[78, "status"] == "merged_acquired"
    assert by_rank.loc[79, "status"] == "closed"
    assert by_rank.loc[87, "status"] == "closed"
    assert by_rank.loc[92, "status"] == "closed"
    assert by_rank.loc[99, "status"] == "closed"
    assert by_rank.loc[100, "status"] == "operating"
    assert by_rank.loc[42, "property_disposition"] == "institutional_sale"
    assert by_rank.loc[42, "sale_price_published"] == ""
    assert by_rank.loc[36, "sale_price_published"] == "combined $30,000"
    assert by_rank.loc[37, "sale_price_published"] == "$24 million"
    assert by_rank.loc[48, "sale_price_published"] == "~$3.5 million"
    priced = set(curated.loc[curated["sale_price_published"] != "", "watchlist_rank"].astype(int))
    assert priced == {30, 36, 37, 48}


def test_run_status_check_does_not_rewrite_the_curated_file(tmp_path):
    curated_src = (ROOT / "data" / "status" / "status_curated.csv").read_bytes()
    dest_dir = tmp_path / "data" / "status"
    dest_dir.mkdir(parents=True)
    curated_path = dest_dir / "status_curated.csv"
    curated_path.write_bytes(curated_src)
    watch_src = ROOT / "outputs" / "watchlist.csv"
    settings = Settings(
        raw={
            "paths": {"raw": "data/raw", "processed": "data/processed", "outputs": "outputs"},
            "status": {"curated_csv": "data/status/status_curated.csv"},
            "scorecard": {},
            "fsa": {},
            "urban": {},
        },
        root=tmp_path,
    )
    table = run_status_check(
        settings,
        top_n=2,
        write_html=False,
        watchlist=watch_src,
        auto_checked_at="2026-10-05",
        scorecard=pd.DataFrame(columns=["unitid", "scorecard_operating"]),
        fsa_closed=pd.DataFrame(columns=["opeid_raw", "closed_name", "closed_date", "unitid"]),
        ipeds=pd.DataFrame(columns=["unitid", "year", "inst_status", "date_closed"]),
    )
    assert curated_path.read_bytes() == curated_src
    assert len(table) == 2
    assert (tmp_path / "outputs" / "status_current.csv").exists()
    refresh = (tmp_path / "outputs" / "status_refresh.md").read_text(encoding="utf-8")
    assert "not modified" in refresh
    assert table.loc[0, "property_source"] == "curated"


def test_report_template_mentions_status_without_treating_it_as_a_score():
    from college_closure.report import _html_page

    page = _html_page("", n=1, score_year=2022, caveats="Watch list only.")
    assert ".badge-closed" in page
    assert "not closure predictions" in page
    assert "do not report them" in page
    assert "2022 federal financial data" in page
    assert "still operating" in page


def _ranked_status_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "watchlist_rank": 1,
                "unitid": 1,
                "inst_name": "DeVry-like",
                "state_abbr": "NV",
                "status": "closed",
                "property_disposition": "no_sale_found",
                "status_detail": "Local campus closed; system still operating",
                "auto_ipeds_status": "1",
                "auto_ipeds_date_closed": "",
                "auto_scorecard_operating": "1",
                "risk_score": 0.9,
                "year": 2022,
                "inst_control": 3,
                "source_url": "https://example.edu/devry",
            },
            {
                "watchlist_rank": 2,
                "unitid": 2,
                "inst_name": "Sold Campus",
                "state_abbr": "CA",
                "status": "closed",
                "property_disposition": "sold",
                "buyer_or_broker": "Buyer",
                "sale_price_published": "$1",
                "auto_ipeds_status": "1",
                "auto_scorecard_operating": "",
                "risk_score": 0.8,
                "year": 2022,
                "inst_control": 3,
                "source_url": "https://example.edu/sold",
            },
            {
                "watchlist_rank": 3,
                "unitid": 3,
                "inst_name": "Teach Out",
                "state_abbr": "CA",
                "status": "not_enrolling",
                "property_disposition": "not_applicable",
                "auto_ipeds_status": "1",
                "auto_scorecard_operating": "1",
                "risk_score": 0.7,
                "year": 2022,
                "inst_control": 3,
                "source_url": "https://example.edu/teach",
            },
            {
                "watchlist_rank": 4,
                "unitid": 4,
                "inst_name": "Still Open",
                "state_abbr": "TX",
                "status": "operating",
                "property_disposition": "no_sale_found",
                "auto_ipeds_status": "1",
                "auto_scorecard_operating": "1",
                "risk_score": 0.6,
                "year": 2022,
                "inst_control": 2,
                "source_url": "https://example.edu/open",
            },
            {
                "watchlist_rank": 5,
                "unitid": 5,
                "inst_name": "Directory Closed",
                "state_abbr": "OH",
                "status": "",
                "property_disposition": "",
                "auto_ipeds_status": "4",
                "auto_ipeds_date_closed": "2024-06-01",
                "auto_scorecard_operating": "",
                "risk_score": 0.5,
                "year": 2022,
                "inst_control": 3,
                "source_url": "https://educationdata.urban.org/example",
            },
            {
                "watchlist_rank": 6,
                "unitid": 6,
                "inst_name": "Directory Merged",
                "state_abbr": "NY",
                "status": "",
                "property_disposition": "",
                "auto_ipeds_status": "3",
                "auto_ipeds_date_closed": "",
                "auto_scorecard_operating": "",
                "risk_score": 0.4,
                "year": 2022,
                "inst_control": 2,
            },
            {
                "watchlist_rank": 7,
                "unitid": 7,
                "inst_name": "Scorecard Closed",
                "state_abbr": "FL",
                "status": "",
                "property_disposition": "",
                "auto_ipeds_status": "1",
                "auto_scorecard_operating": "0",
                "risk_score": 0.3,
                "year": 2022,
                "inst_control": 3,
            },
            {
                "watchlist_rank": 8,
                "unitid": 8,
                "inst_name": "Later Open",
                "state_abbr": "WA",
                "status": "",
                "property_disposition": "",
                "auto_ipeds_status": "1",
                "auto_ipeds_date_closed": "",
                "auto_ipeds_year": "2025",
                "auto_scorecard_operating": "1",
                "risk_score": 0.2,
                "year": 2022,
                "inst_control": 3,
            },
            {
                "watchlist_rank": 9,
                "unitid": 9,
                "inst_name": "Acquired Open",
                "state_abbr": "MO",
                "status": "merged_acquired",
                "property_disposition": "institutional_sale",
                "auto_ipeds_status": "1",
                "auto_scorecard_operating": "1",
                "risk_score": 0.1,
                "year": 2022,
                "inst_control": 2,
                "source_url": "https://example.edu/acquired",
            },
            {
                "watchlist_rank": 10,
                "unitid": 10,
                "inst_name": "Too Far",
                "state_abbr": "OR",
                "status": "operating",
                "property_disposition": "no_sale_found",
                "auto_ipeds_status": "1",
                "risk_score": 0.05,
                "year": 2022,
                "inst_control": 2,
            },
        ]
    )


def test_operating_partition_keeps_only_schools_still_operating():
    from college_closure.status import operating_bucket, partition_operating

    table = _ranked_status_rows()
    assert operating_bucket(table.iloc[0]) == "closed"
    assert (
        operating_bucket(
            {
                "status": "",
                "property_disposition": "",
                "auto_ipeds_status": "1",
                "auto_ipeds_date_closed": "2023-01-15",
                "auto_scorecard_operating": "",
            }
        )
        == "closed"
    )
    assert (
        operating_bucket(
            {
                "status": "not_enrolling",
                "property_disposition": "not_applicable",
                "auto_ipeds_status": "4",
                "auto_ipeds_date_closed": "2024-01-01",
                "auto_scorecard_operating": "1",
            }
        )
        == "closed"
    )
    assert (
        operating_bucket(
            {
                "status": "merged_acquired",
                "property_disposition": "not_applicable",
                "auto_ipeds_status": "1",
                "auto_scorecard_operating": "1",
            }
        )
        == "closed"
    )
    assert (
        operating_bucket(
            {
                "status": "merged_acquired",
                "property_disposition": "institutional_sale",
                "auto_ipeds_status": "1",
                "auto_scorecard_operating": "1",
            }
        )
        == "open"
    )
    open_df, teach, closed, depth = partition_operating(table, 3)
    assert open_df["inst_name"].tolist() == ["Still Open", "Later Open", "Acquired Open"]
    assert teach["inst_name"].tolist() == ["Teach Out"]
    assert set(closed["inst_name"]) == {
        "DeVry-like",
        "Sold Campus",
        "Directory Closed",
        "Directory Merged",
        "Scorecard Closed",
    }
    assert depth == 9
    placed = set(open_df["inst_name"]) | set(teach["inst_name"]) | set(closed["inst_name"])
    assert "Too Far" not in placed


def test_append_operating_rows_does_not_touch_existing_lines(tmp_path):
    from college_closure.status import CURATED_COLUMNS, append_curated_rows, federal_operating_curated_fields

    path = tmp_path / "status_curated.csv"
    original = (
        ",".join(CURATED_COLUMNS)
        + "\n"
        + "111,1,11,1,Holy Names,CA,closed,Sold the campus,sold,Buyer,2023-05,1000000,"
        + "sold the campus,https://example.edu/sale,2026-10-05,\n"
    )
    path.write_text(original, encoding="utf-8")
    new = federal_operating_curated_fields(
        {
            "unitid": 222,
            "opeid6": "2",
            "opeid8": "22",
            "watchlist_rank": 60,
            "inst_name": "New Open",
            "state_abbr": "TX",
            "auto_ipeds_year": "2025",
            "auto_ipeds_status": "1",
            "auto_scorecard_operating": "1",
        },
        "2026-10-05",
    )
    appended = append_curated_rows(path, [new, new])
    assert len(appended) == 1
    text = path.read_text(encoding="utf-8")
    assert text.startswith(original)
    assert "New Open" in text
    assert "1000000" in text
    assert "https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2025/?unitid=222" in text
    assert append_curated_rows(path, [new]) == []
    assert path.read_text(encoding="utf-8") == text


def test_operating_report_sections_list_rank_score_and_sources(tmp_path):
    from college_closure.report import write_operating_report

    table = _ranked_status_rows()
    path = tmp_path / "top50_report.html"
    stats = write_operating_report(path, table, table, open_n=3, score_year=2022)
    page = path.read_text(encoding="utf-8")
    assert stats["n_open"] == 3
    assert stats["depth"] == 9
    assert "Teach-out / not enrolling" in page
    assert "Closed or defunct since the 2022 data" in page
    assert "2022 federal financial data" in page
    assert "not closure predictions" in page
    assert "through rank 9" in page
    assert "watch-list rank 8" in page
    main, _, after_teach = page.partition("Teach-out / not enrolling")
    assert "<h2>1. Still Open</h2>" in main
    assert "Teach Out" not in main
    assert "DeVry-like" not in main
    teach_body, _, closed_body = after_teach.partition("Closed or defunct since the 2022 data")
    assert "Teach Out" in teach_body
    assert "DeVry-like" in closed_body
    assert "Original rank" in closed_body
    assert "0.900" in closed_body
    assert "https://example.edu/devry" in closed_body


def test_status_refresh_workflow_survives_pr_creation_refusal():
    text = (ROOT / ".github/workflows/status-refresh.yml").read_text(encoding="utf-8")
    assert "contents: write" in text
    assert 'branch="status-refresh"' in text
    assert "GITHUB_STEP_SUMMARY" in text
    assert "compare/main...status-refresh" in text
    assert "elif gh pr create" in text
    assert "Pull request was not created" in text
    assert text.strip().endswith("exit 0")
    assert "git push --force-with-lease origin" in text
