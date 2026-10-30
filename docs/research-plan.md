# Research Plan

## The Psychology of Working Motherhood: Employment, Time, and Maternal Well-Being in the United States

| | |
|---|---|
| **Document status** | Draft v0.5: within-early-childhood sub-analysis (0–2 vs. 3–5) added |
| **Created** | 2026-10-30 |
| **Last revised** | 2026-10-30 |
| **Scope** | Descriptive and associational secondary analysis of public U.S. survey and price data |
| **Causal claims** | None. All hypotheses and research questions are stated as associations. |
| **Companion document** | `docs/dataset-inventory.md`: source-backed validation of datasets and variables |

### Revision history

| Version | Changes |
|---|---|
| v0.1 | First specification: "Parenting Under Pressure", covering all parents and caregivers of children 0–5. Datasets: NSCH, GSS, ACS. |
| v0.2 | Central focus changed to **working mothers**. GSS replaced by the **American Time Use Survey (ATUS)**. Added requirements for measuring employment and labor-force status and for identifying mothers. D3.js recorded as the preferred visualization framework. |
| v0.3 | **Child age bands** changed to **0–2, 3–6, 7–12, 13–17** (replacing 0–5 / 6–17). Added a **sleep research strand** covering maternal sleep, child sleep, and their relationship to employment and well-being. Added an **economic and housing dimension**: expanded ACS, new **BEA Regional Price Parities** dataset, NSCH household financial context, six new economic research questions, economic methodology and new visualization concepts. |
| v0.4 | **Child age bands** changed to **0–5, 6–11, 12–17**, replacing 0–2 / 3–6 / 7–12 / 13–17. The new bands match the NSCH questionnaire forms (T1, T2, T3; see `docs/dataset-inventory.md`), so NSCH form-specific items no longer split a band. Primary population is now mothers of children 0–5. |
| v0.5 | Added a **within-early-childhood sub-analysis** comparing mothers of children **0–2 vs. 3–5** (Section 1, Section 3.4), to keep the original interest in the caregiving demands of children under 3. It is a secondary analysis and does **not** replace the primary bands. ATUS feasibility documented in `docs/dataset-inventory.md` Section 6.4. |

### Verification convention

Descriptions in this plan are working descriptions, not quoted question wording. Results of the verification work are recorded in `docs/dataset-inventory.md`, which takes precedence over this plan wherever the two differ.

- **`[VERIFY]`**: Confirm the variable name, survey years, universe (who was asked), response categories and coding against the **official, year-specific documentation** before use. Variable names and codes can change between survey years.
- **`[TO IDENTIFY]`**: The construct is needed but the variable has not been chosen yet. Do not assume a name or that the measure exists.
- Treat all source URLs as entry points. Check that they still resolve before citing them in final outputs.

---

## 1. Project overview

Many U.S. mothers combine paid employment with caregiving, and their circumstances vary widely: full-time or part-time work, unemployment, being out of the labor force, partner presence, earnings, housing costs, the cost of living where they live, sleep, childcare demands and access to support. This project describes how the **psychological well-being and lived experience of working mothers** relate to employment conditions, economic and housing pressures, time and sleep, childcare responsibilities and social support.

**Economic conditions are included to help explain maternal well-being.** The project is not a general economic dashboard. Every economic analysis has to connect back to a question about mothers' experience.

The project is built as a portfolio of reproducible analyses using four national data sources. Each source answers a different part of the question. **Survey respondents from different datasets are never linked at the individual level** (see Section 6).

### Central research question

> How do employment conditions, economic pressures, childcare responsibilities, and social support relate to the psychological well-being of working mothers in the United States?

### Child age bands

These are the project's age groups:

| Band | Ages | Developmental stage | Rationale |
|---|---|---|---|
| 1 | **0–5** | Infancy through preschool | The most intensive caregiving demands, childcare arrangements and the return to work |
| 2 | **6–11** | School age | School-day schedules; before- and after-school care |
| 3 | **12–17** | Adolescence | Lower direct-care demands, different parenting stressors |

**Why these bands.** They match the three NSCH topical questionnaire forms exactly (T1: 0–5, T2: 6–11, T3: 12–17). Every NSCH item is therefore asked either for a whole band or not at all. The 0–5 boundary also matches the ACS "under 6 / 6–17" recodes.

**Applying the bands in each dataset.** Each dataset determines child age differently: in NSCH it is the sampled child, in ATUS the youngest own household child, and in ACS own children (Section 4). Some measures still cover only part of a band. For example, ATUS secondary childcare covers children under 13 only, so band 12–17 is covered only at age 12. Any band a measure covers only partly will be flagged in results.

### Within-early-childhood sub-analysis: 0–2 vs. 3–5

**This is a secondary sub-analysis inside band 1 (0–5). It does not replace the primary bands.** All primary results use 0–5, 6–11 and 12–17. The sub-analysis asks whether caregiving demands, time use, sleep and well-being differ between mothers of children under 3 (infancy and toddlerhood) and mothers of children 3–5 (preschool).

| Subgroup | Ages | Rationale |
|---|---|---|
| 1a | **0–2** | Infancy and toddlerhood: potentially the most intensive caregiving demands, night waking and the period around return to work |
| 1b | **3–5** | Preschool: changing childcare arrangements and preschool entry |

**Defining the subgroups in each dataset** (details in `docs/dataset-inventory.md` Section 6.4):

| Dataset | Age definition | Supported? |
|---|---|---|
| NSCH | **Exact age of the sampled child** (`SC_AGE_YEARS`). Both subgroups are on form T1, so every T1 item is asked of both. | Yes, by sampled child. The youngest child cannot be identified, so a mother is classified by the sampled child even if she has a younger one. |
| ATUS | **Exact age of the mother's youngest own household child**, from roster age and relationship. | Yes in principle. Sample size must be checked before committing to estimates (likely requires pooling years). |
| ACS PUMS | Exact age (`AGEP`) of linkable own children | Possible for linkable mothers only. Not a priority for this sub-analysis. |

**Rules for the sub-analysis:**
- Compare 0–2 with 3–5 **only on measures asked identically of both subgroups**. NSCH T1 items, including `HOURSLEEP05`, meet this. NSCH child sleep for 0–5 must **not** be compared with the weeknight sleep item used for ages 6–17.
- `HOURSLEEP05` has a top category of "12 or more hours" that includes naps. Infant and toddler sleep is often in this range, so the 0–2 group may cluster at the top category (a ceiling effect). Differences there are reported as differences in category distribution, not as estimated hours.
- ATUS secondary childcare (children under 13) covers both subgroups fully. ATUS primary-childcare activities do not identify which child received care, so a mother of both a 1-year-old and a 4-year-old is classified by her **youngest** child, and her childcare time cannot be split between the children.
- Sample sizes are checked first. Estimates that fail each source's reliability rules are suppressed or flagged, and the sub-analysis is dropped for any measure where it cannot be estimated reliably. It is never reported as covering more than the data support.

### Population

- **Primary:** Female biological or adoptive mothers whose child (or youngest child, where the dataset allows) is in **band 1 (0–5)**.
- **Secondary comparison groups:**
  - Mothers whose child (or youngest child) is in band 2 (6–11) or band 3 (12–17).
  - Mothers who are not working (unemployed or out of the labor force), compared with working mothers.

### Defining "mother"

Each dataset identifies mothers differently, and the definitions are **not equivalent**. Details and verified codes are in the dataset inventory.

| Dataset | How a mother is identified | Can biological/adoptive mothers be separated from other female caregivers? |
|---|---|---|
| NSCH | Caregiver sex combined with relationship to the sampled child (`A1_SEX`, `A1_RELATION` and Adult 2 equivalents) `[VERIFY]` | Expected to be possible if a biological/adoptive parent code exists separately from step-, grand-, foster and other caregivers `[VERIFY]` |
| ATUS | Respondent sex plus the presence of own household children `[TO IDENTIFY]` | Uncertain. "Own child" may include stepchildren. `[TO IDENTIFY]` |
| ACS PUMS | Female persons linked to children through relationship-to-householder and family/subfamily variables `[VERIFY]` | Partly. Relationship codes may separate biological, adopted and stepchildren only relative to the householder. Mothers who are not the householder or spouse/partner may be hard to link to specific children. `[VERIFY]` |
| BEA RPP | Not applicable (area-level price data, no respondents) | n/a |

Female caregivers who are not biological or adoptive mothers are **excluded from the primary analysis**. Where the data allow, they are analyzed separately as a sensitivity check. If a dataset cannot separate them, this is reported as a limitation.

## 2. Research objectives

1. **Describe** maternal mental and emotional health, parenting aggravation and family context by employment status and child age band (NSCH).
2. **Estimate associations** between maternal well-being and employment circumstances, economic pressure, housing tenure, household size, emotional support and family resilience (NSCH).
3. **Describe time allocation** across paid work, childcare, household labor, sleep and personal activities for working and nonworking mothers by child age band (ATUS).
4. **Describe sleep**: maternal sleep duration (and quality or interruptions where measured), child sleep duration and bedtime routines, and how they relate to employment and well-being (ATUS, NSCH).
5. **Describe mothers' economic and housing circumstances** (earnings, occupation, household income, housing tenure and cost burden) by employment status and child age band (ACS PUMS).
6. **Place these findings in geographic context** using regional price levels (BEA RPP) and area-level ACS indicators, without presenting area-level associations as individual-level findings.
7. **Triangulate** findings across sources and document where they agree, diverge or cannot be compared.
8. **Produce** reproducible, documented outputs: an analysis pipeline, accessible interactive D3.js visualizations and a written report that states its limitations openly.

## 3. Hypotheses and research questions

All hypotheses and research questions are **associational**. "Associated with," "varies by" or "relates to" does not mean "caused by."

### 3.1 Hypotheses

#### H1 — Employment circumstances and mental health

Working mothers' reported mental and emotional health varies by employment circumstances.

- Data: NSCH. Outcome: caregiver mental/emotional health rating. Exposure: caregiver employment `[VERIFY]` at whatever level of detail the variable records.
- Caveat: Employment status is **not** a measure of job quality, flexibility or work-life balance.

#### H2 — Aggravation, economic pressure and time demands

Parenting aggravation is associated with economic pressure and time demands.

- Data: NSCH for aggravation and economic pressure. ATUS for time demands, analyzed **independently**. Because NSCH has no diary data and ATUS has no aggravation measure, the time-demand part of H2 is tested only through group-level triangulation.

#### H3 — Emotional support

Greater emotional support is associated with better reported maternal well-being.

- Data: NSCH emotional-support items `[TO IDENTIFY]`. Family resilience is analyzed as a **separate** family-level construct.

#### H4 — Time allocation

Working mothers' allocation of time between paid work, childcare and household labor differs by family structure and socioeconomic circumstances.

- Data: ATUS

#### H5 — Child age band

Mothers' employment, time use and well-being patterns differ across child age bands (0–5, 6–11, 12–17), with the largest differences expected between band 1 (0–5) and the older bands.

- ATUS: youngest household child. ACS PUMS: own children. NSCH: sampled child, which may not be the youngest. Each source's definition is stated alongside its results.

#### H6 — Sleep

Shorter maternal sleep is associated with employment circumstances (for example full-time work) and with poorer maternal well-being, especially among mothers whose youngest child is 0–5.

- Data: ATUS for maternal sleep time and its relationship to employment, plus Well-Being Module measures if available `[VERIFY]`. NSCH for child sleep and its association with maternal well-being, **only if** NSCH measures maternal sleep or child sleep for the relevant ages `[TO IDENTIFY]`. The parts of H6 that no single dataset can test are triangulated, not merged.

### 3.2 Economic and housing research questions

- **E1.** How do maternal earnings and occupations vary by employment status and age of youngest child? *(ACS PUMS)*
- **E2.** How does housing cost burden differ between working and nonworking mothers? *(ACS PUMS)*
- **E3.** How do renters and homeowners compare in reported maternal well-being, accounting for income and household size? *(NSCH, **only if** NSCH measures housing tenure `[TO IDENTIFY]`. ACS PUMS can describe tenure and cost burden but has no well-being measures.)*
- **E4.** How do regional price levels relate to maternal earnings and housing costs? *(ACS + BEA RPP, at the area level, or person level with an area-level price index attached)*
- **E5.** Are mothers in high-cost regions more likely to experience financial pressure? *(ACS PUMS cost burden by RPP level of the area. NSCH material hardship by state RPP, if state is available.)*
- **E6.** How do household size and number of children relate to economic pressure and maternal well-being? *(NSCH for well-being; ACS PUMS for economic pressure)*

### 3.3 Sleep research questions

- **S1.** How long do mothers sleep on the diary day, and how does that vary by employment status, work hours and child age band? *(ATUS)*
- **S2.** Where measured, how do sleep quality, sleeplessness or night interruptions vary across these groups? *(ATUS sleeplessness activity code and Well-Being Module items if available `[VERIFY]`; any NSCH caregiver sleep item `[TO IDENTIFY]`.)*
- **S3.** How do child sleep duration and bedtime routines vary by child age band and maternal employment? *(NSCH child sleep items, with age eligibility `[VERIFY]`)*
- **S4.** How are maternal sleep (ATUS) and child sleep (NSCH) associated with maternal psychological well-being in each dataset, and are the patterns consistent across datasets? *(Within each dataset, then triangulated)*

Each sleep dimension is investigated separately. **No dataset is assumed to measure all of them.** Availability and age eligibility must be confirmed in the dataset inventory before analysis.

### 3.4 Within-early-childhood sub-analysis research questions (0–2 vs. 3–5)

These are **secondary** questions within band 0–5 (see Section 1). They are descriptive and associational.

- **U1.** Do maternal mental/emotional health, parenting aggravation and emotional support differ between mothers of a sampled child aged 0–2 and those of a sampled child aged 3–5? *(NSCH)*
- **U2.** Do child sleep (`HOURSLEEP05`, `BEDTIME`), non-parental childcare hours and job disruption due to childcare problems differ between the two subgroups? *(NSCH, T1 items only. Childcare hours only in years the item exists.)*
- **U3.** Do mothers whose youngest own child is 0–2 differ from those whose youngest is 3–5 in diary-day sleep, sleeplessness, paid work, primary and secondary childcare, and household activities, by employment status? *(ATUS, pooled years, subject to sample size)*
- **U4.** Do employment status and usual hours differ between the two subgroups? *(ATUS. NSCH `A1_EMPLOYED_R` for 2023+, which has no hours.)*

## 4. Dataset overview

Full details, verified variable names, codes and documentation links are in **`docs/dataset-inventory.md`**. This section summarizes each dataset's role.

| Dataset | Producer | Level | Role in the project |
|---|---|---|---|
| **NSCH**: National Survey of Children's Health | HRSA MCHB / U.S. Census Bureau | Individual (sampled child and household caregivers) | Maternal mental/emotional health, parenting aggravation, support, family resilience, child sleep, caregiver employment, household financial context |
| **ATUS**: American Time Use Survey | BLS / U.S. Census Bureau | Individual respondent and diary-day activities | Time in paid work, childcare and household labor; maternal sleep time; Well-Being Module (selected years) |
| **ACS**: American Community Survey (PUMS and published tables) | U.S. Census Bureau | Individual and household (PUMS), or area (tables) | Earnings, income, occupation, employment, household composition, housing tenure and costs, commute |
| **BEA RPP**: Regional Price Parities | U.S. Bureau of Economic Analysis | Area (states, metropolitan areas) | Regional price levels, used as geographic economic context |

### 4.1 NSCH: household financial and family context

In addition to the well-being and parenting variables from v0.2, NSCH variables need to be confirmed for:

| Construct | Notes | Status |
|---|---|---|
| Household income and federal poverty level | Income-to-poverty measure, possibly multiply imputed | `[VERIFY]` |
| Housing tenure | Whether NSCH measures own/rent at all is unknown | `[TO IDENTIFY]` |
| Number of children in household | | `[VERIFY]` |
| Family structure | | `[VERIFY]` |
| Caregiver employment | `A1_EMPLOYED_R` or similar, plus Adult 2 equivalent | `[VERIFY]` |
| Caregiver mental/emotional health | `A1_MENTHEALTH`, `A2_MENTHEALTH` | `[VERIFY]` |

**Individual caregiver earnings and household income are different measures.** NSCH is expected to measure household income relative to poverty, not the mother's own earnings `[VERIFY]`. NSCH household income will never be interpreted as maternal earnings.

### 4.2 ATUS

As specified in v0.2: respondent, activity, activity summary, roster, who, ATUS-CPS and replicate-weight files linked by identifiers, plus labor force status, hours, presence and age of children, primary and secondary childcare, household activities, sleep and diary-day information. All `[VERIFY]` in the inventory.

### 4.3 ACS: economic and household analysis

Availability to be confirmed in ACS PUMS (person and housing records) and published tables:

| Domain | Constructs |
|---|---|
| Earnings and income | Individual earnings (wages, self-employment); personal, family and household income; income-to-poverty ratio |
| Occupation and industry | Occupation and industry codes |
| Employment | Employment and labor-force status; usual hours; weeks worked; full-time/part-time (possibly derived); commute time |
| Household composition | Household size; number of own and related children; family type; single-parent households; subfamilies |
| Housing tenure | Owner with mortgage, owner without mortgage, renter, occupied without payment of rent |
| Housing costs | Monthly gross rent; selected monthly owner costs; housing costs as a percentage of household income; property value; mortgage status |

**PUMS suitability question.** Can PUMS support individual-level analyses of mothers, their employment, earnings and household circumstances? The inventory must document the relevant person and housing variables, how housing records link to person records, and **the limits on identifying mothers and linking children to their parents** (for example, if relationships are recorded only relative to the householder).

### 4.4 BEA Regional Price Parities (new)

| Field | Description |
|---|---|
| **What it measures** | Differences in price levels across states and metropolitan areas for a given year, expressed relative to the national level `[VERIFY]` |
| **Components to investigate** | All items; housing rents; utilities; other available categories (goods, other services) `[VERIFY]` |
| **Geography** | States and metropolitan areas; possibly nonmetropolitan portions of states `[VERIFY]` |
| **Years** | Annual series. Year range and the latest release are `[VERIFY]`. |
| **Access** | BEA interactive tables, downloads and the BEA API (registration key) `[VERIFY]` dataset and table names |
| **Use in this project** | Geographic context for ACS earnings and housing costs (E4, E5). Comparing nominal and price-adjusted earnings across areas. |

**How RPP is used with ACS.** Nominal ACS earnings and housing costs can be shown next to the RPP for the area where the mother lives, or adjusted by it, to compare purchasing power across states or metro areas. For example, the same nominal earnings correspond to different price-adjusted amounts in high- and low-price areas. The housing-rent RPP shows whether high housing cost burden in an area coincides with high rent levels or with low earnings.

**What RPP is not.** RPP is **not** a complete household affordability measure, a living-wage measure, or a cost-of-living index for a particular family. It reflects area price levels for a broad consumption basket. It does not account for a specific family's size or composition, childcare costs (unless a component is confirmed `[VERIFY]`), tax differences, public benefits, or whether housing is owned or rented. It describes the area, not the mother.

## 5. Constructs: direct measures vs. proxies

| Concept | Direct measure (preferred) | Proxy / indirect measure | Notes |
|---|---|---|---|
| Maternal mental health | NSCH caregiver mental/emotional health rating, when self-reported | NSCH rating reported by another adult | Single global item, not diagnostic |
| Parenting stress | NSCH aggravation items | none | Respondent may not be the mother `[VERIFY]` |
| Momentary affect | ATUS Well-Being Module, if available `[VERIFY]` | none | Activity-level; limited years |
| Maternal sleep duration | ATUS diary sleep time | none | One diary day, not habitual sleep |
| Maternal sleep quality / interruptions | ATUS sleeplessness code, Well-Being Module items `[VERIFY]` | none | Availability uncertain |
| Child sleep | NSCH child sleep and bedtime items `[VERIFY]` | none | Parent-reported; age-specific |
| Employment | NSCH, ATUS and ACS employment / labor force status | none | Employment ≠ job quality |
| Individual earnings | ACS PUMS earnings; ATUS weekly earnings `[VERIFY]` | none | Not household income |
| Household / family income | ACS PUMS; NSCH income-to-poverty | none | Not maternal earnings |
| Housing cost burden | ACS PUMS gross rent / owner costs as % of income | none | Use official ACS definitions |
| Purchasing power | ACS earnings adjusted by BEA RPP | Nominal income | RPP is area-level |
| Economic pressure (experienced) | NSCH material-hardship item `[TO IDENTIFY]` | Income-to-poverty, cost burden, RPP | Resources and prices ≠ experienced strain |
| Emotional support | NSCH support items `[TO IDENTIFY]` | none | Distinct from family resilience |
| Family structure | NSCH, ATUS roster, ACS family type | none | Definitions differ across sources |

## 6. Integration strategy

**Respondents from different surveys are never merged at the individual level.** NSCH, ATUS and ACS share no respondent identifiers. No statistical matching or cross-survey imputation will be used to create synthetic linked records.

### 6.1 Independent individual-level analyses

- **NSCH:** well-being, aggravation, support, child sleep and household financial context (H1–H3, H5, H6 partly, E3, E6).
- **ATUS:** time use and maternal sleep (H2 time part, H4, H5, H6, S1–S2).
- **ACS PUMS:** mothers' earnings, occupation, employment, household composition, housing tenure and cost burden (E1, E2, E5, E6, H5).

### 6.2 Area-level context (attaching geography, not people)

- **BEA RPP** and **published ACS indicators** are area-level. They can be attached to individual records **by geography** (for example state, or metro area where it can be identified) as contextual variables. This is not individual linkage.
- **Geographic alignment:** BEA metro areas follow specific delineations, while PUMS identifies Public Use Microdata Areas (PUMAs), which do not map cleanly onto metro areas. NSCH public files are expected to identify state only `[VERIFY]`. Each analysis states which geography it uses and how areas were matched.
- **Year alignment:** RPP year, ACS vintage (1-year vs. 5-year) and NSCH/ATUS survey years will be aligned and documented. Where they cannot be aligned exactly, the gap is stated.
- Contextual models need multilevel or cluster-robust methods.

### 6.3 Triangulation

- Results from each source are compared on **direction and pattern**, not pooled.
- A triangulation matrix records, for each hypothesis and research question, which sources can test it and what each found. Disagreements are reported, not reconciled away.

## 7. Methodological and statistical considerations

### 7.1 Employment and labor force measurement

- **Employment vs. labor-force participation:** employed; unemployed (in the labor force but not working); not in the labor force. "Nonworking" is always split into unemployed vs. not in the labor force where the data allow.
- **Full-time / part-time / unemployed / out of labor force** are distinguished where each dataset permits. The full-time threshold and reference period are documented for each source.
- **Employment ≠ job quality, flexibility or work-life balance.** None of these will be inferred from employment status.

### 7.2 Income, earnings and purchasing power

- **Three different concepts:** individual **earnings** (the mother's own wages and self-employment income), **family income** (the income of related family members) and **household income** (the income of all household members). These are never used interchangeably, and each output names the concept it uses.
- **Nominal vs. real:** Income across years must be adjusted for inflation using the official adjustment factors where provided (for example ACS adjustment factors `[VERIFY]`). Income across areas may be adjusted for regional price levels using RPP. "Nominal," "inflation-adjusted" and "RPP-adjusted" are always labeled.
- **Income reference periods** differ across datasets (for example past 12 months vs. weekly earnings) and are documented.

### 7.3 Housing

- **Housing cost burden** is calculated using **official ACS definitions** of gross rent, selected monthly owner costs and housing costs as a percentage of household income, including the documented handling of zero or negative income and of units with no cash rent `[VERIFY]`. Burden thresholds (for example 30% and 50%) are stated explicitly.
- **Avoid simplistic owner vs. renter comparisons.** Tenure is strongly associated with income, age, family structure, household size, geography and length of residence. Comparisons account for these factors, distinguish owners with a mortgage from owners without one, and treat "occupied without payment of rent" as a separate group. Differences by tenure are described as associations, not effects of owning or renting.

### 7.4 Household size and number of children

- Household size and number of children are analyzed explicitly (E6), and income comparisons account for them. For example, poverty thresholds already adjust for family size, but raw household income does not.

### 7.5 Geography and levels of inference

- Area-level associations (for example between RPP and average cost burden) are **geographic findings** and are never presented as individual-level relationships (ecological fallacy).
- Small-area estimates come with margins of error. Metro identification from PUMS is approximate.

### 7.6 Population definition and age bands

- Biological/adoptive mothers are distinguished from other female caregivers wherever the data allow.
- Age bands are applied as defined in Section 1. Every output states whether the band refers to the sampled child (NSCH), the youngest household child (ATUS) or own children (ACS), and flags any band a measure covers only partly.
- The 0–2 vs. 3–5 sub-analysis is labeled **"within-early-childhood sub-analysis"** in every output and kept separate from primary-band results. It uses only measures asked identically of both subgroups.

### 7.7 Sleep measurement

- ATUS sleep is **time recorded in one diary day**, not habitual sleep or sleep quality. Sleep quality or interruptions are reported only where a dataset actually measures them.
- Child sleep is parent-reported, and item wording and eligibility may vary by child age `[VERIFY]`.
- Maternal sleep and child sleep come from **different surveys** and are never linked at the individual level.

### 7.8 General statistical issues

| Issue | Plan |
|---|---|
| **Survey weights** | Use the official weight for each dataset, year, file and record type (person vs. housing in ACS PUMS). Unweighted estimates are diagnostic only. |
| **Complex sampling / variance** | NSCH: design-based variance per documentation. ATUS and ACS PUMS: replicate weights per documentation. Domain estimation for subgroups. |
| **ATUS diary day** | Population patterns, not individual typical days. Weekday/weekend weighting per BLS. |
| **Pooling years** | Likely needed for ATUS and NSCH subgroups. Follow official guidance and check item and code changes across years. |
| **Variable availability** | A year × variable availability matrix is built for each source before pooling. |
| **Period effects** | Pandemic-period sensitivity analyses. 2020 data disruptions `[VERIFY]` for each source. |
| **Missing data** | Report item nonresponse. Distinguish legitimate skips. Use official imputations correctly. Use multiple imputation as a sensitivity analysis where needed. |
| **Confounding / selection** | Adjust for measured confounders. Selection into employment and housing tenure is acknowledged. No "effect of working" or "effect of owning" language. |
| **Correlation vs. causation** | All data are cross-sectional. Reverse causation is possible (for example, poor health leading to less employment). |
| **Multiple comparisons** | H1–H6, E1–E6, S1–S4 and the sub-analysis questions U1–U4 are pre-specified. Other analyses are labeled exploratory. |
| **Small cells** | Low-count or high relative standard error estimates are suppressed or flagged according to each source's guidance. |

## 8. Data access limitations

- **NSCH:** Downloadable public-use files. **No conventional public microdata API.** State-level geography only `[VERIFY]`.
- **ATUS:** Downloadable microdata files from BLS. **The BLS Public Data API does not serve ATUS microdata** `[VERIFY]`. IPUMS ATUS is third-party and uses different variable names.
- **ACS:** Official Census Data API for tables (and possibly PUMS `[VERIFY]`). PUMS file downloads. Sampling error on every estimate. Table IDs and variable names change between releases.
- **BEA RPP:** Interactive tables, downloads and an API that requires a free key `[VERIFY]`. Area-level only.
- **Cross-source:** Different respondents, years, reference periods, geographies and definitions of "mother," "employment," "income" and "family." Compatibility has to be shown for each specific comparison, not assumed.
- **Terms of use:** No attempt will be made to re-identify respondents. Restricted-use data will not be used without the required approvals.

## 9. Visualizations

**Preferred framework: D3.js.** Static exports for the written report come from the same specifications. The visualizations stay centered on mothers' experience. Economic charts exist to explain well-being, not as a general economic dashboard.

### 9.1 Well-being, time and sleep

1. **Interactive 24-hour time-use comparison (ATUS):** The diary day of working vs. nonworking mothers by child age band, with toggles for full-time/part-time, family structure and weekday/weekend.
2. **Daily minutes by activity (ATUS):** Paid work, primary and secondary childcare, household activities, sleep and personal time, by group, with confidence intervals.
3. **Maternal sleep by employment and child age band (ATUS):** Distribution of diary-day sleep, with band 0–5 highlighted. An optional view splits 0–5 into 0–2 and 3–5, labeled as the within-early-childhood sub-analysis and shown only where sample sizes allow.
4. **Child sleep and routines by age band (NSCH):** Shown only for the ages each item covers.
5. **Maternal well-being comparisons (NSCH):** Mental-health ratings and aggravation by employment status and child age band.
6. **Well-being by economic pressure, support and housing tenure (NSCH):** Point estimates with intervals (housing tenure only if NSCH measures it).
7. **Adjusted associations (NSCH):** Coefficient / odds-ratio plot.

### 9.2 Economic and housing context

8. **Interactive U.S. map of regional price levels (BEA RPP):** States, with a metro-area layer, switchable between all-items, housing-rent and utilities RPP.
9. **Metro comparisons of maternal earnings and housing costs (ACS + RPP):** Nominal and RPP-adjusted earnings of mothers next to median housing costs, with margins of error.
10. **Housing cost burden by tenure and family structure (ACS PUMS):** Owners with mortgage, owners without mortgage and renters, by single- vs. two-parent households and employment status.
11. **Earnings and occupation by child age band (ACS PUMS):** Earnings distributions (for example quantile or ridgeline views) and leading occupation groups for mothers, by youngest-child band and employment status.
12. **Income vs. regional price level (ACS + RPP):** Area-level scatterplot, labeled clearly as a geographic association.
13. **Household size, employment and housing affordability explorer (ACS PUMS):** Linked views of household size and number of children, maternal employment and cost burden.

### 9.3 Synthesis

14. **Triangulation matrix:** Each hypothesis or research question × each source, marked supported, unsupported, mixed or not testable.

### 9.4 Accessibility and uncertainty standards

- Every chart has a text summary and an accessible data-table alternative.
- Color palettes are colorblind-safe, and categories are never shown by color alone.
- Interactive controls work with a keyboard and include ARIA labels.
- Confidence intervals or margins of error are shown by default.
- Annotations explain what each measure is and is not. Examples: "one diary day per mother," "employment status, not job quality," "regional price level, not a living wage," "area-level association."
- Suppressed or unreliable estimates are visibly marked.
- Every chart names its data source, years, geography, population definition and age-band definition.

## 10. Final research deliverables

1. **Research plan** (this document), versioned as it is revised.
2. **Dataset inventory** (`docs/dataset-inventory.md`): verified sources, variables, codes and limitations.
3. **Variable verification log** and **year × variable availability matrix** for each dataset.
4. **ATUS file-linkage documentation** and **ACS PUMS person–housing linkage documentation.**
5. **Geographic crosswalk documentation**, covering how states, metro areas and PUMAs are aligned across ACS and BEA RPP, with the delineation vintages used.
6. **Data acquisition notes:** Source, release, download date and checksum for each file.
7. **Reproducible analysis pipeline** in `src/` and `notebooks/`. Raw and processed data stay out of version control.
8. **Data dictionary** for derived variables, including the definitions of "mother," employment status, age band, earnings/income concept and housing cost burden in each source.
9. **Interactive D3.js visualizations** and static exports in `reports/figures/`.
10. **Written report** covering methods, results by hypothesis and research question, triangulation and limitations. All findings are stated as associations.
11. **Short public-facing summary** in plain language, with the same caveats.

## 11. Immediate next steps

1. Complete `docs/dataset-inventory.md`: verify sources, years, access, variables, codes and age eligibility for NSCH, ATUS, ACS and BEA RPP.
2. Resolve the population-defining variables first: maternal identification, child age and the age-band coverage of key items.
3. Confirm whether NSCH measures housing tenure, caregiver sleep and child sleep, and for which ages. E3 and parts of H6 depend on this.
4. Confirm the PUMS mother–child linkage approach and the PUMA–metro alignment for RPP comparisons.
5. Estimate unweighted sample sizes of mothers by age band and employment status in each source to confirm the planned comparisons are feasible, especially band 0–5 in ATUS. Include the 0–2 and 3–5 subgroups in NSCH and ATUS to decide which sub-analysis measures (U1–U4) can be estimated reliably.
6. Revise this plan (v0.5) to match the confirmed variables, and mark any hypotheses or research questions that cannot be tested.

---

## Sources (official entry points)

- NSCH, U.S. Census Bureau: https://www.census.gov/programs-surveys/nsch.html
- NSCH, HRSA Maternal and Child Health Bureau: https://mchb.hrsa.gov/data-research/national-survey-childrens-health
- Data Resource Center for Child and Adolescent Health: https://www.childhealthdata.org
- American Time Use Survey, U.S. Bureau of Labor Statistics: https://www.bls.gov/tus/
- IPUMS ATUS (third-party harmonized data, not an official source): https://www.atusdata.org
- American Community Survey: https://www.census.gov/programs-surveys/acs
- ACS Public Use Microdata Sample: https://www.census.gov/programs-surveys/acs/microdata.html
- data.census.gov: https://data.census.gov
- Census Bureau developer resources (API): https://www.census.gov/data/developers.html
- BEA Regional Price Parities: https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area
- BEA API: https://apps.bea.gov/api/
