# ATUS Feasibility Check

**Status:** v0.1 (2026-11-03). Data: ATUS 2003–2025 multi-year Respondent, Roster, Activity Summary and ATUS-CPS files (U.S. Bureau of Labor Statistics, 2026a). Analysis window: **2022–2025, pooled**.
**Code:** `src/atus.py` (one row per respondent) and `src/atus_feasibility.py` (tables in `reports/tables/atus_feasibility/`).

These numbers only say **which comparisons the data can support**. None of them is a finding about mothers' time use.

## Summary

| Question | Answer |
|---|---|
| Can mothers be identified? | **Yes.** Female respondent with at least one own household child under 18 (roster `TERRP = 22`, `TEAGE` < 18). This agrees 100% with the respondent-file flag `TROHHCHILD = 1`. All mothers are kept, including step-mothers. |
| Which years? | **2022–2025, pooled: 3,847 mothers.** 2021 is left out as too close to the COVID-19 pandemic, and 2020 because of its collection gap and separate weight. |
| Are the groups large enough? | **Yes.** Every youngest-child band × full-time / part-time / not employed cell has at least 129 mothers, including the 0–2 and 3–5 split. "Unemployed" on its own is too small (20–49 per band). |
| Are the estimates precise enough? | **Yes, with a caveat.** Mean sleep, childcare and paid-work minutes have relative standard errors (RSE) of at most 15.5% (paid work for non-employed mothers aside, where the mean is near zero). These SEs are **approximate** (Section 4). |
| Fathers? | Full-time fathers are a large group (632–1,289 per band). Part-time (46–60 per band), unemployed (18–32) and not-in-labor-force fathers (56–59) are small, and some of their estimates fail the provisional rules. |
| Is missing data a problem? | **No.** Labor force status, full/part-time status and respondent age have no missing values among mothers. 4.6% of employed mothers report usual hours as "hours vary." |

## 1. Mother definition (Step 1)

**Definition used:** respondent (roster line 1) with `TESEX = 2` and at least one roster line with `TERRP = 22` ("Own household child") and `TEAGE` < 18. `TERRP = 22` also includes adult children, so the age filter is needed. The ATUS counts biological, step and adopted children as own children; foster children (`TERRP = 27`) are not (see `docs/dataset-inventory.md` Section 3.5).

**Fathers** use the same definition with `TESEX = 1`.

Mothers per year are in `step1_mother_flow.csv`: 1,129 (2022), 1,019 (2023), 960 (2024) and 739 (2025).

**Step-children (description only).** All mothers are kept, as BLS defines own children. For context, the ATUS-CPS file shows how the CPS classified each mother's children. It links through `PEPAR1`/`PEPAR2` and `PEPAR1TYP`/`PEPAR2TYP` from 2020 (`PELNMOM`/`PEMOMTYP` before), matching the child's parent line number to the respondent's CPS line number (`PULINENO`), then the roster child by `TUCASEID` and `TULINENO`.

| 2022–2025 mothers | n | % |
|---|---|---|
| At least one biological/adopted child | 3,630 | 94.4 |
| Only step-children | 58 | 1.5 |
| No CPS parent type for any child | 159 | 4.1 |

119 mothers (3.1%) have at least one step-child. "No CPS parent type" usually means the child was not in the household at the CPS interview 2–5 months before the diary day (for example a newborn), or the CPS did not link the child to the respondent.

## 2. Diary coverage and pooling (Step 2)

| Year | Gap in the data (`step2_diary_coverage.csv`) | Documented reason |
|---|---|---|
| 2020 (excluded) | No April diaries; March has about 60% of a normal month | Diary days March 18 to May 9, 2020 were not collected, and 2020 data are "not representative of the full year." 2020 has its own weight, `TU20FWGT`. |
| 2025 | No October diaries; November has fewer | "All ATUS operations were suspended from October 1 through November 12" (2025 federal shutdown). |

(Sources as cited in `docs/dataset-inventory.md` Sections 3.2 and 3.4.)

**2025 is still included.** Its missing six weeks lower its sample, and the weights adjust for the months collected `[VERIFY how BLS weighted 2025 for the gap]`.

**Weights in the data:** `TUFNWGTP` is positive for every respondent in 2003–2019 and 2021–2025, and missing (negative) for all of 2020. The loader uses `TUFNWGTP`, which covers the whole 2022–2025 window.

**Weekday/weekend balance:** 49.9% of mothers' diaries fall on a weekend, matching the design's 50/50 split (`step2_weekend_share_mothers.csv`). The weights correct for it.

**Later pass:** pre-pandemic, pandemic and post-pandemic periods will be compared separately. They are not part of this check.

## 3. Sample sizes and employment shares (Step 3)

**Child age** is the youngest own household child's age (`YOUNGEST_OWN_AGE`), the ATUS definition in the research plan.

**Employment** comes from `TELFS` and `TRDPFTPT`:
- Employed (`TELFS` 1 or 2): full-time (`TRDPFTPT = 1`) or part-time (`TRDPFTPT = 2`). Every employed mother has one of these, so the "hours status unknown" group in the tables is always 0. How BLS sets the full-time threshold is not stated in the data dictionary `[VERIFY in the User's Guide]`.
- Unemployed (`TELFS` 3 or 4).
- Not in labor force (`TELFS = 5`).

**Mothers, unweighted n, 2022–2025** (`step3_sizes_mothers_primary.csv`, `…_secondary.csv`):

| Youngest child | Full-time | Part-time | Unemployed | Not in labor force | Total |
|---|---|---|---|---|---|
| 0–2 | 435 | 178 | 29 | 276 | 918 |
| 3–5 | 421 | 129 | 20 | 191 | 761 |
| **0–5** | 856 | 307 | 49 | 467 | 1,679 |
| **6–11** | 785 | 216 | 30 | 235 | 1,266 |
| **12–17** | 560 | 153 | 25 | 164 | 902 |
| **All mothers** | | | | | **3,847** |

**Weighted employment shares** (`step3_employment_shares_mothers_primary.csv`):

| Youngest child | Full-time | Part-time | Unemployed | Not in labor force |
|---|---|---|---|---|
| 0–5 | 48.9% | 18.7% | 3.2% | 29.2% |
| 6–11 | 59.2% | 16.4% | 2.9% | 21.5% |
| 12–17 | 61.0% | 17.9% | 3.5% | 17.6% |

These shares are weighted, so they describe mothers, unlike NSCH, whose weights describe children.

**Fathers, unweighted n, 2022–2025** (`step3_sizes_fathers_primary.csv`):

| Youngest child | Full-time | Part-time | Unemployed | Not in labor force | Total |
|---|---|---|---|---|---|
| 0–5 | 1,289 | 60 | 32 | 59 | 1,440 |
| 6–11 | 876 | 48 | 18 | 56 | 998 |
| 12–17 | 632 | 46 | 18 | 57 | 753 |

## 4. Precision of mean minutes (Step 4)

**Outcomes** (Activity Summary file, minutes on the diary day):
- Sleeping, activity 010101.
- Caring for and helping household children, activities 0301xx–0303xx (physical care, education-related and health-related care).
- Working at a job, activity 0501xx.

Sleeplessness (010102) is also kept in the processed file, but not tested here.

**Groups:** youngest-child band × collapsed employment (full-time, part-time, not employed).

**Standard errors are approximate.** They treat each respondent as an independent observation (ATUS interviews one person per household). This ignores the CPS strata and clusters, so the true SEs are likely somewhat larger. Final estimates will use the 160 replicate weights, Var = (4/160) Σ(Ŷᵢ − Ŷ₀)², as the User's Guide specifies (`docs/dataset-inventory.md` Section 3.4). The replicate weight file has not been downloaded yet.

**Provisional reliability rules:** n ≥ 30 and RSE (SE ÷ estimate) ≤ 30%. BLS applies its own publication criteria (User's Guide Appendix N), which have not been checked yet `[VERIFY]`.

**Mothers** (`step4_minutes_precision_mothers_*.csv`): **no cell fails**, in either the primary or the secondary bands.

| Outcome | RSE range |
|---|---|
| Sleep | 0.9–4.6% |
| Childcare | 4.1–15.4% (largest: part-time mothers of teenagers) |
| Paid work, employed mothers | 3.1–15.5% (largest: part-time mothers of 3–5 year-olds) |
| Paid work, non-employed mothers | Mean near zero, so the RSE is large, as expected; not a meaningful comparison |

**Fathers:** these cells fail:
- Childcare for part-time fathers of teenagers (RSE 45.8%) and non-employed fathers of teenagers (31.5%).
- Part-time fathers whose youngest child is 3–5: n = 23, below 30.

## 5. Missing data (Step 5)

**Among mothers, 2022–2025** (`step5_missingness.csv`):
- `TELFS`, `TRDPFTPT` (employed) and respondent age: **0 missing**.
- `TEHRUSLT` (usual weekly hours, employed): no blank/refused codes, but **133 (4.6%) report −4 "hours vary."** Analyses of hours need to report them separately or leave them out.

**Roster** (`step5_roster_codes.csv`, all years): 73 of 702,409 lines have a negative relationship code and 13 a negative age. None of them is an own household child with a missing age.

**Diary minutes** are never missing: the Activity Summary file has a value (0 or more) for every respondent and activity.

## 6. Decisions

1. **Mothers:** all female respondents with own household children under 18 (`TERRP = 22`, `TEAGE` < 18), including step-mothers, as BLS defines own children.
2. **Window:** 2022–2025, pooled. 2020 and 2021 excluded.
3. **Child age:** youngest own household child. Primary bands 0–5 / 6–11 / 12–17 and secondary 0–2 / 3–5 / 6–11 / 12–17 are both feasible.
4. **Weights:** `TUFNWGTP`.
5. **Employment:** full-time, part-time, not employed (unemployed + not in labor force). Unemployed is not reported on its own.
6. **Variance:** replicate weights for every published estimate. **Download the replicate weight file** (292.6 MB) before the analysis.
7. **Fathers (H8):** compare full-time fathers with mothers. Part-time and non-employed fathers are not reported by band.
8. **Later pass:** pre-pandemic / pandemic / post-pandemic comparison.

## 7. Still to verify

- `[VERIFY]` BLS publication criteria (User's Guide Appendix N), to replace the provisional n ≥ 30 / RSE ≤ 30% rules.
- `[VERIFY]` Full-time threshold behind `TRDPFTPT`.
- `[VERIFY]` How the 2025 weights handle the October–November collection gap.
- `[VERIFY]` Variable names in the multi-year replicate weight file.

## References

U.S. Bureau of Labor Statistics. (2026a). *American Time Use Survey (ATUS) 2003–2025 multi-year microdata files* [Data set]. https://www.bls.gov/tus/data/datafiles-0325.htm

U.S. Bureau of Labor Statistics. (2026b). *American Time Use Survey user's guide: Understanding ATUS 2003 to 2025*. https://www.bls.gov/tus/atususersguide.pdf

U.S. Bureau of Labor Statistics. (n.d.). *Changes between 2003–2025 data files: American Time Use Survey (ATUS)*. https://www.bls.gov/tus/other-documentation/changes.pdf `[VERIFY date]`
