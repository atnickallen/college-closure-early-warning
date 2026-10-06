"""Score explanations: plain drivers, artifact flags, and the report panel."""

from pathlib import Path

import pandas as pd

from college_closure.explain import (
    facts_html,
    plain_driver,
    quality_flags,
    suspected_artifact,
    why_panel_html,
)


def test_plain_driver_states_the_five_year_headcount_change():
    text = plain_driver(
        "enr_pct_chg_5y",
        -0.38,
        2024,
        context={
            "fall_headcount_earlier": 407,
            "fall_year_earlier": 2019,
            "fall_headcount": 252,
            "fall_year": 2024,
            "fall_headcount_pct_change": -0.38,
        },
    )
    assert "407" in text
    assert "2019" in text
    assert "2024" in text
    assert "-38%" in text


def test_plain_driver_does_not_pair_a_fte_change_with_different_headcounts():
    text = plain_driver(
        "enr_pct_chg_5y",
        -0.64,
        2024,
        context={
            "fall_headcount_earlier": 63,
            "fall_year_earlier": 2019,
            "fall_headcount": 43,
            "fall_year": 2024,
            "fall_headcount_pct_change": -0.32,
            "fte_earlier": 45,
            "fte_year_earlier": 2019,
            "fte_count": 16,
            "fte_year": 2024,
        },
    )
    assert "FTE moved from 45" in text
    assert "-64%" in text
    assert "63" not in text


def test_plain_driver_states_tuition_share_and_endowment_coverage():
    tuition = plain_driver("tuition_dependence", 0.92, 2023)
    assert "92%" in tuition
    assert "revenue" in tuition
    endow = plain_driver(
        "endowment_per_fte",
        5000,
        2023,
        context={"endowment_market_value": 2_000_000, "expenses": 5_000_000},
    )
    assert "0.4 years" in endow


def test_quality_flag_catches_finance_that_never_reached_the_score():
    row = {"miss_finance": True, "finance_from_parent": False, "enr_pct_chg_5y": None}
    flags = quality_flags(row, {"extract_has_finance": True, "n_missing_features": 28, "control": 2})
    text = " ".join(flags)
    assert "missingness pattern" in text
    artifact, reason = suspected_artifact(flags, ["miss_finance", "log_fte", "miss_composite"])
    assert artifact
    assert "missingness pattern" in reason


def test_system_filing_is_an_artifact_even_when_another_feature_ranks_first():
    flags = [
        "This campus has no finance row in the extract. IPEDS finance for the system is filed under UNITID 155627 (Ottawa University-Ottawa)."
    ]
    artifact, reason = suspected_artifact(flags, ["log_fte", "rural", "fte_under_1000"])
    assert artifact
    assert "155627" in reason


def test_endowment_block_is_outside_the_why_panel():
    summary = {
        "endowment_market_value": 592_903_744,
        "endowment_year": 2023,
        "endowment_per_fte_display": 1_770_000,
        "endowment_scope": "this campus",
        "endowment_source": "IPEDS finance 2023 endowment_end for UNITID 148016",
        "enrollment_source": "IPEDS fall enrollment and 12-month enrollment FTE",
        "fall_headcount": 339,
        "fall_undergrad": 339,
        "fall_grad": None,
        "fall_year": 2024,
        "fte_count": 335,
        "fte_year": 2024,
        "fall_headcount_earlier": 407,
        "fall_year_earlier": 2019,
        "fall_headcount_pct_change": 339 / 407 - 1,
        "endowment_note": "Data USA reports the same figure.",
        "risk_score": 0.524,
        "composite_score": None,
        "composite_year": None,
        "top_driver_1": "IPEDS finance is missing on the scored row",
        "top_driver_2": "enrollment is missing on the scored row",
        "top_driver_3": "no federal composite score is on the scored row",
        "data_quality_flags": "Finance is missing on the scored row",
        "missing_or_imputed": "Left missing.",
        "artifact_reason": "The vintage snapshot never saw the filing.",
    }
    facts = facts_html(summary)
    panel = why_panel_html(
        summary,
        [
            {"feature": "miss_finance", "contribution": 0.12},
            {"feature": "log_fte", "contribution": 0.08},
            {"feature": "endowment_per_fte", "contribution": -0.04},
        ],
    )
    assert "Endowment and enrollment" in facts
    assert "$592.9 million" in facts
    assert "407 in 2019" in facts
    assert "339 in 2024" in facts
    assert "<details" not in facts
    assert "Why it ranks here" in panel
    assert 'class="fill up"' in panel
    assert 'class="fill down"' in panel
    assert facts.index("Endowment and enrollment") >= 0


def test_committed_explanations_cover_the_residential_top_50():
    root = Path(__file__).resolve().parents[1]
    frame = pd.read_csv(root / "outputs" / "score_explanations.csv")
    assert frame["residential_rank"].nunique() == 50
    assert frame["feature"].nunique() == 39
    assert 148016 not in set(frame["unitid"].astype(int))
    assert {119058, 495280, 494685} <= set(frame["unitid"].astype(int))
    seminary = frame[frame["unitid"] == 215813].iloc[0]
    assert str(seminary["finance_from_parent"]).lower() in {"true", "yes", "1"}
    assert int(seminary["finance_parent_unitid"]) == 215798
    ottawa = frame[frame["unitid"] == 464226].iloc[0]
    assert int(ottawa["finance_parent_unitid"]) == 155627
    page = (root / "outputs" / "top50_report.html").read_text(encoding="utf-8")
    assert page.count("Why it ranks here") == 50
    assert page.count("Endowment and enrollment") == 50
    assert page.count("<h3>Library</h3>") == 50
    assert "Federal data: 2023-24 IPEDS" in page
    assert "2022" not in page
    assert "42.273157" not in page
    assert "Insufficient data" not in page
    assert "Left the list" not in page
    assert "finance from parent" not in page
    assert "Principia College" not in page
    libraries = pd.read_csv(root / "outputs" / "top50_libraries.csv")
    assert len(libraries) == 50
    assert set(libraries["physical_books"].astype(str)) != {""}
    assert ((libraries["physical_books"].astype(str) != "")).all()
    assert (libraries["physical_books"].astype(str) != "not reported").all()
    filled = libraries.fillna("").astype(str).apply(lambda col: col.str.strip())
    assert filled["special_collections"].ne("").all()
    has_contact = (
        filled["contact_name"].ne("")
        | filled["contact_email"].ne("")
        | filled["contact_phone"].ne("")
        | filled["fallback_name"].ne("")
        | filled["fallback_email"].ne("")
        | filled["fallback_phone"].ne("")
    )
    assert has_contact.all()
    seminary_books = libraries.loc[libraries["unitid"].astype(int) == 167677].iloc[0]
    assert "172,000" in str(seminary_books["physical_books"])
    davenport = libraries.loc[libraries["unitid"].astype(int) == 169479].iloc[0]
    assert "16,504" in str(davenport["physical_books"])
    assert "2021" in str(davenport["physical_books_source"])
    notes = (root / "outputs" / "score_explanations.md").read_text(encoding="utf-8")
    assert "Saint Vincent Seminary" in notes
    assert "left the residential top 50" not in notes
    assert "Federal data: 2023-24 IPEDS" in notes
