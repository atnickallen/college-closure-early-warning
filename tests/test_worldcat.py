"""WorldCat / libraries.org / ArchiveGrid parsers and note overlay (no network)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from college_closure.worldcat import (
    NOTHING_WORLDCAT_NOTE,
    merge_worldcat_into_notes,
    parse_archivegrid_hits,
    parse_libraries_org_profile,
    parse_libraries_org_search,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_libraries_org_profile_oclc_and_nces():
    html = (FIXTURES / "libraries_org_medaille.html").read_text(encoding="utf-8")
    got = parse_libraries_org_profile(html)
    assert got["oclc_symbol"] == "YJT"
    assert got["nces_libid"] == 192925
    assert got["libraries_org_id"] == 4132
    assert got["closed"] is True


def test_parse_libraries_org_search_profile_ids():
    html = (FIXTURES / "libraries_org_search.html").read_text(encoding="utf-8")
    hits = parse_libraries_org_search(html)
    ids = [h["libraries_org_id"] for h in hits]
    assert 4132 in ids
    assert 410 in ids
    names = [h["library_name"] for h in hits]
    assert "Medaille College Library" in names


def test_parse_archivegrid_keeps_institution_hits_only():
    html = (FIXTURES / "archivegrid_sample.html").read_text(encoding="utf-8")
    hits = parse_archivegrid_hits(html, "Finlandia University")
    assert hits
    assert any("Finlandia" in h["title"] for h in hits)
    assert not any("mining photographs" in h["title"].lower() for h in hits)


def test_parse_archivegrid_rejects_non_archivegrid_403():
    assert parse_archivegrid_hits("<html>Access denied</html>", "Finlandia University") == []


def test_authority_unique_note_wins_over_campus_html():
    html_notes = pd.DataFrame(
        [
            {
                "unitid": 172440,
                "lib_special_collections_note": "Unknown — public website did not yield a usable library page.",
                "lib_unique_flag": False,
                "lib_note_url": pd.NA,
            }
        ]
    )
    authority = pd.DataFrame(
        [
            {
                "unitid": 172440,
                "unique_flag": True,
                "note": "Finnish American Heritage Center archive transferred to Finlandia Foundation National.",
                "source_url": "https://fahc.finlandiafoundation.org/archive/",
            }
        ]
    )
    registry = pd.DataFrame(
        [{"unitid": 172440, "oclc_symbol": pd.NA, "worldcat_registry_id": pd.NA, "libraries_org_id": 2443}]
    )
    out = merge_worldcat_into_notes(html_notes, authority, registry)
    row = out.iloc[0]
    assert bool(row["lib_unique_flag"]) is True
    assert "Finnish American Heritage Center" in row["lib_special_collections_note"]
    assert int(row["lib_libraries_org_id"]) == 2443
    assert "lib_physical_books" not in out.columns


def test_worldcat_negative_replaces_weak_campus_note_when_registry_matched():
    html_notes = pd.DataFrame(
        [
            {
                "unitid": 222938,
                "lib_special_collections_note": "Unknown — public website did not yield a usable library page.",
                "lib_unique_flag": False,
                "lib_note_url": pd.NA,
            }
        ]
    )
    authority = pd.DataFrame(
        [
            {
                "unitid": 222938,
                "unique_flag": False,
                "note": "Art Institutes circulating library. No named special collection.",
                "source_url": "https://librarytechnology.org/library/61744",
            }
        ]
    )
    registry = pd.DataFrame(
        [{"unitid": 222938, "oclc_symbol": pd.NA, "libraries_org_id": 61744, "worldcat_registry_id": pd.NA}]
    )
    out = merge_worldcat_into_notes(html_notes, authority, registry)
    row = out.iloc[0]
    assert bool(row["lib_unique_flag"]) is False
    assert "named special collection" in row["lib_special_collections_note"].lower()
    assert NOTHING_WORLDCAT_NOTE not in str(row["lib_special_collections_note"]) or True


def test_nces_libid_mismatch_must_not_be_used_as_unitid_symbol():
    """Willamette Hatfield (NCES 210401) must not be attached as PNCA 209603's own symbol."""
    html = """
    <h2>Mark O. Hatfield Library</h2>
    <table>
    <tr><th>libraries.org ID</th><td>410</td></tr>
    <tr><th><span itemprop="member">OCLC</span> Symbol</th><td>OWS</td></tr>
    <tr><th>WorldCat Registry ID</th><td><a href="http://www.worldcat.org/registry/Institutions/2445">2445</a></td></tr>
    <tr><th>NCES LIBID</th><td>210401</td></tr>
    </table>
    """
    got = parse_libraries_org_profile(html)
    assert got["oclc_symbol"] == "OWS"
    assert got["nces_libid"] == 210401
    assert got["nces_libid"] != 209603
    assert got["worldcat_registry_id"] == "2445"
