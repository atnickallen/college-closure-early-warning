"""OPEID 8 vs 6-digit FSA root — no silent root shift."""

from college_closure.ids import add_id_keys, normalize_ein, normalize_opeid8, opeid6
import pandas as pd


def test_eight_digit_ipeds_opeid():
    assert normalize_opeid8("00234500") == "00234500"
    assert opeid6("00234500") == "002345"
    assert normalize_opeid8("00234501") == "00234501"
    assert opeid6("00234501") == "002345"


def test_six_digit_fsa_root_is_not_left_padded_to_eight():
    # The bug: zfill(8) on 002345 → 00002345, root 000023.
    assert normalize_opeid8("002345") == "00234500"
    assert opeid6("002345") == "002345"
    assert opeid6(2345) == "002345"
    # IPEDS 00234500 stored as int 234500 (leading zeros dropped)
    assert normalize_opeid8(234500) == "00234500"
    assert opeid6(234500) == "002345"


def test_ein_norm():
    assert normalize_ein("04-2103594") == "042103594"
    assert normalize_ein(None) == ""


def test_add_id_keys():
    df = pd.DataFrame({"unitid": [1], "opeid": ["00234501"], "ein": ["042103594"]})
    out = add_id_keys(df)
    assert out.loc[0, "opeid8"] == "00234501"
    assert out.loc[0, "opeid6"] == "002345"
    assert bool(out.loc[0, "opeid_is_main"]) is False
    assert out.loc[0, "ein_norm"] == "042103594"
