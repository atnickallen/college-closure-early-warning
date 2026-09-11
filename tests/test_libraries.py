"""Academic Libraries join/parse and special-collection note extraction (no network)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from college_closure.libraries import (
    NOTHING_DISTINCTIVE_NOTE,
    UNKNOWN_NOTE,
    attach_library_columns,
    distinctive_notes_html,
    extract_special_collections_note,
    latest_library_snapshot,
    library_section_html,
    match_arl_member,
    normalize_academic_libraries,
    parse_arl_member_names,
)


def test_normalize_urban_al_and_sentinels():
    raw = pd.DataFrame(
        [
            {
                "unitid": 100001,
                "year": 2022,
                "physical_books": 12000,
                "total_electronic_collections": 5400,
                "electronic_books": 4000,
                "exp_total": 250000,
                "librarians_fte": 3.5,
                "total_lib_staff_fte": 8.0,
            },
            {
                "unitid": 100002,
                "year": 2022,
                "physical_books": -2,
                "total_electronic_collections": -1,
                "electronic_books": -3,
                "exp_total": -2,
                "librarians_fte": -1,
                "total_lib_staff_fte": -2,
            },
        ]
    )
    out = normalize_academic_libraries(raw, source="urban")
    assert set(out["unitid"]) == {100001, 100002}
    row = out.loc[out["unitid"] == 100001].iloc[0]
    assert row["lib_physical_books"] == 12000
    assert row["lib_digital_items"] == 5400
    assert row["lib_expenditures"] == 250000
    assert row["lib_fte"] == 3.5
    assert row["lib_source"] == "urban"
    missing = out.loc[out["unitid"] == 100002].iloc[0]
    assert pd.isna(missing["lib_physical_books"])
    assert pd.isna(missing["lib_digital_items"])
    assert pd.isna(missing["lib_expenditures"])
    assert pd.isna(missing["lib_fte"])


def test_normalize_nces_al_aliases_and_digital_sum():
    raw = pd.DataFrame(
        [
            {
                "UNITID": 200001,
                "YEAR": 2021,
                "LPBOOKS": 8000,
                "LDBOOKS": 1500,
                "LDMEDIA": 200,
                "LDSERIAL": 50,
                "LEXPTOT": 99000,
                "LSCLIB": 2.0,
                "LSCTOT": 5.0,
            }
        ]
    )
    out = normalize_academic_libraries(raw, source="nces")
    row = out.iloc[0]
    assert int(row["unitid"]) == 200001
    assert row["lib_physical_books"] == 8000
    assert row["lib_digital_items"] == 1750
    assert row["lib_expenditures"] == 99000
    assert row["lib_fte"] == 2.0
    assert row["lib_source"] == "nces"


def test_digital_items_not_fabricated_when_all_pieces_missing():
    raw = pd.DataFrame(
        [{"unitid": 1, "year": 2022, "physical_books": 10, "electronic_books": None}]
    )
    out = normalize_academic_libraries(raw)
    assert pd.isna(out.iloc[0]["lib_digital_items"])


def test_latest_al_prefers_score_year_then_latest():
    al = pd.DataFrame(
        [
            {"unitid": 1, "year": 2019, "lib_physical_books": 100, "lib_source": "urban"},
            {"unitid": 1, "year": 2021, "lib_physical_books": 110, "lib_source": "urban"},
            {"unitid": 1, "year": 2023, "lib_physical_books": 999, "lib_source": "urban"},
            {"unitid": 2, "year": 2023, "lib_physical_books": 50, "lib_source": "urban"},
        ]
    )
    snap = latest_library_snapshot(al, score_year=2022)
    one = snap.loc[snap["unitid"] == 1].iloc[0]
    assert int(one["lib_year"]) == 2021
    assert one["lib_physical_books"] == 110
    two = snap.loc[snap["unitid"] == 2].iloc[0]
    assert int(two["lib_year"]) == 2023  # no prior year; use latest available


def test_reattach_drops_stale_lib_columns():
    watch = pd.DataFrame(
        [
            {
                "unitid": 1,
                "inst_name": "Rejoin College",
                "year": 2022,
                "lib_physical_books": pd.NA,
                "lib_special_collections_note": "Web note not collected (outside top-50 / nonprofit shortlist).",
                "lib_unique_flag": False,
            }
        ]
    )
    snap = pd.DataFrame(
        [
            {
                "unitid": 1,
                "lib_year": 2022,
                "lib_source": "urban",
                "lib_physical_books": 5000,
                "lib_digital_items": 100,
                "lib_expenditures": 20000,
                "lib_fte": 2.0,
            }
        ]
    )
    notes = pd.DataFrame(
        [
            {
                "unitid": 1,
                "lib_special_collections_note": "Named holdings on a public library page: Example Rare Book Collection.",
                "lib_unique_flag": True,
                "lib_note_url": "https://example.edu/library",
            }
        ]
    )
    out = attach_library_columns(watch, snap, notes, arl_names=[])
    assert "lib_physical_books_x" not in out.columns
    assert out.iloc[0]["lib_physical_books"] == 5000
    assert bool(out.iloc[0]["lib_unique_flag"]) is True


def test_attach_does_not_fill_missing_holdings_with_zero():
    watch = pd.DataFrame(
        [
            {"unitid": 1, "inst_name": "Has Books College", "year": 2022},
            {"unitid": 2, "inst_name": "Unknown Library College", "year": 2022},
        ]
    )
    snap = pd.DataFrame(
        [
            {
                "unitid": 1,
                "lib_year": 2022,
                "lib_source": "urban",
                "lib_physical_books": 1000,
                "lib_digital_items": 200,
                "lib_expenditures": 50000,
                "lib_fte": 1.0,
            }
        ]
    )
    notes = pd.DataFrame(
        [
            {
                "unitid": 1,
                "lib_special_collections_note": "Named holdings on a public library page: Smith Rare Book Collection.",
                "lib_unique_flag": True,
                "lib_note_url": "https://example.edu/library",
            }
        ]
    )
    out = attach_library_columns(watch, snap, notes, arl_names=["Harvard University"])
    has = out.loc[out["unitid"] == 1].iloc[0]
    miss = out.loc[out["unitid"] == 2].iloc[0]
    assert has["lib_physical_books"] == 1000
    assert bool(has["lib_unique_flag"]) is True
    assert pd.isna(miss["lib_physical_books"])
    assert pd.isna(miss["lib_expenditures"])
    assert bool(miss["lib_unique_flag"]) is False
    assert "outside top-50" in str(miss["lib_special_collections_note"]).lower()


def test_extract_named_special_collection_from_html():
    html = """
    <html><body>
      <h2>Special Collections</h2>
      <p>The Shaw Historical Library holds timber-industry manuscripts and
      regional photographs. Researchers may request materials by appointment.</p>
      <p>Library hours are 9 to 5. Ask a librarian for help.</p>
    </body></html>
    """
    got = extract_special_collections_note(html, page_url="https://example.edu/library/special")
    assert got["unique_flag"] is True
    assert "Shaw Historical Library" in got["note"]
    assert "https://example.edu/library/special" in got["note"]
    assert "12000 volumes" not in got["note"]


def test_extract_generic_library_page_is_not_unique():
    html = """
    <html><body>
      <h1>College Library</h1>
      <p>Welcome to the library. Search the catalog and renew your books online.
      Interlibrary loan is available to students. Ask a librarian at the desk.</p>
      <p>Hours of operation Monday through Friday.</p>
    </body></html>
    """
    got = extract_special_collections_note(html, page_url="https://example.edu/library")
    assert got["unique_flag"] is False
    assert got["note"] in {NOTHING_DISTINCTIVE_NOTE, UNKNOWN_NOTE} or "nothing distinctive" in got["note"].lower()
    assert "rare book" not in got["note"].lower() or "no named" in got["note"].lower()


def test_extract_accepts_named_archive_in_a_real_sentence():
    html = """
    <html><body>
      <h2>University Archives</h2>
      <p>Holdings include the Pacific Northwest Artists Archive and the
      Willamette University Archives of regional manuscripts.</p>
    </body></html>
    """
    got = extract_special_collections_note(html, page_url="https://library.example.edu/archives/")
    assert got["unique_flag"] is True
    assert any("Pacific Northwest Artists Archive" in n for n in got["names"])


def test_extract_drops_promotional_extra_sentence():
    html = """
    <html><body>
      <h2>University Archives and Records</h2>
      <p>The Pacific Northwest Artists Archive documents regional studio practice.</p>
      <p>Willamette University Archives is thrilled to launch WUpedia, a dynamic
      online encyclopedia of campus history.</p>
    </body></html>
    """
    got = extract_special_collections_note(html, page_url="https://library.example.edu/archives/")
    assert got["unique_flag"] is True
    assert "Pacific Northwest Artists Archive" in got["note"]
    assert "thrilled" not in got["note"].lower()
    assert "wupedia" not in got["note"].lower()
    assert "University Archives and Records" not in got["note"]


def test_extract_rejects_nav_and_vendor_catalog_junk():
    html = """
    <html><body>
      <nav>Collections Mission Hours Contact Us Staff Policies Archives</nav>
      <p>Search SAGE Digital Library and the HNU Academic Catalog Archive.</p>
    </body></html>
    """
    got = extract_special_collections_note(html, page_url="https://example.edu/nav")
    assert got["unique_flag"] is False
    assert "SAGE" not in (got.get("names") or [])


def test_extract_mentions_special_collections_without_a_name():
    html = """
    <html><body>
      <p>Our special collections and university archives are available to
      visiting scholars by appointment only.</p>
    </body></html>
    """
    got = extract_special_collections_note(html)
    assert got["unique_flag"] is False
    assert "no named collection" in got["note"].lower()


def test_extract_empty_html_is_unknown():
    got = extract_special_collections_note("<html></html>")
    assert got["unique_flag"] is False
    assert got["note"] == UNKNOWN_NOTE


def test_arl_name_match_does_not_false_positive_small_colleges():
    arl = parse_arl_member_names(
        "<html><body><li>Harvard University</li><li>New York Public Library</li>"
        "<li>University of Michigan</li></body></html>"
    )
    assert any("Harvard" in n for n in arl)
    assert match_arl_member("Harvard University", arl) is True
    assert match_arl_member("The King's College", arl) is False
    assert match_arl_member("New York College of Health Professions", ["New York Public Library"]) is False
    assert match_arl_member("Notre Dame College", ["University of Notre Dame"]) is False


def test_library_section_html_uses_unknown_not_zero():
    row = pd.Series(
        {
            "lib_physical_books": pd.NA,
            "lib_digital_items": pd.NA,
            "lib_expenditures": pd.NA,
            "lib_fte": pd.NA,
            "lib_year": pd.NA,
            "lib_source": pd.NA,
            "lib_arl_member": False,
            "lib_unique_flag": False,
            "lib_special_collections_note": UNKNOWN_NOTE,
        }
    )
    html = library_section_html(row)
    assert "Libraries" in html
    assert "not a model feature" in html
    assert "$0" not in html
    assert "—" in html


def test_write_summary_roundtrip(tmp_path: Path):
    from college_closure.libraries import write_libraries_summary

    df = pd.DataFrame(
        [
            {
                "unitid": 1,
                "inst_name": "Example College",
                "lib_year": 2022,
                "lib_physical_books": 100,
                "lib_digital_items": 20,
                "lib_expenditures": 1000,
                "lib_fte": 1.0,
                "lib_arl_member": False,
                "lib_unique_flag": True,
                "lib_special_collections_note": "Named holdings on a public library page: Example Rare Book Collection.",
            }
        ]
    )
    dest = tmp_path / "libraries_top50.md"
    write_libraries_summary(df, dest)
    text = dest.read_text(encoding="utf-8")
    assert "Example Rare Book Collection" in text
    assert "Not a closure verdict" in text
    banner = distinctive_notes_html(df)
    assert "Example College" in banner
    assert "Example Rare Book Collection" in banner
