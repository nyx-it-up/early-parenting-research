# State Paid Family Leave and Full-Time Working Mothers of Children Under 2 (NSCH, Exploratory)

**Status:** v0.1 (2026-11-11). **Exploratory.**
**Data:** NSCH 2023–2025 pooled, plus `data/reference/state_paid_family_leave.csv`. **Code:** `src/nsch_h1_state_policy.py`. **Tables:** `reports/tables/nsch_h1_state_policy/`.

**Question:** among mothers whose sampled child is under 2, is the mental health difference between full-time and other mothers different in states where paid family leave (PFL) bonding benefits were available?

**Why it is relevant:** the literature finds that more generous leave goes with better maternal mental health (Heshmati et al., 2023). Quasi-experimental studies of California and New Jersey find lower psychological distress among parents after PFL (Doran et al., 2020; Irish et al., 2021; Lee et al., 2020), and better coping with parenting demands (Bullinger, 2019). See `docs/literature-review.md` Section C.

**This analysis is associational.** PFL states differ from other states in many ways (income, prices, labor markets, other policies), and the comparison is cross-sectional.

## Policy data

`data/reference/state_paid_family_leave.csv` lists 17 states with a program, with the first date bonding benefits were payable, a source URL and a verification note for each row.

**Mandatory programs with benefits in 2023–2025 (10 "PFL states"):**
- **All three years:** CA, NJ, RI, NY, WA, DC, MA, CT.
- **Oregon:** from September 3, 2023.
- **Colorado:** from January 1, 2024.

**Not counted:**
- **Programs starting after 2025:** DE, MN, ME, MD, VA.
- **Voluntary insurance programs:** NH, VT.

**Sources:**
- **Official state pages:** WA, DC, OR, DE and MD, fetched directly.
- **Official-domain search excerpts:** the other states, whose pages blocked automated access. They are consistent with the National Partnership for Women & Families chart (April 2026).

## Methods

- **Mothers:** Adult 1 female and biological/adoptive parent, sampled child under 2. Employment collapsed to full-time / part-time / not employed.
- **Exposure:**
  - **Main, PFL at birth:** the state's program paid bonding benefits by the child's birth month (`BIRTH_YR`, `BIRTH_MO`; birth date taken as the 15th). Children with a birth-date quality flag (`BIRTH_YR_F` ≠ 0) are left out.
  - **Sensitivity, PFL in survey year:** benefits payable by July 1 of the survey year.
- **Model:** logistic regression with six employment × PFL groups and the H1 M1 covariates (year, income across six imputations, education, marital status, number of children, mother's age).
- **Estimates:** predictive margins in PFL and non-PFL states, the full-time minus other gaps within each, and the **difference in gaps**. The difference compares mothers within the same group of states, so it is less affected by other differences between the states.
- **Standard errors:** clustered by state (51 clusters), because the policy varies by state. Household-level stratified SEs are shown alongside.
- **Sample:** 6,479 (PFL at birth) and 6,679 (PFL in survey year) mothers of under-2s, of whom 1,161 and 1,291 live in PFL states (`sample_sizes.csv`).

## Results (`pfl_gaps.csv`)

**Fair or poor mental health, PFL at birth.** Adjusted %, and gaps in points (full-time minus the other group; positive = full-time worse). 95% CIs clustered by state:

| | Non-PFL states | PFL states | Difference (PFL − non-PFL) |
|---|---|---|---|
| Full-time | 7.5% | 6.8% | |
| Part-time | 6.2% | 5.7% | |
| Not employed | 8.6% | 10.5% | |
| **Full-time − part-time** | +1.4 (−2.1 to 4.8) | +1.2 (−2.4 to 4.7) | −0.2 (−5.7 to 5.4) |
| **Full-time − not employed** | −1.1 (−2.8 to 0.7) | −3.7 (−11.1 to 3.8) | −2.6 (−9.7 to 4.4) |

**Sensitivity, PFL in survey year:** almost identical (differences −1.1 and −2.7 points, both CIs include zero).

**Parenting aggravation:**
- **PFL at birth:** not estimable (too few cases).
- **PFL in survey year:** full-time mothers in PFL states report less aggravation than part-time mothers in those states (−6.0 points, −11.6 to −0.5). The difference in gaps does not exclude zero (−5.1, −10.8 to 0.5). Part-time mothers in PFL states have a high, imprecise rate (7.8%, CI 2.5–13.0) based on few cases, so this is not interpreted.

## What the results show

1. **No evidence that paid family leave changes the full-time gap.** In both PFL and non-PFL states, full-time mothers of under-2s are not worse off than other mothers. The differences between the two groups of states are small and their CIs include zero.
2. **The comparison is underpowered.** Only about 690 full-time mothers of under-2s live in PFL states. The CIs for the difference in gaps span about ±6 to ±8 points, so differences of several points cannot be ruled out. This is an absence of evidence, not evidence of no association.
3. **The direction of the point estimates** (full-time mothers slightly better off relative to non-employed mothers in PFL states) is consistent with the literature, but too imprecise to report as a finding.

## Limitations

- **Cross-sectional comparison between states.** PFL states are more urban and higher-income and have other supportive policies. The difference in gaps reduces but does not remove this.
- **Intent-to-treat exposure.** "PFL at birth" means the state had a program, not that the mother was eligible, took leave, or how long. Eligibility rules differ across states.
- **Program generosity is not modeled.** Weeks and wage replacement differ by state and changed during 2023–2025 (for example Rhode Island's weeks and California's rates).
- **Timing.** A mother of a 1-year-old may be well past her bonding leave, and NSCH does not record leave taken or the timing of return to work.
- **Ten PFL states.** State-clustered SEs with few treated clusters can be unstable. The household-level SEs give similar conclusions.

## Child care prices (not yet added)

The planned second state variable is the DOL Women's Bureau National Database of Childcare Prices (NDCP).
- **Coverage:** county-level data, 2008–2022, with a state-level file. Center-based infant care has a median weekly price (`MCInfant`).
- **Sources:** landing page https://www.dol.gov/agencies/wb/topics/featured-childcare. Technical report (September 2024): https://www.dol.gov/sites/dolgov/files/WB/National-Database-of-Childcare-Prices-Technical-Report.pdf.
- **Caveats:** the latest price year is **2022**, so it would serve as a pre-period baseline for 2023–2025. The DOL site blocks automated downloads, so the file must be downloaded manually: https://www.dol.gov/sites/dolgov/files/WB/NDCP2022.xlsx (county) or https://www.dol.gov/sites/dolgov/files/WB/NDCP2022-state-level-estimates-and-rankings.xlsx (state).

## References

See `docs/literature-review.md`: Bullinger (2019); Doran et al. (2020); Heshmati et al. (2023); Irish et al. (2021); Lee et al. (2020).

National Partnership for Women & Families. (2026, April). *State paid family & medical leave insurance laws*. https://nationalpartnership.org/our-work/resources/economic-justice/paid-leave/state-paid-family-leave-laws.pdf

State program sources: see the `source_url` column of `data/reference/state_paid_family_leave.csv`.
