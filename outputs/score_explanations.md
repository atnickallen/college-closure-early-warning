# Why the residential top 50 ranks where it does

Score year 2023. The published score is an XGBoost probability on the vintage snapshot. It is an elevated-risk indicator, not a closure probability to quote. Each feature row has the raw value on that snapshot, the year the vintage builder used, the percentile and z-score among the scored vintage universe, the feature's share of global mean |SHAP| (weight), and its TreeSHAP contribution in probability units. Contributions are sorted from the one that raises the score most. Missing values were left missing. The booster follows the missing branch. It does not median-fill. Ratio features on the snapshot were winsorized to the 1st–99th percentile of the feature panel before scoring.

## Suspected data artifacts

None of the top 50 were flagged.

## Principia College

Principia College left the residential top 50 after the extract-year repair. The scored row uses the college's own finance and enrollment years, including the years when title_iv_indicator was 3. That score sits below the 50th school that is still operating, has on-campus housing, and has its own campus. The published score on that filing is 0.046. The IPEDS finance extract has a 2023 filing: endowment_end $592,903,744, revenue $97,015,232, expenses $48,254,224, net tuition $738,933, investment return $77,515,584. Fall headcount was 407 in 2019 and 339 in 2024. FTE was 390 in 2019 and 335 in 2024. Net tuition is about 0.8% of revenue. The investment return is most of reported revenue, so the accounting margin is not an operating surplus. Data USA matches the $593 million IPEDS endowment. The Principia Corporation 990 (EIN 43-0652667) covers the college and the Principia School; the card keeps the college IPEDS line.

## School by school

### 1. Saint Vincent Seminary (PA)

Residential rank 1. Watch-list rank 84. Published risk score 0.753. Federal composite score 3.00 (year 2025.0).

Endowment $146.7 million in 2023 ($1.6 million per FTE). Scope: parent filing. Source: IPEDS finance F2H02/F1H02 for UNITID 215798 (Saint Vincent College), the campus that files in this extract. Fall headcount 79 in 2024 (undergraduate not reported; graduate 79). FTE 89 in 2024. Fall headcount 61 in 2019 versus 79 in 2024 (+30%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract. finance from parent UNITID 215798. The figure is the Saint Vincent College filing, not a separate endowment measured for this campus alone. Enrollment on this card is this campus's own headcount and FTE.

Top drivers:

- finance from parent UNITID 215798
- enrollment is about 89 FTE (2024)
- the composite score was carried forward from an older official year

Missing or imputed:

Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true. | Negative-margin years in the last 5: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Yield rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Tuition is at least 70% of revenue: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Admit rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Discount-rate change, 5 years: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Discount rate: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Operating-margin change, 5 years: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Operating margin: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Tuition share of revenue: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Endowment per FTE: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Net assets per dollar of expense: Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

finance from parent UNITID 215798

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Finance copied from a parent campus | 1 | 2023 | 100.0 | 4.64 | 0.0031 | +1.3734 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 4.489 | 2024 | 13.3 | -1.12 | 0.0797 | +0.5922 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | +0.2474 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Students per staff member | 6.357 | 2024 | 43.5 | -0.37 | 0.0347 | +0.0915 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | 0.5893 | 2024 | 84.1 | 0.37 | 0.0046 | +0.0894 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | +0.0800 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Enrollment change, 5 years | 0.3485 | 2024 | 81.0 | 0.28 | 0.0125 | +0.0702 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | +0.0552 | Reported on the scored row. Not imputed. |
| State high-school graduates, 5-year change | -0.03434 | 2025 | 20.2 | -0.77 | 0.0364 | +0.0538 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0317 | Reported on the scored row. Not imputed. |
| Yield rate |  |  |  |  | 0.0418 | +0.0287 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | +0.0044 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | +0.0027 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | +0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | -0.0002 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | -0.0026 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | -0.0029 | Reported on the scored row. Not imputed. |
| Admit rate |  |  |  |  | 0.0252 | -0.0033 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -0.0054 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | -0.0059 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | -0.0069 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year |  |  |  |  | 0.0119 | -0.0077 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Admit-rate change, 5 years |  |  |  |  | 0.0148 | -0.0088 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Yield-rate change, 5 years |  |  |  |  | 0.0192 | -0.0092 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Discount-rate change, 5 years | -0.02204 | 2023 | 17.0 | -0.51 | 0.0198 | -0.0115 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Staff change, 1 year | 0.07692 | 2024 | 78.9 | 0.25 | 0.0212 | -0.0162 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.5365 | 2023 | 85.6 | 1.24 | 0.0204 | -0.0200 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Student-staff ratio change, 1 year | -0.1044 | 2024 | 38.8 | -0.07 | 0.0080 | -0.0207 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | -0.0234 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0308 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 0.1667 | 2024 | 77.5 | 0.14 | 0.0103 | -0.0457 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.05952 | 2024 | 66.9 | 0.10 | 0.0388 | -0.0718 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.05423 | 2023 | 58.0 | 0.12 | 0.0075 | -0.0915 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Operating margin | 0.1849 | 2023 | 78.0 | 0.56 | 0.0479 | -0.1364 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | -0.1393 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.3365 | 2023 | 20.3 | -0.97 | 0.0405 | -0.2378 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Endowment per FTE | 1.193e+06 | 2023 | 100.0 | 3.91 | 0.1018 | -0.2435 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Net assets per dollar of expense | 4.37 | 2023 | 87.7 | 1.03 | 0.1840 | -0.3923 | Copied from the parent campus finance row UNITID 215798, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Federal composite score | 3 | 2025 | 100.0 | 0.77 | 0.0966 | -0.4567 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 2. Boston Baptist College (MA)

Residential rank 2. Watch-list rank 168. Published risk score 0.617. Federal composite score 0.30 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 164614; endowment_end (F2H02/F1H02) is blank. Fall headcount 43 in 2024 (undergraduate 43; graduate not reported). FTE 16 in 2024. Fall headcount 63 in 2019 versus 43 in 2024 (-32%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- FTE moved from 45 in 2019 to 16 in 2024 (-64%)
- state high-school graduates, 5-year change is -2% (2025)
- enrollment is about 16 FTE (2024)

Missing or imputed:

Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

Five-year FTE change is -64%, an outlier against a typical campus. | The model's five-year enrollment feature is the FTE change (-64%). Fall headcount changed -32% over the years shown on the card. Those are different counts. | This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Enrollment change, 5 years | -0.6444 | 2024 | 4.2 | -1.06 | 0.0125 | +0.4657 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.02415 | 2025 | 26.0 | -0.62 | 0.0364 | +0.4157 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 2.773 | 2024 | 2.1 | -2.15 | 0.0797 | +0.4041 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.7714 | 2024 | 3.6 | -0.97 | 0.0046 | +0.3747 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1 | 2024 | 7.8 | -1.10 | 0.0418 | +0.3565 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.36 | 2024 | 4.6 | -1.59 | 0.0388 | +0.3379 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | +0.3013 | Reported on the scored row. Not imputed. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | +0.2248 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Students per staff member | 5.333 | 2024 | 33.4 | -0.45 | 0.0347 | +0.1794 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | +0.1774 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Discount-rate change, 5 years | 0.26 | 2023 | 97.2 | 2.23 | 0.0198 | +0.1190 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.9091 | 2024 | 75.0 | 0.80 | 0.0252 | +0.1188 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.1529 | 2023 | 12.7 | -0.72 | 0.0479 | +0.1085 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | +0.0801 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.6 | 2024 | 0.4 | -3.62 | 0.0192 | +0.0620 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | +0.0389 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -3 | 2024 | 7.5 | -0.63 | 0.0080 | +0.0384 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0234 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | +0.0079 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | +0.0072 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0018 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | +0.0005 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 1 | 2025 | 100.0 | 4.33 | 0.0000 | +0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | -0.0025 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0038 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | -0.0040 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | -0.0076 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | -0.0076 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | -0.0165 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.1645 | 2023 | 15.2 | -0.69 | 0.0075 | -0.0948 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.26 | 2023 | 55.2 | 0.06 | 0.0204 | -0.1072 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0 | 2024 | 46.6 | -0.13 | 0.0148 | -0.1190 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0 | 2024 | 51.1 | -0.09 | 0.0212 | -0.1642 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | -0.75 | 2024 | 2.7 | -1.71 | 0.0119 | -0.1860 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.5714 | 2024 | 2.9 | -1.05 | 0.0103 | -0.1976 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | -0.2114 | Reported on the scored row. Not imputed. |
| Federal composite score | 0.3 | 2025 | 3.6 | -2.64 | 0.0966 | -0.5077 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Net assets per dollar of expense | 0.2071 | 2023 | 22.9 | -0.80 | 0.1840 | -0.8032 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.3979 | 2023 | 26.5 | -0.76 | 0.0405 | -0.8172 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 3. University of Silicon Valley (CA)

Residential rank 3. Watch-list rank 180. Published risk score 0.596. Federal composite score 1.50 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 112394; endowment_end (F2H02/F1H02) is blank. Fall headcount 477 in 2024 (undergraduate 456; graduate 21). FTE 534 in 2024. Fall headcount 552 in 2019 versus 477 in 2024 (-14%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- the operating margin is -30% (2023)
- yield is 42% (2024)
- net assets cover 0.0 years of expenses (2022)

Missing or imputed:

Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Operating margin | -0.2976 | 2023 | 7.0 | -1.27 | 0.0479 | +0.3829 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.4195 | 2024 | 54.2 | -0.12 | 0.0418 | +0.3264 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | 0 | 2022 | 11.9 | -0.89 | 0.1840 | +0.3159 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | +0.2699 | Reported on the scored row. Not imputed. |
| Students per staff member | 10.27 | 2024 | 65.4 | -0.06 | 0.0347 | +0.2691 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.004182 | 2025 | 46.1 | -0.22 | 0.0364 | +0.2580 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | 0.3273 | 2024 | 86.1 | 0.52 | 0.0119 | +0.2104 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | +0.1614 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Discount-rate change, 5 years | 0.05872 | 2023 | 69.7 | 0.27 | 0.0198 | +0.1561 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | 0.2824 | 2024 | 95.1 | 1.92 | 0.0192 | +0.1264 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.09797 | 2024 | 38.3 | -0.33 | 0.0125 | +0.0825 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.105 | 2023 | 42.7 | -0.60 | 0.0204 | +0.0720 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 33.52 | 2009 | 0.7 | -0.53 | 0.1018 | +0.0619 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 3 | 2025 | 78.7 | 0.03 | 0.0331 | +0.0473 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.1186 | 2024 | 12.9 | -0.61 | 0.0212 | +0.0470 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | +0.0458 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | +0.0366 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0276 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 6.28 | 2024 | 44.4 | -0.04 | 0.0797 | +0.0239 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | +0.0096 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | +0.0006 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 3 | 2025 | 100.0 | 1.48 | 0.0010 | +0.0006 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | +0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | -0.0001 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.009276 | 2024 | 53.1 | -0.22 | 0.0046 | -0.0016 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | -0.0039 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Student-staff ratio change, 1 year | 2.913 | 2024 | 90.4 | 0.52 | 0.0080 | -0.0053 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | -0.0060 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -0.0062 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | -0.0147 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0176 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | -0.0232 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.1133 | 2023 | 20.0 | -0.50 | 0.0075 | -0.0408 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.01831 | 2024 | 52.0 | -0.04 | 0.0148 | -0.0696 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.3333 | 2024 | 10.3 | -0.67 | 0.0103 | -0.1952 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.5 | 2025 | 11.3 | -1.12 | 0.0966 | -0.2355 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.999 | 2023 | 89.0 | 1.26 | 0.0405 | -0.3257 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.5118 | 2024 | 18.6 | -0.89 | 0.0252 | -0.6936 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.2304 | 2024 | 88.6 | 0.79 | 0.0388 | -0.7201 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 4. Central Penn College (PA)

Residential rank 4. Watch-list rank 223. Published risk score 0.537. Federal composite score 2.30 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 211477; endowment_end (F2H02/F1H02) is blank. Fall headcount 684 in 2024 (undergraduate 671; graduate 13). FTE 447 in 2024. Fall headcount 1,054 in 2019 versus 684 in 2024 (-35%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- yield-rate change, 5 years is +39% (2024)
- 5 of the last 5 years show a negative margin
- discount-rate change, 5 years is +9% (2023)

Missing or imputed:

Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Yield-rate change, 5 years | 0.391 | 2024 | 97.0 | 2.61 | 0.0192 | +1.7128 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 5 | 2023 | 100.0 | 2.33 | 0.0338 | +1.4415 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.0867 | 2023 | 80.4 | 0.54 | 0.0198 | +1.1119 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.6934 | 2024 | 5.4 | -0.89 | 0.0046 | +1.1064 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | +0.8323 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 5 years | -0.366 | 2024 | 12.5 | -0.69 | 0.0125 | +0.6970 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | +0.6785 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| First-time enrollment change, 1 year | 0.9787 | 2024 | 94.5 | 1.87 | 0.0119 | +0.5946 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.03434 | 2025 | 20.2 | -0.77 | 0.0364 | +0.2500 | Reported on the scored row. Not imputed. |
| Sector | 3 | 2025 | 78.7 | 0.03 | 0.0331 | +0.1979 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 6.103 | 2024 | 39.8 | -0.15 | 0.0797 | +0.1731 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | +0.1601 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | +0.1599 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.22 | 2024 | 6.2 | -1.05 | 0.0212 | +0.1455 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.1166 | 2024 | 14.5 | -0.61 | 0.0388 | +0.1114 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.1233 | 2023 | 44.1 | -0.52 | 0.0204 | +0.0796 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0360 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 3 | 2025 | 100.0 | 1.48 | 0.0010 | +0.0248 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | +0.0218 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.7358 | 2023 | 59.3 | 0.37 | 0.0405 | +0.0106 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | +0.0015 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | +0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | -0.0004 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | -0.0103 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Admit-rate change, 5 years | -0.4944 | 2024 | 1.7 | -2.68 | 0.0148 | -0.0216 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | -0.0252 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -0.0265 | Reported on the scored row. Not imputed. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | -0.0426 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | -0.0537 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 0.6708 | 2024 | 73.3 | 0.08 | 0.0080 | -0.0857 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 5.731 | 2024 | 37.5 | -0.41 | 0.0347 | -0.0936 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.08931 | 2023 | 17.8 | -0.48 | 0.0479 | -0.1438 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.1475 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.05048 | 2023 | 30.6 | -0.27 | 0.0075 | -0.2866 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.3445 | 2024 | 9.4 | -0.69 | 0.0103 | -0.4269 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.3 | 2025 | 35.3 | -0.11 | 0.0966 | -1.1894 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Admit rate | 0.1846 | 2024 | 4.5 | -2.27 | 0.0252 | -1.6214 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.8341 | 2024 | 80.7 | 1.16 | 0.0418 | -1.6877 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | 1.204 | 2022 | 44.9 | -0.36 | 0.1840 | -3.1700 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 5. Alverno College (WI)

Residential rank 5. Watch-list rank 229. Published risk score 0.529. Federal composite score 2.60 (year 2025.0).

Endowment $36.2 million in 2023 ($29,637 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 238193. Fall headcount 1,317 in 2024 (undergraduate 673; graduate 644). FTE 1,222 in 2024. Fall headcount 1,744 in 2019 versus 1,317 in 2024 (-24%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- the composite score was carried forward from an older official year
- 4 of the last 5 years show a negative margin
- staff change, 1 year is -33% (2024)

Missing or imputed:

Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | +3.9883 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | +2.5035 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.3278 | 2024 | 3.8 | -1.53 | 0.0212 | +2.0881 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.1804 | 2024 | 9.2 | -0.87 | 0.0388 | +1.5864 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1664 | 2024 | 27.4 | -0.90 | 0.0418 | +1.3538 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.02509 | 2025 | 54.4 | 0.07 | 0.0364 | +1.2023 | Reported on the scored row. Not imputed. |
| Operating margin | -0.2844 | 2023 | 7.4 | -1.22 | 0.0479 | +0.8270 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.07402 | 2023 | 75.6 | 0.42 | 0.0198 | +0.6023 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.8574 | 2024 | 65.8 | 0.58 | 0.0252 | +0.5311 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | +0.2109 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | +0.1896 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | +0.1666 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.2541 | 2023 | 8.6 | -1.01 | 0.0075 | +0.0690 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0549 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.1637 | 2024 | 81.4 | 0.71 | 0.0148 | +0.0471 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 7.543 | 2024 | 53.0 | -0.28 | 0.0347 | +0.0312 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | +0.0286 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.4067 | 2024 | 7.5 | -1.00 | 0.0119 | +0.0140 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | +0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | -0.0003 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | -0.0136 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | -0.0165 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -0.0264 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | -0.0395 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.1151 | 2024 | 36.4 | -0.35 | 0.0125 | -0.0448 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | -0.0550 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | -0.0625 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | -0.0691 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.3049 | 2024 | 25.7 | -0.51 | 0.0046 | -0.1030 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.6119 | 2023 | 48.0 | -0.04 | 0.0405 | -0.1507 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 1.356 | 2024 | 81.9 | 0.22 | 0.0080 | -0.1515 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3982 | 2023 | 69.3 | 0.65 | 0.0204 | -0.4039 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.1509 | 2024 | 12.3 | -0.80 | 0.0192 | -0.5822 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.4214 | 2024 | 6.6 | -0.81 | 0.0103 | -0.8233 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | -1.1638 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.6 | 2025 | 51.4 | 0.27 | 0.0966 | -1.6783 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Endowment per FTE | 2.429e+04 | 2023 | 37.6 | -0.44 | 0.1018 | -2.0290 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.108 | 2024 | 66.4 | 0.46 | 0.0797 | -2.1626 | Reported on the scored row. Not imputed. |
| Net assets per dollar of expense | 1.45 | 2023 | 50.5 | -0.25 | 0.1840 | -5.4126 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 6. Spartan College of Aeronautics and Technology (OK)

Residential rank 6. Watch-list rank 249. Published risk score 0.506. Federal composite score -1.00 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 207254; endowment_end (F2H02/F1H02) is blank. Fall headcount 840 in 2024 (undergraduate 840; graduate not reported). FTE 1,184 in 2024. Fall headcount 673 in 2019 versus 840 in 2024 (+25%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- the composite score was carried forward from an older official year
- yield is 50% (2014)
- there are 7.8 students per staff member (2024)

Missing or imputed:

Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | +233.3059 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Yield rate | 0.4981 | 2014 | 58.8 | 0.13 | 0.0418 | +151.2610 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 7.841 | 2024 | 54.6 | -0.25 | 0.0347 | +149.6007 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.03287 | 2023 | 58.0 | 0.02 | 0.0198 | +128.7431 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.2838 | 2014 | 84.1 | 0.43 | 0.0119 | +116.3755 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | +100.2038 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| State high-school graduates, 5-year change | 0.08918 | 2025 | 94.0 | 0.97 | 0.0364 | +83.8389 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | +66.6299 | Reported on the scored row. Not imputed. |
| Sector | 3 | 2025 | 78.7 | 0.03 | 0.0331 | +58.5261 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | +52.9605 | Reported on the scored row. Not imputed. |
| Admit rate | 0.7687 | 2014 | 50.7 | 0.20 | 0.0252 | +51.8213 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.03835 | 2023 | 33.6 | -0.88 | 0.0204 | +50.7858 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.5019 | 2014 | 1.3 | -3.01 | 0.0192 | +47.6148 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +22.5432 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | +20.3402 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.3229 | 2024 | 80.1 | 0.24 | 0.0125 | +18.0231 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 3 | 2025 | 100.0 | 1.48 | 0.0010 | +5.0471 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | +4.4993 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.4352 | 2024 | 80.4 | 0.22 | 0.0046 | +0.5790 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | +0.0263 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 1 | 2025 | 100.0 | 4.33 | 0.0000 | +0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | -0.0276 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -1.0739 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | -1.2418 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -3.5874 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | -3.6780 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | -4.2136 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | -9.0759 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -4.25 | 2024 | 5.5 | -0.87 | 0.0080 | -15.8556 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | -1 | 2025 | 0.9 | -4.29 | 0.0966 | -18.3826 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating-margin change, 5 years | 0.1921 | 2023 | 83.2 | 0.62 | 0.0075 | -19.7241 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.9412 | 2023 | 76.3 | 1.06 | 0.0405 | -38.6651 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | -0.1208 | 2014 | 15.6 | -0.75 | 0.0148 | -55.7701 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.7159 | 2024 | 99.0 | 3.06 | 0.0212 | -77.7961 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.3862 | 2024 | 7.7 | -0.75 | 0.0103 | -81.0128 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.1128 | 2024 | 77.4 | 0.31 | 0.0388 | -176.4098 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | 0.1763 | 2023 | 76.1 | 0.52 | 0.0479 | -208.8777 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.077 | 2024 | 65.5 | 0.44 | 0.0797 | -243.5240 | Reported on the scored row. Not imputed. |
| Net assets per dollar of expense | 0.1801 | 2022 | 21.2 | -0.81 | 0.1840 | -403.3266 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 7. Jacksonville College-Main Campus (TX)

Residential rank 7. Watch-list rank 254. Published risk score 0.499. Federal composite score 1.20 (year 2025.0).

Endowment $1.2 million in 2023 ($3,600 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 225876. Fall headcount 518 in 2024 (undergraduate 518; graduate not reported). FTE 347 in 2024. Fall headcount 476 in 2019 versus 518 in 2024 (+9%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.4 years of expenses (2023)
- endowment covers 0.2 years of expenses, $3,422 per FTE (2023)
- tuition is 47% of revenue (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Admit rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Yield rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.3991 | 2023 | 29.4 | -0.72 | 0.1840 | +12.7421 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 3422 | 2023 | 9.7 | -0.52 | 0.1018 | +6.5930 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.4705 | 2023 | 33.8 | -0.52 | 0.0405 | +3.8709 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.186 | 2024 | 21.8 | -0.43 | 0.0103 | +2.1104 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3007 | 2023 | 59.5 | 0.23 | 0.0204 | +0.8646 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.09399 | 2024 | 44.5 | -0.30 | 0.0046 | +0.5099 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.2 | 2025 | 7.4 | -1.50 | 0.0966 | +0.4652 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 1 year | -0.04932 | 2024 | 27.2 | -0.34 | 0.0388 | +0.4140 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.3754 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.2660 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.05405 | 2024 | 24.9 | -0.32 | 0.0212 | +0.2298 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.04942 | 2024 | 50.1 | -0.04 | 0.0080 | +0.1593 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.1406 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.1359 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years |  |  |  |  | 0.0148 | +0.1176 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Yield-rate change, 5 years |  |  |  |  | 0.0192 | +0.0702 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| First-time enrollment change, 1 year |  |  |  |  | 0.0119 | +0.0559 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0503 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0412 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0015 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating-margin change, 5 years | -0.2546 | 2023 | 8.5 | -1.02 | 0.0075 | -0.0138 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.1184 | Reported on the scored row. Not imputed. |
| Admit rate |  |  |  |  | 0.0252 | -0.2254 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Years in the composite zone | 5 | 2025 | 100.0 | 5.42 | 0.0023 | -0.2543 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 1 | 2025 | 100.0 | 4.81 | 0.0009 | -0.4024 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.4505 | Reported on the scored row. Not imputed. |
| Yield rate |  |  |  |  | 0.0418 | -0.4706 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.5619 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.1237 | 2024 | 35.0 | -0.36 | 0.0125 | -1.1294 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 5 | 2025 | 82.1 | 1.32 | 0.0331 | -1.1774 | Reported on the scored row. Not imputed. |
| Four-year institution | 0 | 2025 | 21.3 | -1.93 | 0.0032 | -1.6417 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -2.1130 | Reported on the scored row. Not imputed. |
| Operating margin | -0.2412 | 2023 | 8.2 | -1.06 | 0.0479 | -2.3767 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 9.914 | 2024 | 64.0 | -0.09 | 0.0347 | -2.4581 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 5.849 | 2024 | 35.1 | -0.30 | 0.0797 | -2.7383 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -3.7874 | Carried forward from the last official composite year. composite_is_lagged is true. |
| State high-school graduates, 5-year change | 0.08271 | 2025 | 92.7 | 0.88 | 0.0364 | -4.2987 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.08536 | 2023 | 80.0 | 0.53 | 0.0198 | -4.5206 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 8. Webster University (MO)

Residential rank 8. Watch-list rank 270. Published risk score 0.481. Federal composite score 2.20 (year 2025.0).

Endowment $66.7 million in 2023 ($10,451 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 179894. Fall headcount 8,260 in 2024 (undergraduate 2,322; graduate 5,938). FTE 6,380 in 2024. Fall headcount 9,860 in 2019 versus 8,260 in 2024 (-16%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.9 years of expenses (2023)
- endowment covers 0.4 years of expenses, $10,745 per FTE (2023)
- enrollment is about 6,380 FTE (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.8666 | 2023 | 37.9 | -0.51 | 0.1840 | +3.8130 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 1.075e+04 | 2023 | 22.2 | -0.49 | 0.1018 | +2.2280 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 8.761 | 2024 | 94.4 | 1.45 | 0.0797 | +1.6691 | Reported on the scored row. Not imputed. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +1.1596 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.2 | 2025 | 32.3 | -0.24 | 0.0966 | +0.9833 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 1 year | 0.0282 | 2024 | 56.7 | -0.03 | 0.0388 | +0.9634 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.2218 | 2023 | 52.4 | -0.10 | 0.0204 | +0.6609 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.789 | 2023 | 64.0 | 0.55 | 0.0405 | +0.6023 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.2788 | 2024 | 12.7 | -0.58 | 0.0103 | +0.3744 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.02667 | 2023 | 50.4 | 0.02 | 0.0075 | +0.2792 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.1962 | 2024 | 8.3 | -1.08 | 0.0192 | +0.2363 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.1704 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 1.373 | 2024 | 82.2 | 0.22 | 0.0080 | +0.1362 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0716 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0547 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0440 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | +0.0337 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0116 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0056 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0047 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0004 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0001 | Reported on the scored row. Not imputed. |
| Operating margin | -0.1318 | 2023 | 14.0 | -0.65 | 0.0479 | -0.0167 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0319 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.1050 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.06342 | 2024 | 43.1 | -0.28 | 0.0125 | -0.1094 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.4224 | 2024 | 16.4 | -0.62 | 0.0046 | -0.1725 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.2440 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.09375 | 2024 | 16.0 | -0.50 | 0.0212 | -0.4561 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.8623 | 2024 | 66.8 | 0.60 | 0.0252 | -0.5024 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.2935 | 2024 | 91.7 | 1.38 | 0.0148 | -0.5104 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.02616 | 2025 | 57.1 | 0.09 | 0.0364 | -0.7415 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.01981 | 2023 | 49.1 | -0.11 | 0.0198 | -0.7446 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 11.58 | 2024 | 69.5 | 0.04 | 0.0347 | -0.8481 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.354 | 2024 | 87.6 | 0.57 | 0.0119 | -0.9590 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1363 | 2024 | 19.5 | -0.99 | 0.0418 | -1.0623 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -2.2556 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -4.2851 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 9. Montserrat College of Art (MA)

Residential rank 9. Watch-list rank 283. Published risk score 0.466. Federal composite score 2.50 (year 2025.0).

Endowment $3.1 million in 2023 ($13,368 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 166911. Fall headcount 227 in 2024 (undergraduate 227; graduate not reported). FTE 233 in 2024. Fall headcount 374 in 2019 versus 227 in 2024 (-39%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.7 years of expenses (2023)
- endowment covers 0.3 years of expenses, $10,314 per FTE (2023)
- the federal composite score is 2.50 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.6686 | 2023 | 34.2 | -0.60 | 0.1840 | +2.6134 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 1.031e+04 | 2023 | 21.4 | -0.49 | 0.1018 | +1.4317 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.5 | 2025 | 46.4 | 0.14 | 0.0966 | +1.2242 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.5243 | Reported on the scored row. Not imputed. |
| Discount rate | 0.4597 | 2023 | 76.4 | 0.91 | 0.0204 | +0.3501 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.1569 | 2024 | 76.4 | 0.12 | 0.0103 | +0.2529 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.1443 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.5961 | 2023 | 46.2 | -0.10 | 0.0405 | +0.0910 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year |  | 2005 |  |  | 0.0119 | +0.0888 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Students per staff member | 3.949 | 2024 | 18.7 | -0.55 | 0.0347 | +0.0790 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0700 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0570 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0387 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years |  | 2005 |  |  | 0.0192 | +0.0333 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Admit-rate change, 5 years |  | 2005 |  |  | 0.0148 | +0.0224 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0222 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0201 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0090 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0084 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0045 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Staff change, 1 year | -0.03279 | 2024 | 30.8 | -0.23 | 0.0212 | -0.0025 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0142 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -1.002 | 2024 | 17.3 | -0.24 | 0.0080 | -0.0271 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.3009 | 2023 | 7.1 | -1.19 | 0.0075 | -0.0452 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0960 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.4071 | 2024 | 17.7 | -0.61 | 0.0046 | -0.1378 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.8502 | 2005 | 64.4 | 0.55 | 0.0252 | -0.1492 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.2080 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.3564 | 2024 | 13.2 | -0.68 | 0.0125 | -0.4601 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 5.451 | 2024 | 28.5 | -0.54 | 0.0797 | -0.5007 | Reported on the scored row. Not imputed. |
| Operating margin | -0.2314 | 2023 | 8.6 | -1.02 | 0.0479 | -0.5029 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.07215 | 2023 | 74.7 | 0.40 | 0.0198 | -0.6009 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.02415 | 2025 | 26.0 | -0.62 | 0.0364 | -0.6993 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.7287 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.7355 | Reported on the scored row. Not imputed. |
| Yield rate | 0.277 | 2005 | 43.8 | -0.56 | 0.0418 | -0.8668 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.2285 | 2024 | 7.1 | -1.06 | 0.0388 | -0.8681 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 10. San Diego Christian College (CA)

Residential rank 10. Watch-list rank 294. Published risk score 0.452. Federal composite score 0.50 (year 2025.0).

Endowment $694,522 in 2023 ($6,945 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 112084. Fall headcount 96 in 2024 (undergraduate 89; graduate 7). FTE 100 in 2024. Fall headcount 551 in 2019 versus 96 in 2024 (-83%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- endowment covers 0.1 years of expenses, $8,171 per FTE (2023)
- FTE enrollment changed +18% in one year (2024)
- the federal composite score is 0.50 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

Five-year FTE change is -81%, an outlier against a typical campus.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Endowment per FTE | 8171 | 2023 | 17.8 | -0.50 | 0.1018 | +1.0144 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.1765 | 2024 | 84.8 | 0.57 | 0.0388 | +0.9189 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 0.5 | 2025 | 3.9 | -2.39 | 0.0966 | +0.8064 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.3849 | 2023 | 24.8 | -0.80 | 0.0405 | +0.7197 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.3081 | 2024 | 7.5 | -1.75 | 0.0252 | +0.4807 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.3017 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.1845 | 2024 | 9.6 | -1.01 | 0.0192 | +0.2228 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.6667 | 2024 | 1.7 | -1.20 | 0.0103 | +0.1995 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3083 | 2023 | 60.0 | 0.27 | 0.0204 | +0.1426 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | -0.2444 | 2024 | 7.2 | -1.39 | 0.0148 | +0.0626 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0 | 2024 | 51.4 | -0.16 | 0.0119 | +0.0626 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.1111 | 2024 | 14.1 | -0.57 | 0.0212 | +0.0417 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0349 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 1.528 | 2024 | 83.7 | 0.25 | 0.0080 | +0.0305 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0178 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0159 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0146 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0116 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0061 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0006 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0002 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 1 | 2025 | 100.0 | 4.33 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | -0.0049 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0119 | Reported on the scored row. Not imputed. |
| Students per staff member | 6.25 | 2024 | 42.6 | -0.37 | 0.0347 | -0.0426 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.2551 | 2023 | 8.3 | -1.02 | 0.0075 | -0.0643 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0689 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0813 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0834 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.004192 | 2023 | 37.7 | -0.26 | 0.0198 | -0.1352 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.2005 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.2255 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 10 years | -0.8888 | 2024 | 2.0 | -1.08 | 0.0046 | -0.2299 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | -0.371 | 2023 | 0.4 | -1.05 | 0.1840 | -0.2909 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.004182 | 2025 | 46.1 | -0.22 | 0.0364 | -0.4241 | Reported on the scored row. Not imputed. |
| Operating margin | -0.4664 | 2023 | 4.3 | -1.91 | 0.0479 | -0.4877 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.8141 | 2024 | 2.2 | -1.29 | 0.0125 | -0.6153 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1579 | 2024 | 25.3 | -0.92 | 0.0418 | -0.6767 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 4.605 | 2024 | 14.6 | -1.05 | 0.0797 | -1.0341 | Reported on the scored row. Not imputed. |

### 11. Roosevelt University (IL)

Residential rank 11. Watch-list rank 299. Published risk score 0.447. Federal composite score 1.90 (year 2025.0).

Endowment $152.8 million in 2023 ($42,128 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 148487. Fall headcount 4,281 in 2024 (undergraduate 2,868; graduate 1,413). FTE 3,627 in 2024. Fall headcount 4,071 in 2019 versus 4,281 in 2024 (+5%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- endowment covers 1.3 years of expenses, $45,060 per FTE (2023)
- net assets cover 1.0 years of expenses (2023)
- sector is 2 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

The model's five-year enrollment feature is the FTE change (-28%). Fall headcount changed +5% over the years shown on the card. Those are different counts.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Endowment per FTE | 4.506e+04 | 2023 | 53.4 | -0.37 | 0.1018 | +1.6214 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | 1.033 | 2023 | 41.1 | -0.44 | 0.1840 | +1.5409 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.4227 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.6338 | 2023 | 49.8 | 0.03 | 0.0405 | +0.4181 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.0696 | 2024 | 69.1 | 0.14 | 0.0388 | +0.3628 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.05797 | 2024 | 73.6 | 0.17 | 0.0212 | +0.2850 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.9 | 2025 | 20.9 | -0.62 | 0.0966 | +0.2611 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Staff change, 5 years | -0.1128 | 2024 | 31.7 | -0.31 | 0.0103 | +0.1632 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.05747 | 2023 | 21.6 | -0.36 | 0.0479 | +0.1387 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 8.196 | 2024 | 89.7 | 1.11 | 0.0797 | +0.1152 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | 0.09319 | 2023 | 68.1 | 0.26 | 0.0075 | +0.1050 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3314 | 2023 | 62.1 | 0.36 | 0.0204 | +0.1005 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.07714 | 2024 | 52.1 | -0.03 | 0.0080 | +0.0936 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.222 | 2024 | 32.1 | -0.43 | 0.0046 | +0.0771 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.05167 | 2024 | 62.1 | -0.05 | 0.0119 | +0.0757 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0253 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0160 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0143 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0137 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0134 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0059 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0009 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0004 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0027 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0090 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.003818 | 2024 | 62.7 | 0.12 | 0.0192 | -0.0260 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0377 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0597 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0957 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.03601 | 2023 | 59.6 | 0.05 | 0.0198 | -0.1605 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 7.098 | 2024 | 49.9 | -0.31 | 0.0347 | -0.1930 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.2986 | 2024 | 91.9 | 1.40 | 0.0148 | -0.2405 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.08744 | 2024 | 5.1 | -1.14 | 0.0418 | -0.3469 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.2759 | 2024 | 18.8 | -0.57 | 0.0125 | -0.3606 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.9716 | 2024 | 85.3 | 1.07 | 0.0252 | -0.4736 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.8753 | Reported on the scored row. Not imputed. |
| State high-school graduates, 5-year change | -0.0394 | 2025 | 14.2 | -0.84 | 0.0364 | -1.0607 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -1.5050 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 12. Middlebury Institute of International Studies at Monterey (CA)

Residential rank 12. Watch-list rank 311. Published risk score 0.443. Federal composite score missing.

Endowment $1.60 billion in 2023 ($2.9 million per FTE). Scope: parent filing. Source: IPEDS finance F2H02/F1H02 for UNITID 230959 (Middlebury College), the campus that files in this extract. Fall headcount 526 in 2024 (undergraduate 12; graduate 514). FTE 555 in 2024. Fall headcount 688 in 2019 versus 526 in 2024 (-24%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract. finance from parent UNITID 230959. The figure is the Middlebury College filing, not a separate endowment measured for this campus alone. Enrollment on this card is this campus's own headcount and FTE.

Top drivers:

- endowment covers 4.9 years of expenses, $1.2 million per FTE (2023)
- net assets cover 5.2 years of expenses (2023)
- sector is 2 (2025)

Missing or imputed:

Endowment per FTE: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Net assets per dollar of expense: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Operating-margin change, 5 years: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Operating margin: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Discount-rate change, 5 years: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Tuition share of revenue: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Discount rate: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Tuition is at least 70% of revenue: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Yield rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Federal composite score: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Negative-margin years in the last 5: Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count.

Data-quality flags:

finance from parent UNITID 230959

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Endowment per FTE | 1.193e+06 | 2023 | 100.0 | 3.91 | 0.1018 | +1.5906 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Net assets per dollar of expense | 5.201 | 2023 | 91.3 | 1.39 | 0.1840 | +1.3088 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.4736 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.07512 | 2023 | 26.2 | -0.36 | 0.0075 | +0.3630 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Enrollment change, 1 year | 0.00726 | 2024 | 46.7 | -0.11 | 0.0388 | +0.3057 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 3.265 | 2024 | 13.6 | -0.60 | 0.0347 | +0.2455 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.03328 | 2023 | 26.1 | -0.27 | 0.0479 | +0.2301 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Staff change, 5 years | -0.07104 | 2024 | 38.8 | -0.25 | 0.0103 | +0.2155 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.02204 | 2023 | 50.4 | -0.08 | 0.0198 | +0.1473 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Tuition share of revenue | 0.5807 | 2023 | 45.1 | -0.15 | 0.0405 | +0.1451 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Staff change, 1 year | -0.02299 | 2024 | 33.8 | -0.19 | 0.0212 | +0.1250 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3335 | 2023 | 62.4 | 0.37 | 0.0204 | +0.1052 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0976 | Reported on the scored row. Not imputed. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0617 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 0.09804 | 2024 | 53.5 | -0.03 | 0.0080 | +0.0298 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0248 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years |  |  |  |  | 0.0148 | +0.0245 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Yield-rate change, 5 years |  |  |  |  | 0.0192 | +0.0234 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0197 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year |  |  |  |  | 0.0119 | +0.0081 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Admit rate |  |  |  |  | 0.0252 | +0.0079 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0056 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 0 | 2025 | 20.2 | -1.99 | 0.0026 | +0.0040 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0009 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0005 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Composite below 1.0 |  |  |  |  | 0.0000 | -0.0000 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.3478 | 2024 | 22.5 | -0.55 | 0.0046 | -0.0047 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0126 | Reported on the scored row. Not imputed. |
| Yield rate |  |  |  |  | 0.0418 | -0.0382 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Composite in the 1.0–1.5 zone |  |  |  |  | 0.0009 | -0.0444 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0527 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.1011 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.2346 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.3106 | 2024 | 16.3 | -0.61 | 0.0125 | -0.2934 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.004182 | 2025 | 46.1 | -0.22 | 0.0364 | -0.3526 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 6.319 | 2024 | 45.3 | -0.02 | 0.0797 | -0.3997 | Reported on the scored row. Not imputed. |
| Federal composite score |  |  |  |  | 0.0966 | -0.4346 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.4556 | Copied from the parent campus finance row UNITID 230959, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Finance copied from a parent campus | 1 | 2023 | 100.0 | 4.64 | 0.0031 | -2.7200 | Reported on the scored row. Not imputed. |

### 13. Niagara University (NY)

Residential rank 13. Watch-list rank 327. Published risk score 0.430. Federal composite score 2.50 (year 2025.0).

Endowment $100.3 million in 2023 ($24,745 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 193973. Fall headcount 4,033 in 2024 (undergraduate 2,692; graduate 1,341). FTE 4,053 in 2024. Fall headcount 3,723 in 2019 versus 4,033 in 2024 (+8%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.8 years of expenses (2023)
- the federal composite score is 2.50 (2025)
- endowment covers 0.9 years of expenses, $23,811 per FTE (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.8 | 2023 | 57.5 | -0.10 | 0.1840 | +1.0562 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.5 | 2025 | 46.4 | 0.14 | 0.0966 | +0.5405 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Endowment per FTE | 2.381e+04 | 2023 | 37.1 | -0.45 | 0.1018 | +0.3628 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.5817 | 2023 | 45.2 | -0.14 | 0.0405 | +0.3591 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.3139 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.03775 | 2024 | 30.2 | -0.29 | 0.0388 | +0.2297 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.4833 | 2023 | 79.7 | 1.01 | 0.0204 | +0.1983 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.04508 | 2023 | 23.7 | -0.32 | 0.0479 | +0.1871 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.04638 | 2024 | 41.9 | -0.14 | 0.0192 | +0.1505 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 8.307 | 2024 | 91.4 | 1.18 | 0.0797 | +0.1048 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | -0.01836 | 2024 | 38.0 | -0.23 | 0.0148 | +0.0984 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.02664 | 2024 | 58.1 | -0.09 | 0.0103 | +0.0984 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.3472 | 2024 | 64.7 | 0.02 | 0.0080 | +0.0602 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0601 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.08103 | 2024 | 32.6 | -0.33 | 0.0119 | +0.0522 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.02264 | 2023 | 49.3 | 0.00 | 0.0075 | +0.0442 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0203 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0183 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.09128 | 2024 | 62.0 | -0.12 | 0.0046 | +0.0178 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0157 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0065 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0052 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0040 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0034 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0003 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0109 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0263 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0686 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.1401 | 2024 | 69.2 | -0.00 | 0.0125 | -0.0697 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.07904 | 2024 | 19.2 | -0.43 | 0.0212 | -0.1110 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.8737 | 2024 | 68.6 | 0.65 | 0.0252 | -0.1527 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.0002345 | 2023 | 31.1 | -0.30 | 0.0198 | -0.1979 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 8.09 | 2024 | 55.4 | -0.23 | 0.0347 | -0.2488 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1454 | 2024 | 22.6 | -0.96 | 0.0418 | -0.2514 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.0524 | 2025 | 10.1 | -1.02 | 0.0364 | -0.5840 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.6076 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -1.2729 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 14. Monroe University (NY)

Residential rank 14. Watch-list rank 331. Published risk score 0.426. Federal composite score 2.40 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 193308; endowment_end (F2H02/F1H02) is blank. Fall headcount 8,141 in 2024 (undergraduate 6,205; graduate 1,936). FTE 9,676 in 2024. Fall headcount 6,517 in 2019 versus 8,141 in 2024 (+25%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.0 years of expenses (2022)
- the federal composite score is 2.40 (2025)
- the operating margin is +6% (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.001 | 2022 | 40.4 | -0.45 | 0.1840 | +1.0657 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.4 | 2025 | 41.1 | 0.01 | 0.0966 | +0.6872 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | 0.06386 | 2023 | 50.6 | 0.10 | 0.0479 | +0.4151 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.0224 | 2024 | 54.0 | -0.05 | 0.0388 | +0.2439 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.1477 | 2024 | 87.6 | 0.56 | 0.0212 | +0.1473 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.2337 | 2023 | 53.1 | -0.05 | 0.0204 | +0.1463 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 9.177 | 2024 | 96.6 | 1.70 | 0.0797 | +0.1089 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.9672 | 2023 | 79.3 | 1.15 | 0.0405 | +0.0930 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -2.062 | 2024 | 10.3 | -0.45 | 0.0080 | +0.0731 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.03047 | 2024 | 59.1 | -0.08 | 0.0103 | +0.0713 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.0622 | 2023 | 60.3 | 0.15 | 0.0075 | +0.0639 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.03319 | 2024 | 58.6 | -0.09 | 0.0119 | +0.0516 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.0416 | 2024 | 50.0 | -0.25 | 0.0046 | +0.0460 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0163 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0147 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0075 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0041 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0023 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 3 | 2025 | 100.0 | 1.48 | 0.0010 | -0.0013 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0030 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0062 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | 0.03098 | 2024 | 75.7 | 0.34 | 0.0192 | -0.0064 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.1952 | 2024 | 84.9 | 0.87 | 0.0148 | -0.0338 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | 0.1485 | 2024 | 69.9 | 0.01 | 0.0125 | -0.0378 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0424 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0504 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0592 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0821 | Reported on the scored row. Not imputed. |
| Sector | 3 | 2025 | 78.7 | 0.03 | 0.0331 | -0.0934 | Reported on the scored row. Not imputed. |
| Admit rate | 0.6751 | 2024 | 34.7 | -0.19 | 0.0252 | -0.1428 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.1546 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Yield rate | 0.4316 | 2024 | 55.1 | -0.08 | 0.0418 | -0.1851 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.002746 | 2023 | 27.0 | -0.33 | 0.0198 | -0.2496 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 16.83 | 2024 | 82.7 | 0.44 | 0.0347 | -0.2508 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.0524 | 2025 | 10.1 | -1.02 | 0.0364 | -0.4866 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.9695 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 15. Salem University (WV)

Residential rank 15. Watch-list rank 354. Published risk score 0.406. Federal composite score 1.60 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 237783; endowment_end (F2H02/F1H02) is blank. Fall headcount 1,083 in 2024 (undergraduate 892; graduate 191). FTE 1,007 in 2024. Fall headcount 960 in 2019 versus 1,083 in 2024 (+13%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.2 years of expenses (2022)
- enrollment is about 1,007 FTE (2024)
- tuition is 90% of revenue (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Admit rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.1856 | 2022 | 22.2 | -0.81 | 0.1840 | +0.4574 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.915 | 2024 | 61.3 | 0.34 | 0.0797 | +0.2926 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.8953 | 2023 | 71.5 | 0.91 | 0.0405 | +0.2686 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.05005 | 2024 | 64.4 | 0.06 | 0.0388 | +0.2542 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.6 | 2025 | 13.3 | -1.00 | 0.0966 | +0.2403 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 1 | 2025 | 100.0 | 3.91 | 0.0030 | +0.1155 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | -0.1667 | 2024 | 23.9 | -0.40 | 0.0103 | +0.0649 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0527 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 1.43 | 2024 | 82.9 | 0.23 | 0.0080 | +0.0454 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0385 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.5374 | 2024 | 82.7 | 0.32 | 0.0046 | +0.0354 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | +0.0260 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0134 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.0991 | 2024 | 15.5 | -0.52 | 0.0212 | +0.0121 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year |  |  |  |  | 0.0119 | +0.0115 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Admit-rate change, 5 years |  |  |  |  | 0.0148 | +0.0092 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0088 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years |  |  |  |  | 0.0192 | +0.0087 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0069 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.1469 | 2024 | 69.8 | 0.01 | 0.0125 | +0.0054 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0024 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating-margin change, 5 years | -0.2083 | 2023 | 11.4 | -0.85 | 0.0075 | +0.0018 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0013 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 3 | 2025 | 100.0 | 1.48 | 0.0010 | -0.0004 | Reported on the scored row. Not imputed. |
| Admit rate |  |  |  |  | 0.0252 | -0.0124 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Discount rate | 0.1389 | 2023 | 45.2 | -0.45 | 0.0204 | -0.0196 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 3 | 2025 | 78.7 | 0.03 | 0.0331 | -0.0511 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0574 | Reported on the scored row. Not imputed. |
| Yield rate |  |  |  |  | 0.0418 | -0.0626 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Operating margin | -0.1614 | 2023 | 11.8 | -0.76 | 0.0479 | -0.0771 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 10.07 | 2024 | 64.8 | -0.08 | 0.0347 | -0.1432 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.1619 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Discount-rate change, 5 years | -0.03136 | 2023 | 13.7 | -0.60 | 0.0198 | -0.1707 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.008648 | 2025 | 28.6 | -0.41 | 0.0364 | -0.2143 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.2850 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.3345 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 16. Hawaii Pacific University (HI)

Residential rank 16. Watch-list rank 358. Published risk score 0.403. Federal composite score 2.00 (year 2025.0).

Endowment $51.4 million in 2023 ($13,929 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 141644. Fall headcount 4,921 in 2024 (undergraduate 3,533; graduate 1,388). FTE 3,690 in 2024. Fall headcount 4,170 in 2019 versus 4,921 in 2024 (+18%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.6 years of expenses (2023)
- endowment covers 0.5 years of expenses, $15,131 per FTE (2023)
- the operating margin is -1% (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.567 | 2023 | 32.3 | -0.64 | 0.1840 | +0.6516 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 1.513e+04 | 2023 | 28.4 | -0.48 | 0.1018 | +0.4051 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.009909 | 2023 | 30.4 | -0.18 | 0.0479 | +0.2207 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.2047 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | 0.08625 | 2024 | 73.5 | 0.20 | 0.0388 | +0.1907 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2 | 2025 | 22.8 | -0.49 | 0.0966 | +0.1905 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.677 | 2023 | 53.8 | 0.18 | 0.0405 | +0.1595 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.03942 | 2024 | 66.8 | 0.09 | 0.0212 | +0.1538 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 8.213 | 2024 | 89.9 | 1.12 | 0.0797 | +0.1399 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 0.1651 | 2024 | 76.9 | 0.13 | 0.0103 | +0.1313 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.09588 | 2024 | 20.9 | -0.46 | 0.0192 | +0.0809 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.3176 | 2024 | 63.7 | 0.01 | 0.0080 | +0.0506 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | -0.1436 | 2024 | 21.9 | -0.46 | 0.0119 | +0.0226 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.1277 | 2023 | 74.0 | 0.39 | 0.0075 | +0.0211 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3561 | 2023 | 64.9 | 0.47 | 0.0204 | +0.0203 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0202 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.1596 | 2024 | 38.3 | -0.36 | 0.0046 | +0.0158 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0132 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0108 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0030 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0024 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.1104 | 2024 | 73.7 | 0.44 | 0.0148 | +0.0023 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0013 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0002 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0052 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0052 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0100 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0219 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.1981 | 2024 | 73.6 | 0.07 | 0.0125 | -0.0368 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0499 | Reported on the scored row. Not imputed. |
| Students per staff member | 7.365 | 2024 | 51.6 | -0.29 | 0.0347 | -0.0785 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.8587 | 2024 | 66.2 | 0.59 | 0.0252 | -0.1025 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.01686 | 2023 | 47.1 | -0.14 | 0.0198 | -0.1404 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.08347 | 2024 | 4.7 | -1.15 | 0.0418 | -0.1970 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.01998 | 2025 | 26.8 | -0.56 | 0.0364 | -0.3326 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.4774 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.8754 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 17. Davenport University (MI)

Residential rank 17. Watch-list rank 361. Published risk score 0.400. Federal composite score 2.30 (year 2025.0).

Endowment $32.0 million in 2023 ($9,234 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 169479. Fall headcount 4,815 in 2024 (undergraduate 3,741; graduate 1,074). FTE 3,465 in 2024. Fall headcount 6,429 in 2019 versus 4,815 in 2024 (-25%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.3 years of expenses (2023)
- endowment covers 0.4 years of expenses, $9,142 per FTE (2023)
- the federal composite score is 2.30 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.328 | 2023 | 47.7 | -0.31 | 0.1840 | +0.6799 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 9142 | 2023 | 19.7 | -0.50 | 0.1018 | +0.4033 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.3 | 2025 | 35.3 | -0.11 | 0.0966 | +0.2395 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | -0.02069 | 2023 | 27.9 | -0.22 | 0.0479 | +0.1950 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1942 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 8.15 | 2024 | 89.0 | 1.08 | 0.0797 | +0.1733 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.01 | 2024 | 38.6 | -0.18 | 0.0388 | +0.1593 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.007833 | 2024 | 53.3 | -0.05 | 0.0212 | +0.1421 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.7465 | 2023 | 60.2 | 0.41 | 0.0405 | +0.1106 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.1975 | 2023 | 50.8 | -0.20 | 0.0204 | +0.0999 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.1647 | 2024 | 11.4 | -0.89 | 0.0192 | +0.0700 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.1734 | 2024 | 23.0 | -0.41 | 0.0103 | +0.0534 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -0.1617 | 2024 | 35.7 | -0.08 | 0.0080 | +0.0532 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.01537 | 2023 | 47.5 | -0.03 | 0.0075 | +0.0432 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0326 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.01022 | 2024 | 46.7 | -0.18 | 0.0119 | +0.0280 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0135 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0124 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0088 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0038 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0029 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0025 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0054 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0091 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.1591 | 2024 | 80.9 | 0.69 | 0.0148 | -0.0116 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.3941 | 2024 | 18.7 | -0.59 | 0.0046 | -0.0254 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0281 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0456 | Reported on the scored row. Not imputed. |
| Admit rate | 0.9784 | 2024 | 86.1 | 1.09 | 0.0252 | -0.0975 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.2426 | 2024 | 21.9 | -0.52 | 0.0125 | -0.1018 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.01363 | 2023 | 45.2 | -0.17 | 0.0198 | -0.1334 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 8.977 | 2024 | 60.0 | -0.16 | 0.0347 | -0.1615 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1352 | 2024 | 18.9 | -0.99 | 0.0418 | -0.2093 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.02716 | 2025 | 22.8 | -0.67 | 0.0364 | -0.2342 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.4331 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.8483 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 18. Post University (CT)

Residential rank 18. Watch-list rank 365. Published risk score 0.399. Federal composite score 2.10 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 130183; endowment_end (F2H02/F1H02) is blank. Fall headcount 16,178 in 2024 (undergraduate 14,116; graduate 2,062). FTE 14,766 in 2024. Fall headcount 10,642 in 2019 versus 16,178 in 2024 (+52%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- the federal composite score is 2.10 (2025)
- the operating margin is +3% (2023)
- 0 of the last 5 years show a negative margin

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

Five-year FTE change is +53%, an outlier against a typical campus. | For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Federal composite score | 2.1 | 2025 | 24.5 | -0.36 | 0.0966 | +0.3493 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | 0.03099 | 2023 | 42.4 | -0.03 | 0.0479 | +0.2966 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 0 | 2023 | 27.5 | -1.14 | 0.0338 | +0.2170 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 9.6 | 2024 | 98.1 | 1.96 | 0.0797 | +0.1976 | Reported on the scored row. Not imputed. |
| Students per staff member | 31.62 | 2024 | 95.8 | 1.59 | 0.0347 | +0.1575 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | 0.1307 | 2022 | 19.9 | -0.83 | 0.1840 | +0.1344 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.04966 | 2019 | 39.5 | -0.16 | 0.0192 | +0.1314 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.04705 | 2024 | 27.8 | -0.33 | 0.0388 | +0.0862 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.02218 | 2023 | 37.7 | -0.16 | 0.0075 | +0.0845 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | 0.533 | 2024 | 86.3 | 0.53 | 0.0125 | +0.0494 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.9435 | 2023 | 76.7 | 1.07 | 0.0405 | +0.0483 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | 1.579 | 2024 | 92.7 | 1.34 | 0.0046 | +0.0282 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.09472 | 2019 | 70.6 | 0.35 | 0.0148 | +0.0187 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0182 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | -0.2332 | 2024 | 16.8 | -0.51 | 0.0103 | +0.0148 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.06762 | 2023 | 38.9 | -0.76 | 0.0204 | +0.0135 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0105 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0092 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | +0.0038 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0022 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0017 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 3 | 2025 | 100.0 | 1.48 | 0.0010 | -0.0010 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0070 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 14.74 | 2024 | 98.8 | 2.81 | 0.0080 | -0.0154 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0330 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0360 | Reported on the scored row. Not imputed. |
| Sector | 3 | 2025 | 78.7 | 0.03 | 0.0331 | -0.0509 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0567 | Reported on the scored row. Not imputed. |
| Admit rate | 0.9654 | 2019 | 84.8 | 1.04 | 0.0252 | -0.0667 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.0769 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Yield rate | 0.4164 | 2019 | 54.1 | -0.13 | 0.0418 | -0.1286 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.2386 | 2019 | 81.9 | 0.34 | 0.0119 | -0.1307 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.01632 | 2025 | 50.3 | -0.05 | 0.0364 | -0.1442 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | -0.07746 | 2023 | 7.2 | -1.05 | 0.0198 | -0.1740 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.4913 | 2024 | 1.6 | -2.25 | 0.0212 | -0.2648 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.3118 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 19. Wheeling University (WV)

Residential rank 19. Watch-list rank 368. Published risk score 0.398. Federal composite score 1.90 (year 2025.0).

Endowment $4.6 million in 2023 ($6,508 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 238078. Fall headcount 774 in 2024 (undergraduate 619; graduate 155). FTE 707 in 2024. Fall headcount 798 in 2019 versus 774 in 2024 (-3%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.3 years of expenses (2023)
- endowment covers 0.2 years of expenses, $6,972 per FTE (2023)
- tuition is 42% of revenue (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.3456 | 2023 | 27.6 | -0.74 | 0.1840 | +0.5656 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 6972 | 2023 | 15.5 | -0.51 | 0.1018 | +0.3661 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.4192 | 2023 | 28.3 | -0.69 | 0.0405 | +0.2394 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.07121 | 2024 | 69.7 | 0.14 | 0.0388 | +0.1714 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1510 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | -0.1719 | 2024 | 23.1 | -0.41 | 0.0103 | +0.1037 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.5754 | 2023 | 89.4 | 1.40 | 0.0204 | +0.0989 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.6316 | 2024 | 29.3 | -0.38 | 0.0252 | +0.0757 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.2184 | 2024 | 91.8 | 0.87 | 0.0212 | +0.0687 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.9 | 2025 | 20.9 | -0.62 | 0.0966 | +0.0530 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Admit-rate change, 5 years | -0.05091 | 2024 | 27.9 | -0.39 | 0.0148 | +0.0496 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.05882 | 2024 | 62.9 | -0.04 | 0.0119 | +0.0165 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -0.9164 | 2024 | 18.2 | -0.22 | 0.0080 | +0.0141 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0129 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0092 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0082 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0078 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0066 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0057 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0028 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0026 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0011 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.2284 | 2023 | 10.1 | -0.92 | 0.0075 | -0.0031 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0047 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.1686 | 2024 | 71.3 | 0.04 | 0.0125 | -0.0169 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0289 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0355 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.4238 | 2024 | 16.4 | -0.62 | 0.0046 | -0.0355 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 6.67 | 2024 | 46.5 | -0.34 | 0.0347 | -0.0447 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.561 | 2024 | 51.2 | 0.13 | 0.0797 | -0.0876 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.009186 | 2024 | 60.5 | 0.09 | 0.0192 | -0.0914 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 2 | 2023 | 73.1 | 0.25 | 0.0338 | -0.1003 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.08887 | 2023 | 81.2 | 0.56 | 0.0198 | -0.1947 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1019 | 2024 | 8.4 | -1.09 | 0.0418 | -0.2084 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.008648 | 2025 | 28.6 | -0.41 | 0.0364 | -0.2259 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.2439 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | -0.3227 | 2023 | 6.3 | -1.37 | 0.0479 | -0.3324 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 20. Talladega College (AL)

Residential rank 20. Watch-list rank 383. Published risk score 0.382. Federal composite score 3.00 (year 2025.0).

Endowment $2.6 million in 2023 ($3,790 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 102298. Fall headcount 760 in 2024 (undergraduate 701; graduate 59). FTE 692 in 2024. Fall headcount 1,239 in 2019 versus 760 in 2024 (-39%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 2.3 years of expenses (2023)
- the federal composite score is 3.00 (2025)
- endowment covers 0.1 years of expenses, $3,032 per FTE (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 2.334 | 2023 | 67.9 | 0.14 | 0.1840 | +0.7364 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 3 | 2025 | 100.0 | 0.77 | 0.0966 | +0.4310 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Endowment per FTE | 3032 | 2023 | 9.1 | -0.52 | 0.1018 | +0.3334 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.2049 | 2023 | 10.3 | -1.41 | 0.0405 | +0.3189 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1372 | Reported on the scored row. Not imputed. |
| Discount rate | 0.6019 | 2023 | 91.9 | 1.51 | 0.0204 | +0.1171 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0419 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 0.09615 | 2024 | 69.2 | 0.02 | 0.0103 | +0.0331 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0236 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0206 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.4295 | 2023 | 4.4 | -1.66 | 0.0075 | +0.0179 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0140 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0091 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.5142 | 2024 | 82.1 | 0.30 | 0.0046 | +0.0070 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0062 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 0.1328 | 2024 | 55.4 | -0.02 | 0.0080 | +0.0060 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years |  | 2024 |  |  | 0.0192 | +0.0053 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0049 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years |  | 2024 |  |  | 0.0148 | +0.0024 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0022 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0018 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Log enrollment (FTE) | 6.54 | 2024 | 50.9 | 0.12 | 0.0797 | +0.0009 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Students per staff member | 4.047 | 2024 | 19.7 | -0.55 | 0.0347 | -0.0001 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0058 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0208 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0418 | Reported on the scored row. Not imputed. |
| Admit rate | 0.8542 | 2024 | 65.2 | 0.57 | 0.0252 | -0.0543 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.1009 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.2262 | 2024 | 6.0 | -1.08 | 0.0212 | -0.1244 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.2233 | 2023 | 96.4 | 1.87 | 0.0198 | -0.1406 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.1961 | 2024 | 78.7 | 0.25 | 0.0119 | -0.1409 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.01019 | 2025 | 48.4 | -0.14 | 0.0364 | -0.1892 | Reported on the scored row. Not imputed. |
| Yield rate | 0.08347 | 2024 | 4.7 | -1.15 | 0.0418 | -0.1921 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.4314 | 2024 | 10.0 | -0.78 | 0.0125 | -0.1975 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.2 | 2024 | 8.0 | -0.95 | 0.0388 | -0.1976 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1976 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | -0.3073 | 2023 | 6.7 | -1.31 | 0.0479 | -0.3093 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 21. Utica University (NY)

Residential rank 21. Watch-list rank 394. Published risk score 0.376. Federal composite score 2.70 (year 2025.0).

Endowment $35.4 million in 2023 ($10,911 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 197045. Fall headcount 3,627 in 2024 (undergraduate 2,329; graduate 1,298). FTE 3,241 in 2024. Fall headcount 4,947 in 2019 versus 3,627 in 2024 (-27%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.5 years of expenses (2023)
- endowment covers 0.4 years of expenses, $10,407 per FTE (2023)
- the federal composite score is 2.70 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.5188 | 2023 | 31.4 | -0.66 | 0.1840 | +0.6447 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 1.041e+04 | 2023 | 21.6 | -0.49 | 0.1018 | +0.3412 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.7 | 2025 | 56.2 | 0.39 | 0.0966 | +0.2569 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1722 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 8.084 | 2024 | 87.9 | 1.04 | 0.0797 | +0.1143 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | -0.06621 | 2024 | 39.8 | -0.24 | 0.0103 | +0.0793 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.02798 | 2024 | 52.0 | -0.03 | 0.0192 | +0.0750 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.0462 | 2024 | 27.9 | -0.33 | 0.0388 | +0.0645 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.652 | 2023 | 51.4 | 0.09 | 0.0405 | +0.0615 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.2776 | 2023 | 57.0 | 0.14 | 0.0204 | +0.0492 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.05114 | 2024 | 60.3 | 0.13 | 0.0148 | +0.0491 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.1858 | 2023 | 13.4 | -0.76 | 0.0075 | +0.0296 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -0.03364 | 2024 | 43.6 | -0.05 | 0.0080 | +0.0194 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | 0.01313 | 2024 | 55.1 | -0.20 | 0.0046 | +0.0173 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.1275 | 2023 | 14.3 | -0.63 | 0.0479 | +0.0092 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0092 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0062 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0061 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0051 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0048 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0026 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0017 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0010 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0034 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.04215 | 2024 | 27.5 | -0.27 | 0.0212 | -0.0049 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0067 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.253 | 2024 | 13.2 | -0.68 | 0.0119 | -0.0167 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0236 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0309 | Reported on the scored row. Not imputed. |
| Students per staff member | 7.924 | 2024 | 54.8 | -0.24 | 0.0347 | -0.0525 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1266 | 2024 | 16.1 | -1.02 | 0.0418 | -0.0887 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.9195 | 2024 | 76.8 | 0.84 | 0.0252 | -0.0981 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.2689 | 2024 | 19.0 | -0.56 | 0.0125 | -0.0998 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.1002 | 2023 | 84.5 | 0.68 | 0.0198 | -0.1232 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.2243 | Reported on the scored row. Not imputed. |
| State high-school graduates, 5-year change | -0.0524 | 2025 | 10.1 | -1.02 | 0.0364 | -0.2724 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.6220 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 22. Saint John's Seminary (MA)

Residential rank 22. Watch-list rank 407. Published risk score 0.366. Federal composite score 2.20 (year 2025.0).

Endowment $38.4 million in 2023 ($451,632 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 167677. Fall headcount 86 in 2024 (undergraduate 23; graduate 63). FTE 85 in 2024. Fall headcount 111 in 2019 versus 86 in 2024 (-23%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 10.5 years of expenses (2023)
- yield is 100% (2013)
- endowment covers 6.0 years of expenses, $376,360 per FTE (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

Investment return ($10.0 million) is more than half of reported revenue ($13.3 million). The IPEDS operating margin is not a tuition operating result.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 10.51 | 2023 | 100.0 | 3.72 | 0.1840 | +0.3850 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 1 | 2013 | 100.0 | 1.67 | 0.0418 | +0.3288 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 3.764e+05 | 2023 | 88.9 | 0.87 | 0.1018 | +0.3281 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.1766 | 2023 | 8.5 | -1.50 | 0.0405 | +0.2153 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.2 | 2025 | 32.3 | -0.24 | 0.0966 | +0.2067 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0962 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 0.2381 | 2024 | 82.2 | 0.25 | 0.0103 | +0.0534 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3717 | 2023 | 66.5 | 0.54 | 0.0204 | +0.0418 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0 | 2013 | 51.4 | -0.16 | 0.0119 | +0.0288 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 1 | 2013 | 100.0 | 1.19 | 0.0252 | +0.0259 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.08333 | 2024 | 80.2 | 0.28 | 0.0212 | +0.0213 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0170 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years |  | 2013 |  |  | 0.0192 | +0.0153 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0103 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0061 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years |  | 2013 |  |  | 0.0148 | +0.0058 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0057 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0051 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | +0.0047 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0026 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0014 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Student-staff ratio change, 1 year | -0.9808 | 2024 | 17.7 | -0.24 | 0.0080 | +0.0009 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0002 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | -0.0010 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0019 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0036 | Reported on the scored row. Not imputed. |
| Students per staff member | 3.269 | 2024 | 13.8 | -0.60 | 0.0347 | -0.0085 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.4817 | 2024 | 13.3 | -0.68 | 0.0046 | -0.0107 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0391 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | 0.9807 | 2023 | 99.0 | 3.52 | 0.0075 | -0.0465 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.1607 | 2023 | 3.5 | -1.86 | 0.0198 | -0.0477 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.1667 | 2024 | 10.1 | -0.81 | 0.0388 | -0.0695 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.02415 | 2025 | 26.0 | -0.62 | 0.0364 | -0.0717 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.2917 | 2024 | 17.7 | -0.59 | 0.0125 | -0.0823 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0960 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.2257 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | 0.5182 | 2023 | 98.4 | 1.82 | 0.0479 | -0.3263 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 4.443 | 2024 | 12.8 | -1.15 | 0.0797 | -0.4327 | Reported on the scored row. Not imputed. |

### 23. Concordia University-Chicago (IL)

Residential rank 23. Watch-list rank 415. Published risk score 0.358. Federal composite score 2.10 (year 2025.0).

Endowment $32.4 million in 2023 ($8,743 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 144351. Fall headcount 4,770 in 2024 (undergraduate 1,368; graduate 3,402). FTE 3,711 in 2024. Fall headcount 6,205 in 2019 versus 4,770 in 2024 (-23%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.9 years of expenses (2023)
- endowment covers 0.5 years of expenses, $8,884 per FTE (2023)
- the federal composite score is 2.10 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.8503 | 2023 | 37.4 | -0.52 | 0.1840 | +0.4085 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 8884 | 2023 | 18.9 | -0.50 | 0.1018 | +0.2187 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.1 | 2025 | 24.5 | -0.36 | 0.0966 | +0.1721 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | 0.06614 | 2023 | 51.1 | 0.11 | 0.0479 | +0.1556 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1293 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | 0.01616 | 2024 | 51.4 | -0.08 | 0.0388 | +0.1050 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 8.219 | 2024 | 90.0 | 1.13 | 0.0797 | +0.0974 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.7238 | 2023 | 58.1 | 0.33 | 0.0405 | +0.0855 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.2611 | 2023 | 55.4 | 0.07 | 0.0204 | +0.0654 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.02715 | 2024 | 52.5 | -0.02 | 0.0192 | +0.0618 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.2407 | 2024 | 16.3 | -0.52 | 0.0103 | +0.0329 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.6751 | 2024 | 73.5 | 0.08 | 0.0080 | +0.0230 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0203 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.08257 | 2024 | 32.1 | -0.33 | 0.0119 | +0.0173 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.04086 | 2023 | 53.9 | 0.07 | 0.0075 | +0.0134 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0078 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0064 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.03572 | 2024 | 57.2 | -0.17 | 0.0046 | +0.0045 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0024 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0020 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0016 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0014 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0000 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0028 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0033 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.1806 | 2024 | 83.4 | 0.80 | 0.0148 | -0.0083 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.05963 | 2024 | 23.0 | -0.35 | 0.0212 | -0.0149 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0214 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.1469 | 2024 | 32.0 | -0.39 | 0.0125 | -0.0319 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 2 | 2023 | 73.1 | 0.25 | 0.0338 | -0.0426 | Reported on the scored row. Not imputed. |
| Admit rate | 0.9279 | 2024 | 77.8 | 0.88 | 0.0252 | -0.0786 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.003676 | 2023 | 25.8 | -0.34 | 0.0198 | -0.1051 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.08347 | 2024 | 4.7 | -1.15 | 0.0418 | -0.1078 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 9.051 | 2024 | 60.2 | -0.16 | 0.0347 | -0.1080 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.0394 | 2025 | 14.2 | -0.84 | 0.0364 | -0.2469 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.5264 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 24. Arkansas Baptist College (AR)

Residential rank 24. Watch-list rank 418. Published risk score 0.355. Federal composite score -0.70 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 106306; endowment_end (F2H02/F1H02) is blank. Fall headcount 342 in 2024 (undergraduate 342; graduate not reported). FTE 291 in 2024. Fall headcount 531 in 2019 versus 342 in 2024 (-36%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 2.1 years of expenses (2023)
- tuition is 6% of revenue (2023)
- the operating margin is +2% (2023)

Missing or imputed:

First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Admit rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 2.1 | 2023 | 63.4 | 0.03 | 0.1840 | +0.5176 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.05935 | 2023 | 2.9 | -1.90 | 0.0405 | +0.1568 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | 0.01533 | 2023 | 37.7 | -0.09 | 0.0479 | +0.1501 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1453 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0684 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.3975 | 2023 | 100.0 | 3.57 | 0.0198 | +0.0618 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.1216 | 2024 | 72.7 | 0.06 | 0.0103 | +0.0436 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 3.506 | 2024 | 15.5 | -0.59 | 0.0347 | +0.0354 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year |  |  |  |  | 0.0119 | +0.0242 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0083 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0074 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years |  |  |  |  | 0.0192 | +0.0069 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0061 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -0.3025 | 2024 | 30.3 | -0.10 | 0.0080 | +0.0059 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.2135 | 2023 | 85.0 | 0.70 | 0.0075 | +0.0050 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0045 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0022 | Reported on the scored row. Not imputed. |
| Discount rate | 0.6843 | 2023 | 96.0 | 1.86 | 0.0204 | +0.0021 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0016 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years |  |  |  |  | 0.0148 | +0.0010 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 1 | 2025 | 100.0 | 4.33 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Admit rate |  |  |  |  | 0.0252 | -0.0002 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0042 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0068 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0113 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.117 | 2024 | 13.1 | -0.60 | 0.0212 | -0.0166 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 47.45 | 2011 | 0.9 | -0.53 | 0.1018 | -0.0180 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate |  |  |  |  | 0.0418 | -0.0200 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0214 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0222 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 5.673 | 2024 | 32.4 | -0.41 | 0.0797 | -0.0449 | Reported on the scored row. Not imputed. |
| Federal composite score | -0.7 | 2025 | 1.8 | -3.91 | 0.0966 | -0.0695 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 1 year | -0.1872 | 2024 | 8.8 | -0.90 | 0.0388 | -0.0773 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.0987 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.1080 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.3604 | 2024 | 12.8 | -0.68 | 0.0125 | -0.1107 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.66 | 2024 | 6.0 | -0.86 | 0.0046 | -0.1258 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.04523 | 2025 | 71.5 | 0.35 | 0.0364 | -0.1673 | Reported on the scored row. Not imputed. |

### 25. Keystone College (PA)

Residential rank 25. Watch-list rank 426. Published risk score 0.349. Federal composite score 0.40 (year 2025.0).

Endowment $6.2 million in 2023 ($6,800 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 213303. Fall headcount 952 in 2024 (undergraduate 894; graduate 58). FTE 905 in 2024. Fall headcount 1,364 in 2019 versus 952 in 2024 (-30%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- endowment covers 0.2 years of expenses, $5,514 per FTE (2023)
- enrollment is about 905 FTE (2024)
- the federal composite score is 0.40 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Endowment per FTE | 5514 | 2023 | 12.7 | -0.51 | 0.1018 | +0.2622 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.808 | 2024 | 58.6 | 0.28 | 0.0797 | +0.2550 | Reported on the scored row. Not imputed. |
| Federal composite score | 0.4 | 2025 | 3.7 | -2.52 | 0.0966 | +0.1774 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.538 | 2023 | 40.2 | -0.29 | 0.0405 | +0.1708 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1348 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.1049 | 2024 | 18.9 | -0.51 | 0.0192 | +0.0796 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.3439 | 2024 | 9.5 | -0.68 | 0.0103 | +0.0742 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3024 | 2023 | 59.8 | 0.24 | 0.0204 | +0.0436 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.0606 | 2024 | 62.7 | 0.18 | 0.0148 | +0.0412 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | 0.1314 | 2023 | 20.0 | -0.83 | 0.1840 | +0.0238 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0183 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.05759 | 2024 | 37.3 | -0.28 | 0.0119 | +0.0173 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0070 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0042 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0023 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0017 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0013 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0013 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Student-staff ratio change, 1 year | 0.5805 | 2024 | 71.2 | 0.07 | 0.0080 | +0.0004 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0002 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 1 | 2025 | 100.0 | 4.33 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0026 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.2035 | 2023 | 11.8 | -0.83 | 0.0075 | -0.0072 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0086 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | -0.1262 | 2023 | 4.6 | -1.53 | 0.0198 | -0.0157 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0170 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0211 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.2426 | 2024 | 5.5 | -1.15 | 0.0212 | -0.0268 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.3848 | 2024 | 19.3 | -0.59 | 0.0046 | -0.0283 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.848 | 2024 | 64.0 | 0.54 | 0.0252 | -0.0449 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.2905 | 2023 | 7.3 | -1.25 | 0.0479 | -0.0608 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.0663 | Reported on the scored row. Not imputed. |
| Students per staff member | 8.786 | 2024 | 59.0 | -0.18 | 0.0347 | -0.0820 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.4431 | 2024 | 9.6 | -0.79 | 0.0125 | -0.1051 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.1891 | 2024 | 8.6 | -0.90 | 0.0388 | -0.1081 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.03434 | 2025 | 20.2 | -0.77 | 0.0364 | -0.1153 | Reported on the scored row. Not imputed. |
| Yield rate | 0.1075 | 2024 | 10.0 | -1.08 | 0.0418 | -0.1388 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1424 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 26. Southwestern Christian College (TX)

Residential rank 26. Watch-list rank 431. Published risk score 0.345. Federal composite score 1.40 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 228486; endowment_end (F2H02/F1H02) is blank. Fall headcount 110 in 2024 (undergraduate 110; graduate not reported). FTE 111 in 2024. Fall headcount 106 in 2019 versus 110 in 2024 (+4%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 2.0 years of expenses (2023)
- tuition is 19% of revenue (2023)
- sector is 2 (2025)

Missing or imputed:

Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Admit rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 2.019 | 2023 | 61.6 | -0.00 | 0.1840 | +0.3821 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.1934 | 2023 | 9.5 | -1.45 | 0.0405 | +0.2225 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1122 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.378 | 2023 | 98.1 | 3.38 | 0.0198 | +0.1074 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.9474 | 2024 | 98.4 | 3.67 | 0.0388 | +0.0645 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.5345 | 2023 | 85.4 | 1.23 | 0.0204 | +0.0597 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0287 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.2885 | 2024 | 26.7 | -0.49 | 0.0046 | +0.0233 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0177 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | 0.8824 | 2024 | 99.2 | 3.80 | 0.0212 | +0.0163 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0071 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0067 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 0.1158 | 2024 | 54.5 | -0.02 | 0.0080 | +0.0064 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years |  |  |  |  | 0.0192 | +0.0063 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Enrollment change, 5 years | 0.03738 | 2024 | 57.7 | -0.14 | 0.0125 | +0.0043 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0042 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year |  |  |  |  | 0.0119 | +0.0040 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0040 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 0.4545 | 2024 | 89.5 | 0.60 | 0.0103 | +0.0039 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years |  |  |  |  | 0.0148 | +0.0038 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0015 | Reported on the scored row. Not imputed. |
| Federal composite score | 1.4 | 2025 | 9.2 | -1.25 | 0.0966 | +0.0008 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Admit rate |  |  |  |  | 0.0252 | -0.0007 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Operating-margin change, 5 years | -0.2362 | 2023 | 9.5 | -0.95 | 0.0075 | -0.0017 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0037 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 5 | 2025 | 100.0 | 5.42 | 0.0023 | -0.0043 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | -0.0108 | Reported on the scored row. Not imputed. |
| Yield rate |  |  |  |  | 0.0418 | -0.0185 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0212 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 1 | 2025 | 100.0 | 4.81 | 0.0009 | -0.0428 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Students per staff member | 3.469 | 2024 | 15.1 | -0.59 | 0.0347 | -0.0483 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.0709 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| State high-school graduates, 5-year change | 0.08271 | 2025 | 92.7 | 0.88 | 0.0364 | -0.0740 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0823 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.0857 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | -0.194 | 2023 | 10.0 | -0.88 | 0.0479 | -0.0923 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 4.71 | 2024 | 16.2 | -0.98 | 0.0797 | -0.2086 | Reported on the scored row. Not imputed. |

### 27. Carolina University (NC)

Residential rank 27. Watch-list rank 443. Published risk score 0.340. Federal composite score 3.00 (year 2025.0).

Endowment $386,000 in 2023 ($429 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 489937. Fall headcount 880 in 2024 (undergraduate 460; graduate 420). FTE 899 in 2024. Fall headcount 668 in 2019 versus 880 in 2024 (+32%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- the federal composite score is 3.00 (2025)
- FTE enrollment changed +36% in one year (2024)
- enrollment is about 899 FTE (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Enrollment change, 10 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Federal composite score | 3 | 2025 | 100.0 | 0.77 | 0.0966 | +0.2699 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 1 year | 0.356 | 2024 | 93.6 | 1.29 | 0.0388 | +0.2182 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.801 | 2024 | 58.4 | 0.27 | 0.0797 | +0.1806 | Reported on the scored row. Not imputed. |
| Admit rate | 0.3954 | 2024 | 10.7 | -1.38 | 0.0252 | +0.1464 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.6103 | 2023 | 47.7 | -0.05 | 0.0405 | +0.1120 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1009 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | -0.2022 | 2024 | 19.9 | -0.46 | 0.0103 | +0.0902 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.5083 | 2023 | 82.6 | 1.12 | 0.0204 | +0.0582 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.354 | 2024 | 3.3 | -2.08 | 0.0192 | +0.0394 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0207 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.161 | 2023 | 15.4 | -0.67 | 0.0075 | +0.0158 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.04054 | 2024 | 28.2 | -0.27 | 0.0212 | +0.0119 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | -0.3529 | 2024 | 9.1 | -0.89 | 0.0119 | +0.0077 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | 0.09629 | 2023 | 17.2 | -0.85 | 0.1840 | +0.0076 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 3.703 | 2024 | 92.4 | 0.67 | 0.0080 | +0.0073 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0069 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0057 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0048 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years |  | 2024 |  |  | 0.0046 | +0.0048 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Admit-rate change, 5 years | 0.109 | 2024 | 73.5 | 0.43 | 0.0148 | +0.0025 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0016 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0014 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0012 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 5 years | 0.3873 | 2024 | 82.7 | 0.33 | 0.0125 | +0.0007 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0005 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | -0.0003 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0023 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0074 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0087 | Reported on the scored row. Not imputed. |
| Endowment per FTE | 582.2 | 2023 | 3.9 | -0.53 | 0.1018 | -0.0127 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0257 | Reported on the scored row. Not imputed. |
| Students per staff member | 12.66 | 2024 | 72.9 | 0.12 | 0.0347 | -0.0766 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.04486 | 2025 | 70.8 | 0.35 | 0.0364 | -0.0839 | Reported on the scored row. Not imputed. |
| Yield rate | 0.2646 | 2024 | 42.6 | -0.59 | 0.0418 | -0.0946 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.2191 | 2023 | 96.2 | 1.83 | 0.0198 | -0.1165 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1683 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | -0.2965 | 2023 | 7.1 | -1.27 | 0.0479 | -0.1706 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.2329 | Reported on the scored row. Not imputed. |

### 28. Hilbert College (NY)

Residential rank 28. Watch-list rank 446. Published risk score 0.334. Federal composite score 2.20 (year 2025.0).

Endowment $3.8 million in 2023 ($3,726 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 191621. Fall headcount 968 in 2024 (undergraduate 931; graduate 37). FTE 1,022 in 2024. Fall headcount 766 in 2019 versus 968 in 2024 (+26%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.9 years of expenses (2023)
- endowment covers 0.2 years of expenses, $3,376 per FTE (2023)
- enrollment is about 1,022 FTE (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.8529 | 2023 | 37.6 | -0.52 | 0.1840 | +0.3652 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 3376 | 2023 | 9.5 | -0.52 | 0.1018 | +0.2095 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.93 | 2024 | 61.6 | 0.35 | 0.0797 | +0.1981 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.2 | 2025 | 32.3 | -0.24 | 0.0966 | +0.1184 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0990 | Reported on the scored row. Not imputed. |
| Discount rate | 0.4622 | 2023 | 76.7 | 0.92 | 0.0204 | +0.0788 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.07095 | 2023 | 19.8 | -0.41 | 0.0479 | +0.0438 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.6488 | 2023 | 51.2 | 0.08 | 0.0405 | +0.0427 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.04386 | 2024 | 61.4 | -0.06 | 0.0103 | +0.0362 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.04617 | 2024 | 58.9 | 0.10 | 0.0148 | +0.0266 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0235 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.004 | 2024 | 47.8 | -0.17 | 0.0119 | +0.0194 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.05678 | 2023 | 59.0 | 0.13 | 0.0075 | +0.0153 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -0.3641 | 2024 | 28.0 | -0.12 | 0.0080 | +0.0098 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0057 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0052 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0033 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.06237 | 2024 | 59.3 | -0.15 | 0.0046 | +0.0014 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0013 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.09397 | 2024 | 17.9 | -0.52 | 0.0388 | +0.0013 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0011 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0004 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -0.0002 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.05556 | 2024 | 24.5 | -0.33 | 0.0212 | -0.0014 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0027 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0048 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0090 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.3187 | 2024 | 79.9 | 0.24 | 0.0125 | -0.0130 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0186 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | 0.05048 | 2024 | 79.4 | 0.47 | 0.0192 | -0.0430 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.972 | 2024 | 85.5 | 1.07 | 0.0252 | -0.0554 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.0524 | 2025 | 10.1 | -1.02 | 0.0364 | -0.0663 | Reported on the scored row. Not imputed. |
| Students per staff member | 8.588 | 2024 | 57.9 | -0.19 | 0.0347 | -0.0691 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.184 | 2024 | 31.0 | -0.84 | 0.0418 | -0.0698 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.1168 | 2023 | 88.4 | 0.84 | 0.0198 | -0.0800 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.1840 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.3779 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 29. Mid-Atlantic Christian University (NC)

Residential rank 29. Watch-list rank 448. Published risk score 0.333. Federal composite score 1.60 (year 2025.0).

Endowment $4.6 million in 2023 ($36,482 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 199458. Fall headcount 140 in 2024 (undergraduate 140; graduate not reported). FTE 125 in 2024. Fall headcount 198 in 2019 versus 140 in 2024 (-29%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 2.2 years of expenses (2023)
- endowment covers 0.8 years of expenses, $37,076 per FTE (2023)
- tuition is 13% of revenue (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 2.16 | 2023 | 64.9 | 0.06 | 0.1840 | +0.3605 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 3.708e+04 | 2023 | 48.6 | -0.40 | 0.1018 | +0.3182 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.13 | 2023 | 6.2 | -1.66 | 0.0405 | +0.1529 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0786 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.3251 | 2024 | 4.4 | -1.90 | 0.0192 | +0.0533 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.3333 | 2024 | 86.6 | 0.40 | 0.0103 | +0.0522 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.6 | 2025 | 13.3 | -1.00 | 0.0966 | +0.0402 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 1 year | 0.01626 | 2024 | 51.5 | -0.08 | 0.0388 | +0.0389 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.2236 | 2024 | 32.0 | -0.43 | 0.0046 | +0.0171 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.6216 | 2024 | 28.2 | -0.42 | 0.0252 | +0.0163 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.2222 | 2024 | 92.1 | 0.89 | 0.0212 | +0.0154 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3641 | 2023 | 65.6 | 0.50 | 0.0204 | +0.0141 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0092 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0073 | Reported on the scored row. Not imputed. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0065 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0039 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0034 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0033 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -0.5758 | 2024 | 22.8 | -0.16 | 0.0080 | +0.0031 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0017 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0011 | Reported on the scored row. Not imputed. |
| Students per staff member | 2.841 | 2024 | 10.3 | -0.64 | 0.0347 | -0.0013 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | -0.0018 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0019 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0029 | Reported on the scored row. Not imputed. |
| Operating margin | 0.3923 | 2023 | 95.0 | 1.34 | 0.0479 | -0.0107 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | -0.3043 | 2024 | 11.0 | -0.79 | 0.0119 | -0.0123 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.006045 | 2023 | 24.1 | -0.36 | 0.0198 | -0.0139 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.2066 | 2024 | 86.1 | 0.93 | 0.0148 | -0.0150 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.501 | 2023 | 96.3 | 1.76 | 0.0075 | -0.0211 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0285 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0657 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.1987 | 2024 | 26.2 | -0.46 | 0.0125 | -0.0707 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1051 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Yield rate | 0.1988 | 2024 | 34.2 | -0.80 | 0.0418 | -0.1185 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.04486 | 2025 | 70.8 | 0.35 | 0.0364 | -0.1224 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 4.828 | 2024 | 18.1 | -0.91 | 0.0797 | -0.2937 | Reported on the scored row. Not imputed. |

### 30. Fairleigh Dickinson University-Metropolitan Campus (NJ)

Residential rank 30. Watch-list rank 449. Published risk score 0.333. Federal composite score 3.00 (year 2025.0).

Endowment $100.2 million in 2023 ($22,122 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 184603. Fall headcount 8,045 in 2024 (undergraduate 5,690; graduate 2,355). FTE 4,531 in 2024. Fall headcount 8,206 in 2019 versus 8,045 in 2024 (-2%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.1 years of expenses (2023)
- the federal composite score is 3.00 (2025)
- endowment covers 0.4 years of expenses, $24,306 per FTE (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.106 | 2023 | 42.5 | -0.41 | 0.1840 | +0.3146 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 3 | 2025 | 100.0 | 0.77 | 0.0966 | +0.1775 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Endowment per FTE | 2.431e+04 | 2023 | 37.7 | -0.44 | 0.1018 | +0.1654 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 8.419 | 2024 | 92.1 | 1.25 | 0.0797 | +0.1186 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | 0.09869 | 2024 | 75.3 | 0.26 | 0.0388 | +0.1028 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0997 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.02022 | 2024 | 34.7 | -0.18 | 0.0212 | +0.0897 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.04043 | 2023 | 24.8 | -0.30 | 0.0479 | +0.0642 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3334 | 2023 | 62.4 | 0.37 | 0.0204 | +0.0497 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.0964 | 2024 | 20.8 | -0.46 | 0.0192 | +0.0439 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | -0.01522 | 2024 | 39.7 | -0.21 | 0.0148 | +0.0344 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.7282 | 2023 | 58.6 | 0.35 | 0.0405 | +0.0339 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.9201 | 2024 | 77.2 | 0.13 | 0.0080 | +0.0287 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0194 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.1166 | 2023 | 19.6 | -0.51 | 0.0075 | +0.0175 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.02805 | 2024 | 57.2 | -0.10 | 0.0119 | +0.0173 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.1131 | 2024 | 31.6 | -0.31 | 0.0103 | +0.0160 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.1531 | 2024 | 39.0 | -0.36 | 0.0046 | +0.0074 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0067 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0063 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0051 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0035 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0027 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0014 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0011 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0018 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0085 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.09049 | 2024 | 64.1 | -0.07 | 0.0125 | -0.0168 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0237 | Reported on the scored row. Not imputed. |
| Admit rate | 0.9071 | 2024 | 74.5 | 0.79 | 0.0252 | -0.0548 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.01811 | 2025 | 52.6 | -0.03 | 0.0364 | -0.0628 | Reported on the scored row. Not imputed. |
| Students per staff member | 8.501 | 2024 | 57.6 | -0.20 | 0.0347 | -0.0824 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1179 | 2024 | 13.3 | -1.05 | 0.0418 | -0.0865 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.06397 | 2023 | 8.7 | -0.92 | 0.0198 | -0.1074 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.2458 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.4253 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 31. Yeshiva Ohr Elchonon Chabad West Coast Talmudical Seminary (CA)

Residential rank 31. Watch-list rank 453. Published risk score 0.332. Federal composite score 2.20 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 126076; endowment_end (F2H02/F1H02) is blank. Fall headcount 163 in 2024 (undergraduate 163; graduate not reported). FTE 162 in 2024. Fall headcount 138 in 2019 versus 163 in 2024 (+18%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.5 years of expenses (2023)
- yield is 100% (2024)
- tuition is 38% of revenue (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

The model's five-year enrollment feature is the FTE change (-30%). Fall headcount changed +18% over the years shown on the card. Those are different counts. | This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.516 | 2023 | 52.4 | -0.23 | 0.1840 | +0.3778 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 1 | 2024 | 100.0 | 1.67 | 0.0418 | +0.2698 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.3831 | 2023 | 24.7 | -0.81 | 0.0405 | +0.2196 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.2 | 2025 | 32.3 | -0.24 | 0.0966 | +0.1445 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0704 | Reported on the scored row. Not imputed. |
| Admit rate | 0.5821 | 2024 | 24.4 | -0.59 | 0.0252 | +0.0534 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.2543 | 2023 | 54.7 | 0.04 | 0.0204 | +0.0337 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.24 | 2024 | 93.1 | 0.97 | 0.0212 | +0.0155 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.2062 | 2023 | 11.6 | -0.84 | 0.0075 | +0.0143 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.25 | 2024 | 29.6 | -0.45 | 0.0046 | +0.0123 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0113 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0064 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0061 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | -0.2337 | 2024 | 8.2 | -1.33 | 0.0148 | +0.0061 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0043 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0042 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0035 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0016 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0013 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | -0.0002 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -2.934 | 2024 | 7.6 | -0.61 | 0.0080 | -0.0009 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 5.226 | 2024 | 32.0 | -0.45 | 0.0347 | -0.0019 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0032 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0045 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0055 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 0.8235 | 2024 | 94.9 | 1.19 | 0.0103 | -0.0111 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0214 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.2987 | 2024 | 17.4 | -0.60 | 0.0125 | -0.0425 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.2787 | 2024 | 83.9 | 0.42 | 0.0119 | -0.0517 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.09103 | 2023 | 81.7 | 0.59 | 0.0198 | -0.0518 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.004182 | 2025 | 46.1 | -0.22 | 0.0364 | -0.0572 | Reported on the scored row. Not imputed. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.0694 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Operating margin | -0.1971 | 2023 | 9.9 | -0.89 | 0.0479 | -0.0900 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | 0.09677 | 2024 | 84.3 | 0.76 | 0.0192 | -0.0912 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.0922 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.2059 | 2024 | 7.7 | -0.97 | 0.0388 | -0.1117 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1124 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Log enrollment (FTE) | 5.088 | 2024 | 22.8 | -0.76 | 0.0797 | -0.1286 | Reported on the scored row. Not imputed. |

### 32. Maharishi International University (IA)

Residential rank 32. Watch-list rank 459. Published risk score 0.329. Federal composite score 2.60 (year 2025.0).

Endowment $12.1 million in 2023 ($5,459 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 153861. Fall headcount 2,592 in 2024 (undergraduate 922; graduate 1,670). FTE 2,219 in 2024. Fall headcount 1,861 in 2019 versus 2,592 in 2024 (+39%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.0 years of expenses (2023)
- endowment covers 0.2 years of expenses, $5,001 per FTE (2023)
- enrollment is about 2,219 FTE (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.019 | 2023 | 40.9 | -0.44 | 0.1840 | +0.3072 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 5001 | 2023 | 11.7 | -0.52 | 0.1018 | +0.2281 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.705 | 2024 | 80.3 | 0.82 | 0.0797 | +0.1425 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.6 | 2025 | 51.4 | 0.27 | 0.0966 | +0.1138 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Yield rate | 0.7528 | 2024 | 76.1 | 0.91 | 0.0418 | +0.0990 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0932 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.6109 | 2023 | 47.8 | -0.04 | 0.0405 | +0.0452 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.02305 | 2024 | 47.5 | -0.17 | 0.0103 | +0.0348 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.4296 | 2024 | 67.0 | 0.04 | 0.0080 | +0.0189 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.08576 | 2023 | 18.4 | -0.47 | 0.0479 | +0.0170 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0170 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.09154 | 2023 | 23.1 | -0.42 | 0.0075 | +0.0162 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 6.546 | 2024 | 45.3 | -0.35 | 0.0347 | +0.0103 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.06349 | 2024 | 64.0 | -0.03 | 0.0119 | +0.0082 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.1457 | 2024 | 79.3 | 0.62 | 0.0148 | +0.0073 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0053 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0045 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0041 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0020 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.4224 | 2024 | 80.0 | 0.21 | 0.0046 | +0.0020 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0014 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0011 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0016 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.08382 | 2024 | 19.4 | -0.48 | 0.0388 | -0.0022 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0092 | Reported on the scored row. Not imputed. |
| Discount rate | 0.1014 | 2023 | 42.2 | -0.61 | 0.0204 | -0.0158 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0182 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0206 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.1439 | 2024 | 10.7 | -0.72 | 0.0212 | -0.0217 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | 0.1835 | 2024 | 72.5 | 0.06 | 0.0125 | -0.0219 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0262 | Reported on the scored row. Not imputed. |
| State high-school graduates, 5-year change | 0.07143 | 2025 | 83.8 | 0.72 | 0.0364 | -0.0352 | Reported on the scored row. Not imputed. |
| Admit rate | 0.957 | 2024 | 83.0 | 1.00 | 0.0252 | -0.0514 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.03318 | 2023 | 13.3 | -0.62 | 0.0198 | -0.0870 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | 0.2412 | 2024 | 93.6 | 1.67 | 0.0192 | -0.1702 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.3925 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 33. Huston-Tillotson University (TX)

Residential rank 33. Watch-list rank 463. Published risk score 0.327. Federal composite score 1.40 (year 2025.0).

Endowment $13.6 million in 2023 ($25,207 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 225575. Fall headcount 1,059 in 2024 (undergraduate 1,024; graduate 35). FTE 540 in 2024. Fall headcount 1,121 in 2019 versus 1,059 in 2024 (-6%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.9 years of expenses (2023)
- endowment covers 0.4 years of expenses, $20,782 per FTE (2023)
- tuition is 42% of revenue (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

The model's five-year enrollment feature is the FTE change (-45%). Fall headcount changed -6% over the years shown on the card. Those are different counts.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.908 | 2023 | 59.8 | -0.05 | 0.1840 | +0.4267 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 2.078e+04 | 2023 | 34.1 | -0.46 | 0.1018 | +0.1913 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.4182 | 2023 | 28.2 | -0.69 | 0.0405 | +0.1418 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.3909 | 2024 | 10.6 | -1.40 | 0.0252 | +0.1050 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.1043 | Reported on the scored row. Not imputed. |
| Operating margin | -0.04453 | 2023 | 23.9 | -0.31 | 0.0479 | +0.0740 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.05036 | 2024 | 71.4 | 0.14 | 0.0212 | +0.0434 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.2696 | 2024 | 83.8 | 0.30 | 0.0103 | +0.0254 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.4 | 2025 | 9.2 | -1.25 | 0.0966 | +0.0238 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating-margin change, 5 years | -0.1769 | 2023 | 14.1 | -0.73 | 0.0075 | +0.0221 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0104 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | -0.2342 | 2024 | 8.1 | -1.34 | 0.0148 | +0.0097 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0066 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0036 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0024 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -1.014 | 2024 | 17.1 | -0.24 | 0.0080 | +0.0008 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0012 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0033 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0050 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.4079 | 2024 | 17.5 | -0.61 | 0.0046 | -0.0062 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 3.699 | 2024 | 16.7 | -0.57 | 0.0347 | -0.0123 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.292 | 2024 | 44.7 | -0.03 | 0.0797 | -0.0126 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 1 | 2025 | 100.0 | 4.81 | 0.0009 | -0.0160 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Discount rate | 0.1236 | 2023 | 44.1 | -0.52 | 0.0204 | -0.0169 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0176 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0195 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | 0.03457 | 2023 | 58.8 | 0.04 | 0.0198 | -0.0255 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0258 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | 0.2267 | 2022 | 81.0 | 0.31 | 0.0119 | -0.0384 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 5 | 2025 | 100.0 | 5.42 | 0.0023 | -0.0415 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | 0.1146 | 2024 | 86.9 | 0.87 | 0.0192 | -0.0831 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.0958 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 1 year | -0.1756 | 2024 | 9.4 | -0.85 | 0.0388 | -0.0982 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.2326 | 2024 | 39.2 | -0.69 | 0.0418 | -0.1024 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.08271 | 2025 | 92.7 | 0.88 | 0.0364 | -0.1086 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.454 | 2024 | 9.0 | -0.81 | 0.0125 | -0.1581 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 34. Grace Christian University (MI)

Residential rank 34. Watch-list rank 467. Published risk score 0.325. Federal composite score 1.80 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 170000; endowment_end (F2H02/F1H02) is blank. Fall headcount 1,017 in 2024 (undergraduate 928; graduate 89). FTE 628 in 2024. Fall headcount 1,097 in 2019 versus 1,017 in 2024 (-7%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.9 years of expenses (2023)
- tuition is 48% of revenue (2023)
- sector is 2 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.9126 | 2023 | 38.7 | -0.49 | 0.1840 | +0.3153 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.4774 | 2023 | 34.2 | -0.49 | 0.0405 | +0.1555 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0879 | Reported on the scored row. Not imputed. |
| Operating margin | -0.04187 | 2023 | 24.3 | -0.30 | 0.0479 | +0.0765 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 1874 | 2012 | 6.9 | -0.53 | 0.1018 | +0.0744 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.006329 | 2024 | 40.1 | -0.17 | 0.0388 | +0.0553 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.08333 | 2024 | 80.2 | 0.28 | 0.0212 | +0.0473 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.09901 | 2024 | 34.0 | -0.29 | 0.0103 | +0.0351 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.8 | 2025 | 18.9 | -0.74 | 0.0966 | +0.0259 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Admit rate | 0.9916 | 2024 | 88.0 | 1.15 | 0.0252 | +0.0245 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | -0.008368 | 2024 | 41.6 | -0.17 | 0.0148 | +0.0231 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3246 | 2023 | 61.4 | 0.34 | 0.0204 | +0.0229 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.1373 | 2023 | 17.5 | -0.59 | 0.0075 | +0.0121 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0075 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0046 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0037 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0037 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0028 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0013 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0012 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.07719 | 2024 | 60.5 | -0.13 | 0.0046 | +0.0009 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | +0.0006 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | -0.0001 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -0.6227 | 2024 | 22.0 | -0.17 | 0.0080 | -0.0006 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0008 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0023 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 6.443 | 2024 | 48.6 | 0.06 | 0.0797 | -0.0047 | Reported on the scored row. Not imputed. |
| Students per staff member | 6.901 | 2024 | 48.6 | -0.32 | 0.0347 | -0.0082 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0181 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0209 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0348 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | 0.1798 | 2024 | 77.8 | 0.21 | 0.0119 | -0.0582 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.214 | 2024 | 24.6 | -0.48 | 0.0125 | -0.0650 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.443 | 2024 | 56.0 | -0.04 | 0.0418 | -0.0704 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.06657 | 2023 | 72.8 | 0.35 | 0.0198 | -0.0720 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.02716 | 2025 | 22.8 | -0.67 | 0.0364 | -0.0938 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1005 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Yield-rate change, 5 years | 0.2633 | 2024 | 94.7 | 1.80 | 0.0192 | -0.1298 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 35. University of Advancing Technology (AZ)

Residential rank 35. Watch-list rank 501. Published risk score 0.308. Federal composite score 2.60 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 363934; endowment_end (F2H02/F1H02) is blank. Fall headcount 933 in 2024 (undergraduate 855; graduate 78). FTE 869 in 2024. Fall headcount 789 in 2019 versus 933 in 2024 (+18%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.6 years of expenses (2022)
- the federal composite score is 2.60 (2025)
- the operating margin is +8% (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

The model's five-year enrollment feature is the FTE change (-13%). Fall headcount changed +18% over the years shown on the card. Those are different counts. | For-profit FASB filers do not report endowment assets. A blank endowment is the IPEDS definition, not a missing 990.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.6179 | 2022 | 33.0 | -0.62 | 0.1840 | +0.3411 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.6 | 2025 | 51.4 | 0.27 | 0.0966 | +0.1682 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | 0.08025 | 2023 | 54.0 | 0.16 | 0.0479 | +0.1211 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.767 | 2024 | 57.5 | 0.25 | 0.0797 | +0.0834 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 0 | 2023 | 27.5 | -1.14 | 0.0338 | +0.0731 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.8552 | 2023 | 68.3 | 0.78 | 0.0405 | +0.0670 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.02041 | 2024 | 34.7 | -0.18 | 0.0212 | +0.0470 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | 0.1294 | 2024 | 73.8 | 0.08 | 0.0103 | +0.0427 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | -0.117 | 2024 | 26.2 | -0.40 | 0.0119 | +0.0192 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.001937 | 2023 | 44.4 | -0.07 | 0.0075 | +0.0144 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0113 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -0.6316 | 2024 | 21.7 | -0.17 | 0.0080 | +0.0081 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0046 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0039 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.1266 | 2024 | 34.8 | -0.36 | 0.0125 | +0.0034 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0031 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0019 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.1062 | 2024 | 72.7 | 0.41 | 0.0148 | +0.0011 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0011 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.001152 | 2024 | 53.7 | -0.21 | 0.0046 | -0.0002 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 3 | 2025 | 100.0 | 1.48 | 0.0010 | -0.0004 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0017 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.0843 | 2024 | 19.3 | -0.48 | 0.0388 | -0.0100 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0116 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0131 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0166 | Reported on the scored row. Not imputed. |
| Discount rate | 0.1425 | 2023 | 45.5 | -0.44 | 0.0204 | -0.0171 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 3 | 2025 | 78.7 | 0.03 | 0.0331 | -0.0314 | Reported on the scored row. Not imputed. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.0408 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Admit rate | 0.9806 | 2024 | 86.7 | 1.10 | 0.0252 | -0.0418 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.4278 | 2024 | 54.8 | -0.09 | 0.0418 | -0.0506 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.1121 | 2025 | 96.9 | 1.29 | 0.0364 | -0.0650 | Reported on the scored row. Not imputed. |
| Students per staff member | 9.052 | 2024 | 60.2 | -0.16 | 0.0347 | -0.0681 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.06633 | 2023 | 8.3 | -0.94 | 0.0198 | -0.0753 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | 0.2281 | 2024 | 93.2 | 1.58 | 0.0192 | -0.0796 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.2081 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 36. Ohio Dominican University (OH)

Residential rank 36. Watch-list rank 503. Published risk score 0.308. Federal composite score 2.10 (year 2025.0).

Endowment $19.8 million in 2023 ($17,587 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 204617. Fall headcount 1,209 in 2024 (undergraduate 843; graduate 366). FTE 1,127 in 2024. Fall headcount 1,640 in 2019 versus 1,209 in 2024 (-26%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.6 years of expenses (2023)
- endowment covers 0.6 years of expenses, $16,811 per FTE (2023)
- enrollment is about 1,127 FTE (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.6358 | 2023 | 33.1 | -0.61 | 0.1840 | +0.2549 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 1.681e+04 | 2023 | 30.4 | -0.47 | 0.1018 | +0.1209 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.027 | 2024 | 64.3 | 0.41 | 0.0797 | +0.0888 | Reported on the scored row. Not imputed. |
| Operating margin | 0.02973 | 2023 | 42.1 | -0.03 | 0.0479 | +0.0875 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.1 | 2025 | 24.5 | -0.36 | 0.0966 | +0.0832 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.5257 | 2023 | 39.0 | -0.33 | 0.0405 | +0.0788 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0773 | Reported on the scored row. Not imputed. |
| Discount rate | 0.4791 | 2023 | 79.0 | 0.99 | 0.0204 | +0.0557 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.04411 | 2024 | 28.4 | -0.32 | 0.0388 | +0.0495 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.1765 | 2024 | 22.6 | -0.41 | 0.0103 | +0.0451 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.1314 | 2024 | 14.5 | -0.68 | 0.0192 | +0.0314 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | -0.1111 | 2024 | 27.2 | -0.39 | 0.0119 | +0.0107 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.2583 | 2024 | 62.0 | 0.00 | 0.0080 | +0.0105 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0046 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0040 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0035 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0014 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0009 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -0.0019 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0021 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0022 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.07784 | 2024 | 19.6 | -0.43 | 0.0212 | -0.0031 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.1029 | 2024 | 72.1 | 0.40 | 0.0148 | -0.0033 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0043 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.07471 | 2024 | 41.6 | -0.29 | 0.0125 | -0.0072 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0076 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0163 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.4424 | 2024 | 15.5 | -0.64 | 0.0046 | -0.0193 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.221 | 2023 | 85.8 | 0.73 | 0.0075 | -0.0230 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 7.318 | 2024 | 51.4 | -0.29 | 0.0347 | -0.0250 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.9423 | 2024 | 80.6 | 0.94 | 0.0252 | -0.0340 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.0005049 | 2023 | 30.4 | -0.30 | 0.0198 | -0.0355 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.04643 | 2025 | 75.7 | 0.37 | 0.0364 | -0.0544 | Reported on the scored row. Not imputed. |
| Yield rate | 0.1137 | 2024 | 11.5 | -1.06 | 0.0418 | -0.0774 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.0920 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.3157 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 37. Benedictine University (IL)

Residential rank 37. Watch-list rank 505. Published risk score 0.306. Federal composite score 2.70 (year 2025.0).

Endowment $34.7 million in 2023 ($12,103 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 145619. Fall headcount 2,917 in 2024 (undergraduate 1,972; graduate 945). FTE 2,864 in 2024. Fall headcount 4,401 in 2019 versus 2,917 in 2024 (-34%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.5 years of expenses (2023)
- enrollment is about 2,864 FTE (2024)
- the federal composite score is 2.70 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.522 | 2023 | 52.5 | -0.22 | 0.1840 | +0.3431 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.96 | 2024 | 85.3 | 0.97 | 0.0797 | +0.2135 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.7 | 2025 | 56.2 | 0.39 | 0.0966 | +0.1445 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Endowment per FTE | 1.193e+04 | 2023 | 24.7 | -0.49 | 0.1018 | +0.1444 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0704 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.01411 | 2024 | 37.2 | -0.20 | 0.0388 | +0.0585 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.4852 | 2023 | 80.0 | 1.02 | 0.0204 | +0.0581 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.3732 | 2024 | 8.1 | -0.73 | 0.0103 | +0.0505 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.7168 | 2023 | 57.6 | 0.31 | 0.0405 | +0.0429 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.0159 | 2024 | 58.0 | 0.05 | 0.0192 | +0.0422 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.1605 | 2023 | 15.5 | -0.67 | 0.0075 | +0.0215 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0167 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 1.325 | 2024 | 81.7 | 0.21 | 0.0080 | +0.0067 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0041 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0031 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0030 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0023 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0008 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0008 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0001 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0029 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0043 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0078 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.1359 | 2024 | 11.5 | -0.69 | 0.0212 | -0.0109 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0138 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.5133 | 2024 | 11.5 | -0.71 | 0.0046 | -0.0181 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.1559 | 2023 | 12.4 | -0.74 | 0.0479 | -0.0239 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1556 | 2024 | 24.5 | -0.93 | 0.0418 | -0.0285 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.2762 | 2024 | 18.7 | -0.57 | 0.0125 | -0.0403 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 10.73 | 2024 | 66.7 | -0.03 | 0.0347 | -0.0476 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.9523 | 2024 | 82.2 | 0.98 | 0.0252 | -0.0482 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.5352 | 2024 | 98.2 | 2.62 | 0.0148 | -0.0624 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.274 | 2024 | 83.6 | 0.41 | 0.0119 | -0.0634 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.1633 | 2023 | 94.1 | 1.29 | 0.0198 | -0.0667 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.0394 | 2025 | 14.2 | -0.84 | 0.0364 | -0.0760 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.1192 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.3099 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 38. Life Pacific University (CA)

Residential rank 38. Watch-list rank 514. Published risk score 0.298. Federal composite score 2.50 (year 2025.0).

Endowment $4.9 million in 2023 ($9,146 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 117104. Fall headcount 621 in 2024 (undergraduate 460; graduate 161). FTE 538 in 2024. Fall headcount 552 in 2019 versus 621 in 2024 (+12%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 2.0 years of expenses (2023)
- the federal composite score is 2.50 (2025)
- endowment covers 0.3 years of expenses, $10,910 per FTE (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.994 | 2023 | 61.3 | -0.01 | 0.1840 | +0.2703 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.5 | 2025 | 46.4 | 0.14 | 0.0966 | +0.1670 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Endowment per FTE | 1.091e+04 | 2023 | 22.8 | -0.49 | 0.1018 | +0.1331 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.5289 | 2023 | 39.4 | -0.32 | 0.0405 | +0.0996 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.1929 | 2024 | 86.2 | 0.63 | 0.0388 | +0.0994 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0488 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 0.01754 | 2024 | 57.0 | -0.10 | 0.0103 | +0.0305 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.04431 | 2024 | 58.4 | 0.10 | 0.0148 | +0.0261 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.2686 | 2024 | 5.9 | -1.54 | 0.0192 | +0.0229 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.2771 | 2023 | 56.9 | 0.13 | 0.0204 | +0.0192 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0138 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.04472 | 2023 | 32.2 | -0.25 | 0.0075 | +0.0137 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0042 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0034 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0027 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0027 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0027 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0010 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0008 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0007 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 6.288 | 2024 | 44.5 | -0.04 | 0.0797 | +0.0007 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 2.644 | 2024 | 89.8 | 0.47 | 0.0080 | +0.0006 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | -0.0002 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | 0.076 | 2024 | 60.4 | -0.13 | 0.0046 | -0.0005 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0025 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.07171 | 2024 | 62.0 | -0.10 | 0.0125 | -0.0070 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.04054 | 2024 | 59.8 | -0.07 | 0.0119 | -0.0087 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0135 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0177 | Reported on the scored row. Not imputed. |
| Admit rate | 0.958 | 2024 | 83.5 | 1.01 | 0.0252 | -0.0298 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.1471 | 2024 | 10.5 | -0.73 | 0.0212 | -0.0375 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 9.276 | 2024 | 61.3 | -0.14 | 0.0347 | -0.0530 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.08598 | 2023 | 80.2 | 0.54 | 0.0198 | -0.0606 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.2729 | 2023 | 7.6 | -1.18 | 0.0479 | -0.0664 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.004182 | 2025 | 46.1 | -0.22 | 0.0364 | -0.0717 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.0993 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.0996 | Reported on the scored row. Not imputed. |
| Yield rate | 0.3377 | 2024 | 48.5 | -0.37 | 0.0418 | -0.1211 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 39. Shaw University (NC)

Residential rank 39. Watch-list rank 523. Published risk score 0.291. Federal composite score 1.20 (year 2025.0).

Endowment $14.3 million in 2023 ($16,492 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 199643. Fall headcount 964 in 2024 (undergraduate 877; graduate 87). FTE 867 in 2024. Fall headcount 1,291 in 2019 versus 964 in 2024 (-25%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.1 years of expenses (2023)
- enrollment is about 867 FTE (2024)
- endowment covers 0.4 years of expenses, $16,549 per FTE (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.124 | 2023 | 43.2 | -0.40 | 0.1840 | +0.2607 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.765 | 2024 | 57.3 | 0.25 | 0.0797 | +0.1486 | Reported on the scored row. Not imputed. |
| Endowment per FTE | 1.655e+04 | 2023 | 30.2 | -0.47 | 0.1018 | +0.1244 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.2748 | 2023 | 15.3 | -1.17 | 0.0405 | +0.0946 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0751 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.05192 | 2024 | 37.8 | -0.18 | 0.0192 | +0.0572 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.003472 | 2024 | 44.7 | -0.13 | 0.0388 | +0.0541 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.2 | 2025 | 7.4 | -1.50 | 0.0966 | +0.0421 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Staff change, 5 years | -0.1574 | 2024 | 25.3 | -0.38 | 0.0103 | +0.0415 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.4404 | 2023 | 74.3 | 0.83 | 0.0204 | +0.0329 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0033 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0027 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0026 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0023 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 0.5284 | 2024 | 70.2 | 0.06 | 0.0080 | +0.0011 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0009 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0013 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0025 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.3712 | 2023 | 5.3 | -1.45 | 0.0075 | -0.0033 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0046 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.1677 | 2024 | 82.2 | 0.73 | 0.0148 | -0.0050 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 1 | 2025 | 100.0 | 4.81 | 0.0009 | -0.0073 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 10 years | -0.4307 | 2024 | 16.0 | -0.63 | 0.0046 | -0.0089 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.1078 | 2024 | 14.3 | -0.56 | 0.0212 | -0.0114 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 4.764 | 2024 | 26.8 | -0.49 | 0.0347 | -0.0116 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0117 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0128 | Reported on the scored row. Not imputed. |
| Admit rate | 0.8016 | 2024 | 56.7 | 0.34 | 0.0252 | -0.0202 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 5 | 2025 | 100.0 | 5.42 | 0.0023 | -0.0213 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 2 | 2023 | 73.1 | 0.25 | 0.0338 | -0.0388 | Reported on the scored row. Not imputed. |
| Yield rate | 0.08347 | 2024 | 4.7 | -1.15 | 0.0418 | -0.0407 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.3065 | 2024 | 85.1 | 0.48 | 0.0119 | -0.0452 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.2757 | 2024 | 18.8 | -0.57 | 0.0125 | -0.0502 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.2375 | 2023 | 96.8 | 2.01 | 0.0198 | -0.0714 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.04486 | 2025 | 70.8 | 0.35 | 0.0364 | -0.0719 | Reported on the scored row. Not imputed. |
| Operating margin | -0.3155 | 2023 | 6.4 | -1.34 | 0.0479 | -0.0740 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1619 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 40. Ottawa University-Surprise (AZ)

Residential rank 40. Watch-list rank 534. Published risk score 0.286. Federal composite score missing.

Endowment $25.9 million in 2023 ($31,074 per FTE). Scope: parent filing. Source: IPEDS finance F2H02/F1H02 for UNITID 155627 (Ottawa University-Ottawa), the campus that files in this extract. Fall headcount 912 in 2024 (undergraduate 837; graduate 75). FTE 833 in 2024. Fall headcount 806 in 2019 versus 912 in 2024 (+13%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract. finance from parent UNITID 155627. The figure is the Ottawa University-Ottawa filing, not a separate endowment measured for this campus alone. Enrollment on this card is this campus's own headcount and FTE.

Top drivers:

- endowment covers 0.4 years of expenses, $33,792 per FTE (2023)
- net assets cover 0.4 years of expenses (2023)
- enrollment is about 833 FTE (2024)

Missing or imputed:

Endowment per FTE: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Net assets per dollar of expense: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Operating-margin change, 5 years: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Discount rate: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Operating margin: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Tuition share of revenue: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Enrollment change, 10 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Tuition is at least 70% of revenue: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Discount-rate change, 5 years: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. | Federal composite score: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Negative-margin years in the last 5: Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count.

Data-quality flags:

finance from parent UNITID 155627

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Endowment per FTE | 3.379e+04 | 2023 | 46.0 | -0.41 | 0.1018 | +0.2568 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Net assets per dollar of expense | 0.356 | 2023 | 28.1 | -0.73 | 0.1840 | +0.2565 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Log enrollment (FTE) | 6.725 | 2024 | 55.9 | 0.23 | 0.0797 | +0.2001 | Reported on the scored row. Not imputed. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0748 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.09029 | 2023 | 23.6 | -0.41 | 0.0075 | +0.0601 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Staff change, 5 years | 0.1071 | 2024 | 70.9 | 0.04 | 0.0103 | +0.0588 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.08747 | 2024 | 73.6 | 0.21 | 0.0388 | +0.0507 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.4718 | 2023 | 78.2 | 0.96 | 0.0204 | +0.0495 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Operating margin | -0.04767 | 2023 | 23.4 | -0.33 | 0.0479 | +0.0420 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Yield-rate change, 5 years | -0.1911 | 2024 | 8.8 | -1.05 | 0.0192 | +0.0333 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0168 | Reported on the scored row. Not imputed. |
| Tuition share of revenue | 0.603 | 2023 | 47.0 | -0.07 | 0.0405 | +0.0161 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Enrollment change, 10 years |  | 2024 |  |  | 0.0046 | +0.0051 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0018 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0017 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0017 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0013 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 0 | 2025 | 20.2 | -1.99 | 0.0026 | +0.0013 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0009 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Staff change, 1 year | -0.08824 | 2024 | 17.7 | -0.47 | 0.0212 | +0.0005 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 |  |  |  |  | 0.0000 | -0.0000 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0019 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 1.447 | 2024 | 83.0 | 0.23 | 0.0080 | -0.0022 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone |  |  |  |  | 0.0009 | -0.0033 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0036 | Reported on the scored row. Not imputed. |
| Admit rate | 0.7815 | 2024 | 53.1 | 0.26 | 0.0252 | -0.0057 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | 0.1634 | 2024 | 71.1 | 0.03 | 0.0125 | -0.0102 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0172 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0251 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | 0.3223 | 2024 | 85.7 | 0.51 | 0.0119 | -0.0314 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.35 | 2024 | 93.9 | 1.67 | 0.0148 | -0.0339 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.1388 | 2023 | 91.7 | 1.05 | 0.0198 | -0.0360 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Yield rate | 0.2635 | 2024 | 42.4 | -0.60 | 0.0418 | -0.0479 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score |  |  |  |  | 0.0966 | -0.0552 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Students per staff member | 8.957 | 2024 | 59.9 | -0.17 | 0.0347 | -0.0557 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.1121 | 2025 | 96.9 | 1.29 | 0.0364 | -0.0613 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.0820 | Copied from the parent campus finance row UNITID 155627, then winsorized with the rest of the panel. Enrollment is this campus's own count. |
| Finance copied from a parent campus | 1 | 2023 | 100.0 | 4.64 | 0.0031 | -0.3940 | Reported on the scored row. Not imputed. |

### 41. Inter American University of Puerto Rico-Metro (PR)

Residential rank 41. Watch-list rank 548. Published risk score 0.277. Federal composite score 3.00 (year 2025.0).

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 242653; endowment_end (F2H02/F1H02) is blank. Fall headcount 4,101 in 2024 (undergraduate 2,711; graduate 1,390). FTE 3,212 in 2024. Fall headcount 7,791 in 2019 versus 4,101 in 2024 (-47%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- the federal composite score is 3.00 (2025)
- tuition is 54% of revenue (2023)
- State high-school graduates, 5-year change is missing on the scored row

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | State high-school graduates, 5-year change: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Net assets per dollar of expense: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Federal composite score | 3 | 2025 | 100.0 | 0.77 | 0.0966 | +0.1897 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.5405 | 2023 | 40.5 | -0.28 | 0.0405 | +0.1265 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change |  |  |  |  | 0.0364 | +0.1017 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Operating margin | 0.05267 | 2023 | 47.4 | 0.06 | 0.0479 | +0.0842 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0702 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.01864 | 2024 | 35.8 | -0.22 | 0.0388 | +0.0641 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 0 | 2023 | 27.5 | -1.14 | 0.0338 | +0.0572 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 8.075 | 2024 | 87.7 | 1.04 | 0.0797 | +0.0446 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.05572 | 2023 | 29.6 | -0.29 | 0.0075 | +0.0381 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.2819 | 2024 | 12.5 | -0.58 | 0.0103 | +0.0208 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.5946 | 2024 | 8.2 | -0.79 | 0.0046 | +0.0096 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | +0.0076 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | 0.03081 | 2024 | 58.1 | -0.09 | 0.0119 | +0.0076 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0032 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | 0.2636 | 2024 | 62.2 | 0.01 | 0.0080 | +0.0026 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0018 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0009 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0007 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0001 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0015 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0020 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0063 | Reported on the scored row. Not imputed. |
| Admit rate | 0.6972 | 2024 | 38.7 | -0.10 | 0.0252 | -0.0107 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0137 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.4367 | 2024 | 96.3 | 2.12 | 0.0148 | -0.0148 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.543 | 2024 | 0.7 | -3.27 | 0.0192 | -0.0152 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0187 | Reported on the scored row. Not imputed. |
| Discount rate | 0.04481 | 2023 | 34.9 | -0.85 | 0.0204 | -0.0237 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.04859 | 2024 | 26.1 | -0.30 | 0.0212 | -0.0237 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.0316 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Discount-rate change, 5 years | -0.03876 | 2023 | 12.2 | -0.68 | 0.0198 | -0.0375 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.2746 | 2024 | 43.7 | -0.56 | 0.0418 | -0.0622 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 8.634 | 2024 | 58.1 | -0.19 | 0.0347 | -0.0688 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense |  | 2023 |  |  | 0.1840 | -0.0758 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Enrollment change, 5 years | -0.4987 | 2024 | 7.3 | -0.87 | 0.0125 | -0.0850 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.0863 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 42. La Roche University (PA)

Residential rank 42. Watch-list rank 561. Published risk score 0.271. Federal composite score 1.80 (year 2025.0).

Endowment $13.8 million in 2023 ($12,002 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 213358. Fall headcount 2,153 in 2024 (undergraduate 1,828; graduate 325). FTE 1,146 in 2024. Fall headcount 1,401 in 2019 versus 2,153 in 2024 (+54%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.5 years of expenses (2023)
- endowment covers 0.4 years of expenses, $10,106 per FTE (2023)
- enrollment is about 1,146 FTE (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

The model's five-year enrollment feature is the FTE change (-10%). Fall headcount changed +54% over the years shown on the card. Those are different counts.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.5075 | 2023 | 31.1 | -0.67 | 0.1840 | +0.2375 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 1.011e+04 | 2023 | 20.9 | -0.50 | 0.1018 | +0.1183 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.044 | 2024 | 64.6 | 0.42 | 0.0797 | +0.0892 | Reported on the scored row. Not imputed. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0668 | Reported on the scored row. Not imputed. |
| Federal composite score | 1.8 | 2025 | 18.9 | -0.74 | 0.0966 | +0.0449 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Staff change, 5 years | -0.1659 | 2024 | 24.0 | -0.40 | 0.0103 | +0.0433 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.3626 | 2023 | 65.5 | 0.50 | 0.0204 | +0.0376 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.07147 | 2024 | 28.7 | -0.30 | 0.0192 | +0.0292 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.7079 | 2023 | 56.6 | 0.28 | 0.0405 | +0.0240 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.06752 | 2023 | 27.1 | -0.33 | 0.0075 | +0.0104 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -0.4735 | 2024 | 24.6 | -0.14 | 0.0080 | +0.0087 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.1347 | 2023 | 13.7 | -0.66 | 0.0479 | +0.0085 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0083 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0076 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.1033 | 2024 | 43.9 | -0.31 | 0.0046 | +0.0063 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0031 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0026 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0024 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0016 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.1026 | 2024 | 37.8 | -0.33 | 0.0125 | +0.0007 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0006 | Carried forward from the last official composite year. composite_is_lagged is true. |
| First-time enrollment change, 1 year | -0.1512 | 2024 | 21.1 | -0.47 | 0.0119 | +0.0004 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | -0.2367 | 2024 | 7.9 | -1.35 | 0.0148 | -0.0002 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.095 | 2024 | 15.8 | -0.51 | 0.0212 | -0.0007 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0012 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | -0.0013 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0015 | Reported on the scored row. Not imputed. |
| Students per staff member | 6.331 | 2024 | 43.2 | -0.37 | 0.0347 | -0.0092 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0114 | Reported on the scored row. Not imputed. |
| Admit rate | 0.7576 | 2024 | 48.6 | 0.16 | 0.0252 | -0.0215 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.05664 | 2023 | 9.4 | -0.85 | 0.0198 | -0.0256 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.0555 | Reported on the scored row. Not imputed. |
| Yield rate | 0.09753 | 2024 | 7.0 | -1.11 | 0.0418 | -0.0582 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.158 | 2024 | 10.8 | -0.78 | 0.0388 | -0.0599 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.03434 | 2025 | 20.2 | -0.77 | 0.0364 | -0.0623 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1961 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 43. Shasta Bible College and Graduate School (CA)

Residential rank 43. Watch-list rank 588. Published risk score 0.263. Federal composite score 2.20 (year 2025.0).

Endowment $47,615 in 2023 ($2,976 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 123280. Fall headcount 25 in 2024 (undergraduate 21; graduate 4). FTE 16 in 2024. Fall headcount 41 in 2019 versus 25 in 2024 (-39%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 2.1 years of expenses (2023)
- tuition is 22% of revenue (2023)
- the federal composite score is 2.20 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 2.103 | 2023 | 63.6 | 0.03 | 0.1840 | +0.1679 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.2191 | 2023 | 11.2 | -1.36 | 0.0405 | +0.1172 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.2 | 2025 | 32.3 | -0.24 | 0.0966 | +0.0997 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 1 year | 0.1429 | 2024 | 82.1 | 0.43 | 0.0388 | +0.0817 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.8333 | 2024 | 80.7 | 1.16 | 0.0418 | +0.0764 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 3401 | 2023 | 9.6 | -0.52 | 0.1018 | +0.0761 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0400 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | -0.3333 | 2024 | 10.3 | -0.67 | 0.0103 | +0.0272 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 1 | 2024 | 100.0 | 1.19 | 0.0252 | +0.0177 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0 | 2024 | 46.6 | -0.13 | 0.0148 | +0.0155 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0 | 2024 | 51.1 | -0.09 | 0.0212 | +0.0087 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | +0.0065 | Reported on the scored row. Not imputed. |
| Students per staff member | 4 | 2024 | 19.1 | -0.55 | 0.0347 | +0.0047 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 0.5 | 2024 | 69.3 | 0.05 | 0.0080 | +0.0041 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0033 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0030 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | +0.0029 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | -0.6175 | 2023 | 2.5 | -2.35 | 0.0075 | +0.0019 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0017 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0010 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0009 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 1 | 2025 | 100.0 | 2.68 | 0.0001 | -0.0002 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0019 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0035 | Reported on the scored row. Not imputed. |
| Discount rate | 0.08926 | 2023 | 41.2 | -0.66 | 0.0204 | -0.0076 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0085 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0126 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | -0.03388 | 2023 | 13.1 | -0.63 | 0.0198 | -0.0145 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.004182 | 2025 | 46.1 | -0.22 | 0.0364 | -0.0263 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | 2.168 | 2024 | 100.0 | 4.33 | 0.0119 | -0.0316 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 2 | 2023 | 73.1 | 0.25 | 0.0338 | -0.0330 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.5556 | 2024 | 9.5 | -0.75 | 0.0046 | -0.0431 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.4074 | 2024 | 10.8 | -0.74 | 0.0125 | -0.0505 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.3289 | 2023 | 6.2 | -1.39 | 0.0479 | -0.0554 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | 0.3333 | 2024 | 96.2 | 2.24 | 0.0192 | -0.0582 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.0642 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Log enrollment (FTE) | 2.773 | 2024 | 2.1 | -2.15 | 0.0797 | -0.1078 | Reported on the scored row. Not imputed. |

### 44. Greenville University (IL)

Residential rank 44. Watch-list rank 590. Published risk score 0.262. Federal composite score 2.20 (year 2025.0).

Endowment $28.6 million in 2023 ($26,742 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 145372. Fall headcount 1,104 in 2024 (undergraduate 986; graduate 118). FTE 1,069 in 2024. Fall headcount 1,092 in 2019 versus 1,104 in 2024 (+1%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.9 years of expenses (2023)
- enrollment is about 1,069 FTE (2024)
- endowment covers 0.9 years of expenses, $28,082 per FTE (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.885 | 2023 | 59.3 | -0.06 | 0.1840 | +0.1709 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 6.974 | 2024 | 63.0 | 0.38 | 0.0797 | +0.0911 | Reported on the scored row. Not imputed. |
| Endowment per FTE | 2.808e+04 | 2023 | 40.8 | -0.43 | 0.1018 | +0.0909 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 2.2 | 2025 | 32.3 | -0.24 | 0.0966 | +0.0881 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.2886 | 2023 | 16.5 | -1.13 | 0.0405 | +0.0814 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | 0.1897 | 2023 | 78.4 | 0.57 | 0.0479 | +0.0688 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0496 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | 0.0501 | 2024 | 64.4 | 0.06 | 0.0388 | +0.0328 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.1404 | 2024 | 27.4 | -0.36 | 0.0103 | +0.0317 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.09029 | 2024 | 22.6 | -0.42 | 0.0192 | +0.0313 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.5717 | 2023 | 89.0 | 1.39 | 0.0204 | +0.0311 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0125 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.1681 | 2024 | 37.3 | -0.37 | 0.0046 | +0.0077 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0031 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0028 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0025 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0021 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.05632 | 2024 | 60.1 | -0.12 | 0.0125 | +0.0010 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0007 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0007 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0006 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Student-staff ratio change, 1 year | 0.8696 | 2024 | 76.6 | 0.12 | 0.0080 | -0.0006 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0021 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0028 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0090 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0119 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.07547 | 2024 | 20.1 | -0.42 | 0.0212 | -0.0131 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.2357 | 2023 | 86.6 | 0.78 | 0.0075 | -0.0187 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 2 | 2023 | 73.1 | 0.25 | 0.0338 | -0.0210 | Reported on the scored row. Not imputed. |
| Students per staff member | 7.272 | 2024 | 51.0 | -0.29 | 0.0347 | -0.0263 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1489 | 2024 | 23.5 | -0.95 | 0.0418 | -0.0267 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.975 | 2024 | 85.8 | 1.08 | 0.0252 | -0.0307 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.2143 | 2024 | 80.1 | 0.28 | 0.0119 | -0.0412 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | 0.0953 | 2023 | 83.1 | 0.63 | 0.0198 | -0.0413 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.4138 | 2024 | 95.8 | 2.00 | 0.0148 | -0.0456 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | -0.0394 | 2025 | 14.2 | -0.84 | 0.0364 | -0.0752 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1962 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 45. Paine College (GA)

Residential rank 45. Watch-list rank 596. Published risk score 0.258. Federal composite score 1.20 (year 2025.0).

Endowment $11.6 million in 2023 ($63,255 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 140720. Fall headcount 390 in 2024 (undergraduate 390; graduate not reported). FTE 184 in 2024. Fall headcount 448 in 2019 versus 390 in 2024 (-13%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- endowment covers 0.8 years of expenses, $39,189 per FTE (2023)
- net assets cover 1.1 years of expenses (2023)
- tuition is 31% of revenue (2023)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

Five-year FTE change is -54%, an outlier against a typical campus. | The model's five-year enrollment feature is the FTE change (-54%). Fall headcount changed -13% over the years shown on the card. Those are different counts.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Endowment per FTE | 3.919e+04 | 2023 | 50.1 | -0.39 | 0.1018 | +0.2446 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Net assets per dollar of expense | 1.144 | 2023 | 43.5 | -0.39 | 0.1840 | +0.2271 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.3148 | 2023 | 18.8 | -1.04 | 0.0405 | +0.0962 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0462 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | -0.2645 | 2024 | 14.1 | -0.56 | 0.0103 | +0.0446 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score | 1.2 | 2025 | 7.4 | -1.50 | 0.0966 | +0.0410 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | -0.09406 | 2023 | 17.4 | -0.50 | 0.0479 | +0.0297 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.0154 | 2024 | 58.5 | 0.05 | 0.0192 | +0.0242 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | -0.187 | 2023 | 13.3 | -0.77 | 0.0075 | +0.0058 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 2.067 | 2024 | 6.4 | -0.70 | 0.0347 | +0.0057 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.1717 | 2023 | 48.8 | -0.31 | 0.0204 | +0.0055 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0031 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.1167 | 2024 | 26.3 | -0.40 | 0.0119 | +0.0025 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0020 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0016 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0005 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0007 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0011 | Reported on the scored row. Not imputed. |
| Student-staff ratio change, 1 year | -1.026 | 2024 | 17.0 | -0.24 | 0.0080 | -0.0013 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0042 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | -0.0509 | 2023 | 10.3 | -0.79 | 0.0198 | -0.0043 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone | 1 | 2025 | 100.0 | 4.81 | 0.0009 | -0.0053 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment down more than 30% in 5 years | 1 | 2024 | 100.0 | 2.19 | 0.0033 | -0.0073 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.07292 | 2024 | 20.6 | -0.41 | 0.0212 | -0.0108 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.762 | 2024 | 4.0 | -0.96 | 0.0046 | -0.0120 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 5 | 2025 | 100.0 | 5.42 | 0.0023 | -0.0140 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 2 | 2023 | 73.1 | 0.25 | 0.0338 | -0.0145 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0172 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.3049 | 2024 | 92.2 | 1.44 | 0.0148 | -0.0443 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.9543 | 2024 | 82.4 | 0.99 | 0.0252 | -0.0484 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | -0.3805 | 2024 | 4.0 | -1.67 | 0.0388 | -0.0490 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.07472 | 2025 | 86.3 | 0.77 | 0.0364 | -0.0530 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.0544 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Log enrollment (FTE) | 5.215 | 2024 | 24.7 | -0.68 | 0.0797 | -0.0607 | Reported on the scored row. Not imputed. |
| Yield rate | 0.08347 | 2024 | 4.7 | -1.15 | 0.0418 | -0.0638 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.5365 | 2024 | 6.3 | -0.92 | 0.0125 | -0.0782 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |

### 46. Indian Bible College (AZ)

Residential rank 46. Watch-list rank 597. Published risk score 0.258. Federal composite score missing.

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 495280; endowment_end (F2H02/F1H02) is blank. Fall headcount 38 in 2024 (undergraduate 38; graduate not reported). FTE 22 in 2024. Five-year fall headcount is not available. Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.6 years of expenses (2023)
- tuition is 12% of revenue (2023)
- 0 of the last 5 years show a negative margin

Missing or imputed:

Discount-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | First-time enrollment change, 1 year: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Staff change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Enrollment change, 10 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Admit-rate change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Operating-margin change, 5 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Yield rate: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Federal composite score: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank.

Data-quality flags:

This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.591 | 2023 | 54.0 | -0.19 | 0.1840 | +0.2211 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.1159 | 2023 | 5.4 | -1.71 | 0.0405 | +0.1126 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 0 | 2023 | 27.5 | -1.14 | 0.0338 | +0.0585 | Reported on the scored row. Not imputed. |
| Operating margin | 0.01601 | 2023 | 38.1 | -0.08 | 0.0479 | +0.0569 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0540 | Reported on the scored row. Not imputed. |
| Discount rate | 0.2931 | 2023 | 58.6 | 0.20 | 0.0204 | +0.0192 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years |  | 2023 |  |  | 0.0198 | +0.0168 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0142 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.04348 | 2024 | 45.3 | -0.25 | 0.0125 | +0.0081 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years |  |  |  |  | 0.0192 | +0.0048 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0041 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year |  |  |  |  | 0.0119 | +0.0038 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Staff change, 5 years |  | 2024 |  |  | 0.0103 | +0.0036 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Staff change, 1 year | 0.1667 | 2024 | 89.1 | 0.65 | 0.0212 | +0.0031 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0027 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years |  | 2024 |  |  | 0.0046 | +0.0026 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Admit rate |  |  |  |  | 0.0252 | +0.0017 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Student-staff ratio change, 1 year | -0.5119 | 2024 | 24.0 | -0.14 | 0.0080 | +0.0013 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years |  |  |  |  | 0.0148 | +0.0013 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0012 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0011 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0007 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 0 | 2025 | 20.2 | -1.99 | 0.0026 | +0.0004 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 |  |  |  |  | 0.0000 | -0.0000 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years |  | 2023 |  |  | 0.0075 | -0.0002 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0023 | Reported on the scored row. Not imputed. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0037 | Reported on the scored row. Not imputed. |
| Yield rate |  |  |  |  | 0.0418 | -0.0042 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Students per staff member | 1.571 | 2024 | 3.9 | -0.74 | 0.0347 | -0.0051 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone |  |  |  |  | 0.0009 | -0.0055 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.12 | 2024 | 14.2 | -0.63 | 0.0388 | -0.0069 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0129 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0138 | Reported on the scored row. Not imputed. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.0339 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| State high-school graduates, 5-year change | 0.1121 | 2025 | 96.9 | 1.29 | 0.0364 | -0.0471 | Reported on the scored row. Not imputed. |
| Federal composite score |  |  |  |  | 0.0966 | -0.0674 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| Log enrollment (FTE) | 3.091 | 2024 | 3.4 | -1.96 | 0.0797 | -0.1561 | Reported on the scored row. Not imputed. |

### 47. Columbia International University (SC)

Residential rank 47. Watch-list rank 602. Published risk score 0.255. Federal composite score 2.40 (year 2025.0).

Endowment $5.1 million in 2023 ($2,399 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 217925. Fall headcount 2,914 in 2024 (undergraduate 965; graduate 1,949). FTE 2,136 in 2024. Fall headcount 1,649 in 2019 versus 2,914 in 2024 (+77%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.4 years of expenses (2023)
- tuition is 38% of revenue (2023)
- enrollment is about 2,136 FTE (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

Five-year FTE change is +72%, an outlier against a typical campus.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.364 | 2023 | 48.6 | -0.29 | 0.1840 | +0.1312 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.3766 | 2023 | 24.0 | -0.83 | 0.0405 | +0.1299 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.667 | 2024 | 79.3 | 0.79 | 0.0797 | +0.1117 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.4 | 2025 | 41.1 | 0.01 | 0.0966 | +0.0992 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Operating margin | 0.04216 | 2023 | 45.0 | 0.01 | 0.0479 | +0.0637 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 1 year | 0.2213 | 2024 | 88.0 | 0.75 | 0.0388 | +0.0579 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 2930 | 2023 | 8.8 | -0.52 | 0.1018 | +0.0573 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0517 | Reported on the scored row. Not imputed. |
| Discount rate | 0.2943 | 2023 | 58.8 | 0.21 | 0.0204 | +0.0327 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.004425 | 2024 | 49.9 | -0.14 | 0.0103 | +0.0245 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.1863 | 2023 | 82.5 | 0.60 | 0.0075 | +0.0100 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 2.082 | 2024 | 87.1 | 0.36 | 0.0080 | +0.0093 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0032 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0030 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0008 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0007 | Reported on the scored row. Not imputed. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0006 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0005 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Enrollment change, 10 years | 1.433 | 2024 | 92.1 | 1.20 | 0.0046 | +0.0005 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0004 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0015 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.7212 | 2024 | 89.7 | 0.78 | 0.0125 | -0.0021 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0065 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0074 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | -0.4687 | 2024 | 1.7 | -2.80 | 0.0192 | -0.0082 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0139 | Reported on the scored row. Not imputed. |
| Staff change, 1 year | -0.04661 | 2024 | 26.6 | -0.29 | 0.0212 | -0.0175 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.06438 | 2023 | 8.6 | -0.93 | 0.0198 | -0.0238 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.1126 | 2025 | 98.1 | 1.30 | 0.0364 | -0.0245 | Reported on the scored row. Not imputed. |
| Admit rate | 0.9447 | 2024 | 81.1 | 0.95 | 0.0252 | -0.0328 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 9.493 | 2024 | 62.4 | -0.12 | 0.0347 | -0.0337 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.4655 | 2024 | 96.7 | 2.26 | 0.0148 | -0.0420 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | 0.1897 | 2024 | 78.6 | 0.23 | 0.0119 | -0.0445 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 3 | 2023 | 87.6 | 0.94 | 0.0338 | -0.0467 | Reported on the scored row. Not imputed. |
| Yield rate | 0.3511 | 2024 | 49.3 | -0.33 | 0.0418 | -0.0531 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1984 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 48. Christian Brothers University (TN)

Residential rank 48. Watch-list rank 605. Published risk score 0.254. Federal composite score 2.70 (year 2025.0).

Endowment $44.3 million in 2023 ($30,405 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 219833. Fall headcount 1,772 in 2024 (undergraduate 1,155; graduate 617). FTE 1,458 in 2024. Fall headcount 1,968 in 2019 versus 1,772 in 2024 (-10%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 1.8 years of expenses (2023)
- enrollment is about 1,458 FTE (2024)
- the federal composite score is 2.70 (2025)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 1.813 | 2023 | 57.9 | -0.09 | 0.1840 | +0.1951 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.285 | 2024 | 70.5 | 0.56 | 0.0797 | +0.1012 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.7 | 2025 | 56.2 | 0.39 | 0.0966 | +0.0986 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.5158 | 2023 | 37.9 | -0.36 | 0.0405 | +0.0636 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | 0.0102 | 2023 | 36.2 | -0.11 | 0.0479 | +0.0602 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 2.327e+04 | 2023 | 36.8 | -0.45 | 0.1018 | +0.0566 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0506 | Reported on the scored row. Not imputed. |
| Discount rate | 0.491 | 2023 | 80.5 | 1.04 | 0.0204 | +0.0421 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.1464 | 2024 | 26.4 | -0.37 | 0.0103 | +0.0350 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | -0.07223 | 2024 | 28.4 | -0.31 | 0.0192 | +0.0210 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -0.9033 | 2024 | 18.3 | -0.22 | 0.0080 | +0.0080 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| First-time enrollment change, 1 year | -0.125 | 2024 | 24.7 | -0.42 | 0.0119 | +0.0065 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 10 years | -0.1837 | 2024 | 35.5 | -0.39 | 0.0046 | +0.0064 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.05512 | 2023 | 58.4 | 0.12 | 0.0075 | +0.0062 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0031 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0028 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0025 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0022 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0021 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0017 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0005 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0001 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0014 | Reported on the scored row. Not imputed. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0036 | Reported on the scored row. Not imputed. |
| Students per staff member | 6.1 | 2024 | 41.3 | -0.39 | 0.0347 | -0.0045 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 1 | 2025 | 100.0 | 0.90 | 0.0050 | -0.0066 | Reported on the scored row. Not imputed. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0110 | Reported on the scored row. Not imputed. |
| Admit rate | 0.867 | 2024 | 67.7 | 0.62 | 0.0252 | -0.0139 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 2 | 2023 | 73.1 | 0.25 | 0.0338 | -0.0187 | Reported on the scored row. Not imputed. |
| Admit-rate change, 5 years | 0.3655 | 2024 | 94.5 | 1.75 | 0.0148 | -0.0203 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | -0.1213 | 2024 | 12.6 | -0.62 | 0.0212 | -0.0237 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Enrollment change, 5 years | -0.2115 | 2024 | 24.9 | -0.48 | 0.0125 | -0.0312 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.01183 | 2023 | 20.8 | -0.41 | 0.0198 | -0.0397 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.1342 | 2024 | 18.7 | -0.99 | 0.0418 | -0.0416 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.04232 | 2025 | 67.0 | 0.31 | 0.0364 | -0.0494 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.2346 | 2024 | 6.9 | -1.09 | 0.0388 | -0.0624 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.2079 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 49. Upper Iowa University (IA)

Residential rank 49. Watch-list rank 609. Published risk score 0.252. Federal composite score 2.10 (year 2025.0).

Endowment $21.8 million in 2023 ($7,541 per FTE). Scope: this campus. Source: IPEDS finance 2023 endowment_end (FASB F2H02 or GASB F1H02) for UNITID 154493. Fall headcount 3,941 in 2024 (undergraduate 3,054; graduate 887). FTE 2,892 in 2024. Fall headcount 4,279 in 2019 versus 3,941 in 2024 (-8%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.6 years of expenses (2023)
- enrollment is about 2,892 FTE (2024)
- FTE enrollment changed +22% in one year (2024)

Missing or imputed:

Federal composite score: Carried forward from the last official composite year. composite_is_lagged is true. | Composite in the 1.0–1.5 zone: Carried forward from the last official composite year. composite_is_lagged is true. | Composite below 1.0: Carried forward from the last official composite year. composite_is_lagged is true. | Composite score is carried forward: Carried forward from the last official composite year. composite_is_lagged is true.

Data-quality flags:

None.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.6028 | 2023 | 32.7 | -0.63 | 0.1840 | +0.1675 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Log enrollment (FTE) | 7.97 | 2024 | 85.5 | 0.98 | 0.0797 | +0.1059 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | 0.2234 | 2024 | 88.1 | 0.76 | 0.0388 | +0.0778 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Endowment per FTE | 9225 | 2023 | 19.9 | -0.50 | 0.1018 | +0.0775 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | -0.01066 | 2023 | 30.2 | -0.19 | 0.0479 | +0.0520 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0472 | Reported on the scored row. Not imputed. |
| Federal composite score | 2.1 | 2025 | 24.5 | -0.36 | 0.0966 | +0.0470 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Tuition share of revenue | 0.6409 | 2023 | 50.4 | 0.06 | 0.0405 | +0.0436 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.2811 | 2023 | 57.2 | 0.15 | 0.0204 | +0.0305 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 5 years | -0.3708 | 2024 | 8.3 | -0.73 | 0.0103 | +0.0279 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.03226 | 2024 | 63.3 | 0.06 | 0.0212 | +0.0277 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Rural locale | 1 | 2025 | 100.0 | 3.91 | 0.0030 | +0.0202 | Reported on the scored row. Not imputed. |
| Operating-margin change, 5 years | 0.04292 | 2023 | 54.7 | 0.08 | 0.0075 | +0.0172 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | 2.017 | 2024 | 86.7 | 0.34 | 0.0080 | +0.0103 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0076 | Reported on the scored row. Not imputed. |
| First-time enrollment change, 1 year | -0.06329 | 2024 | 35.9 | -0.29 | 0.0119 | +0.0051 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0030 | Reported on the scored row. Not imputed. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0026 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0021 | Reported on the scored row. Not imputed. |
| Composite in the 1.0–1.5 zone | 0 | 2025 | 95.9 | -0.21 | 0.0009 | +0.0007 | Carried forward from the last official composite year. composite_is_lagged is true. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0006 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0006 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 0 | 2023 | 55.7 | -0.89 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 | 0 | 2025 | 94.9 | -0.23 | 0.0000 | -0.0000 | Carried forward from the last official composite year. composite_is_lagged is true. |
| FTE under 1,000 | 0 | 2024 | 38.9 | -1.25 | 0.0115 | -0.0000 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | -0.0054 | Reported on the scored row. Not imputed. |
| Yield-rate change, 5 years | 0.08404 | 2024 | 83.0 | 0.68 | 0.0192 | -0.0059 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0100 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years | -0.4666 | 2024 | 14.3 | -0.67 | 0.0046 | -0.0131 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit rate | 0.9646 | 2024 | 84.6 | 1.04 | 0.0252 | -0.0256 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Students per staff member | 12.91 | 2024 | 73.7 | 0.14 | 0.0347 | -0.0288 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.3394 | 2024 | 48.5 | -0.36 | 0.0418 | -0.0290 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| State high-school graduates, 5-year change | 0.07143 | 2025 | 83.8 | 0.72 | 0.0364 | -0.0300 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | -0.2498 | 2024 | 21.3 | -0.53 | 0.0125 | -0.0312 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.4518 | 2024 | 96.5 | 2.19 | 0.0148 | -0.0403 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount-rate change, 5 years | -0.0217 | 2023 | 17.1 | -0.51 | 0.0198 | -0.0406 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Negative-margin years in the last 5 | 4 | 2023 | 95.6 | 1.64 | 0.0338 | -0.0890 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 1 | 2025 | 100.0 | 0.50 | 0.0026 | -0.1973 | Carried forward from the last official composite year. composite_is_lagged is true. |

### 50. Urshan University (MO)

Residential rank 50. Watch-list rank 612. Published risk score 0.251. Federal composite score missing.

Endowment not reported in 2023. Scope: not reported. Source: IPEDS finance 2023 for UNITID 494685; endowment_end (F2H02/F1H02) is blank. Fall headcount 474 in 2024 (undergraduate 474; graduate not reported). FTE 453 in 2024. Fall headcount 309 in 2019 versus 474 in 2024 (+53%). Enrollment source: IPEDS fall enrollment and 12-month enrollment FTE, Urban extract.

Top drivers:

- net assets cover 0.2 years of expenses (2023)
- yield is 84% (2024)
- the operating margin is +11% (2023)

Missing or imputed:

Enrollment change, 10 years: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Endowment per FTE: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. | Federal composite score: Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank.

Data-quality flags:

Five-year FTE change is +59%, an outlier against a typical campus. | This nonprofit filed IPEDS finance and left endowment assets blank. No confirmed Form 990 endowment was substituted.

| Feature | Raw value | Year | Percentile | Z-score | Weight | Contribution | How the model saw it |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Net assets per dollar of expense | 0.2076 | 2023 | 23.0 | -0.80 | 0.1840 | +0.1213 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield rate | 0.8387 | 2024 | 80.9 | 1.18 | 0.0418 | +0.0804 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating margin | 0.1092 | 2023 | 62.0 | 0.27 | 0.0479 | +0.0768 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Sector | 2 | 2025 | 65.3 | -0.61 | 0.0331 | +0.0577 | Reported on the scored row. Not imputed. |
| Students per staff member | 32.36 | 2024 | 96.1 | 1.64 | 0.0347 | +0.0406 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Tuition share of revenue | 0.8944 | 2023 | 71.4 | 0.91 | 0.0405 | +0.0379 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Admit-rate change, 5 years | 0.001299 | 2024 | 46.8 | -0.13 | 0.0148 | +0.0109 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Staff change, 1 year | 0.5556 | 2024 | 98.5 | 2.36 | 0.0212 | +0.0097 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Operating-margin change, 5 years | 0.03408 | 2023 | 52.1 | 0.04 | 0.0075 | +0.0089 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Student-staff ratio change, 1 year | -22.2 | 2024 | 0.3 | -4.34 | 0.0080 | +0.0081 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Urban locale | 0 | 2025 | 44.6 | -1.11 | 0.0050 | +0.0070 | Reported on the scored row. Not imputed. |
| Enrollment change, 5 years | 0.5895 | 2024 | 87.5 | 0.60 | 0.0125 | +0.0055 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Control (2 nonprofit, 3 for-profit) | 2 | 2025 | 68.7 | -0.68 | 0.0010 | +0.0051 | Reported on the scored row. Not imputed. |
| Finance copied from a parent campus | 0 | 2023 | 95.6 | -0.22 | 0.0031 | +0.0036 | Reported on the scored row. Not imputed. |
| Four-year institution | 1 | 2025 | 100.0 | 0.52 | 0.0032 | +0.0029 | Reported on the scored row. Not imputed. |
| Enrollment down more than 30% in 5 years | 0 | 2024 | 82.8 | -0.46 | 0.0033 | +0.0020 | Reported on the scored row. Not imputed. |
| Finance missing on the scored row | 0 | 2023 | 97.8 | -0.15 | 0.0036 | +0.0013 | Reported on the scored row. Not imputed. |
| Enrollment change, 10 years |  | 2024 |  |  | 0.0046 | +0.0012 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| First-time enrollment change, 1 year | -0.1875 | 2024 | 17.2 | -0.55 | 0.0119 | +0.0007 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Years in the composite zone | 0 | 2025 | 96.7 | -0.18 | 0.0023 | +0.0006 | Reported on the scored row. Not imputed. |
| Composite score is carried forward | 0 | 2025 | 20.2 | -1.99 | 0.0026 | +0.0004 | Reported on the scored row. Not imputed. |
| Faith-related Carnegie class | 0 | 2025 | 87.8 | -0.37 | 0.0001 | +0.0000 | Reported on the scored row. Not imputed. |
| Composite below 1.0 |  |  |  |  | 0.0000 | -0.0000 | Reported on the scored row. Not imputed. |
| Tuition is at least 70% of revenue | 1 | 2023 | 100.0 | 1.12 | 0.0001 | -0.0000 | Reported on the scored row. Not imputed. |
| Rural locale | 0 | 2025 | 93.9 | -0.26 | 0.0030 | -0.0008 | Reported on the scored row. Not imputed. |
| Staff change, 5 years | 1 | 2024 | 96.2 | 1.48 | 0.0103 | -0.0048 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite in the 1.0–1.5 zone |  |  |  |  | 0.0009 | -0.0054 | Reported on the scored row. Not imputed. |
| Admit rate | 0.8378 | 2024 | 62.6 | 0.50 | 0.0252 | -0.0066 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| FTE under 1,000 | 1 | 2024 | 100.0 | 0.80 | 0.0115 | -0.0074 | Reported on the scored row. Not imputed. |
| Log enrollment (FTE) | 6.116 | 2024 | 40.2 | -0.14 | 0.0797 | -0.0106 | Reported on the scored row. Not imputed. |
| Enrollment change, 1 year | -0.07739 | 2024 | 20.8 | -0.45 | 0.0388 | -0.0109 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Yield-rate change, 5 years | 0.06859 | 2024 | 81.3 | 0.58 | 0.0192 | -0.0128 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Discount rate | 0.04915 | 2023 | 35.6 | -0.83 | 0.0204 | -0.0152 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Composite score missing | 1 | 2025 | 100.0 | 0.00 | 0.0158 | -0.0189 | Reported on the scored row. Not imputed. |
| Negative-margin years in the last 5 | 1 | 2023 | 52.2 | -0.44 | 0.0338 | -0.0263 | Reported on the scored row. Not imputed. |
| Endowment per FTE |  | 2023 |  |  | 0.1018 | -0.0274 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |
| State high-school graduates, 5-year change | 0.02616 | 2025 | 57.1 | 0.09 | 0.0364 | -0.0294 | Reported on the scored row. Not imputed. |
| Discount-rate change, 5 years | -0.1121 | 2023 | 5.1 | -1.39 | 0.0198 | -0.0341 | Reported on the scored row. Winsorized to the 1st–99th percentile of the feature panel before scoring. |
| Federal composite score |  |  |  |  | 0.0966 | -0.0440 | Left missing. The published XGBoost score follows the missing branch. It is not filled with a median or a zero. The logistic baseline would median-impute; that score is not the published rank. |

