"""Shared codes, labels, and sentinel values for Urban IPEDS extracts."""

from __future__ import annotations

# Urban / IPEDS reserved numeric codes (treat as missing on *measure* columns)
SENTINEL_VALUES = {-1, -2, -3, -1.0, -2.0, -3.0}

CONTROL_LABELS = {
    1: "public",
    2: "private_nonprofit",
    3: "for_profit",
}

SECTOR_LABELS = {
    0: "administrative_unit",
    1: "public_4yr",
    2: "private_nonprofit_4yr",
    3: "for_profit_4yr",
    4: "public_2yr",
    5: "private_nonprofit_2yr",
    6: "for_profit_2yr",
    7: "public_lt2",
    8: "private_nonprofit_lt2",
    9: "for_profit_lt2",
    -1: "unknown_inactive",
}

# Title IV participating / limited-new-participant codes on title_iv_indicator
TITLE_IV_PARTICIPATING = {1, 2, 4, 8}

# Fall-enrollment level_of_study
LEVEL_UNDERGRAD = 1
LEVEL_GRADUATE = 2
LEVEL_FIRST_PROFESSIONAL = 3

LEVEL_PATHS = {
    "undergraduate": 1,
    "graduate": 2,
    "first-professional": 3,
}

# Directory / identity columns — never coerce sentinels on these
IDENTITY_COLUMNS = {
    "unitid",
    "year",
    "opeid",
    "ein",
    "newid",
    "parent_unitid",
    "fips",
    "county_fips",
}

# Finance columns aligned with Kelchen, Ritter & Webber (WP 24-20) constructs:
# tuition dependence, operating margin, liquidity/leverage, endowment.
FINANCE_PANEL_COLUMNS = [
    "rev_tuition_fees_gross",
    "rev_tuition_fees_net",
    "rev_total_current",
    "rev_operating",
    "rev_investment_return",
    "rev_endowment_income",
    "rev_gifts_grants_contracts",
    "exp_total_current",
    "exp_total_salaries",
    "exp_instruc_total",
    "sch_allowances_tuition_fees",
    "sch_grants_institutional",
    "endowment_end",
    "assets",
    "liabilities",
    "assets_net",
    "longterm_debt",
    "income_net",
    "net_position_change",
    "parent_child_flag",
    "parent_unitid",
    "est_fte",
    "rep_fte",
    "calc_fte",
]

DIRECTORY_PANEL_COLUMNS = [
    "unitid",
    "year",
    "inst_name",
    "opeid",
    "ein",
    "state_abbr",
    "city",
    "fips",
    "county_fips",
    "region",
    "inst_control",
    "control",
    "control_label",
    "sector",
    "sector_label",
    "institution_level",
    "is_four_year",
    "degree_granting",
    "title_iv_indicator",
    "title_iv_participating",
    "inst_status",
    "date_closed",
    "newid",
    "year_deleted",
    "hbcu",
    "tribal_college",
    "inst_size",
    "inst_category",
    "inst_system_flag",
    "inst_system_name",
    "primarily_postsecondary",
    "in_risk_model_universe",
]
