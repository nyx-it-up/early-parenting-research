# H1: Mothers' Mental Health by Employment Status (NSCH), First Pass

**Status:** v0.1 (2026-11-03). Descriptive, unadjusted.
**Data:** NSCH 2023–2025 topical files, pooled. **Code:** `src/nsch_h1.py`. **Tables:** `reports/tables/nsch_h1/`.

**Hypothesis (research plan H1):** working mothers' reported mental and emotional health varies by employment circumstances.

**What this pass is and isn't.** It compares groups without adjusting for anything else, such as income, family structure or the mother's age. The differences are **associations**: poor mental health can make work harder to find or keep as much as the reverse. Adjusted models come in a later pass.

## Methods

Everything follows the decisions in `docs/nsch-feasibility.md` Section 5.

- **Mothers:** Adult 1 is female and the sampled child's biological or adoptive parent. They are estimated as a domain, with every record kept in the variance calculation.
- **Outcome:** the mother's self-rated mental or emotional health (`A1_MENTHEALTH`), grouped as excellent or very good / good / **fair or poor**. Fair or poor is the headline measure.
- **Employment** (`A1_EMPLOYED_R`), four groups:
  - Full-time.
  - Part-time.
  - Not employed, looking for work.
  - Not employed, not looking. This includes 882 retired mothers; leaving them out changes the results by at most 0.3 points.

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
- **Retired mothers** (`nsch_h1.py` check): excluding them changes the "not looking" estimates by at most 0.3 points.

## Limitations of this pass

- **Unadjusted.** Groups differ in income, family structure, education, age and health, all of which relate to both employment and mental health. The next pass adds them.
- **Direction unknown.** Poor mental health can lead to job loss or difficulty finding work.
- **Single global self-rating.** `A1_MENTHEALTH` is not a diagnostic measure.
- **Respondent selection.** Only mothers who answered the survey are included (`docs/nsch-feasibility.md` Section 1.3).
- **Multiple comparisons.** The table has 9 primary-band comparisons, and the sensitivity analyses repeat them. Individual intervals are not corrected for this, so isolated borderline results (such as +2.7 for 6–11) should be read with caution.
- **Employment ≠ job quality.** NSCH has no hours, schedule or job-quality items.

## Next pass (proposed)

1. **Adjusted model:** survey-weighted logistic regression of fair/poor mental health on employment, child age band and covariates (income-to-poverty combined across imputations, family structure, education, age, number of children), with design-based SEs.
2. **Test whether the employment gap differs by band** (employment × band interaction), especially for "not looking."
3. **Mothers vs. fathers (H8):** the same table for fathers, full-time vs. not employed.
