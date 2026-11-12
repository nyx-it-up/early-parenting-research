# H1: Mothers' Mental Health by Employment Status (NSCH)

**Status:** v0.2 (2026-11-03). Part A: descriptive, unadjusted. Part B: adjusted logistic regression. Part C: Fairlie decomposition (exploratory).
**Data:** NSCH 2023–2025 topical files, pooled.
**Code:** `src/nsch_h1.py` (A), `src/nsch_h1_models.py` and `src/survey_logit.py` (B), `src/nsch_h1_fairlie.py` (C).
**Tables:** `reports/tables/nsch_h1/`, `reports/tables/nsch_h1_models/`, `reports/tables/nsch_h1_fairlie/`.

**Hypothesis (research plan H1):** working mothers' reported mental and emotional health varies by employment circumstances.

**All results are associations.** Poor mental health can make work harder to find or keep as much as the reverse, and no model here estimates an effect of employment.

# Part A: Descriptive comparison

This part compares groups without adjusting for anything else, such as income, family structure or the mother's age.

## Methods

Everything follows the decisions in `docs/nsch-feasibility.md` Section 5.

- **Mothers:** Adult 1 is female and the sampled child's biological or adoptive parent. They are estimated as a domain, with every record kept in the variance calculation.
- **Outcome:** the mother's self-rated mental or emotional health (`A1_MENTHEALTH`), grouped as excellent or very good / good / **fair or poor**. Fair or poor is the headline measure.
- **Employment** (`A1_EMPLOYED_R`), four groups:
  - Full-time.
  - Part-time.
  - Not employed, looking for work.
  - Not employed, not looking. This includes 882 retired mothers. Leaving them out changes the fair/poor percentages and gaps by at most 0.3 points in the primary bands (see Sensitivity analyses).

  "Working without pay" (1,361 mothers) and missing employment (821) are left out.
- **Child age bands:** the sampled child's age (primary 0–5 / 6–11 / 12–17, and secondary with 0–2 / 3–5). The youngest child's band is a sensitivity analysis.
- **Estimation:**
  - **Weights:** `FWC` divided by 3.
  - **Standard errors:** Taylor linearization with year × state × stratum as strata and households as primary sampling units.
  - **Confidence intervals:** logit 95% CIs for shares. Differences use the linearized difference of the two domain estimates.
- **Reliability:** NSCH rules (n ≥ 30; flag CIs wider than 20 points or 1.2× the estimate). **No estimate is flagged.**
- **Analysis sample:** 88,047 mothers. A further 186 had an employment answer but no mental health answer (`table3_exclusions.csv`).

## Results

Results are about children, because NSCH weights are child weights: "X% of children have a mother who rates her mental health as fair or poor."

### Fair or poor mental health, primary bands (`table1_mental_health_primary.csv`)

| Mother's employment | Child 0–5 | Child 6–11 | Child 12–17 |
|---|---|---|---|
| Full-time | 7.4% (6.6–8.3) | 6.7% (5.9–7.7) | 6.7% (6.1–7.4) |
| Part-time | 8.4% (7.0–10.0) | 7.6% (6.2–9.2) | 6.9% (5.8–8.1) |
| Not employed, looking | **15.0%** (11.8–19.0) | **13.8%** (11.2–16.9) | **12.2%** (9.9–15.0) |
| Not employed, not looking | 7.5% (6.3–9.0) | 9.4% (7.6–11.7) | **12.1%** (9.6–15.1) |

95% confidence intervals in brackets. The full three-category distributions are in the table files.

### Differences from full-time employment (`table2_fair_poor_difference_primary.csv`)

| Mother's employment | Child 0–5 | Child 6–11 | Child 12–17 |
|---|---|---|---|
| Part-time | +1.0 pts (−0.7 to 2.7) | +0.8 (−0.9 to 2.6) | +0.2 (−1.1 to 1.5) |
| Not employed, looking | **+7.7** (4.0 to 11.3) | **+7.0** (4.1 to 10.0) | **+5.5** (2.8 to 8.1) |
| Not employed, not looking | +0.1 (−1.4 to 1.7) | **+2.7** (0.5 to 4.9) | **+5.4** (2.5 to 8.2) |

Bold: the 95% CI excludes zero.

### What the pattern shows

1. **Mothers looking for work** stand out in every band. Children whose mother is unemployed and looking are about **twice as likely** to have a mother with fair or poor mental health as children whose mother works full-time (12–15% vs. about 7%).
2. **Part-time and full-time are about the same** in every band. No difference is distinguishable from zero.
3. **Mothers not looking for work** look like full-time mothers when the child is 0–5, but **diverge as children get older**: +2.7 points for 6–11 and +5.4 for 12–17. One possible reading is that staying home with a young child is a common, often chosen arrangement, while being out of the labor force with a teenager more often reflects other circumstances, such as health problems. This data cannot tell these apart.

### Sensitivity analyses

- **0–2 vs. 3–5** (`…_secondary.csv`): the "looking for work" gap appears in both (+6.9 and +8.3 points). The "not looking" group does not differ from full-time in either (+1.4 and −1.1).
- **Youngest child's band** (`…_youngest.csv`): the same pattern. Looking: +6.4 / +6.7 / +7.6 points. Not looking: +0.9 / +3.6 / +6.1 points.
- **Retired mothers** (`sensitivity_no_retired_*.csv`, from `nsch_h1.py`): Tables 1 and 2 are re-estimated without the retired mothers. Only the "not looking" group changes. Primary bands: fair/poor percentages and gaps change by at most 0.3 points (12–17: 12.1% → 12.4%, gap +5.4 → +5.7), but excellent/very good changes by up to 0.6 points (12–17: 65.4% → 64.8%). Youngest-child bands: changes up to 0.5 points for fair/poor (12–17 gap +6.1 → +6.6) and 1.0 point for excellent/very good. No conclusion changes. (The three-group check for mothers and fathers is in `docs/nsch-h8.md`.)

## Limitations of Part A

- **Unadjusted.** Groups differ in income, family structure, education, age and health, all of which relate to both employment and mental health. Part B adjusts for them.
- **Direction unknown.** Poor mental health can lead to job loss or difficulty finding work.
- **Single global self-rating.** `A1_MENTHEALTH` is not a diagnostic measure.
- **Respondent selection.** Only mothers who answered the survey are included (`docs/nsch-feasibility.md` Section 1.3).
- **Multiple comparisons.** The table has 9 primary-band comparisons, and the sensitivity analyses repeat them. Individual intervals are not corrected for this, so isolated borderline results (such as +2.7 for 6–11) should be read with caution.
- **Employment ≠ job quality.** NSCH has no hours, schedule or job-quality items.

# Part B: Adjusted logistic regression

## Why logistic regression

The outcome (fair or poor mental health) is yes/no, so logistic regression is the standard model; a linear model can predict values outside 0–100%. Survey-weighted logistic regression with design-based standard errors is the usual approach for NSCH (Lumley, n.d.; Korn & Graubard, 1998). Results are reported mainly as **adjusted percentages and percentage-point gaps** (predictive margins), which read like the Part A tables. Odds ratios are in the appendix tables. Because only about 8% of mothers report fair or poor mental health, odds ratios are close to risk ratios here.

## What "adjusted" means

Each employment group is compared **as if it had the same mix of other characteristics** as all mothers in the sample. For the adjusted percentage of a group, every mother is set to that employment group while keeping her other characteristics, her predicted probability is computed, and the weighted average is taken. The gap between two such averages cannot be explained by differences in the adjusted characteristics. It can still reflect anything that is not measured.

## Models

All models use the same 87,318 mothers: the Part A sample minus 729 mothers missing marital status (291), age (243) or physical health (206) (`sample.csv`).

| Model | Covariates | Role |
|---|---|---|
| **M0** | Employment, child age band, survey year | Baseline, close to Part A |
| **M1** | M0 + income, education, marital status, number of children, mother's age | **Main model** |
| **M2** | M1 + mother's physical health | Sensitivity. Physical health may be a cause or a consequence of both employment and mental health, so adjusting for it may remove part of a real association. |
| **M1x** | M1 + employment × child age band | Tests whether the employment gaps differ by band |

**Covariates** (codes from the 2023–2025 Stata label files, identical in all three years; the first group listed is the reference):

| Covariate | Variable | Groups |
|---|---|---|
| Income-to-poverty ratio | `FPL_I1`–`FPL_I6` | 400%+; <100%; 100–199%; 200–399% |
| Education | `A1_GRADE` | Bachelor's; high school or less (1–3); some college, vocational or associate (4–6); graduate (8–9) |
| Marital status | `A1_MARITAL` | Married; living with a partner; never married; divorced, separated or widowed |
| Number of children | `TOTKIDS_R` | 1; 2; 3; 4+ |
| Mother's age | `A1_AGE` | 35–44; 18–24; 25–34; 45+ |
| Child age band | `SC_AGE_YEARS` | 0–5; 6–11; 12–17 |
| Survey year | `SURVEY_YEAR` | 2023; 2024; 2025 |
| Physical health (M2 only) | `A1_PHYSHEALTH` | Excellent or very good; good; fair or poor |

## Estimation

- **Weights:** `FWC` / 3.
- **Standard errors:** Taylor linearization (Binder, 1983), strata = year × state × stratum, each household its own PSU, with mothers as a domain of the full file. Implemented in `src/survey_logit.py`, because statsmodels has no survey-design regression. **Checks:** the coefficients equal statsmodels' weighted GLM (difference < 10⁻¹⁴), and an intercept-only model reproduces the design-based SE of the Part A share exactly.
- **Adjusted percentages:** predictive margins. Their SEs include both the coefficient uncertainty and the variation of covariates across records, like Stata's `svy` margins.
- **Income imputations:** 19.7% of children's families have imputed income (`FPL_IF`). Each model is fitted on all six imputations and combined with Rubin's rules (Rubin, 1987). Confidence intervals and p-values use t critical values with Barnard–Rubin (1999) degrees of freedom.
- **Interaction test:** the D1 multivariate Wald F test for multiply imputed data (Li, Raghunathan & Rubin, 1991) of the six employment × band terms.
- **Sample rule:** every model, Table 1 and the H8, under-2 and state-policy models use one complete-case rule (`has_covariates()` in `src/nsch_h1_models.py`: marital status, age and physical health answered).
- **Not estimable:** a model whose information matrix is singular or that does not converge is written as "not estimable" instead of stopping the script.

## Results

### Adjusted gaps vs. full-time (`adjusted_gaps.csv`)

Percentage points, 95% CI.

| Mother's employment | M0 | M1 (main) | M2 |
|---|---|---|---|
| Part-time | +0.6 (−0.4 to 1.5) | 0.0 (−0.9 to 0.9) | +0.2 (−0.7 to 1.1) |
| Not employed, looking | **+6.7** (4.9 to 8.5) | **+3.0** (1.5 to 4.5) | **+1.8** (0.4 to 3.2) |
| Not employed, not looking | **+2.5** (1.2 to 3.8) | **+2.7** (1.3 to 4.1) | +1.1 (0.0 to 2.3) |

Adjusted percentages in M1: full-time 7.3%, part-time 7.3%, looking 10.3%, not looking 10.0% (`adjusted_percentages.csv`).

### Gaps by child age band, M1x (`adjusted_gaps_by_band.csv`)

The employment × band terms are jointly significant (D1 F(6, 1.2 × 10⁸) = 3.37, p = 0.003; `interaction_test.csv`). The denominator df is very large because the six imputations give almost identical interaction estimates, so the test is practically the same as the earlier χ²(6) = 20.2.

| Mother's employment | Child 0–5 | Child 6–11 | Child 12–17 |
|---|---|---|---|
| Part-time | −0.4 (−2.1 to 1.3) | +0.2 (−1.5 to 2.0) | 0.0 (−1.3 to 1.3) |
| Not employed, looking | +2.9 (−0.1 to 5.8) | **+3.7** (1.2 to 6.2) | +2.2 (0.0 to 4.3) |
| Not employed, not looking | −0.4 (−2.1 to 1.3) | **+2.9** (0.5 to 5.2) | **+6.1** (3.2 to 8.9) |

### What the models show

1. **Part-time and full-time mothers do not differ** in any model or band.
2. **The "looking for work" gap more than halves** with adjustment (+6.7 to +3.0 points) but does not disappear. After adjustment it is similar across child age bands (+2.2 to +3.7).
3. **The "not looking" gap does not shrink** with the M1 covariates (+2.5 to +2.7). It **grows with child age**: none for children 0–5, +2.9 for 6–11 and +6.1 for 12–17. This confirms the Part A pattern after adjustment.
4. **Adding physical health (M2)** shrinks both gaps (+1.8 and +1.1). Health is closely tied to both employment and mental health, but the direction is unknown, so this is a sensitivity result.
5. **Other covariates (M1 odds ratios, `odds_ratios_M1.csv`):** fair or poor mental health is more common with lower income (OR 1.6–1.7 for every group below 400% FPL), without a bachelor's degree, and among mothers who are not married (OR 1.6 living with a partner, 2.3 never married, 2.3 divorced/separated/widowed). It is less common at age 45+ (OR 0.71).

# Part C: Fairlie decomposition (exploratory)

**Question:** how much of each raw gap is accounted for by measured differences between the groups (income, education, marital status, number of children, age, child age band and year)?

**Method** (Fairlie, 2005), in `src/nsch_h1_fairlie.py`:
1. One logistic regression on both groups, with the M1 covariates and a group indicator, so the group difference is not absorbed into the covariate coefficients.
2. **Explained part** = average predicted probability with group A's characteristics minus that with full-time mothers' characteristics, using the same coefficients.
3. **Covariate contributions:** equal-sized weighted samples of both groups are paired by predicted probability, and one covariate at a time is switched from A's value to the partner's value. The switching order is randomized in each of 100 replications, and results are averaged over replications and the six income imputations.

**Exploratory:** point estimates only. No design-based CIs for the contributions.

### Results (`fairlie_totals.csv`, `fairlie_contributions.csv`)

| | Looking for work vs. full-time | Not looking vs. full-time |
|---|---|---|
| Raw gap | 6.7 pts | 2.5 pts |
| **Explained** by measured differences | **2.7 pts (41%)** | **−0.1 pts (≈ 0%)** |
| Unexplained | 4.0 pts | 2.6 pts |

**Contributions** (percentage points; positive means this difference widens the gap):

| Covariate | Looking for work | Not looking |
|---|---|---|
| Marital status | +0.99 | **−0.91** |
| Mother's age | +0.83 | +0.20 |
| Income | +0.67 | +0.50 |
| Education | +0.32 | +0.40 |
| Number of children | −0.08 | −0.18 |
| Child age band | −0.03 | −0.08 |
| Survey year | 0.00 | 0.00 |

**Reading:**
- **Looking for work:** about 40% of the gap goes with measured differences. These mothers are more often unmarried, younger and lower-income than full-time mothers, and each of these is linked to poorer mental health. The remaining 60% is not explained by these factors.
- **Not looking:** measured differences explain almost nothing on balance, because they **pull in opposite directions**. These mothers have lower income and less education, which would raise their rate, but they are more often married, which would lower it. The two roughly cancel out, which is why adjustment did not shrink this gap in Part B.

## Limitations (Parts B and C)

- All Part A limitations apply: cross-sectional, direction unknown, single self-rating, respondent selection, no job-quality measures.
- **Unmeasured factors** (for example mental health history, partner support, childcare access, job loss experiences) may account for the remaining gaps.
- **Adjusting for income may over-adjust.** Job loss lowers income, which may then affect mental health. M1 shows the gap beyond income differences, not a "true" gap.
- **Covariate groupings** are chosen to keep groups large; finer groupings could change estimates slightly.
- **The interaction test** (D1) assumes that the share of missing information is similar across the six terms (Li et al., 1991).
- **Fairlie contributions** depend on the reference coefficients and have no design-based CIs.

## Next steps

1. Compare one model with an independent implementation (Stata `svy: logit` or R `survey::svyglm`) if available.
2. Ordinal logistic regression on the full five-point rating (sensitivity).
3. H8: the same models for fathers (full-time vs. not employed).

## References

Binder, D. A. (1983). On the variances of asymptotically normal estimators from complex surveys. *International Statistical Review, 51*(3), 279–292. `[VERIFY]`

Fairlie, R. W. (2005). An extension of the Blinder–Oaxaca decomposition technique to logit and probit models. *Journal of Economic and Social Measurement, 30*(4), 305–316. `[VERIFY]`

Korn, E. L., & Graubard, B. I. (1998). *Analysis of health surveys*. Wiley. (As in `docs/nsch-feasibility.md`.)

Lumley, T. (n.d.). *survey: Analysis of complex survey samples* [R package documentation]. (As in `docs/nsch-feasibility.md`.)

Barnard, J., & Rubin, D. B. (1999). Small-sample degrees of freedom with multiple imputation. *Biometrika, 86*(4), 948–955. https://doi.org/10.1093/biomet/86.4.948 `[VERIFY]`

Li, K. H., Raghunathan, T. E., & Rubin, D. B. (1991). Large-sample significance levels from multiply imputed data using moment-based statistics and an *F* reference distribution. *Journal of the American Statistical Association, 86*(416), 1065–1073. https://doi.org/10.1080/01621459.1991.10475152 `[VERIFY]`

Rubin, D. B. (1987). *Multiple imputation for nonresponse in surveys*. Wiley. (As in `docs/nsch-feasibility.md`.)
