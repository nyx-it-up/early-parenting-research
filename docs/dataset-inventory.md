# Dataset Inventory

**Project:** The Psychology of Working Motherhood: Employment, Time, and Maternal Well-Being in the United States
**Companion to:** `docs/research-plan.md` (v0.5)
**Status:** v0.1, validation against official documentation
**Documentation reviewed:** 2026-10-30

This inventory identifies the official datasets, variables and documentation needed to answer the research plan's questions. Where it is more specific than the research plan, or differs from it, **this inventory takes precedence** until the plan is next revised.

---

## How to read this document

### Verification status

| Label | Meaning |
|---|---|
| **VERIFIED** | Name, label or wording, and codes were read in the cited official document (questionnaire, data dictionary, codebook/variable list, user guide, methodology report or API metadata). |
| **UNCERTAIN** | Partly confirmed: for example, the variable exists but a code, year range or derivation rule was not seen. Resolve before use. |
| **NOT FOUND** | Searched for in the official documentation and not found. Treat as unavailable unless new evidence appears. |
| **NOT IN PUBLIC FILE** | Collected by the survey but not released in public-use data. |

### Method and caveats

- All documentation was read from official sources: census.gov / www2.census.gov, bls.gov, bea.gov and api.census.gov metadata. **No microdata was downloaded.** The few non-government sources are labeled.
- Verification covered the latest documentation available on 2026-10-30. **Year coverage** comes from comparing year-specific variable lists or dictionaries. Where only the latest year was checked, this is stated.
- Question wording in quotation marks is **verbatim** from the cited document. Unquoted descriptions are summaries.
- Before code is written against any variable, re-check it in the **data dictionary for the exact year being analyzed**.
- Some sources could not be read during this review: the HRSA MCHB NSCH page and the Data Resource Center (DRC) codebook pages returned HTTP 403, and the BEA API line-code listing requires an API key. Items that depend on these are marked UNCERTAIN.

### Measure categories

| Code | Category |
|---|---|
| A | Maternal identification and demographics |
| B | Child age and family composition |
| C | Employment status and work hours |
| D | Occupation and industry |
| E | Individual earnings and household income |
| F | Housing tenure and housing costs |
| G | Regional cost of living |
| H | Maternal mental/emotional health |
| I | Parenting stress and aggravation |
| J | Maternal sleep |
| K | Child sleep |
| L | Paid work, childcare and unpaid household labor |
| M | Social and emotional support |

---

## 1. Summary

### 1.1 Datasets at a glance

| | NSCH | ATUS | ACS | BEA RPP |
|---|---|---|---|---|
| **Producer** | HRSA MCHB / U.S. Census Bureau | BLS / U.S. Census Bureau | U.S. Census Bureau | U.S. Bureau of Economic Analysis |
| **Unit** | One sampled child per household, with up to two caregivers | One respondent aged 15+ per household, one diary day | Person and housing unit (PUMS); area (tables) | Area |
| **Individual-level analysis?** | **Yes** (estimates are framed as "children whose mother…") | **Yes** | **Yes** (PUMS) | **No** (area-level only) |
| **Years** | 2016–2025 | 2003–2025 | Tables: 1-year through 2025; PUMS: 1-year through 2024, 5-year 2020–2024 | 2008–2024 |
| **Latest release** | 2025 data, Oct 2026 | 2025 data, Jun 25, 2026 | 2025 1-year tables, Oct 29, 2026 | 2024 data, Feb 19, 2026 (2025 data due Dec 10, 2026) |
| **Finest public geography** | State, plus metro status and limited CBSA flags | State (from linked CPS); some CBSAs | PUMS: state + PUMA. Tables: down to tract/block group (5-year) | State; metro areas (status after 2024 uncertain) |
| **Microdata API** | **None** | **None** (BLS API serves published series only) | **Yes** (Census Microdata API for PUMS) and table APIs | API for area data (key required) |
| **Weights / variance** | FWC; strata FIPSST + STRATUM; PSU HHID | TUFINLWGT / TUFNWGTP / TU20FWGT; 160 replicate weights | PWGTP / WGTP; 80 replicate weights (SDR) | n/a |

### 1.2 Coverage matrix

✅ = direct measure verified. ◐ = partial, proxy or limited years/ages. ✖ = not found.

| Category | NSCH | ATUS | ACS PUMS | BEA RPP |
|---|---|---|---|---|
| A. Maternal identification | ✅ bio/adoptive parent code | ◐ "own child" includes step; parent type only 2007+ via CPS | ◐ relationship to householder only; no parent pointer | ✖ |
| B. Child age & family composition | ◐ sampled child's exact age; other children only in age-group counts | ✅ roster ages | ✅ ages via AGEP for linkable children | ✖ |
| C. Employment & hours | ◐ employment status (scheme changes by year); **no hours** | ✅ labor force status, FT/PT, usual hours | ✅ ESR, WKHP, WKWN | ✖ |
| D. Occupation & industry | ✖ | ✅ | ✅ | ✖ |
| E. Earnings & income | ◐ family income-to-poverty only (imputed); **no earnings** | ◐ weekly earnings (wage/salary only); categorical family income | ✅ earnings, person, family and household income | ✖ |
| F. Housing tenure & costs | ◐ tenure (2018+); housing instability (2022+); **no costs** | ◐ tenure (3 categories, from CPS) | ✅ tenure (4 categories), rent, owner costs, burden | ◐ housing-rent price parity (area) |
| G. Regional cost of living | ✖ | ✖ | ✖ (no price index) | ✅ RPP all items + components |
| H. Maternal mental health | ✅ single-item rating (self-report for Adult 1) | ◐ Well-Being Module affect (2010, 2012, 2013, 2021) | ✖ | ✖ |
| I. Parenting aggravation | ✅ K8Q30–K8Q34 | ✖ (WB stress is activity-level) | ✖ | ✖ |
| J. Maternal sleep | ✖ | ◐ diary sleep minutes + sleeplessness; WB "well-rested" | ✖ | ✖ |
| K. Child sleep | ✅ hours (different items by age) + bedtime regularity | ◐ household children's (<13) wake and bed times only | ✖ | ✖ |
| L. Work, childcare, household labor | ◐ hours of non-parental care (0–5, 2025); job disruption due to childcare (0–5) | ✅ full diary | ◐ commute only | ✖ |
| M. Social & emotional support | ✅ K8Q35; resilience; neighborhood support | ◐ time with others (proxy) | ✖ | ✖ |

### 1.3 Corrections to the research plan

These verification results changed assumptions in `research-plan.md` v0.3. Item 5 is resolved in v0.4. The others are still to be folded into the plan.

1. **NSCH has housing tenure** (`TENURE`, 2018–2025), so research question E3 (renters vs. owners and maternal well-being) **can be tested in NSCH**. NSCH has no housing **cost** amounts.
2. **NSCH has no caregiver sleep measure.** Maternal sleep comes only from ATUS. Child sleep comes from NSCH.
3. **NSCH employment measures change over time.** From 2023, `A1_EMPLOYED_R` distinguishes full-time, part-time, unpaid work, looking for work, not looking and retired. 2020–2022 used `A1_EMPLOYED` (no "retired" category). 2016–2019 had only an indicator of employment for at least 50 of the past 52 weeks. **NSCH has no work-hours item.**
4. **NSCH Adult 1 is always the respondent**, and Adult 2 items are proxy-reported. NSCH weighted estimates represent **children**, not mothers.
5. **NSCH uses age-specific forms: T1 (0–5), T2 (6–11), T3 (12–17).** Several key items are asked on T1 only. *(Resolved in research plan v0.4: the project bands now match these forms; see Section 6.3.)*
6. **NSCH's emotional-support source items (`EMOSUP*`) were discontinued after 2022.** `K8Q35` continues.
7. **There is no RPP childcare component.** Childcare fees carry no regional price variation in the RPP (Section 5).
8. **BEA announced it was discontinuing metro-area statistics** in the 2024 release, but published 2024 metro RPPs still appear in BEA material. Metro RPPs after 2024 are uncertain.

---

## 2. National Survey of Children's Health (NSCH)

### 2.1 Source, documentation and access

| Item | Detail | Source |
|---|---|---|
| **Producer** | Funded and directed by HRSA Maternal and Child Health Bureau. Conducted by the U.S. Census Bureau. | census.gov NSCH pages |
| **Landing page** | https://www.census.gov/programs-surveys/nsch.html | |
| **Datasets** | https://www.census.gov/programs-surveys/nsch/data/datasets.html (2025: `.../datasets/nsch2025.html`) | |
| **Technical documentation** | https://www.census.gov/programs-surveys/nsch/technical-documentation.html | |
| **Questionnaires (2025)** | https://www.census.gov/programs-surveys/nsch/technical-documentation/questionnaires.2025.html. Forms S1 (screener), T1, T2, T3 | |
| **Variable lists (codebooks)** | `https://www2.census.gov/programs-surveys/nsch/technical-documentation/codebook/{YEAR}-NSCH-Topical-Variable-List.pdf` (2016–2025) | |
| **Interactive codebook** | https://www.census.gov/data-tools/demo/uccb/nschdict | |
| **2025 FAQs** | https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/2025-NSCH-FAQs.pdf | |
| **2025 Methodology Report** | https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/2025-NSCH-Methodology-Report.pdf | |
| **Guide to Multiply Imputed Data Analysis** | https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Analysis-with-Imputed-Data-Guide.pdf | |
| **Guide to Multi-Year Estimates** | https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Guide-to-Multi-Year-Estimates.pdf | |
| **Analytic Guide** | https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Analytic-Guide.pdf (downloaded, not yet read in detail) | |
| **Nonresponse bias analysis** | https://www.census.gov/programs-surveys/nsch/technical-documentation/nonresponse-bias-analysis.html | |
| **Secondary (non-Census)** | Data Resource Center for Child and Adolescent Health: https://www.childhealthdata.org. Provides tabulations and DRC-constructed indicators. Codebook pages were not accessible during this review. | |
| **Access** | SAS and Stata zip files (for example `nsch_2025_topical_SAS.zip`). **No microdata API.** | FAQ25 |

### 2.2 Years, geography and design

- **Years:** 2016–2025, annual. The 2025 data were released in October 2026. Fieldwork ran June 2025 to March 2026 and was extended by the October–November 2025 federal funding lapse. There were 45,139 topical questionnaires, and the weighted overall response rate was 34.7%. *(FAQ25)*
- **Screener public file discontinued after 2024.** *(MR25, FAQ25)*
- **Pooling with 2016–2021** must use the re-released "enhanced" files (`nsch_YYYYe_topical`). *(FAQ25; Multi-Year Guide)*
- **Geography:** The public file identifies only areas of at least 250,000 people: `FIPSST` (state), plus `METRO_YN`, `MPC_YN` and `CBSAFP_YN`. Finer geography requires the restricted file, accessed through a Federal Statistical Research Data Center. *(FAQ25)*
- **Questionnaire forms:** A screener (S1) rosters the children in the household. One child is sampled, and the household receives **T1 (ages 0–5), T2 (6–11) or T3 (12–17)** according to that child's age. `FORMTYPE` records which form was used. Items not on the form are coded `.N`. Other missing codes are `.L` (legitimate skip), `.M` (missing in error), `.D` (suppressed) and `.K` (don't know). *(FAQ25; MR25)*
- **Sampling:** One child per household. Children with special health care needs are oversampled, with a secondary oversample of ages 0–5. Some states purchase oversamples. *(FAQ25)*
- **Weight and design:** weight **`FWC`**; strata **`FIPSST` × `STRATUM`**; PSU **`HHID`**. Use subpopulation (domain) options rather than deleting records. Reliability rules: n ≥ 30, and flag estimates with a 95% CI wider than 20 points or a relative standard error above 30%. *(FAQ25; MR25)*
- **Pooling:** Divide `FWC` by the number of years. Recode `STRATUM` "2a" to "2" when 2016 is included. *(FAQ25; Multi-Year Guide)*
- **Target population of estimates:** In the documentation's words: "Weighted estimates do not generalize to the population of parents, mothers, or pediatric health care providers… estimates should be framed in terms of children, e.g., 51% of US children live with a college educated mother." *(FAQ25; MR25)*

### 2.3 Respondent and caregiver structure

- The form is completed by "a parent or adult caregiver who lives in this household and who is familiar with this child's health and health care." *(T1 cover)*
- **Adult 1 is the respondent.** Items are worded "How are you related to this child?", "What is your sex?" and so on. There is no separate respondent-ID variable.
- **Adult 2** is a second primary caregiver, **reported by the respondent** ("this caregiver's…"). Adult 2 health and employment are therefore **proxy reports**.
- Each adult's relationship is reported **to the child only**, so the relationship between the two adults is unknown. In multigenerational homes a parent may go unreported. *(MR25 p. 32)*

### 2.4 Candidate variables

**Universe:** "T1–T3" means the item is asked for sampled children of all ages. "T1 only" means the sampled child is aged 0–5. Years come from comparing the 2016–2025 variable lists unless noted. **Source:** 2025 Topical Variable List (VL25) and the 2025 questionnaires, unless noted.

#### A. Maternal identification and demographics

| Variable | Status | Wording / label | Codes | Universe | Years |
|---|---|---|---|---|---|
| `A1_SEX` | VERIFIED | "What is your sex?" | 1 Male; 2 Female | T1–T3 | 2016–2025 |
| `A1_RELATION` | VERIFIED | "How are you related to this child?" | 1 Biological or Adoptive Parent; 2 Step-parent; 3 Grandparent; 4 Foster Parent; 6 Other: Relative; 7 Other: Non-Relative | T1–T3 | 2016–2025 (2016–2017 also had 5 Aunt or Uncle) |
| `A2_SEX` | VERIFIED | "What is this caregiver's sex?" | 1/2. Skipped if `A2_RELATION` = 8 | T1–T3 | 2016–2025 |
| `A2_RELATION` | VERIFIED | "How is this other caregiver related to this child?" | As A1, plus 8 "There is only one primary adult caregiver in the household for this child" | T1–T3 | 2016–2025 |
| `A1_AGE` / `A2_AGE` | VERIFIED | "What is your age?" / "What is this caregiver's age?" | 18 to "70 or older" | T1–T3 | 2016–2025 |
| `A1_MARITAL` (and A2) | VERIFIED | Marital status | 6 codes (not transcribed here) | T1–T3 | 2016–2025 |
| `A1_GRADE` (and A2) | VERIFIED | Education | 9 codes. Imputed; flag `A1_GRADE_IF` | T1–T3 | 2016–2025 |
| `A1_BORN` (and A2) | VERIFIED | Born in or outside the U.S. | — | T1–T3 | 2016–2025 (`A1_LIVEUSA` ended after 2022) |

**Identifying mothers.**
- **Primary definition:** `A1_SEX = 2` **and** `A1_RELATION = 1`, a female biological or adoptive parent who is also the respondent, so all her measures are self-reports.
- **Secondary definition:** `A2_SEX = 2` and `A2_RELATION = 1`. A mother recorded as Adult 2 is described by someone else, so her measures are proxy reports and are analyzed separately.
- **Excluded from the primary population:** step-mothers (`A1_RELATION = 2`), grandmothers (3), foster mothers (4) and other relatives or non-relatives (6, 7).
- **Limits:** Biological and adoptive mothers share one code and **cannot be told apart**. About 3–4% of `A1_SEX` values are missing (2025 frequencies). Estimates must be framed as "children whose mother…".

#### B. Child age and family composition

| Variable | Status | Wording / label | Codes | Universe | Years |
|---|---|---|---|---|---|
| `SC_AGE_YEARS` | VERIFIED | "How old is this child?" | 0–17 | All | 2016–2025 |
| `SC_AGE_LT4`, `_LT6`, `_LT9`, `_LT10` | VERIFIED | Child younger than 4 / 6 / 9 / 10 months | 1 younger; 2 at least | All | 2025 checked |
| `TOTKIDS_R` | VERIFIED | Number of children in household | 1, 2, 3, 4+ | All | 2016–2025 |
| `TOTAGE_0_5`, `TOTAGE_6_11`, `TOTAGE_12_17` | VERIFIED | Number of children in each age group | 0–4 | All | 2016–2025 |
| `AGEPOS4` | VERIFIED | "Birth Order of Selected Children in Household" | 1 Only; 2 Oldest; 3 Second oldest; 4 Third oldest; 5 Fourth or greater | All | 2016–2025 |
| `HHCOUNT` | VERIFIED | "How many people are living or staying at this address?" | 2 to "10 or more". Imputed; flag `HHCOUNT_IF` | T1–T3 | 2016–2025 |
| `FAMCOUNT` | VERIFIED | "How many of these people in your household are family members?" | 1 to "8 or more" | T1–T3 | 2016–2025 |
| `FAMILY_R` | VERIFIED (derived) | Family structure | 1 Two biological/adoptive parents, married; 2 …not married; 3/4 two parents, at least one not biological/adoptive, married / not married; **5 Single mother**; 6 Single father; 7 Grandparent household; 8 Other relation | T1–T3 | **2017–2025** (2016 uses `FAMILY` with a different 9-category scheme) |
| Exact ages of other children | **NOT IN PUBLIC FILE** | The screener collects them, but only age-group counts and `AGEPOS4` are released. | — | — | — |

**Youngest child:** The youngest child's exact age cannot be determined. The `TOTAGE_0_5` count shows whether any child aged 0–5 is present, so it can identify households with a child in band 0–5 even when the sampled child is older.

#### C. Employment status and work hours

| Variable | Status | Wording / label | Codes | Universe | Years |
|---|---|---|---|---|---|
| `A1_EMPLOYED_R` | VERIFIED | "Which of the following best describes your current employment status?" | 1 Employed full-time; 2 Employed part-time; 3 Working WITHOUT pay; 4 Not employed but looking for work; 5 Not employed and not looking for work; 6 Retired | T1–T3 | **2023–2025** |
| `A1_EMPLOYED` | VERIFIED | Same question | Codes 1–5 (no "Retired") | T1–T3 | **2020–2022** |
| `A1_K11Q50_R` | VERIFIED | "Were you employed at least 50 out of the past 52 weeks?" (2019 wording) | 1 Yes; 2 No | T1–T3 | **2016–2019** |
| `A2_EMPLOYED_R` / `A2_EMPLOYED` / `A2_K11Q50_R` | VERIFIED | "…this caregiver's current employment status?" (proxy) | As Adult 1 | T1–T3 | Same year breaks |
| `K6Q27` | VERIFIED | "DURING THE PAST 12 MONTHS, did you or anyone in the family have to quit a job, not take a job, or greatly change your job because of problems with child care for this child?" | 1 Yes; 2 No | **T1 only (0–5)** | 2016–2025 |
| `CUTHOURS` / `STOPWORK` | VERIFIED | "DURING THE PAST 12 MONTHS, have you or other family members:" "Cut down on the hours you work…" / "Left a job or taken a leave of absence…" (because of **this child's health**) | 1/2 | T1–T3 | 2016–2025 |
| `AVOIDCHG` | VERIFIED | "Avoided changing jobs because of concerns about maintaining health insurance…" | 1/2 | T1–T3 | 2025 checked |
| Work hours | **NOT FOUND** | — | — | — | — |

**Labor force mapping (2023–2025 only):**
- Codes 1–2 = employed (full-time / part-time).
- Code 4 = unemployed (looking).
- Codes 5–6 = not in the labor force.
- Code 3 (working without pay) needs an explicit decision.
- 2020–2022 cannot separate retirees. 2016–2019 supports only a "steadily employed" indicator.

#### D. Occupation and industry

**NOT FOUND.** NSCH has no occupation or industry variables.

#### E. Earnings and household income

| Variable | Status | Wording / label | Codes | Universe | Years |
|---|---|---|---|---|---|
| `FPL_I1`–`FPL_I6` | VERIFIED | Family poverty ratio, six multiply imputed versions | 50 ("50 or less") to 400 ("400 or more"). About 20% imputed; flag `FPL_IF` | T1–T3 | 2016–2025 |
| Combining imputations | VERIFIED | All six must be combined with multiple-imputation procedures (SAS, SUDAAN or Stata `mi`). Using one understates standard errors. | — | — | Imputed-Data Guide |
| FPL definition | VERIFIED | Total **family** income ÷ Census **poverty threshold** (not HHS guidelines). Income refers to the **prior calendar year** (the 2025 form asks for "your 2024 income"). | — | — | MR25 p. 31 |
| Income amounts | **NOT IN PUBLIC FILE** | "only FPL is reported in the Public Use File; total family income and the family poverty threshold are not included." | — | — | MR25 p. 28, 32 |
| Individual caregiver earnings | **NOT FOUND** | Income is collected for the family only. | — | — | — |
| `ACE1` | VERIFIED | "SINCE THIS CHILD WAS BORN, how often has it been very hard to cover the basics, like food or housing, on your family's income?" | 1 Never; 2 Rarely; 3 Somewhat often; 4 Very often | T1–T3 | 2016–2025 |
| `FOODSIT` | VERIFIED | "Which of these statements best describes your household's ability to afford the food you need DURING THE PAST 12 MONTHS?" | 1–4 (always nutritious → often not enough) | T1–T3 | 2016–2025 |
| `K11Q60`, `K11Q61`, `K11Q62`, `S9Q34`, `EBTCARDS` | VERIFIED | Past-12-month family receipt of cash assistance, SNAP, free or reduced-cost school meals, WIC, school-meal EBT | 1/2 | T1–T3 | `K11Q61` 2016–2025; others checked only for 2025 |

**NSCH household income is family income relative to poverty, never the mother's earnings.**

#### F. Housing tenure and costs

| Variable | Status | Wording / label | Codes | Universe | Years |
|---|---|---|---|---|---|
| `TENURE` | VERIFIED | "Is this house, apartment, or mobile home" (screener item carried onto the topical file) | 1 Owned with mortgage or loan; 2 Owned free and clear; 3 Rented; 4 Occupied without payment of rent. Hot-deck imputed; flag `TENURE_IF` | All | **2018–2025** |
| `MISSMORTGAGE` | VERIFIED | "DURING THE PAST 12 MONTHS, was there a time when you were not able to pay the mortgage or rent on time?" | 1 Yes; 2 No; 3 Don't Know | T1–T3 | 2022–2025 |
| `HOMEEVIC` | VERIFIED | "…how often were you worried or stressed about being evicted, foreclosed on, or having your housing condemned?" | 1 Always … 5 Never | T1–T3 | 2022–2025 |
| `EVERHOMELESS` | VERIFIED | "SINCE this child WAS BORN, have they ever been homeless or lived in a shelter?" | 1/2/3 | T1–T3 | 2022–2025 |
| `K11Q43R` / `MOVES` | VERIFIED | Moves since the child's birth / in the past 12 months | — | T1–T3 | 2025 checked |
| Housing cost amounts | **NOT FOUND** | — | — | — | — |

#### G. Regional cost of living

**NOT FOUND.** Area price context would come from BEA RPP, attached by state (`FIPSST`).

#### H. Maternal mental and emotional health

| Variable | Status | Wording | Codes | Universe | Years |
|---|---|---|---|---|---|
| `A1_MENTHEALTH` | VERIFIED | "In general, how is your mental or emotional health?" | 1 Excellent; 2 Very Good; 3 Good; 4 Fair; 5 Poor | T1–T3 | 2016–2025 |
| `A1_PHYSHEALTH` | VERIFIED | "In general, how is your physical health?" | Same | T1–T3 | 2016–2025 |
| `A2_MENTHEALTH` / `A2_PHYSHEALTH` | VERIFIED (**proxy**) | "In general, how is this caregiver's mental or emotional health?" / "…physical health?" | Same. Skipped if `A2_RELATION` = 8 | T1–T3 | 2016–2025 |

This is a single global self-rating, **not** a diagnostic instrument or validated screener.

#### I. Parenting stress and aggravation

| Variable | Status | Wording | Codes | Universe | Years |
|---|---|---|---|---|---|
| `K8Q30` | VERIFIED | "How well do you think you are handling the day-to-day demands of raising children?" | 1 Very well; 2 Somewhat well; 3 Not very well; 4 Not well at all | T1–T3 | 2016–2025 |
| `K8Q31` | VERIFIED | "DURING THE PAST MONTH, how often have you felt: That this child is much harder to care for than most children their age?" | 1 Never; 2 Rarely; 3 Sometimes; 4 Usually; 5 Always | T1–T3 | 2016–2025 |
| `K8Q32` | VERIFIED | "…That this child does things that really bother you a lot?" | Same | T1–T3 | 2016–2025 |
| `K8Q34` | VERIFIED | "…Angry with this child?" | Same | T1–T3 | 2016–2025 |
| DRC "Parental aggravation" / "Coping with daily demands" indicators | UNCERTAIN | Listed in the DRC 2024–2025 content map (6.14, 6.16). How they are constructed has not been verified, and they are not Census variables. | — | — | — |

The respondent (Adult 1) answers these items. They refer to the **sampled child**.

#### J. Maternal sleep

**NOT FOUND.** NSCH has no caregiver sleep items.

#### K. Child sleep

| Variable | Status | Wording | Codes | Universe | Years |
|---|---|---|---|---|---|
| `HOURSLEEP05` | VERIFIED | "DURING THE PAST WEEK, how many hours of sleep did this child get during an average day (count both nighttime sleep and naps)?" | 1 Less than 7; 2 7; 3 8; 4 9; 5 10; 6 11; 7 12 or more hours | **T1 only (0–5)** | 2016–2025 (2016 wording: "on an average day") |
| `HOURSLEEP` | VERIFIED | "DURING THE PAST WEEK, how many hours of sleep did this child get on most weeknights?" | 1 Less than 6; 2 6; 3 7; 4 8; 5 9; 6 10; 7 11 or more hours | **T2–T3 (6–17)** | 2016–2025 |
| `BEDTIME` | VERIFIED | "How often does this child go to bed at about the same time on weeknights?" | 1 Always … 5 Never | T1–T3 | 2016–2025 |
| `SLEEPPOS` | VERIFIED (discontinued) | Infant sleep position | not checked | T1 | 2016–2022 |
| Child sleep problems | **NOT FOUND** | — | — | — | — |

**The two hours-of-sleep items are not comparable.** `HOURSLEEP05` is a 24-hour total including naps, while `HOURSLEEP` counts weeknight sleep only. Band 0–5 uses `HOURSLEEP05`, and bands 6–11 and 12–17 use `HOURSLEEP`.

#### L. Paid work, childcare and household labor

| Variable | Status | Wording | Codes | Universe | Years |
|---|---|---|---|---|---|
| `HOURSOFCARE` | VERIFIED (**new 2025**) | "IN AN AVERAGE WEEK, how many hours does this child receive care from someone other than their parent or guardian?" | 1 = 0; 2 = 1–10; 3 = 11–20; 4 = 21–30; 5 = 31–40; 6 = more than 40 | **T1 only (0–5)** | 2025 |
| `K6Q20` | VERIFIED (discontinued) | "Does this child receive care for at least 10 hours per week from someone other than their parent or guardian?" | 1/2 | T1 only | 2016–2022 |
| `K6Q27` | VERIFIED | Job change due to childcare problems (see C) | — | T1 only | 2016–2025 |
| Time use / household labor | **NOT FOUND** | — | — | — | — |

There is no childcare item at all for 2023–2024, and no childcare-arrangement item for ages 6–17.

#### M. Social and emotional support

| Variable | Status | Wording | Codes | Universe | Years |
|---|---|---|---|---|---|
| `K8Q35` | VERIFIED | "DURING THE PAST 12 MONTHS, was there someone that you could turn to for day-to-day emotional support with parenting or raising children?" | 1 Yes; 2 No | T1–T3 | 2016–2025 |
| `EMOSUPSPO`, `EMOSUPFAM`, `EMOSUPHCP`, `EMOSUPWOR`, `EMOSUPADV`, `EMOSUPPEER`, `EMOSUPMHP`, `EMOSUPOTH` | VERIFIED (**discontinued**) | "Did you receive emotional support from:" (for example "Spouse or Domestic Partner?") | 1/2. Skipped if `K8Q35` = 2 | T1–T3 | **2016–2022 only** |
| `TALKABOUT`, `WKTOSOLVE`, `STRENGTHS`, `HOPEFUL` | VERIFIED | Family resilience. "When your family faces problems, how often are you likely to…": "Talk together about what to do" / "Work together to solve our problems" / "Know we have strengths to draw on" / "Stay hopeful even in difficult times" | 1 All of the time … 4 None of the time | T1–T3 | 2016–2025 |
| `K10Q30`, `K10Q31`, `GOFORHELP` | VERIFIED | Neighborhood support: "People in this neighborhood help each other out" / "We watch out for each other's children…" / "When we encounter difficulties, we know where to go for help in our community" | 1 Definitely agree … 4 Definitely disagree | T1–T3 | 2016–2025 |
| `K8Q21` | VERIFIED | Parent–child communication | 1–4 | **T2–T3 only** | 2016–2025 |
| DRC "Family resilience" indicator | UNCERTAIN | DRC construct, not a Census variable. Construction not verified. | — | — | — |

### 2.5 NSCH limitations for this project

- **Estimates represent children, not mothers.** A mother appears once, linked to one sampled child (with oversampling) who may not be her youngest.
- **Proxy reporting:** Mothers recorded as Adult 2 are described by another adult.
- **No hours, occupation, earnings, housing costs or maternal sleep.**
- **Employment measures change in 2020 and 2023**, so trend analyses need harmonized categories.
- **Items asked on T1 only** (`K6Q27`, `HOURSOFCARE`, `HOURSLEEP05`) cover band 0–5 only.
- **Income** refers to the prior calendar year, while employment status is current.

---

## 3. American Time Use Survey (ATUS)

### 3.1 Source, documentation and access

| Item | Detail |
|---|---|
| **Producer** | U.S. Bureau of Labor Statistics. Data collected by the U.S. Census Bureau. |
| **Landing page** | https://www.bls.gov/tus/ |
| **Data files** | https://www.bls.gov/tus/data.htm. Multi-year 2003–2025: https://www.bls.gov/tus/data/datafiles-0325.htm |
| **Data dictionaries** | https://www.bls.gov/tus/dictionaries.htm. Interview dictionary 2003–2025 [INT]: https://www.bls.gov/tus/dictionaries/atusintcodebk0325.pdf. ATUS-CPS dictionary [CPS]: https://www.bls.gov/tus/dictionaries/atuscpscodebk0325.pdf |
| **User's Guide** [UG] | "Understanding ATUS 2003 to 2025" (Sept 2026): https://www.bls.gov/tus/atususersguide.pdf |
| **Activity lexicons** [LEX] | https://www.bls.gov/tus/lexicons.htm. Multi-year: https://www.bls.gov/tus/lexicons/lexiconnoex0325.pdf |
| **Changes across years** | https://www.bls.gov/tus/other-documentation/changes.pdf |
| **Well-Being Module** | Files: https://www.bls.gov/tus/modules/wbdatafiles.htm. Dictionaries: 2021 https://www.bls.gov/tus/dictionaries/wbmintcodebk21.pdf; 2010/2012/2013 https://www.bls.gov/tus/dictionaries/wbmintcodebk.pdf |
| **Access** | Downloadable zip files containing `.dat` data files. **No microdata API.** The BLS Public Data API serves "published historical timeseries data" only (https://www.bls.gov/developers/home.htm). |
| **Secondary (non-BLS)** | IPUMS ATUS (https://www.atusdata.org): harmonized extracts with its own variable names. Not consulted for this inventory. |

### 3.2 Years, geography and design

- **Years:** 2003–2025. The latest (2025) was released June 25, 2026, with about 6,100 respondents. Response rates fell from about 58% in 2003 to the 30s by 2021–2023. Verify the latest values in UG Table 3.3.
- **2020:** Diary days from March 18 to May 9, 2020 were not collected, and the data are "not representative of the full year." Use `TU20FWGT`. *(INT)*
- **2025:** "All ATUS operations were suspended from October 1 through November 12." There are no data for September 30 to November 11. *(BLS notice, `notices/2026/october2025shutdown.htm`)*
- **Universe:** Household residents aged 15+, excluding active military and institutionalized persons. ATUS draws from households two months after their final CPS interview, and one person per household is selected. "No substitutes or proxy responses are allowed." **Households with children are oversampled.** *(UG §3)*
- **Diary day:** "starting at 4 a.m. the previous day and ending at 4 a.m. on the interview day." The sample is split 50% weekdays and 50% weekend days. Variables: `TUDIARYDAY` (1 Sunday … 7 Saturday), `TUDIARYDATE`, `TRHOLIDAY`. *(UG)*
- **Geography** (ATUS-CPS file, measured at the CPS interview 2–5 months earlier):
  - `GESTFIPS` state.
  - `GEREG` region.
  - `GTMETSTA` metro status.
  - `GTCBSA`: "Not all CBSAs are identified."
  - `GTCO`: "most counties are not identified."
  - "ATUS does not have a State reliability requirement." *(CPS; UG §3.3)*

### 3.3 Files and identifiers

| File | Level | Keys |
|---|---|---|
| Respondent | One per respondent | `TUCASEID` |
| Roster | One per household member, plus own nonhousehold children <18 | `TUCASEID` + `TULINENO` |
| Activity | One per activity episode | `TUCASEID` + `TUACTIVITY_N` |
| Activity Summary | One per respondent; minutes per activity (`t` + 6-digit code) | `TUCASEID` |
| Who | One per person present per activity | `TUCASEID` + `TUACTIVITY_N` (+ `TULINENO`) |
| ATUS-CPS | One per CPS household member | `TUCASEID` + `TULINENO` (also CPS `PULINENO`) |
| Replicate weights | One per respondent | `TUCASEID` |
| Eldercare roster (2011–2025) / Case history (2005–2025) / Pandemic replicate weights (2019–2020) | — | `TUCASEID` (+ `TULINENO`) |
| Well-Being respondent / activity / replicate weights | WB years only | `TUCASEID` / + `TUACTIVITY_N` |

`TUCASEID` is the "ATUS Case ID (14-digit identifier)." `TULINENO` is the "ATUS person line number," and the respondent is always line 1. *(INT; UG §7.3)*

### 3.4 Weights and variance

- **Final weights:**
  - `TUFINLWGT` in single-year files.
  - `TUFNWGTP` in the multi-year file for 2003–2019 and 2021+.
  - `TU20FWGT` for 2020.
  - When combining single-year files: `TU06FWGT` for 2003–2005.
- **Replicate weights:** 160 per final weight. In single-year files they are named `FINLWGT001`–`FINLWGT160`. The names in the multi-year replicate file are **UNCERTAIN**.
- **Variance:** Var = (4/160) Σ(Ŷᵢ − Ŷ₀)². This is CPS-based modified balanced half-sample (Fay) replication. *(UG §7.5)*
- Weights are person-day weights. Pooled totals need to be divided by the number of years. Weighted means are unaffected.

### 3.5 Candidate variables

Source is [INT] unless noted. Years are 2003–2025 unless noted.

#### A. Maternal identification and demographics

| Variable | Status | Definition | Codes | File / universe | Years |
|---|---|---|---|---|---|
| `TESEX` | VERIFIED | "Edited: sex" | 1 Male; 2 Female | Roster, Activity Summary | 2003–2025 |
| `TEAGE` | VERIFIED | "Edited: age" | 0–85 (top-coded; rules changed in 2005) | Roster, Activity Summary | 2003–2025 |
| `TERRP` | VERIFIED | "Edited: how is this person related to you?" | 18/19 Self; 20 Spouse; 21 Unmarried partner; **22 Own household child**; 23 Grandchild; 24 Parent; 25 Brother/sister; 26 Other relative; **27 Foster child**; 28 Housemate/roommate; 29 Roomer/boarder; 30 Other nonrelative; **40 Own nonhousehold child < 18** | Roster | 2003–2025 |
| `TROHHCHILD` | VERIFIED | "Presence of own household children < 18" | 1 Yes; 2 No | Respondent | 2003–2025 |
| `TRNHHCHILD` | VERIFIED | "Presence of own non-household child < 18" | 1/2 | Respondent | 2003–2025 |
| `TRHHCHILD` | VERIFIED | "Presence of household children < 18" (any relationship) | 1/2 | Respondent | 2003–2025 |
| `TRSPPRES` | VERIFIED | Presence of spouse or unmarried partner | 1 Spouse; 2 Unmarried partner; 3 None | Respondent | 2003–2025 |
| "Own children" concept | VERIFIED | "Biological, step-, and adopted children are considered own children; foster children are not." | — | [UG] | — |
| `PEMOMTYP` | VERIFIED | "Is household child a biological, step, or adopted child?" | 1 Biological; 2 Step; 3 Adopted | ATUS-CPS | **2007–2019** |
| `PELNMOM` | VERIFIED | Line number (`PULINENO`) of mother | — | ATUS-CPS | **2007–2019** |
| `PEPAR1` / `PEPAR2` | VERIFIED | Line number of first/second parent ("Always the mother, if present" for `PEPAR1`) | — | ATUS-CPS | **2020+** |
| `PEPAR1TYP` / `PEPAR2TYP` | VERIFIED | Type of parent | 1 Biological; 2 Step; 3 Adopted | ATUS-CPS | **2020+** |

**Identifying mothers:**
- Start with the respondent being female: `TESEX = 2` on line 1.
- Add own household children under 18: `TROHHCHILD = 1`, or roster lines with `TERRP = 22` and `TEAGE < 18`. `TERRP = 22` also includes adult children, so filter by age.
- Separating biological or adoptive children from step-children requires the ATUS-CPS parent-type variables. These exist only from 2007, change name in 2020, link through `PULINENO`, and were measured 2–5 months before the diary day. Before 2007 they **cannot be separated**.
- Mothers whose children live elsewhere: `TRNHHCHILD = 1` or `TERRP = 40`.

#### B. Child age and family composition

| Variable | Status | Definition | Notes |
|---|---|---|---|
| Roster `TEAGE` + `TERRP` | VERIFIED | Exact ages of own household children | **Use this to build the 0–5 / 6–11 / 12–17 bands** |
| `TRYHHCHILD` | VERIFIED | "Age of youngest household child < 18" | Household child of **any** relationship, not necessarily own |
| `TRCHILDNUM` | VERIFIED | "Number of household children < 18" | Any relationship |
| `TRNUMHOU` | VERIFIED | "Number of people living in respondent's household" | 1–30 |
| `HRHTYPE` | VERIFIED (codes not fully read) | Household type | ATUS-CPS |

#### C. Employment status and work hours

The labor force questions refer to "the last seven days."

| Variable | Status | Definition | Codes | Universe |
|---|---|---|---|---|
| `TELFS` | VERIFIED | "Edited: labor force status" | 1 Employed–at work; 2 Employed–absent; 3 Unemployed–on layoff; 4 Unemployed–looking; 5 Not in labor force | All |
| `TRDPFTPT` | VERIFIED | Full-time or part-time | 1 Full time; 2 Part time (hour threshold **UNCERTAIN**, not stated in the dictionary) | `TELFS` = 1, 2 |
| `TEHRUSL1` | VERIFIED | "how many hours per week do you usually work at your main job?" | 0–99; −4 hours vary | `TELFS` = 1, 2 |
| `TEHRUSLT` | VERIFIED | Total usual weekly hours (all jobs) | −4 hours vary | `TELFS` = 1, 2 |
| `TEMJOT` | VERIFIED | More than one job | 1/2 | `TELFS` = 1, 2 |
| `TEABSRSN` | VERIFIED | Reason absent from work; includes 6 "Childcare problems" and 8 "Maternity/paternity leave" | — | `TELFS` = 2 |
| `TEIO1COW` | VERIFIED | Class of worker | 1–8 | `TELFS` = 1, 2 |
| `TESPEMPNOT`, `TESPUHRS`, `TRSPFTPT` | VERIFIED | Spouse/partner employment, usual hours, full-time/part-time | — | Spouse/partner present |

#### D. Occupation and industry

| Variable | Status | Definition / notes |
|---|---|---|
| `TEIO1OCD` | VERIFIED | Occupation code, main job. The Census occupation scheme changed in 2011 and 2020; BLS says it is "not strictly comparable across all the years." |
| `TEIO1ICD` | VERIFIED | Industry code, main job. Scheme changed in 2010, 2014, 2020 and 2025. |
| `TRMJOCC1` / `TRDTOCC1` | VERIFIED | Major (1–10) / detailed occupation recode |
| `TRMJIND1` / `TRDTIND1` | VERIFIED | Major (1–13) / detailed (1–51) industry recode |

#### E. Earnings and income

| Variable | Status | Definition | Notes |
|---|---|---|---|
| `TRERNWA` | VERIFIED | "Weekly earnings at main job (2 implied decimals)" | **Wage and salary workers only** (excludes self-employed and unpaid). Top-coded. May be carried forward from the CPS (`TRERNUPD`). |
| `TRERNHLY` | VERIFIED | "Hourly earnings at main job" | Hourly-paid workers only |
| `HEFAMINC` | VERIFIED | "Edited: family income" (12 months) | ATUS-CPS; categorical 1–16; **2010+**; allocation rate up to 20%. Bracket labels **UNCERTAIN** for this file. |
| `HUFAMINC` | VERIFIED | "Family income" | ATUS-CPS; 16 categories; **2003–2009** (missing 2010+) |

#### F. Housing tenure

| Variable | Status | Definition | Codes |
|---|---|---|---|
| `HETENURE` | VERIFIED | "are your living quarters owned, rented for cash, or occupied without payment of cash rent?" | 1 Owned or being bought; 2 Rented for cash; 3 Occupied without payment of cash rent (ATUS-CPS; measured at the CPS interview) |

ATUS does not separate owners with a mortgage from owners without one, and it has no housing cost variables.

#### G. Regional cost of living

**NOT FOUND.**

#### H. Maternal well-being (Well-Being Module only)

**Module years:** 2010, 2012 and 2013 (sponsored by NIA), and 2021 (March–December). Three diary activities are randomly selected per respondent. Sleeping, grooming and personal activities are excluded. *(UG §4.5.2; WB dictionaries)*

| Variable | Status | Question / label | Scale | Years |
|---|---|---|---|---|
| `WUHAPPY`, `WUSAD`, `WUSTRESS`, `WUTIRED`, `WUPAIN` | VERIFIED | "From 0 to 6, where a 0 means you were not happy at all and a 6 means you were very happy, how happy did you feel during this time?" (parallel wording for each) | 0–6 | All 4 |
| `WUMEANING` | VERIFIED | "how meaningful did you consider what you were doing?" | 0–6 | All 4 |
| `WUINTERACT` | VERIFIED | Interacting with anyone during the activity | 1/2 | All 4 |
| `WECANTRIL` | VERIFIED | Cantril ladder: "…on which step of the ladder do you feel you personally stand at the present time?" | 0–10 | **2012, 2013, 2021** |
| `WETYPICAL` | VERIFIED | Feelings yesterday compared with a typical day of the week | 1 Better; 2 Same; 3 Worse | 2012, 2013, 2021 |
| `WEGENHTH` | VERIFIED | General health | 1 Excellent … 5 Poor | All 4 |
| `WUFINLWGT` / `WUFNACTWT` / `WUFNACTWTC` / `WUFNACTWTP` | VERIFIED | Respondent weight / activity weights. For 2010–13 use the **corrected** activity weights. | — | — |

- **Activity-selection error:** "an error in the activity selection process for the 2010, 2012, and part of the 2013" modules, fixed March 25, 2013. *(WB10)*
- **Interpreting activity weights:** they estimate average affect across person-days, not "how the average person felt while [doing activity X]." *(WB21)*

#### I. Parenting stress

**NOT FOUND.** `WUSTRESS` is activity-level stress, available only in module years. It is not a parenting-stress measure.

#### J. Maternal sleep

| Measure | Status | Definition | Notes |
|---|---|---|---|
| Activity 010101 / `t010101` | VERIFIED | "Sleeping" | Minutes on the diary day |
| Activity 010102 / `t010102` | VERIFIED | "Sleeplessness" | Minutes on the diary day |
| Activity 010199 | VERIFIED | "Sleeping, n.e.c." | — |
| `WEREST` | VERIFIED | "When you woke up yesterday, how well-rested did you feel?" | 1 Very … 4 Not at all; **WB years only** |
| `WUTIRED` | VERIFIED | Tiredness during selected activities (0–6) | WB years only |
| Sleep quality / usual sleep / insomnia scale | **NOT FOUND** | — | — |

No "who" or "where" information is collected for sleep. Night-waking for infant care appears only if it was reported as a childcare activity (0301xx).

#### K. Child sleep

| Variable | Status | Definition | Notes |
|---|---|---|---|
| `TUCC2` | VERIFIED | "Time first household child < 13 woke up" | Household-level, children under 13 together |
| `TUCC4` | VERIFIED | "Time last household child < 13 went to bed" | Same |
| Child sleep duration | **NOT FOUND** | — | — |

#### L. Paid work, childcare and household labor

| Measure | Status | Codes / variables |
|---|---|---|
| Primary childcare, household children | VERIFIED | 0301xx "Caring For & Helping HH Children" (030101 physical care; 030102 reading; 030103 playing; … 030109 looking after; 030112 picking up/dropping off). 0302xx education. 0303xx health. *(LEX)* |
| Nonhousehold children | VERIFIED | 0401xx care; 0402xx education; **0403xx health** |
| Household activities | VERIFIED | 02xxxx (0201 housework, 0202 food preparation … 0209 household management) |
| Work | VERIFIED | 0501xx (050101 main job, 050102 other jobs …); 0502xx work-related activities |
| Travel | VERIFIED | 180381 for household childcare; 180501 travel related to working |
| Activity Summary naming | VERIFIED | `t` + 6-digit code (for example `t030101`). The multi-year file uses pooled codes (`TRCODEP`). |
| Secondary childcare | VERIFIED | `TRTCC`, `TRTCCTOT`, `TRTHH`, `TRTOHH` (own household children), `TRTNOHH`, `TRTONHH`, `TRTO`, `TRTCOC`. All refer to children **under 13**: "Secondary childcare is defined as having a child under age 13 in one's care while doing other activities." |
| Time with others | VERIFIED | Who file (`TUWHO_CODE`: 18/19 Alone; 20 Spouse; 22 Own household child …). Summary variables `TRTOHHCHILD`, `TRTSPOUSE`, `TRTFAMILY`, `TRTFRIEND`, `TRTALONE`. Not collected for sleep, grooming or personal activities, nor for work before 2010. |

Primary-childcare records do not identify which child received the care. Only the Who file links time to specific children.

#### M. Social support

**NOT FOUND.** Proxies only: time alone or with family and friends (Who file), and `WUINTERACT` in module years.

### 3.6 ATUS limitations for this project

- **Small samples:** about 6,100 respondents in 2025. Mothers with a youngest child aged 0–5, broken down by employment status, will require pooling years.
- **One diary day per person** gives population averages, not any individual's typical day.
- **Secondary childcare and `TUCC2`/`TUCC4` cover children under 13 only**, so band 12–17 is covered only at age 12.
- **CPS-derived covariates** (income, tenure, geography, parent type) are measured 2–5 months before the diary day.
- **Well-being and "well-rested" measures exist only in 4 module years**, and the 2010–13 activity-selection error applies.
- **Disrupted years:** 2020 (partial year) and 2025 (shutdown gap).

---

## 4. American Community Survey (ACS)

### 4.1 Source, documentation and access

| Item | Detail |
|---|---|
| **Producer** | U.S. Census Bureau |
| **ACS landing page** | https://www.census.gov/programs-surveys/acs |
| **PUMS landing / documentation / access** | https://www.census.gov/programs-surveys/acs/microdata.html · `.../microdata/documentation.html` · `.../microdata/access.html` |
| **PUMS data dictionaries** | https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/ (for example `PUMS_Data_Dictionary_2024.csv` [DD24], `PUMS_Data_Dictionary_2020-2024.csv` [DD5]) |
| **PUMS user guides** | 2024 1-year [UG24]: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/2024ACS_PUMS_User_Guide.pdf · 2020–2024 5-year [UG5]: `.../tech_docs/pums/2020_2024ACS_PUMS_User_Guide.pdf` |
| **Variable changes** | `https://www2.census.gov/programs-surveys/acs/tech_docs/pums/variable_changes/` |
| **Code lists (occupation/industry)** | `https://www2.census.gov/programs-surveys/acs/tech_docs/pums/code_lists/` |
| **Accuracy documents** | `https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/` |
| **Subject definitions** [SD24] | https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2024_ACSSubjectDefinitions.pdf (a 2025 version also exists) |
| **Microdata API** | https://www.census.gov/data/developers/data-sets/census-microdata-api.html. Documented form: `https://api.census.gov/data/2024/acs/acs1/pums?get=SEX,PWGTP,MAR&for=state:*&key=…` (5-year: `/data/2024/acs/acs5/pums`) |
| **Table APIs** | https://www.census.gov/data/developers/data-sets/acs-1year.html · `.../acs-5year.html` |
| **Other** | data.census.gov; MDAT (https://data.census.gov/mdat/), which "cannot currently inflation adjust PUMS variables." |

### 4.2 Years, geography and design

- **Published 1-year tables:** latest **2025**, released October 29, 2026.
- **1-year PUMS:** latest **2024**. The 2025 1-year PUMS release date is "TBD", and the `2025/acs/acs1/pums` endpoint returns 404.
- **5-year:** latest **2020–2024**, for both tables and PUMS.
- **2020 1-year:** Not released as standard data. In the Bureau's words: "The PUMS data have been released with experimental weights and replicate weights… [and] will not be released on data.census.gov." There is no 2020 `acs/acs1` API dataset.
- **PUMS geography:** region, division, `STATE` and `PUMA` only. "towns and counties (and other low-level geography) are not identified by any variables in the PUMS datasets." *(UG24 §VIII.B)*
  - Records from 2022 on use 2020-based PUMAs. Earlier records use 2010 PUMAs. The 2020–2024 5-year file crosswalks all its records to 2020 PUMAs.
- **Metro areas from PUMS:** There is **no official PUMA-to-CBSA file**. The official file is "2020 Census Tract to 2020 PUMA Relationship File." A metro approximation needs tract→PUMA plus tract→county→CBSA, or the GEOCORR tool (Missouri Census Data Center, non-federal, cited in UG5).
- **Published tables:** available for state, county, place, metropolitan/micropolitan area, PUMA and other geographies (1-year). The 5-year tables add tract and block group.
- **Sample:** 1-year PUMS is about 1% of the population, 5-year about 5%. PUMS is about two-thirds of the full ACS sample, so its estimates will not match published tables exactly. *(UG24 §II)*

### 4.3 Weights, variance and adjustment

- **Weights:** `PWGTP` (person) with `PWGTP1`–`PWGTP80`; `WGTP` (housing) with `WGTP1`–`WGTP80`.
- **Variance:** successive difference replication. Var = (4/80) Σ(xᵣ − x)². 90% MOE = 1.645 × SE. *(UG24 §VII)*
- **Linking records:** person and housing records merge on `SERIALNO`. `SPORDER` is the person number.
- **Income adjustment:** multiply by `ADJINC`/1,000,000. Applies to `WAGP`, `SEMP`, `PERNP`, `PINCP`, `HINCP`, `FINCP` and other income variables.
- **Housing adjustment:** multiply by `ADJHSG`/1,000,000. Applies to `GRNTP`, `SMOCP`, `VALP`, `RNTP`, `MRGP`, utilities and others. In 1-year PUMS, `ADJHSG` = 1,000,000. In 5-year files both factors differ by data year (for example, 2020: `ADJINC` 1222017, `ADJHSG` 1214548). *(UG24 §X.F–G; DD5)*

### 4.4 Candidate PUMS variables

Labels and codes are from DD24 unless noted. Variable name changes:
- **2019:** `RELP`→`RELSHIPP`, `WKW`→`WKWN`, `JWTR`→`JWTRNS`.
- **2021:** `FES` deleted (use `WORKSTAT`).
- **2023:** `ST`→`STATE`; industry codes moved to the 2022 basis.
- **2024:** HOA fees added to `CONP`.

#### A. Maternal identification and demographics

| Variable | Status | Label | Codes | Universe |
|---|---|---|---|---|
| `SEX` | VERIFIED | "Sex" | 1 Male; 2 Female | All |
| `AGEP` | VERIFIED | "Age" | 0 (under 1) … 99 (top-coded) | All |
| `RELSHIPP` | VERIFIED | "Relationship" (to reference person) | 20 Reference person; 21 Opposite-sex spouse; 22 Opposite-sex unmarried partner; 23 Same-sex spouse; 24 Same-sex unmarried partner; **25 Biological son or daughter; 26 Adopted son or daughter; 27 Stepson or stepdaughter**; 28 Sibling; 29 Father or mother; 30 Grandchild; 31 Parent-in-law; 32 Son/daughter-in-law; 33 Other relative; 34 Roommate/housemate; 35 Foster child; 36 Other nonrelative; 37/38 GQ | All; **2019+** (`RELP` before) |
| `MSP` / `MAR` | VERIFIED | Marital status (with spouse present/absent) | MSP 1–6; MAR 1–5 | MSP age 15+ |
| `SFN` / `SFR` | VERIFIED | Subfamily number / relationship | SFR: 1 Married couple, no children; 2 Married couple with children; **3 Parent in one-parent subfamily**; 4 Child in married-couple subfamily; **5 Child in mother-child subfamily**; 6 Child in father-child subfamily | Persons in subfamilies |
| `PAOC` | VERIFIED | "Presence and age of own children" | 1 Own children under 6 only; 2 6–17 only; 3 Both; 4 No own children | **Females 16+**, not in group quarters. Derivation rule for subfamily mothers **UNCERTAIN** |
| `OC` / `RC` | VERIFIED | Own child / related child | 0/1 | Not GQ |
| `FER` | VERIFIED | "Gave birth to child within the past 12 months" | 1 Yes; 2 No | Females 15–50 |
| `ESP` | VERIFIED | "Employment status of parents" (on the child's record) | 1–8 (two parents / father only / mother only × labor force) | Own children of householder and subfamily children |
| Parent pointer | **NOT FOUND** | No variable links a child to their parent's person number | — | — |
| "Own child" concept | VERIFIED | "A never-married child under 18 years who is a son or daughter by birth, a stepchild, or an adopted child of the householder." *(SD24)* | — | — |

#### B. Child age and family composition

| Variable | Status | Label | Codes / notes |
|---|---|---|---|
| `NP` | VERIFIED | "Number of persons in this household" | 1–20 |
| `NOC` / `NRC` | VERIFIED | Number of own / related children in household (unweighted) | 0–19 |
| `HUPAC` / `HUPAOC` / `HUPARC` | VERIFIED | Household presence and age of children / own children / related children | 1 Under 6 only; 2 6–17 only; 3 Both; 4 None |
| `FPARC` | VERIFIED | "Family presence and age of related children" | **Under 5** / 5–17 cut point (not under 6) |
| `HHT` | VERIFIED | "Household/family type" | 1 Married couple; 2 Male householder, no spouse; 3 Female householder, no spouse; 4–7 Nonfamily |
| `HHT2` | VERIFIED | "Household/family type (includes cohabiting)" | 01–12 (for example 06 Female householder, no spouse/partner, with children of the householder <18); 2019+ |
| `CPLT`, `PARTNER`, `MULTG`, `NPF`, `PSF` | VERIFIED | Couple type; unmarried partner household; multigenerational; persons in family; subfamilies present | — |
| `WIF` / `WKEXREL` / `WORKSTAT` | VERIFIED | Workers in family; work experience of householder and spouse; work status (replaces `FES` from 2021) | — |

#### C. Employment status and work hours

| Variable | Status | Label | Codes | Universe |
|---|---|---|---|---|
| `ESR` | VERIFIED | "Employment status recode" | 1 Civilian employed, at work; 2 …with a job but not at work; 3 Unemployed; 4/5 Armed forces; 6 Not in labor force | Age 16+ |
| `WKHP` | VERIFIED | "Usual hours worked per week past 12 months" | 1–98; 99 = 99+ | Worked in past 12 months |
| `WKWN` | VERIFIED | "Weeks worked during past 12 months" | 1–52 | Same; 2019+ |
| `WKL` | VERIFIED | "When last worked" | 1 Within 12 months; 2 1–5 years; 3 Over 5 years or never | Age 16+ |
| `WRK` | VERIFIED | "Worked last week" | 1/2 | — |
| `COW` | VERIFIED | "Class of worker" | 1–9 | — |
| `JWMNP` | VERIFIED | "Travel time to work" | 1–200 minutes | Workers not working from home |
| `JWTRNS` | VERIFIED | Means of transportation | 11 = Worked from home | 2019+ |
| `JWAP` / `JWDP` | VERIFIED | Time of arrival at / departure for work | Time intervals | — |
| Full-time, year-round | Derived | "usually worked 35 hours or more per week for 50 to 52 weeks in the past 12 months" *(SD24)* | `WKHP` ≥ 35 and `WKWN` ≥ 50 | — |

`ESR` is current status (reference week). `WKHP` and `WKWN` refer to the past 12 months.

#### D. Occupation and industry

| Variable | Status | Label |
|---|---|---|
| `OCCP` | VERIFIED | "Occupation recode for 2018 and later based on 2018 OCC codes" |
| `SOCP` | VERIFIED | SOC-based occupation, 2018 SOC |
| `INDP` | VERIFIED | "Industry recode for 2023 and later based on 2022 IND codes" (2018–2022 used 2017 codes) |
| `NAICSP` | VERIFIED | NAICS-based industry (2022 NAICS for 2023+) |

How 2020–2022 industry codes are harmonized in the 5-year file is **UNCERTAIN**.

#### E. Earnings and income

All amounts cover the past 12 months and must be multiplied by `ADJINC`.

| Variable | Status | Label | Universe |
|---|---|---|---|
| `WAGP` | VERIFIED | "Wages or salary income past 12 months" | Age 15+ |
| `SEMP` | VERIFIED | "Self-employment income past 12 months" (losses allowed) | Age 15+ |
| `PERNP` | VERIFIED | "Total person's earnings" | **Age 16+** |
| `PINCP` | VERIFIED | "Total person's income" | Age 15+ |
| `FINCP` | VERIFIED | "Family income (past 12 months…)" | Housing record; families |
| `HINCP` | VERIFIED | "Household income (past 12 months…)" | Housing record |
| `POVPIP` | VERIFIED | "Income-to-poverty ratio recode" | 0–500; 501 = 501%+ |
| `FS`, `PAP`, `SSIP`, … | VERIFIED | SNAP receipt (household); public assistance; SSI; other components | — |

**Official definitions (SD24):**
- **Earnings:** "the sum of wage or salary income and net income from self-employment."
- **Household income:** "the income of the householder and all other individuals 15 years old and over in the household, whether they are related to the householder or not."
- **Family income:** "the incomes of all members 15 years old and over related to the householder are summed."

#### F. Housing tenure and costs

These are housing-record variables. Dollar amounts must be multiplied by `ADJHSG`.

| Variable | Status | Label | Codes / notes |
|---|---|---|---|
| `TEN` | VERIFIED | "Tenure" | **1 Owned with mortgage or loan (include home equity loans); 2 Owned free and clear; 3 Rented; 4 Occupied without payment of rent** |
| `GRNTP` | VERIFIED | "Gross rent (monthly amount…)" | Renters paying rent |
| `RNTP` | VERIFIED | "Monthly rent" (contract rent) | — |
| `GRPIP` | VERIFIED | "Gross rent as a percentage of household income past 12 months" | 1–100; 101 = 101%+. Blank for owners, no-rent units and households with no income |
| `SMOCP` | VERIFIED | "Selected monthly owner costs" | Owners |
| `OCPIP` | VERIFIED | "Selected monthly owner costs as a percentage of household income during the past 12 months" | 1–100; 101+ |
| `VALP` | VERIFIED | "Property value" | `ADJHSG` required since 2022 |
| `MRGP`, `MRGX`, `MRGI`, `MRGT`, `SMP` | VERIFIED | First mortgage payment; mortgage status (1 Mortgage; 2 Contract to purchase; 3 None); whether payment includes insurance or taxes; second mortgage / home equity | — |
| `TAXAMT`, `INSP`, `CONP`, `MHP` | VERIFIED | Property taxes; insurance; condo/HOA fee (HOA included from 2024); mobile home costs | — |
| `ELEP`, `GASP`, `WATP`, `FULP` (+ flags) | VERIFIED | Utility costs | — |

**Official definitions (SD24):**
- **Gross rent:** "the contract rent plus the estimated average monthly cost of utilities (electricity, gas, and water and sewer) and fuels (oil, coal, kerosene, wood, etc.) if these are paid by the renter (or paid for the renter by someone else)."
- **Rent burden:** monthly gross rent ÷ (household income ÷ 12). "Units for which no rent is paid and units occupied by households that reported no income or a net loss comprise the category 'Not computed.'"
- **Selected monthly owner costs:** mortgages (first, second, home equity), real estate taxes, insurance, utilities and fuels, plus condo/HOA and mobile home fees where applicable.

**Comparability breaks:**
- **2020:** limits on owner-cost components changed, and home-equity-only loans are no longer counted as a first mortgage.
- **2022:** `VALP` adjustment required.
- **2024:** HOA fees added.

#### G–M. Well-being, sleep, aggravation, time use, support

**NOT FOUND.** ACS has none of these. Disability items such as `DREM` (cognitive difficulty) measure functional limitation, not well-being. The only work-time context is commute time and departure time.

### 4.5 Published tables (all VERIFIED to exist in 2024 acs5 and 2025 acs1; row-level detail not checked)

| Table | Title |
|---|---|
| B23003 | "Presence of Own Children Under 18 Years by Age of Own Children Under 18 Years by Employment Status for Females 20 to 64 Years" |
| B23008 | "Age of Own Children Under 18 Years in Families and Subfamilies by Living Arrangements by Employment Status of Parents" |
| B23007 / B23009 / B23010 | Own children by family type × employment status / number of workers / work experience |
| B13012 | "Women 16 to 50 Years Who Had a Birth in the Past 12 Months by Marital Status and Labor Force Status" |
| B17010 / B17006 / S1702 | Poverty of families / related children by family type and age of children |
| B11003 / B09002 / S1101 / S0901 | Family type by presence and age of own children; children's characteristics |
| B19126 / B20017 / B20004 / S2001 / S1903 | Median family income by presence of own children; median earnings |
| S2301 / S2302 | Employment status; employment characteristics of families |
| B25003 / B25070 / B25091 / B25106 / B25064 / B25071 / B25092 / S2503 | Tenure; gross rent as % of income; mortgage status by owner costs as % of income; tenure by housing costs as % of income; medians; financial characteristics |

### 4.6 ACS limitations for this project

- **Linking mothers and children:**
  - **Linkable:** a female householder (`RELSHIPP` = 20, `SEX` = 2) with children coded 25/26/27, with exact ages from `AGEP`; and subfamily mothers (`SFR` = 3) with `SFR` = 5 children sharing an `SFN`.
  - **Not reliably linkable:**
    - Mothers who are the householder's **spouse or partner**: the children's codes describe their relationship to the householder.
    - Mothers who are roommates or other nonrelatives, when no subfamily is formed.
    - Some grandchild situations.
  - **Without linking:** `PAOC` and `FER` flag mothers, but give only under-6 / 6–17 detail.
  - **Not observable:** non-co-resident children.
- **Own child includes step- and adopted children.** Biological, adopted and step can be separated only for the householder's children (`RELSHIPP` 25/26/27).
- **Income concepts:** `PERNP` (the mother's earnings) ≠ `FINCP` (householder's family) ≠ `HINCP` (all household members). A subfamily mother's own family income is not separated out. Income covers a rolling 12 months, while household composition is as of the interview date.
- **Housing burden is based on household income**, not the mother's earnings, and is capped at 101%.
- **Age cut points in published variables** are under 6 / 6–17 (under 5 in `FPARC`). The under-6 split matches band 0–5, but 6–11 and 12–17 cannot be separated without linked children and `AGEP`.
- **No well-being measures.** ACS describes circumstances, not experience.

---

## 5. BEA Regional Price Parities (RPP)

### 5.1 Source, documentation and access

| Item | Detail |
|---|---|
| **Producer** | U.S. Bureau of Economic Analysis |
| **Landing page** | https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area |
| **Latest release** | "Real Personal Consumption Expenditures by State and Real Personal Income by State, 2024" (BEA 26-10), **Feb 19, 2026**: https://www.bea.gov/news/2026/real-personal-consumption-expenditures-state-and-real-personal-income-state-2024 · PDF: https://www.bea.gov/sites/default/files/2026-02/rpp0226.pdf |
| **Next release** | 2025 data, **Dec 10, 2026** |
| **Methodology** | "Methodology for Regional Price Parities, Real Personal Consumption Expenditures, and Real Personal Income" (July 2025): https://www.bea.gov/sites/default/files/methodologies/Methodology-for-Regional-Price-Parities_0.pdf |
| **Technical notes** | https://www.bea.gov/news/technical-notes-regional-price-parities-and-implicit-regional-price-deflators |
| **Guidance article** | "Price Adjustment Using Regional Price Parities," *Survey of Current Business*, May 2024: https://apps.bea.gov/scb/issues/2024/05-may/0524-regional-price-parities.htm |
| **Interactive tables** | https://apps.bea.gov/itable/?ReqID=70&step=1 (PDF, Excel and CSV export) |
| **Bulk downloads** | https://apps.bea.gov/regional/downloadzip.htm (RPP file names **UNCERTAIN**) |
| **API** | User guide: https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf (Appendix N "Regional", Apr 2026). Free key: https://apps.bea.gov/api/signup/ |
| **Data archive** | https://apps.bea.gov/histdata/RegionalAccounts.html (superseded vintages) |

### 5.2 Definition and construction

- **Definition:** RPPs "measure the differences in price levels across states for a given year and are expressed as a percentage of the overall national price level." *(2024 release)* They are "a weighted average of the price level of goods and services for the average consumer in one geographic region compared to all other regions in the United States." *(Methodology ¶1.2)* U.S. = 100.
- **All items:** "covers all consumption goods and services including housing rents. Housing rents are often the main driver in differences in RPPs." *(2024 release)*
- **Inputs:**
  - BLS CPI price quotes from 32 index areas. Rural counties take their CPI regional price level.
  - **ACS PUMS tenant rents and utility costs** at the PUMA level. Owners are assigned rent price levels.
  - EIA electricity and gas prices from 2017.
  - BEA's PCE by state for expenditure weights.
  - About 170 categories for more than 3,000 counties are combined with the Geary method. Results are estimated at county level but **published only for larger areas**. *(Methodology §2, §4)*

### 5.3 Components, geography and years

| Measure | Status | Definition | API table / line code |
|---|---|---|---|
| RPP, all items | VERIFIED | All consumption goods and services, including rents | `SARPP` (state), `MARPP` (metro), `PARPP` (state metro/nonmetro portions). iTable Statistic 1 = "All Items (Index)". API `LineCode` **UNCERTAIN** (likely 1) |
| RPP, goods | VERIFIED (component exists) | One of four components: "goods, housing rents, utilities, and 'other services'" *(Methodology ¶4.22)* | Line code **UNCERTAIN** |
| RPP, housing rents | VERIFIED | Labeled "Services: Rents (Index)" in the release's interactive table | iTable Statistic 3. API `LineCode` **UNCERTAIN** |
| RPP, utilities | VERIFIED (component exists) | Electricity, gas, other fuels, water | Exact label and line code **UNCERTAIN** |
| RPP, other services | VERIFIED (component exists) | Remaining services | Exact label and line code **UNCERTAIN** |
| Finer categories (food, medical, childcare…) | **NOT FOUND** as published | — | — |
| Real personal income / real PCE | VERIFIED | Nominal values adjusted by RPP and the national PCE price index, constant 2017 dollars | **States only** after the 2024 release. iTable `SARPI`; not in the API table list |
| Implicit regional price deflator | VERIFIED | RPP × U.S. PCE price index; used for change over time | iTable `SAIRPD`; states |
| County RPPs | NOT PUBLISHED | Estimated internally only | — |

**API structure** (Appendix N):
- Dataset `Regional` (the old `RegionalData` no longer works).
- Parameters: `UserID` (key), `TableName`, `LineCode`, `GeoFips` (for example `STATE`, `MSA`, `PORT`), `Year` (`ALL`, `LAST5`, `LAST10` or a list).
- `SARPP`, `MARPP` and `PARPP` are listed as starting in **2008**.
- Line codes can be discovered with `GetParameterValuesFiltered`, which needs a key.

**Years:** 2008–2024. Earlier figures were experimental. Past years are revised in each release, so record the release vintage used. *(Methodology ¶5.3)*

**Geography:**
- **States and DC:** VERIFIED.
- **Metro areas: UNCERTAIN going forward.** The 2024 release states: "BEA has discontinued publication of statistics for metropolitan statistical areas and metropolitan and nonmetropolitan portions… RPPs will continue to be published by state and local areas." The same release says "Metropolitan area RPP statistics are available on the BEA website," and an April 2026 BEA infographic shows 2024 RPPs for 387 metro areas plus a U.S. nonmetropolitan portion. **Confirm in the interactive tables whether 2024 metro and portion RPPs exist and whether metro RPPs will continue for 2025.**
- **Metro delineation vintage: UNCERTAIN.** The 387-area count suggests the July 2023 OMB delineations, but that is unconfirmed.

### 5.4 Using RPP with ACS earnings and housing costs

- **BEA adjustment formula:** "RPP-adjusted results are obtained by dividing each region's current dollar estimates by its RPP" *(SCB 2024)*, i.e., nominal ÷ (RPP/100). The technical notes give an example: $12,000 at RPP 120 = $10,000.
- **Uses in this project:**
  - Compare mothers' nominal and RPP-adjusted earnings across states (E4).
  - Place ACS rent burden alongside the housing-rent RPP, to see whether high burden coincides with high rent levels or with low earnings (E4, E5).
  - Attach state RPP to NSCH records by `FIPSST` as context for material hardship (`ACE1`) (E5).
- **Comparing across years:** "Each set of annual RPPs is independently estimated and cannot be compared across years." *(SCB 2024)* Use implicit regional price deflators for change over time.

### 5.5 What RPP is not

- **Not a complete affordability, cost-of-living or living-wage measure.** It is a relative price-level index with no absolute costs or thresholds. It reflects an average consumer's basket under PCE weights, not the spending of a specific household type such as a mother with young children.
- **No childcare component.** "Child care and nursery school fees" are in the basket but have no CPI regional price variation *(Methodology ¶4.11)*. RPP therefore **cannot measure geographic differences in childcare costs**. Medical items and education fees are treated the same way.
- **Owner costs are proxied by rents.**
- **Possible circularity:** the rent component is built from ACS PUMS rents, so ACS housing-cost analyses and RPP rent parities share a source.
- **Area-level only:** associations with RPP are geographic findings, not individual-level ones.
- **No BEA guidance was found for adjusting individual or subgroup estimates.** BEA presents adjustment for aggregate area estimates.
- BEA did not explicitly say RPP is "not a cost-of-living index". This inventory takes that position based on the methodology described above.

---

## 6. Cross-dataset comparison

### 6.1 Individual-level analysis and linkage

| Dataset | Individual-level? | Can be merged with other surveys at the individual level? |
|---|---|---|
| NSCH | Yes (child-level weights; mother via Adult 1/Adult 2) | **No** |
| ATUS | Yes (respondent; diary activities) | **No** |
| ACS PUMS | Yes (person and housing unit) | **No** |
| BEA RPP | No (area) | Attached by geography only, as context |

NSCH, ATUS and ACS respondents are different people. **No individual-level merging, matching or cross-survey imputation will be done.** Each survey is analyzed separately, and results are triangulated by direction and pattern. Area-level indicators (RPP, published ACS tables) may be attached to individual records by geography as contextual variables.

### 6.2 Definitional differences

| Concept | NSCH | ATUS | ACS | Implication |
|---|---|---|---|---|
| **Mother** | Female respondent who is the "Biological or Adoptive Parent" **of the sampled child** | Female respondent with "own" household children (biological, step **and** adopted together) | Female householder with children coded 25/26/27, subfamily mothers, or `PAOC` | Step-mothers are excluded in NSCH but included in the ATUS "own child" concept unless separated with CPS parent type (2007+) |
| **Child age** | Sampled child's exact age; others only as age-group counts | Exact ages of all own household children | Exact ages for linkable children; otherwise under-6 / 6–17 recodes | "Youngest child" is not available in NSCH |
| **Employment** | Current status (2020+); 50-of-52-weeks indicator (2016–2019); no hours | Last 7 days; `TELFS` 5 categories; FT/PT; usual hours | `ESR` reference week; hours and weeks over past 12 months | Reference periods differ; NSCH has no hours |
| **Unemployed vs. not in labor force** | Code 4 vs. 5/6 (2023+); not separable 2016–2019 | `TELFS` 3–4 vs. 5 | `ESR` 3 vs. 6 | Comparable from 2020 only, and only approximately |
| **Income** | Family income ÷ poverty threshold, prior calendar year, imputed, 50–400 | Weekly earnings (wage/salary); categorical family income (CPS) | Earnings, person, family and household income, past 12 months | Never compare NSCH family-income ratios with ACS earnings directly |
| **Housing tenure** | 4 categories (2018+) | 3 categories (owned / rented / no cash rent) | 4 categories (`TEN`) | NSCH and ACS tenure categories match; ATUS does not separate mortgage status |
| **Sleep** | Child only; different items for 0–5 and 6–17 | Respondent's diary minutes; WB "well-rested" | None | Maternal and child sleep come from different surveys |
| **Population of estimates** | Children | Person-days (population 15+) | Persons / households | Labels must reflect each frame |

### 6.3 Coverage of age bands

The project bands (0–5, 6–11, 12–17; research plan v0.4) match the NSCH topical forms T1, T2 and T3 exactly, so every NSCH item covers either a whole band or none of it.

| Measure | 0–5 | 6–11 | 12–17 |
|---|---|---|---|
| NSCH items on all forms (mental health, aggravation, support, tenure, FPL, `BEDTIME`) | ✅ | ✅ | ✅ |
| NSCH T1-only items (`K6Q27`, `HOURSOFCARE`, `HOURSLEEP05`) | ✅ | ✖ | ✖ |
| NSCH `HOURSLEEP` (weeknight) | ✖ | ✅ | ✅ |
| NSCH T2–T3-only items (`K8Q21`, `K9Q96`) | ✖ | ✅ | ✅ |
| ATUS primary childcare (0301xx) | ✅ | ✅ | ✅ |
| ATUS secondary childcare; `TUCC2`/`TUCC4` (children under 13) | ✅ | ✅ | ◐ age 12 only |
| ACS exact-age bands (linked children + `AGEP`) | ✅ | ✅ | ✅ |
| ACS recodes (`PAOC`, `HUPAOC`: under 6 / 6–17) | ✅ | ◐ combined with 12–17 | ◐ combined with 6–11 |

Child sleep hours still use different NSCH items for band 0–5 (`HOURSLEEP05`) and bands 6–11/12–17 (`HOURSLEEP`). These can be compared within a band, but not across the 0–5 boundary.

### 6.4 Within-early-childhood sub-analysis: 0–2 vs. 3–5

This is a **secondary sub-analysis within band 0–5** (research plan v0.5, Section 1 and Section 3.4). It does not replace the primary bands. This section records what each dataset can support, based on the variables verified above. **No sample sizes have been estimated yet.** Feasibility depends on counts that can only be produced once the data are downloaded.

#### NSCH

| Aspect | Assessment | Basis |
|---|---|---|
| Exact age | ✅ `SC_AGE_YEARS` (0–17) gives the sampled child's exact age. `SC_AGE_LT4`/`LT6`/`LT9`/`LT10` add detail under 1 year. | VERIFIED (Section 2.4 B) |
| Same questionnaire | ✅ Ages 0–2 and 3–5 are both on form T1, so every T1 item is asked of both subgroups with identical wording. | VERIFIED (Section 2.2) |
| Whose age | ◐ The **sampled child's** age, not the youngest child's. `TOTAGE_0_5` shows how many children aged 0–5 are in the household but not whether any is under 3. A mother of a sampled 4-year-old and an unsampled 1-year-old is classified as 3–5. | VERIFIED (Section 2.4 B) |
| Measures comparable across subgroups | Mental health (`A1_MENTHEALTH`), aggravation (`K8Q30`–`K8Q34`), support (`K8Q35`), resilience, employment (`A1_EMPLOYED_R`, 2023+), FPL, `ACE1`, `TENURE`, `BEDTIME`, `HOURSLEEP05`, `K6Q27`, `HOURSOFCARE` (2025 only) | VERIFIED universes (T1 or T1–T3) |
| Child sleep caveat | `HOURSLEEP05` (24 hours including naps; top category "12 or more hours") is comparable between 0–2 and 3–5, but the 0–2 group may cluster in the top category (possible ceiling effect). Report category distributions, not estimated hours. **Do not compare with `HOURSLEEP`** (weeknights, ages 6–17). | Codes VERIFIED; the ceiling effect is an expectation to check in the data |
| Childcare caveat | `HOURSOFCARE` exists only in 2025, and `K6Q20` (10+ hours of care) only in 2016–2022. Neither exists in 2023–2024. Do not pool the two items. | VERIFIED |
| Weights | Children 0–5 are oversampled, which helps both subgroups. Use subpopulation estimation. | VERIFIED (FAQ25) |
| **Verdict** | **Supported**, defined by the sampled child's age. | |

#### ATUS

| Aspect | Assessment | Basis |
|---|---|---|
| Exact age | ✅ Roster `TEAGE` gives each household member's exact age (0 = under 1). Combined with `TERRP` = 22 (own household child), this gives the **exact age of the mother's youngest own household child**. | VERIFIED (Section 3.5 A–B) |
| Do not use `TRYHHCHILD` | ✖ It gives the youngest **household** child of any relationship (for example a niece or grandchild), not the youngest own child. | VERIFIED |
| Own-child definition | ◐ "Own" includes step- and adopted children. Separating biological/adoptive children needs the ATUS-CPS parent-type variables (2007+, renamed 2020), measured 2–5 months earlier. A child born after the CPS interview has no CPS parent-type record. | VERIFIED |
| Timing of roster ages | UNCERTAIN whether the roster (and therefore `TEAGE`) is updated at the ATUS interview or carried from the CPS interview. This matters at the age-3 boundary. Check the User's Guide. | Not verified |
| Maternal sleep | ✅ Diary minutes for sleeping (`t010101`) and sleeplessness (`t010102`) apply equally to both subgroups. `WEREST` (well-rested) exists only in Well-Being Module years (2010, 2012, 2013, 2021), so subgroup cells there will be very small. | VERIFIED |
| Paid work | ✅ Work activity codes (0501xx), `TELFS`, `TRDPFTPT`, usual hours `TEHRUSLT` | VERIFIED |
| Primary childcare | ◐ 0301xx codes apply to both subgroups, but activities do **not** identify which child received care. Classifying mothers by youngest child is a household-level comparison, not a child-level one. | VERIFIED |
| Secondary childcare | ✅ All secondary-childcare measures cover children **under 13**, so both 0–2 and 3–5 are fully covered. (Band 12–17 coverage limits are unchanged; Section 6.3.) | VERIFIED |
| Unpaid household labor | ✅ Household activity codes (02xxxx) apply equally | VERIFIED |
| Sample size | UNCERTAIN. About 6,100 respondents in 2025. Mothers whose youngest own child is 0–2 or 3–5, split by employment status, are expected to need **pooled years**. Weekday/weekend splits will thin the cells further. Counts must be produced before committing to estimates. Households with children are oversampled, which helps. | Respondent count VERIFIED; subgroup counts not yet estimated |
| Disrupted years | Exclude or handle 2020 (partial year, `TU20FWGT`) and late 2025 (shutdown gap) explicitly when pooling. | VERIFIED |
| **Verdict** | **Supported in principle** for maternal sleep, paid work, primary and secondary childcare and unpaid labor, defined by the youngest own household child. **Reliability depends on pooled sample sizes**, still to be confirmed. Well-Being Module subgroup estimates are likely too small. | |

#### ACS PUMS (not a priority for this sub-analysis)

`AGEP` gives exact ages for children who can be linked to their mother (female householder's children coded 25/26/27; subfamily children). The `PAOC` and `HUPAOC` recodes cannot separate 0–2 from 3–5. Possible for linkable mothers only (Section 4.6).

#### Rules carried into the analysis

- Label every result "within-early-childhood sub-analysis (0–2 vs. 3–5)" and keep it separate from primary-band results.
- Compare the subgroups only on measures asked identically of both. Never compare NSCH `HOURSLEEP05` with `HOURSLEEP`.
- State the age definition: sampled child (NSCH) vs. youngest own household child (ATUS). Because these definitions differ, NSCH and ATUS sub-analysis results are triangulated, not combined.
- Suppress or flag estimates that fail each source's reliability rules. Drop the sub-analysis for measures that cannot be estimated reliably, rather than implying coverage.

### 6.5 Geographic comparability

- **Common level: state.** NSCH (`FIPSST`), ATUS (`GESTFIPS`), ACS PUMS (`STATE`), ACS tables and BEA RPP (`SARPP`) all identify states. ATUS state samples are not designed for state estimates.
- **Metro areas:**
  - ACS tables have metro areas directly.
  - ACS PUMS needs an approximate PUMA-to-metro allocation.
  - NSCH has only metro status and limited CBSA flags.
  - ATUS identifies only some CBSAs.
  - BEA metro RPPs are uncertain after 2024.
  - Metro delineations differ by vintage across sources.
- **Ecological inference:** state- or metro-level associations remain area-level findings.

### 6.6 Temporal comparability

| Dataset | Usable span | Key breaks |
|---|---|---|
| NSCH | 2016–2025 | Employment items change in 2020 and 2023; `FAMILY_R` from 2017; `TENURE` from 2018; housing instability items from 2022; `EMOSUP*` end after 2022; childcare item gap 2023–2024; use enhanced files for 2016–2021 |
| ATUS | 2003–2025 | 2020 partial year (special weight); 2025 shutdown gap; occupation/industry scheme changes; CPS parent-type variables 2007–2019 vs. 2020+; WB module only 2010, 2012, 2013, 2021 |
| ACS PUMS | 1-year through 2024; 5-year 2020–2024 | 2020 1-year experimental only; variable renames in 2019, 2021 and 2023; PUMA vintage change in 2022; owner-cost definition changes in 2020 and 2024 |
| BEA RPP | 2008–2024 | **Not comparable across years** (use deflators for change); revised each release; metro series status after 2024 |

**Overlap:** **2018–2024** is the common window where NSCH tenure, ATUS, ACS PUMS and BEA RPP all exist. 2020 needs special handling in every source.

---

## 7. Open items for further investigation

| # | Item | Dataset | Why it matters |
|---|---|---|---|
| 1 | Read the NSCH Analytic Guide in full | NSCH | Analysis guidance not yet reviewed |
| 2 | DRC construction of the aggravation, coping and family resilience indicators (DRC pages returned 403) | NSCH | Needed only if DRC indicators will be compared with project composites |
| 3 | Codes for `A1_MARITAL`; confirm `TOTAGE_*` and `AGEPOS4` across all years | NSCH | Family structure and youngest-child approximation |
| 4 | `TRDPFTPT` hours threshold; `HEFAMINC` bracket labels; multi-year replicate weight names | ATUS | Employment categories, income bands, variance |
| 5 | Latest response rates (UG Table 3.3) | ATUS | Nonresponse context |
| 6 | `PAOC` derivation for subfamily mothers; industry harmonization in the 5-year file; treatment of negative income in `GRPIP`/`OCPIP` | ACS | Mother identification; occupation trends; burden calculation |
| 7 | Row structure of B23003, B23008 and B17010 (age cut points) | ACS | Whether tables match the project bands |
| 8 | API `LineCode` values for every RPP component; exact component labels | BEA | Retrieval |
| 9 | Whether 2024 `MARPP`/`PARPP` exist, and whether metro RPPs continue for 2025 | BEA | Metro comparisons (visualization 9) |
| 10 | Metro delineation vintage used by BEA | BEA | PUMA/metro alignment |
| 11 | A separate official source for geographic childcare costs, if wanted | — | RPP has no childcare component |
| 12 | Whether ATUS roster ages (`TEAGE`) are updated at the ATUS interview or carried from the CPS interview | ATUS | Classification at the age-3 boundary in the 0–2 vs. 3–5 sub-analysis (Section 6.4) |
| 13 | Unweighted counts of mothers with a child 0–2 vs. 3–5, by employment status, per year and pooled | NSCH, ATUS | Whether sub-analysis questions U1–U4 can be estimated reliably |

---

## 8. Recommended retrieval order

Priority is based on research value, verification status and how hard each source is to process.

1. **NSCH 2025 topical file (Stata or SAS), then the enhanced 2018–2024 files.** This is the core well-being dataset: maternal mental health, aggravation, support, child sleep, employment (2023+ detail), FPL, tenure. 2018 is the first year with `TENURE`.
2. **ACS 1-year PUMS 2024 (person + housing) and/or 5-year PUMS 2020–2024.** Earnings, occupation, employment, household composition, tenure and housing burden for linkable mothers. The Microdata API is available for targeted extracts.
3. **BEA RPP, state level (`SARPP`), 2018–2024.** Small and simple. Confirm line codes after obtaining an API key, or export from the interactive tables. Add metro-level data only after item 9 above is resolved.
4. **ATUS multi-year 2003–2025 files** (respondent, activity summary, roster, ATUS-CPS, replicate weights), plus **Well-Being Module** files. These are the largest and most complex files, and are needed for time-use and maternal sleep analyses.
5. **Published ACS tables** (B23003, B23008, B25070, B25091, S2302 …) for state and metro context, after their row structures are checked.

For each file, record the source URL, release vintage, download date and checksum, as required by the research plan's data acquisition notes.
