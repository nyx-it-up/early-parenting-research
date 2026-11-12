# Other U.S. Datasets for Postpartum Mental Health and Return to Work

**Status:** v0.1 (2026-11-11). Checked against official codebooks and questionnaires on 2026-11-11. Variable names come from those documents; `[VERIFY]` marks anything not confirmed.

**Why:** NSCH has no maternal postpartum depression or anxiety measure and no leave or return-to-work timing (`docs/nsch-h1-under2.md`). This document lists datasets that could test the under-2 hypothesis with better measures.

**Bottom line:** no public U.S. dataset combines a validated postpartum depression/anxiety scale, return-to-work timing and hours, and an exact child age under 2.

## Comparison

| Dataset (producer) | Mental health | Return to work, leave, hours | Mothers of under-2s identifiable? | Years | Access |
|---|---|---|---|---|---|
| **NHIS** (NCHS) | PHQ-8 (`PHQ81_A`–`PHQ88_A`, `PHQCAT_A`) and GAD-7 (`GAD71_A`–`GAD77_A`, `GADCAT_A`) in 2019, 2022, 2025. K6 (`K6SPD_A`) in 2021, 2024. `DEPFREQ_A`, `ANXFREQ_A` every year. | Weekly hours (`EMPWKHRS3_A`, 2021+). Absent from work last week (`EMPNOWRK_A`). No leave length or timing. | Partly: Sample Child file `SCPARENTSC_C` = 1 (sample adult is the child's parent) + `AGEP_C` + `SEX_A`. Only when the sampled child is under 2. | 2019–2025 | Public download |
| **MEPS-HC** (AHRQ) | PHQ-2 (`PHQ242`), K6 (`K6SUM42`) from the Self-Administered Questionnaire | Hours per week by round (`HOUR31`, `HOUR42`, `HOUR53`). No leave. | Yes: children carry the mother's person ID (`MOPID31X` etc.) and age (`AGE22X`, `AGELAST`). | 2019–2023 confirmed | Public download |
| **PRAMS** (CDC) | Phase 9 core: 4 postpartum items (down/depressed, little interest, nervous/anxious, can't stop worrying) on a never–always scale; depression/anxiety screening by a provider | Standard (site-optional) items: worked during pregnancy, returned to job, leave taken, weeks of leave, barriers to leave. No hours. | Yes by design (recent births; survey 2–4 months after delivery) | Phase 9: 2023+ | **Restricted**; CDC states "PRAMS ARF data requests are not currently being processed" (page dated 2024-08-22) |
| **CPS** basic monthly (Census/BLS) | None | Absent for maternity/paternity leave (`PEABSRSN` = 8; `PRABSREA`), paid for time off (`PEABSPDO`), usual hours (`PEHRUSL1`) | Yes: parent line numbers (`PEPAR1`, `PEPAR2`) + child `PRTAGE` | Monthly | Public download |
| **SIPP** (Census) | No validated scale found `[VERIFY]` | Weeks not working before birth (`TPREBIRTHINT`), child age at return to work (`TPSTBRTHINT`, `EPSTBRTH_TP`), types of leave (`EBIRTHRSN1`–`10`); first child only | Fertility history + roster `[VERIFY]` | 2019+ (2022+ not comparable with earlier) | Public download |
| **Household Pulse / HTOPS** (Census) | PHQ-2, GAD-2 (`ANXIOUS`, `WORRY`, `INTEREST`, `DOWN`) | Working status; reason not working includes child care | Weak: `KIDS_LT1Y` (household has a child under 1), relationship unknown | 2020–2026 | Public download |
| BRFSS, NHANES, NSFG, ACS | Limited (no postpartum timing or no mental health scale) | Limited | Mostly no | Annual | Public download |

## Recommendation

1. **NHIS 2019–2025 (best option):** public, validated PHQ-8/GAD-7, a documented parent–child link and weekly hours (to define full-time). Main limit: small samples. A rough estimate is 200–250 mothers of under-2s per PHQ/GAD year, or about 700 pooling 2019, 2022 and 2025 (estimate, not documented).
2. **MEPS 2019–2023 (replication):** PHQ-2 and K6 with a clean mother–child link; also small samples.
3. **PRAMS:** the only source with postpartum symptoms and leave measured on the same mother, but access is currently closed, leave items are in some states only, and there is no hours measure.
4. **CPS and SIPP:** describe leave and return-to-work patterns (for example, how many mothers of 0–1-year-olds are on maternity leave or work full-time). They cannot link these to mental health.

## Sources (APA 7)

Agency for Healthcare Research and Quality. (2021–2025). *MEPS HC-216, HC-224, HC-233, HC-243, HC-251: 2019–2023 full year consolidated data file documentation*. https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-243

Centers for Disease Control and Prevention. (n.d.). *PRAMS data access and research*. https://www.cdc.gov/prams/php/data-research/index.html

Centers for Disease Control and Prevention. (n.d.). *PRAMS Phase 9 core questionnaire*. https://www.cdc.gov/prams/pdf/questionnaire/Phase-9-Core-Questionaire-508.pdf

Centers for Disease Control and Prevention. (2025). *PRAMS Phase 9.2 topic reference guide*. https://www.cdc.gov/prams/pdf/questionnaire/Phase-9-Topic-Reference-508.pdf

National Center for Health Statistics. (2020–2026). *NHIS sample adult and sample child codebooks, 2019–2025*. https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHIS/2025/adult-codebook.pdf

U.S. Census Bureau. (2026). *CPS basic monthly data dictionary 2026*. https://www2.census.gov/programs-surveys/cps/datasets/2026/basic/2026_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt

U.S. Census Bureau. (n.d.). *2025 SIPP: Comparing 2025 SIPP parental leave data to previous years*. https://www.census.gov/programs-surveys/sipp/tech-documentation/user-notes/2025-usernotes/2025-comp-sipp-parent-leav-data-prev-yrs.html

U.S. Census Bureau. (2024, 2026). *Household Pulse Survey public use files and data dictionaries*. https://www.census.gov/programs-surveys/household-pulse-survey/data/datasets.html
