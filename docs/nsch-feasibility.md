# NSCH Feasibility Check: Mother Definition, Sample Sizes and Missing Data

**Status:** Results of research plan Section 11, step 5, for NSCH 2023–2025 (pooled; data: U.S. Census Bureau, 2025a, 2025b, 2026d). Decisions in Section 5 were agreed on 2026-11-01.
**Code:** `src/nsch_feasibility.py` (reads `data/processed/nsch_2023_2025.parquet`, written by `src/nsch.py`).
**Tables:** `reports/tables/nsch_feasibility/*.csv` (every number below comes from these files).
**Sources:** cited in APA 7th edition style; full reference list in Section 6.

> **These are feasibility results, not findings.** The shares below only test whether the planned comparisons can be estimated reliably. They describe associations in survey data and say nothing about cause.

---

## Summary

| Question | Answer |
|---|---|
| How many usable mothers? | **90,415** children whose responding adult is their biological or adoptive mother (59.6% of the 151,676 sampled children). |
| Are the primary comparisons (0–5 / 6–11 / 12–17 × employment) feasible? | **Yes**, for full-time, part-time, not employed (looking) and not employed (not looking). Every cell has n ≥ 1,300 pooled and passes the NSCH reliability rules. |
| Is the 0–2 vs. 3–5 split feasible? | **Yes**, for the same four employment groups (n ≥ 650 per cell). |
| Can we identify mothers with more than one young child? | **Partly.** We can identify "2+ children aged 0–5" and "a child aged 0–2 plus another child aged 0–5", but not "two children under 3" (Section 2.4). Both groups are large enough for mothers. |
| Is a father comparison feasible? | **Yes, for full-time vs. not employed.** Part-time fathers are too few for reliable outcome estimates in most groups (Section 2.5). |
| Which employment groups are too small? | **"Retired"** for mothers of children under 12. **"Working without pay"** is borderline. |
| Is missing data a problem? | **No.** Item nonresponse among mothers is at most 1.9% for every kept variable. |
| Main caveat | Requiring the mother to be the **respondent** drops 42,099 children whose mother appears only as Adult 2 (described by someone else). This is a selection, not random loss (Section 1.3). |

---

## 0. Key terms

### 0.1 Statistical terms

| Term | Plain-language meaning | Source |
|---|---|---|
| **Weight (`FWC`)** | Each sampled child stands in for many children in the population. `FWC` is how many. Weights correct for oversampling (for example, children aged 0–5 and children with special health care needs were deliberately sampled more often) and for nonresponse. | (U.S. Census Bureau, 2026c, pp. 10–11, 44; U.S. Census Bureau, 2026b, p. 8) |
| **Child-level weight** | `FWC` is the only weight in the topical file and is built for **children**. The Census Bureau says weighted estimates "do not generalize to the population of parents, mothers…" and "should be framed in terms of children". | (U.S. Census Bureau, 2026b, pp. 8, 11) |
| **Pooled weight (`FWC` / 3)** | Each year's weights add up to all US children. Stacking three years would count every child three times, so the official guidance is to divide the weight by the number of years combined. This only changes **totals**; shares are unaffected because the factor cancels. | (U.S. Census Bureau, 2025d, p. 2; U.S. Census Bureau, 2026b, p. 12) |
| **Domain (subpopulation) estimation** | To estimate a subgroup (e.g., mothers), keep every record and give the others zero weight. Deleting records first gives wrong standard errors. | (U.S. Census Bureau, 2026c, p. 49; U.S. Census Bureau, 2026a, p. 8) |
| **Design-based standard error** | Uncertainty that accounts for how the sample was drawn: strata = state × `STRATUM`, primary sampling unit = household (`HHID`). NSCH standard errors here are about twice as large as a simple-random-sample formula would give. | (U.S. Census Bureau, 2026b, p. 12; U.S. Census Bureau, 2026c, p. 49) |
| **95% confidence interval (CI)** | The range the true value plausibly falls in. Narrow = precise. | — |
| **Logit-transformed CI** | The simple interval (estimate ± 1.96 × SE) is symmetric, so for a small share with a large SE its lower end can fall below 0%. Example: 8.3% ± 8.8 gives −0.5% to 17.2%, which is impossible. The logit interval is computed on the log-odds scale, log(p / (1 − p)), and converted back. It always stays between 0% and 100% and is lopsided near 0%, as it should be. It is Stata's default for survey proportions and is used in the NSCH Analytic Guide's own SAS examples. | (StataCorp, 2025; Lumley, n.d.; U.S. Census Bureau, 2026a) |
| **Korn–Graubard CI** | An alternative: a survey-adjusted version of the "exact" (Clopper–Pearson) binomial interval. It uses an *effective* sample size (n adjusted for the survey design). NCHS recommends it in its data presentation standards. Not used here; noted for reference. | (Parker et al., 2017; Korn & Graubard, 1998) |
| **Relative standard error (RSE)** | SE ÷ estimate. It measures uncertainty relative to the size of the number. An RSE of 54% means the uncertainty is about half the estimate itself. Reported in the tables for information. | — |
| **Sensitivity analysis** | Re-running an analysis with a different but reasonable choice to see whether the conclusions change. If they don't, the result is robust. | — |
| **Rubin's rules** | How to combine results from multiply imputed data. Income is missing for many families, so the Census Bureau provides **six** plausible versions (`FPL_I1`–`FPL_I6`). Run the analysis on each version and average the six estimates. The final uncertainty is the average within-version variance plus (1 + 1/6) × the variance *between* the six estimates. Where income was reported, the versions agree and nothing changes. Where it was imputed, uncertainty grows honestly. The NSCH guide cites Rubin (1996) and defers to software (Stata `mi estimate: svy:`) rather than giving the formula. The formula itself is from Rubin (1987). | (U.S. Census Bureau, 2025c, pp. 1–2, 7–8; Rubin, 1996; Rubin, 1987) |

### 0.2 NSCH reliability rules

Stated in the 2025 Methodology Report (U.S. Census Bureau, 2026c, pp. 49–50), the FAQs (U.S. Census Bureau, 2026b, p. 13) and the Analytic Guide (U.S. Census Bureau, 2026a, p. 13):

1. **Only present estimates with an unweighted denominator of 30 or more.** With fewer than 30 people, a few unusual answers swing the result, and small groups risk identifying individuals. Flag in tables: `n<30`.
2. **Flag estimates for poor reliability if the 95% CI is wider than 20 percentage points, or wider than 1.2 times the estimate.** The report notes the second condition is about the same as an RSE above 30%. Flags in tables: `CI>20pts`, `CI>1.2x estimate`.

"Flag" means show the estimate with a reliability warning (or a measure of its precision). These are NSCH's own rules. NCHS has different, stricter standards for its own publications (Parker et al., 2017); we follow the survey's guidance.

### 0.3 Missing-value codes

The NSCH public files use these codes (U.S. Census Bureau, 2026c, pp. 30–31, 37). The loader turns them into empty values and keeps the letter in a `<VAR>__MISS` column.

| Code | Meaning | Among mothers (pooled) |
|---|---|---|
| `.m` | **No valid response** ("missing in error"): the question was asked but left blank or answered invalidly. | 0.4–1.5% per item |
| `.l` | **Logical skip**: not asked because of an earlier answer, e.g. Adult 2 questions when there is no second adult. | 14,262 for Adult 2 items |
| `.n` | **Not in universe**: the question is not on this child's form, e.g. a T1-only item for a 10-year-old. | All children 6–17 for T1 items |
| `.d` | **Suppressed for confidentiality**: blanked by the Census Bureau because it could help identify someone. | 0 (none of our variables) |
| `.k` | **Don't know.** Only assigned to `FASD_YEARS`, and not present on the 2025 file (U.S. Census Bureau, 2026c, footnote 25). None of the 2023–2025 label files we use define it. | Not used |
| *Numeric "don't know"* | Some items store "don't know" as an ordinary answer code. Among kept variables only **`MISSMORTGAGE` = 3**. This is counted as nonresponse here and must be recoded to missing in the analysis. | 979 (1.1%) |

### 0.4 Variables used in this check

Wording from `docs/dataset-inventory.md` Section 2.4 and the 2025 label files. T1 = questionnaire for children 0–5, T2 = 6–11, T3 = 12–17.

| Variable | Plain name | Asked for | Wording / meaning |
|---|---|---|---|
| `A1_SEX`, `A1_RELATION` | Respondent's sex; relationship to the child | All | 1 = biological or adoptive parent (the two cannot be separated) |
| `A2_SEX`, `A2_RELATION` | Second adult's sex and relationship, reported by the respondent | All | 8 = no second caregiver |
| `A1_EMPLOYED_R` | Respondent's current employment | All | 1 full-time; 2 part-time; 3 working without pay; 4 not employed, looking; 5 not employed, not looking; 6 retired |
| `A1_MENTHEALTH` | Respondent's self-rated mental or emotional health | All | 1 excellent … 5 poor. A single self-rating, not a clinical measure |
| `K8Q30` | Coping with parenting | All | How well handling the day-to-day demands of raising children |
| `K8Q31`, `K8Q32`, `K8Q34` | Parenting aggravation | All | Past month: child much harder to care for; child does things that really bother you; felt angry with this child. These describe the **respondent's** experience |
| `K8Q35` | Emotional support | All | Someone to turn to for day-to-day emotional support with parenting |
| `TALKABOUT`, `WKTOSOLVE`, `STRENGTHS`, `HOPEFUL` | Family resilience | All | How the family handles problems |
| `ACE1` | Economic hardship | All | How often hard to cover basics like food or housing on the family's income |
| `FOODSIT` | Food sufficiency | All | Household's ability to afford needed food, past 12 months |
| `TENURE` | Housing tenure | All | Own with mortgage / own free and clear / rent / no rent (imputed where missing) |
| `MISSMORTGAGE`, `HOMEEVIC` | Housing strain | All | Unable to pay mortgage/rent on time; worried about eviction or foreclosure |
| `HOURSLEEP05` | Child's sleep, ages 0–5 | T1 | Hours of sleep per 24 hours, including naps |
| `HOURSLEEP` | Child's sleep, ages 6–17 | T2, T3 | Hours of sleep on most weeknights. **Not comparable** with `HOURSLEEP05` |
| `BEDTIME` | Regular bedtime | All | How often the child goes to bed at the same time |
| **`K6Q27`** | **Job change because of childcare problems** | **T1** | "During the past 12 months, did you or anyone in the family have to quit a job, not take a job, or greatly change your job because of problems with child care for this child?" |
| `HOURSOFCARE` | Hours of non-parental childcare | T1, 2025 only | Weekly hours of care by someone other than a parent |
| `TOTKIDS_R` | Number of children in the household | All | 1, 2, 3, 4+ (children under 18 only) |
| `TOTAGE_0_5`, `TOTAGE_6_11`, `TOTAGE_12_17` | Children per age band in the household | All | Counts, **including** the sampled child |
| `AGEPOS4` | Sampled child's birth order | All | Only, oldest, second oldest, … |
| `FPL_I1`–`FPL_I6` (+ `FPL_IF`) | Family income as % of the poverty line | All | Six imputed versions; combine with Rubin's rules |
| `A1_GRADE_IF`, `HHCOUNT_IF`, `TENURE_IF` | Imputation flags | All | 1 = the value was imputed by the Census Bureau |

---

## 1. Step 3: Defining "mother"

**Definition used:** Adult 1 (the person who filled in the survey) is female (`A1_SEX = 2`) **and** is the sampled child's biological or adoptive parent (`A1_RELATION = 1`).
**Comparison group:** fathers, defined the same way with `A1_SEX = 1`: **44,245** children.

### 1.1 Children remaining after each filter

Unweighted counts. Table: `step3_mother_flow.csv`.

| Step | 0–5 | 6–11 | 12–17 | All |
|---|---:|---:|---:|---:|
| 1. All sampled children | 47,465 | 44,163 | 60,048 | 151,676 |
| 2. Adult 1 is female | 30,893 | 28,922 | 39,196 | 99,011 |
| 3. …and biological/adoptive parent | **28,606** | **26,289** | **35,520** | **90,415** |

By year (all ages): 2023 = 33,365; 2024 = 30,629; 2025 = 26,421.

**2023 has many more children aged 0–5 in the sample** (21,524, compared with 13,841 in 2024 and 12,100 in 2025). Weighted totals are stable at about 22.1 million children 0–5 each year, so the weights correct for this. However, 2023 contributes 46% of the pooled 0–5 sample. The reason is **not yet verified** [VERIFY in the 2023 Methodology Report].

### 1.2 Why children were excluded

Pooled 2023–2025. Table: `step3_exclusion_reasons.csv`.

| Filter | Reason | n |
|---|---|---:|
| Sex | Adult 1 male | 48,048 |
| Sex | Adult 1 sex missing (`.m`) | 4,617 |
| Relationship (female Adult 1) | Grandparent | 5,782 |
| Relationship (female Adult 1) | Step-parent | 1,259 |
| Relationship (female Adult 1) | Other relative | 997 |
| Relationship (female Adult 1) | Other non-relative | 267 |
| Relationship (female Adult 1) | Foster parent | 227 |
| Relationship (female Adult 1) | Relationship missing | 64 |

- 575 of the 4,617 children with missing `A1_SEX` have a biological/adoptive-parent respondent. Some are likely mothers, but the data cannot confirm it, so they are excluded.
- Step-mothers, grandmothers and foster mothers are excluded by design. They could form separate comparison groups later.

### 1.3 Mothers who are not the respondent (Adult 2)

Table: `step3_adult2_mothers.csv`.

| Band | Mother is Adult 1 (kept) | Mother is only Adult 2 (excluded) | No mother identified |
|---|---:|---:|---:|
| 0–5 | 28,606 | 14,498 | 4,361 |
| 6–11 | 26,289 | 12,110 | 5,764 |
| 12–17 | 35,520 | 15,491 | 9,037 |

About a third of children with an identified mother have her only as Adult 2. Her employment and health are then **reported by someone else**, usually the father. The aggravation items (`K8Q30`–`K8Q34`) describe the *respondent's* experience, not hers. That is why she is excluded from the main sample.

**Does excluding them change the employment picture?** Table: `step3_employment_adult1_vs_adult2.csv`; weighted shares among valid answers.

| Band | Group | Full-time | Part-time | Not employed, looking | Not employed, not looking |
|---|---|---:|---:|---:|---:|
| 0–5 | Adult 1 mother | 51.6% | 16.3% | 8.7% | 21.5% |
| 0–5 | Adult 2 mother (proxy) | 51.2% | 15.5% | 7.1% | 24.8% |
| 6–11 | Adult 1 mother | 55.5% | 16.7% | 8.8% | 16.8% |
| 6–11 | Adult 2 mother (proxy) | 57.1% | 16.5% | 6.2% | 18.3% |
| 12–17 | Adult 1 mother | 59.9% | 15.8% | 7.1% | 14.0% |
| 12–17 | Adult 2 mother (proxy) | 58.3% | 17.2% | 4.7% | 16.9% |

Full-time shares are close. Respondent mothers are somewhat more often "looking for work" and less often "not looking". We cannot tell whether this reflects real differences between households or differences between self-report and proxy report.

---

## 2. Step 4: Sample sizes and reliability

**Method:**
- Weighted shares with design-based standard errors (Taylor linearization; strata = year × `FIPSST` × `STRATUM`; household as PSU). Subgroups are estimated as domains.
- Pooled weight = `FWC` / 3.
- **Logit-transformed 95% CIs.**
- NSCH reliability rules (Section 0.2) applied to every estimate.

`STRATUM` keeps its values "1" and "2A". The recode of "2A" to "2" is only needed when 2016 is pooled (U.S. Census Bureau, 2025d, pp. 2–3).

### 2.1 Unweighted sample sizes, mothers, primary bands

Pooled n. Tables `step4_sizes_mothers_*.csv` also give per-year n and weighted counts.

| Employment (`A1_EMPLOYED_R`) | 0–5 | 6–11 | 12–17 |
|---|---:|---:|---:|
| 1 Employed full-time | 16,552 | 16,275 | 23,274 |
| 2 Employed part-time | 4,603 | 4,337 | 5,460 |
| 3 Working without pay | 431 | 411 | 519 |
| 4 Not employed, looking for work | 1,477 | 1,347 | 1,574 |
| 5 Not employed, not looking for work | 5,247 | 3,520 | 3,685 |
| 6 Retired | 62 ⚠ | 197 | 623 |
| Missing | 234 | 202 | 385 |

⚠ = fewer than 30 in at least one single year (0–5 retired: 29 / 19 / 14).

### 2.2 Unweighted sample sizes, mothers, 0–2 vs. 3–5

| Employment | 0–2 | 3–5 |
|---|---:|---:|
| Employed full-time | 7,233 | 9,319 |
| Employed part-time | 2,075 | 2,528 |
| Working without pay | 188 | 243 |
| Not employed, looking | 656 | 821 |
| Not employed, not looking | 2,561 | 2,686 |
| Retired | **22** ✗ | 40 ⚠ |

✗ = fewer than 30 even with three years pooled.

### 2.3 Precision test with a real outcome

Having n ≥ 30 does not guarantee a usable estimate when the outcome is uncommon. As a stress test, we estimated the share reporting **fair or poor mental health** (`A1_MENTHEALTH` = 4 or 5) in every group.

How it was estimated, for each group (e.g. "mothers of children 0–5 who work full-time"):
1. **Group:** respondent mothers in that band and employment status who answered `A1_MENTHEALTH`.
2. **Weighted share:** the sum of weights of those rating their mental health fair or poor, divided by the sum of weights of everyone in the group.
3. **Uncertainty:** design-based SE, logit 95% CI, then the reliability rules.

Tables: `step4_mentalhealth_precision_*.csv`.

| Mothers: cell | n | 95% CI width | Result |
|---|---:|---:|---|
| Full-time, part-time, both not-employed groups (primary and 0–2 / 3–5) | 651–23,227 | 1.3–10.5 pts | **Pass** |
| Working without pay, primary bands | 410–519 | 9.1–10.2 pts | Pass |
| Working without pay, 3–5 | 242 | 10.7 pts | **Flag** (CI > 1.2 × estimate) |
| Retired, 0–5 and 6–11 | 62 / 196 | 19.7 / 10.2 pts | **Flag** (CI > 1.2 × estimate) |
| Retired, 0–2 / 3–5 | 22 / 40 | 22.1 / 30.8 pts | **Fail** (n < 30 / CI > 20 pts) |

Employment shares within each band (`step4_employment_shares_*.csv`) all pass, except the very small shares of retired mothers (0.1–0.4%) in the 0–2 band and the multiple-young-children groups.

### 2.4 Mothers with more than one young child

**What the public file allows.** One child is randomly selected per household (U.S. Census Bureau, 2026c, p. 5). The topical file gives that child's exact age, but other children appear only as **counts per age band** (`TOTAGE_0_5`, `TOTAGE_6_11`, `TOTAGE_12_17`, which include the sampled child) and the sampled child's birth order (`AGEPOS4`).

So we **can** identify:
- whether there is any child aged 0–5 in the household, and how many;
- whether the sampled child is aged 0–2 **and** there is at least one other child aged 0–5.

We **cannot** identify "two children under 3", because the other child's exact age is unknown. We also can't see children aged 18 or over, such as a child at college: they are not counted as children. If they live at home they are only in the total household size (`HHCOUNT`).

**Possible improvement (to check):** for 2016–2024 a separate Screener file "included all children rostered on completed screeners" (U.S. Census Bureau, 2026c, p. 8). It was discontinued in 2025. If the 2023–2024 screener files include each child's age and can be linked to the topical file by `HHID`, "two children under 3" may be measurable for those two years. [VERIFY: not yet downloaded or checked.]

Three groupings were tested (tables `step4_*_youngest`, `*_young_children`, `*_baby`):

**(a) Youngest child's band.** The band of the youngest child in the household, rather than the sampled child. **8,391 mothers** (9.3%) have a child aged 0–5 but were sampled through an older child. Under the sampled-child definition they are counted in band 6–11 or 12–17.

| Youngest child | 0–5 | 6–11 | 12–17 |
|---|---:|---:|---:|
| Mothers (n) | 36,997 | 26,173 | 27,245 |

**(b) Number of children aged 0–5.**

| Children 0–5 in household | None | 1 | 2+ |
|---|---:|---:|---:|
| Mothers (n) | 53,418 | 24,157 | 12,840 |
| …of whom full-time / part-time / not looking | 35,230 / 8,360 / 5,437 | 14,367 / 3,881 / 3,851 | 6,504 / 2,159 / 3,164 |

**(c) "Baby plus another young child".** The sampled child is 0–2 and there is at least one more child aged 0–5. This is the closest available proxy for "two under 3".

| Group | Mothers (n) | Full-time | Part-time | Not employed (any) |
|---|---:|---:|---:|---:|
| Child 0–2 + another child 0–5 | 5,619 | 2,872 | 973 | 1,606 |
| Child 0–2, no other child 0–5 | 7,218 | 4,361 | 1,102 | 1,633 |

All three groupings pass the reliability rules for mothers' mental health in the main employment groups. For example, group (c) has CI widths of 2.9–7.1 points. "Retired" and "working without pay" fail in (b) and (c).

### 2.5 Fathers as a comparison group

44,245 fathers (biological/adoptive, respondent). Most fathers work full-time, so the other employment groups are small. Employment shares among fathers of children 0–5: full-time 89.6%; part-time 4.1%; looking 3.2%; not looking 1.6%; retired 1.1%; without pay 0.4%.

To compare mothers and fathers, employment is collapsed to three groups: **full-time**, **part-time**, and **not employed** (looking + not looking + retired). Fair/poor mental health precision (tables `*_emp3.csv`):

| Grouping | Full-time fathers | Not-employed fathers | Part-time fathers |
|---|---|---|---|
| Primary bands (0–5 / 6–11 / 12–17) | Pass (n ≥ 11,416) | **Pass** (n = 669 / 775 / 1,497) | Flag in 0–5 and 12–17 (n = 389, 573) |
| Youngest child's band | Pass | Pass (n = 853 / 817 / 1,271) | Flag in 0–5 and 12–17 |
| Number of children 0–5 | Pass | Pass | Flag for 1 and 2+ children 0–5 |
| 0–2 / 3–5 | Pass | Flag in 0–2 (n = 282); pass in 3–5 | Flag |
| Baby plus another young child | Pass (n = 2,600) | Flag (n = 123) | Flag (n = 59) |

All mothers' cells pass in every grouping with this collapsed scheme.

---

## 3. Step 5: Missing data among mothers

Tables: `step5_missingness.csv` (every kept variable, by year and pooled) and `step5_missing_by_band.csv`.

**Item nonresponse** = no valid response (`.m`) + suppressed (`.d`) + "don't know", as a share of mothers who were asked.

- **Every kept variable has at most 1.9% item nonresponse**, in every year and band. Most are below 1%.
- **Key items**, pooled:

  | Variable | Nonresponse |
  |---|---:|
  | `A1_EMPLOYED_R` | 0.9% (821) |
  | `A1_MENTHEALTH` | 0.7% |
  | `K8Q30`–`K8Q35` | 0.6–0.9% |
  | Resilience items | 1.0–1.2% |
  | `ACE1` | 0.5% |
  | `FOODSIT` | 0.8% |
  | `MISSMORTGAGE` | 1.8%, including 979 "don't know" answers (code 3) |

- **No missing data, because the values are imputed:** `FPL_I1`–`I6`, `TENURE`, `A1_GRADE` and `HHCOUNT`.
  - The Census Bureau imputes these. The flags `FPL_IF`, `TENURE_IF`, `A1_GRADE_IF` and `HHCOUNT_IF` (1 = imputed) identify the imputed cases, and all are kept by the loader.
  - Among mothers, education is imputed for 414 (0.5%) and household count for 423 (0.5%). Across all children the rate is about 3%, so imputation is concentrated among non-mother respondents.
- **Skips behave as expected:**
  - Adult 2 items are `.l` for 14,262 mothers with no second caregiver.
  - `HOURSLEEP05` and `K6Q27` are `.n` for all children 6–17, and `HOURSLEEP` is `.n` for all children 0–5.
- **`HOURSOFCARE`** exists only in 2025: 7,084 valid answers, all for children 0–5.

---

## 4. Who the results describe

The precise population is **children living with a biological or adoptive mother who answered the survey**. It is not "all mothers".

**Why "children, not mothers" matters.** The NSCH is a survey about children. Parents answer questions about themselves because they are part of the child's environment. The weight of each sampled child reflects how many children were in the household (U.S. Census Bureau, 2026c, p. 44). So a mother with three children carries more weight than a mother with one, compared with a count of mothers.
- ✅ "51.6% of children aged 0–5 have a mother who is employed full-time."
- ❌ "51.6% of mothers of young children work full-time."

If mothers with more children work less, the two figures differ. This matters when comparing with ATUS and ACS, which count people, not children.

| Group | In our sample? |
|---|---|
| Mothers answering about their own child | ✅ Yes |
| Mothers in two-mother households | ✅ If one of them answered |
| Fathers answering about their own child | ✅ As a comparison group |
| Mothers who appear only as Adult 2 | ❌ Proxy-reported; sensitivity check for employment only |
| Step-mothers, grandmothers, foster mothers raising children | ❌ Excluded by definition |
| Mothers not living with their child | ❌ Not covered by the NSCH |
| Mothers whose children are all 18 or older | ❌ Not covered |
| Respondents with missing sex (575 likely parents) | ❌ Excluded; very small |

---

## 5. How these results are applied

Agreed 2026-11-01.

### 5.1 Sample definition

1. **Main sample:** children whose Adult 1 is female and their biological or adoptive parent (n = 90,415 pooled).
2. **Keep all records** in the file and estimate mothers as a domain. Do not delete non-mother records before computing standard errors.
3. **Report the selection.** Every result covers "mothers who answered the survey about their child". The Adult 1 vs. Adult 2 comparison (Section 1.3) goes into the limitations.
4. **Sensitivity analysis: add Adult 2 mothers for employment only.** A mother's employment is an observable fact another adult can report fairly accurately. Her mental health is an internal state, so a proxy rating is much less trustworthy, and the aggravation items describe the respondent, not her. This is a small appendix table: one comparison and one sentence of conclusion. Her answers are not used anywhere else.

### 5.2 Wording of results

5. **Results describe children, not mothers** (Section 4). Write "X% of children aged 0–5 have a mother who…".
6. **No causal language.** Differences between employment groups are associations. Mental health can affect employment as much as the reverse.

### 5.3 Employment categories

7. **Mothers: four groups.** Full-time; part-time; not employed and looking; not employed and not looking. All pass every reliability rule in every grouping tested.
8. **"Retired"** is merged into "not employed, not looking", which is also out of the labor force. Report how many cases this moves.
9. **"Working without pay"** (about 1.6%) is kept out of the main comparisons. It does not fit "paid work" and is flagged in the 3–5 band. Show it only for the primary bands, with a reliability note.
10. **Missing employment** (0.9%) is excluded from employment comparisons, and the count is reported.
11. **Mothers vs. fathers:** use the collapsed scheme (full-time / part-time / not employed). Compare **full-time vs. not employed** in the primary bands and the youngest-child bands. Show part-time fathers only with reliability flags.

### 5.4 Age bands and number of children

12. **Primary bands (0–5 / 6–11 / 12–17):** feasible as planned, based on the sampled child's age.
13. **Secondary split (0–2 vs. 3–5):** feasible for mothers in the four main groups. This answers research plan Section 3.4 and inventory open item 13 for NSCH; the ATUS half is still open. For fathers, only full-time is reliable at this level.
14. **Youngest-child bands:** an alternative definition. It reclassifies 8,391 mothers into the 0–5 band and matches how ATUS defines mothers (by youngest child). Used as a sensitivity analysis for the main comparisons.
15. **Multiple young children:** "number of children aged 0–5" (none / 1 / 2+) and "child 0–2 plus another child 0–5" are added as measures of caregiving load. "Two children under 3" is not measurable in the topical file (Section 2.4).
16. **Pool all three years** for subgroup estimates.

### 5.5 Reliability and intervals

17. Apply the NSCH rules (Section 0.2) to **every published estimate**. Do not present estimates with n < 30, and flag the others.
18. Use **logit-transformed 95% CIs**, as in this check, which matches Stata's default and the NSCH Analytic Guide's examples.

### 5.6 Missing data

19. Use **complete-case analysis** per item. Nonresponse is ≤ 1.9%, so multiple imputation for item nonresponse is not justified. State the per-item n in every table.
20. Recode `MISSMORTGAGE` = 3 ("don't know") to missing.
21. Combine income (`FPL_I1`–`I6`) **across the six imputations** with Rubin's rules rather than using `FPL_I1` alone.

### 5.7 Open items

- [VERIFY] Why the 2023 sample has so many more children aged 0–5.
- [VERIFY] Whether the 2023–2024 Screener files give other children's exact ages and link by `HHID` (would allow "two under 3" for those years).
- Add hypotheses for caregiving load (number of young children) and the father comparison to the research plan (v0.7), with these decisions.
- `docs/dataset-inventory.md` Section 2.2 describes the reliability rules as three separate tests; correct it to match Section 0.2 here in v0.7 of the plan/inventory.
- The ATUS sample-size check (plan Section 11, step 5, second half) is still to do.

---

## 6. References

APA 7th edition. Page numbers in the in-text citations are PDF page numbers. In the 2025 Methodology Report, the printed page number is about 3 lower. Census Bureau document dates are the dates printed on each document; dataset dates are the server release dates recorded in `docs/data-acquisition.md`.

Korn, E. L., & Graubard, B. I. (1998). Confidence intervals for proportions with small expected number of positive counts estimated from survey data. *Survey Methodology, 24*(2), 193–201. https://www150.statcan.gc.ca/n1/en/catalogue/12-001-X19980024356

Lumley, T. (n.d.). *svyciprop: Confidence intervals for proportions* [R documentation]. In *survey: Analysis of complex survey samples* (R package). Retrieved November 1, 2026, from https://search.r-project.org/CRAN/refmans/survey/html/svyciprop.html

Parker, J. D., Talih, M., Malec, D. J., Beresovsky, V., Carroll, M., Gonzalez, J. F., Jr., Hamilton, B. E., Ingram, D. D., Kochanek, K., McCarty, F., Moriarity, C., Shimizu, I., Strashny, A., & Ward, B. W. (2017). *National Center for Health Statistics data presentation standards for proportions* (Vital and Health Statistics, Series 2, No. 175). National Center for Health Statistics. https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf

Rubin, D. B. (1987). *Multiple imputation for nonresponse in surveys*. Wiley. https://doi.org/10.1002/9780470316696

Rubin, D. B. (1996). Multiple imputation after 18+ years. *Journal of the American Statistical Association, 91*(434), 473–489. https://doi.org/10.1080/01621459.1996.10476908

StataCorp. (2025). proportion: Estimate proportions. In *Stata base reference manual*. Stata Press. https://www.stata.com/manuals/rproportion.pdf

U.S. Census Bureau. (2025a). *2023 National Survey of Children's Health: Topical public use file (enhanced), Stata format* [Data set]. https://www2.census.gov/programs-surveys/nsch/datasets/2023/nsch_2023e_topical_Stata.zip

U.S. Census Bureau. (2025b). *2024 National Survey of Children's Health: Topical public use file, Stata format* [Data set]. https://www2.census.gov/programs-surveys/nsch/datasets/2024/nsch_2024_topical_Stata.zip

U.S. Census Bureau. (2025c, October 6). *National Survey of Children's Health: Analysis with multiply imputed data*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Analysis-with-Imputed-Data-Guide.pdf

U.S. Census Bureau. (2025d, October 6). *National Survey of Children's Health: Guide to multi-year estimates*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Guide-to-Multi-Year-Estimates.pdf

U.S. Census Bureau. (2026a, October 1). *2025 National Survey of Children's Health: Comprehensive analytic guide*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Analytic-Guide.pdf

U.S. Census Bureau. (2026b, October 5). *2025 National Survey of Children's Health: Data users frequently asked questions (FAQs)*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/2025-NSCH-FAQs.pdf

U.S. Census Bureau. (2026c, October 1). *2025 National Survey of Children's Health: Methodology report*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/2025-NSCH-Methodology-Report.pdf

U.S. Census Bureau. (2026d). *2025 National Survey of Children's Health: Topical public use file (enhanced), Stata format* [Data set]. https://www2.census.gov/programs-surveys/nsch/datasets/2025/nsch_2025_topical_Stata.zip

### Notes on the references

- **Checked against the documents themselves:**
  - all U.S. Census Bureau documents (titles and dates read from each PDF);
  - Parker et al. (2017), including the full author list;
  - the Stata manual (© 1985–2025 StataCorp);
  - the R documentation page.
- **Taken from another document's reference list, not checked against the original:**
  - **Korn & Graubard (1998):** as cited by Parker et al. (2017). The Statistics Canada catalogue lists the authors in the opposite order, and the R documentation gives the volume as 23. Confirm against the article before publication. [VERIFY]
  - **Rubin (1996):** as cited by U.S. Census Bureau (2025c). The issue number (434) and DOI were added from memory and have not been checked. [VERIFY]
- **Not checked:** Rubin (1987), the standard source for the combining formula; DOI not checked. [VERIFY]
- **Dataset release dates:** the dates are the server "Last-Modified" dates at download (`docs/data-acquisition.md`), not formal publication dates.
- **Same author and year:** works are labelled a, b, c… in title order (APA 7, Section 9.47).
