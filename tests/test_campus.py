"""Residential-campus filter: housing year, dorms, and own-campus gate."""

from pathlib import Path

import pandas as pd

from college_closure.campus import (
    acquisition_ready,
    exclusion_reason,
    extend_ranked_universe,
    housing_is_reported,
    is_residential,
    is_small_housing,
    latest_reported_housing,
    load_ranked_universe,
    partition_acquisition,
    prefix_through_acquisition,
    satellite_maps_url,
    write_ranked_universe,
)


def _row(**kwargs):
    base = {
        "status": "operating",
        "property_disposition": "not_applicable",
        "auto_ipeds_status": "1",
        "auto_ipeds_date_closed": "",
        "auto_scorecard_operating": "1",
        "oncampus_housing": 1,
        "dormitory_capacity": 100,
        "own_campus": "yes",
        "watchlist_rank": 1,
    }
    base.update(kwargs)
    return base


def test_housing_sentinels_are_not_a_reported_yes_or_no():
    assert housing_is_reported(1)
    assert housing_is_reported(0)
    assert housing_is_reported("1")
    assert not housing_is_reported(-1)
    assert not housing_is_reported(-2)
    assert not housing_is_reported(-3)
    assert not housing_is_reported(None)


def test_latest_housing_year_skips_a_newer_missing_code():
    frame = pd.DataFrame(
        [
            {"unitid": 1, "year": 2022, "oncampus_housing": 1, "dormitory_capacity": 80},
            {"unitid": 1, "year": 2024, "oncampus_housing": -1, "dormitory_capacity": -1},
            {"unitid": 1, "year": 2025, "oncampus_housing": -1, "dormitory_capacity": -1},
            {"unitid": 2, "year": 2023, "oncampus_housing": 0, "dormitory_capacity": -2},
        ]
    )
    latest = latest_reported_housing(frame).set_index("unitid")
    assert int(latest.loc[1, "housing_year"]) == 2022
    assert int(float(latest.loc[1, "dormitory_capacity"])) == 80
    assert int(latest.loc[2, "housing_year"]) == 2023
    assert not is_residential({"oncampus_housing": 0, "dormitory_capacity": -2})


def test_residential_requires_housing_yes_and_a_positive_capacity():
    assert is_residential(_row())
    assert not is_residential(_row(oncampus_housing=0, dormitory_capacity=100))
    assert not is_residential(_row(oncampus_housing=1, dormitory_capacity=0))
    assert not is_residential(_row(oncampus_housing=1, dormitory_capacity=-1))
    assert not is_residential(_row(oncampus_housing=1, dormitory_capacity=-3))
    assert not is_residential(_row(oncampus_housing=-1, dormitory_capacity=40))
    assert is_small_housing(_row(dormitory_capacity=49))
    assert not is_small_housing(_row(dormitory_capacity=50))
    assert not is_small_housing(_row(dormitory_capacity=-1))


def test_own_campus_yes_is_required_and_a_missing_row_is_not_confirmed():
    assert acquisition_ready(_row())
    assert not acquisition_ready(_row(own_campus="no"))
    assert not acquisition_ready(_row(own_campus="unknown"))
    assert not acquisition_ready(_row(own_campus=""))
    assert not acquisition_ready(_row(status="closed", property_disposition="no_sale_found"))
    assert exclusion_reason(_row(oncampus_housing=0)) == "no on-campus dorms"
    assert exclusion_reason(_row(own_campus="no")) == "no standalone campus"
    assert exclusion_reason(_row(own_campus="")) == "campus not confirmed"
    assert exclusion_reason(_row(status="closed", property_disposition="sold")) == ""


def test_walker_continues_past_the_watchlist_when_fifty_are_not_filled():
    watch = pd.DataFrame(
        [
            {"unitid": 1, "year": 2022, "risk_score": 0.9, "inst_name": "First", "watchlist_rank": 1},
            {"unitid": 2, "year": 2022, "risk_score": 0.8, "inst_name": "Second", "watchlist_rank": 2},
        ]
    )
    scored = pd.DataFrame(
        [
            {"unitid": 1, "year": 2022, "risk_score": 0.9, "inst_name": "First"},
            {"unitid": 9, "year": 2022, "risk_score": 0.2, "inst_name": "Later"},
            {"unitid": 8, "year": 2021, "risk_score": 0.99, "inst_name": "Wrong year"},
        ]
    )
    universe = extend_ranked_universe(watch, scored)
    assert universe["inst_name"].tolist() == ["First", "Second", "Later"]
    assert universe["watchlist_rank"].tolist() == [1, 2, 3]
    assert extend_ranked_universe(watch, None).equals(watch) or len(extend_ranked_universe(watch, None)) == 2

    rows = []
    for rank in range(1, 4):
        rows.append(
            _row(
                watchlist_rank=rank,
                unitid=rank,
                inst_name=f"School {rank}",
                oncampus_housing=0 if rank < 3 else 1,
                own_campus="yes" if rank == 3 else "",
                dormitory_capacity=120 if rank == 3 else 0,
            )
        )
    table = pd.DataFrame(rows)
    prefix = prefix_through_acquisition(table, 1)
    assert prefix["watchlist_rank"].tolist() == [1, 2, 3]
    acquired, excluded, _teach, _closed, depth = partition_acquisition(table, 1)
    assert acquired["inst_name"].tolist() == ["School 3"]
    assert excluded["inst_name"].tolist() == ["School 1", "School 2"]
    assert depth == 3


def test_committed_ranked_universe_continues_ranks_after_the_watchlist(tmp_path):
    scored = pd.DataFrame(
        [
            {"unitid": 1, "year": 2022, "risk_score": 0.9, "inst_name": "First", "label_complete_h3": False, "miss_finance": False},
            {"unitid": 7, "year": 2022, "risk_score": 0.4, "inst_name": "Seventh", "label_complete_h3": False, "miss_finance": False},
            {"unitid": 8, "year": 2023, "risk_score": 0.99, "inst_name": "Newer", "label_complete_h3": False, "miss_finance": False},
        ]
    )
    dest = tmp_path / "ranked_universe.csv"
    n = write_ranked_universe(scored, dest, prefer_year=2022)
    assert n == 2
    loaded = load_ranked_universe(dest)
    watch = pd.DataFrame(
        [{"unitid": 1, "year": 2022, "risk_score": 0.99, "inst_name": "First", "watchlist_rank": 1}]
    )
    universe = extend_ranked_universe(watch, loaded)
    assert universe["inst_name"].tolist() == ["First", "Seventh"]
    assert universe["watchlist_rank"].tolist() == [1, 2]
    assert load_ranked_universe(tmp_path / "missing.csv").empty


def test_repo_ranked_universe_extends_the_watchlist_past_500():
    root = Path(__file__).resolve().parents[1]
    loaded = load_ranked_universe(root / "outputs" / "ranked_universe.csv")
    assert not loaded.empty
    assert set(loaded["year"].dropna().astype(int)) == {2022}
    assert len(loaded) > 500
    watch = pd.read_csv(root / "outputs" / "watchlist.csv")
    universe = extend_ranked_universe(watch, loaded)
    assert int(universe["watchlist_rank"].max()) > 500
    assert universe["unitid"].astype(int).head(500).tolist() == watch["unitid"].astype(int).head(500).tolist()


def test_satellite_maps_url_uses_the_campus_center():
    url = satellite_maps_url("42.307206", "-83.694097")
    assert url == (
        "https://www.google.com/maps/@?api=1&map_action=map"
        "&center=42.307206,-83.694097&zoom=17&basemap=satellite"
    )
    assert satellite_maps_url("", "-83.6") == ""
    assert satellite_maps_url(None, None) == ""
    assert satellite_maps_url("91", "0") == ""


def test_land_file_has_a_campus_pin_for_every_row():
    root = Path(__file__).resolve().parents[1]
    land = pd.read_csv(root / "data" / "campus" / "campus_land.csv", dtype=str, keep_default_na=False)
    assert {"lat", "lon", "coord_source"} <= set(land.columns)
    assert (land["lat"].str.strip() != "").all()
    assert (land["lon"].str.strip() != "").all()
    assert land["coord_source"].str.contains("IPEDS HD").all()
    moved = land[land["coord_source"].str.contains("Adjusted")]
    assert moved["unitid"].tolist() == ["169363"]
    concordia = land[land["unitid"] == "169363"].iloc[0]
    assert abs(float(concordia["lat"]) - 42.307206) < 0.001
    assert abs(float(concordia["lon"]) + 83.694097) < 0.001
    assert "3475 Plymouth" in concordia["coord_source"]
    assert "4090 Geddes" in concordia["coord_source"]
    html = (root / "outputs" / "top50_report.html").read_text(encoding="utf-8")
    main, _, _ = html.partition("Teach-out / not enrolling")
    assert main.count(">Satellite view</a>") == 50
    assert html.count(">Satellite view</a>") == 71
    assert "center=42.307206,-83.694097&amp;zoom=17&amp;basemap=satellite" in html
    assert "42.273157" not in html
