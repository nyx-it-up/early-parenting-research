# Full-Time Working Mothers of Children Under 2 (NSCH)

**Status:** v0.1 (2026-11-11).
**Data:** NSCH 2023–2025 topical files, pooled. **Code:** `src/nsch_h1_under2.py` (uses `src/nsch_h1_models.py` and `src/survey_logit.py`). **Table:** `reports/tables/nsch_h1_under2/under2_all_outcomes.csv`.

**Hypothesis (user):** mothers who work full-time and whose child is under 2 have worse mental health (higher rates of fair or poor mental health).

**Result in one sentence:** the hypothesis is **not supported** on any outcome. Full-time working mothers of children under 2 look the same as, or slightly better than, other mothers of children under 2 and full-time mothers of older children.

All results are associations from cross-sectional data.

## Design

**Two comparisons:**
1. **Among mothers of children under 2:** full-time vs. part-time, not employed and looking, and not employed and not looking. The hypothesis predicts the other groups do *better*.
2. **Among full-time mothers:** child under 2 vs. child 2–5, 6–11 and 12–17. The hypothesis predicts the older-child groups do *better*.

**"Under 2"** means the sampled child's exact age is 0 or 1 (`SC_AGE_YEARS`). A mother whose sampled child is older may also have a baby; NSCH cannot identify that. Sensitivity analysis: "under 3" (ages 0–2).

**Outcomes** (every outcome is coded so that higher = worse):

| Outcome | Definition |
|---|---|
| Mental health rating, mean | `A1_MENTHEALTH`, 1 excellent … 5 poor |
| Very good or worse | rating 2–5 |
| Good, fair or poor | rating 3–5 |
| Fair or poor | rating 4–5 (H1 headline) |
| Poor | rating 5; descriptive only (46 mothers of under-2s) |
| Parenting aggravation | "usually" or "always" on at least one of: child much harder to care for than most (`K8Q31`), child does things that really bother you (`K8Q32`), felt angry with the child (`K8Q34`) |
| Not handling demands | handling the day-to-day demands of raising children "not very well" or "not well at all" (`K8Q30`) |
| Job change because of child care | `K6Q27` = yes ("Job Change Because Problems with Child Care"); asked for children 0–5 only |

Together, the four cut-offs of the rating scale show whether a pattern holds along the whole scale. They are an informal check of what an ordinal model would assume.

**Estimation:** as in H1 Part B (`docs/nsch-h1.md`):
- **Unadjusted:** design-based shares or means.
- **Adjusted:** M1 covariates (survey year, income across six imputations, education, marital status, number of children, mother's age). Binary outcomes use logistic regression with predictive margins; the mean rating uses weighted least squares.
- **Sample:** the adjusted models use the same complete-case rule as H1 (marital status, age and physical health answered).
- **Not estimable:** "poor" is descriptive only (too rare for about 20 model terms). A model that cannot be estimated (singular or not converging) is written as "not estimable"; that applies to "not handling demands" in comparison 1.

## Results

### Comparison 1: mothers of children under 2, by employment

Adjusted gap vs. full-time (95% CI). **Positive = the other group is worse than full-time.**

| Outcome | Full-time (adjusted) | Part-time | Not employed, looking | Not employed, not looking |
|---|---|---|---|---|
| Mean rating (1–5) | 2.13 | −0.01 (−0.11 to 0.10) | +0.18 (−0.03 to 0.40) | +0.04 (−0.08 to 0.15) |
| Very good or worse | 72.5% | +3.3 (−2.3 to 8.8) | +2.2 (−7.2 to 11.7) | +0.8 (−4.6 to 6.1) |
| Good, fair or poor | 32.7% | −2.6 (−8.3 to 3.1) | +8.8 (−1.3 to 18.8) | +1.6 (−4.1 to 7.3) |
| Fair or poor | 7.4% | −1.4 (−4.3 to 1.5) | +3.1 (−1.7 to 8.0) | +1.2 (−2.3 to 4.7) |
| Poor (unadjusted) | 0.3% | +0.3 | +3.4 | +0.2 |
| Parenting aggravation | 1.5% | **+2.6** (0.2 to 4.9)† | +2.5 (−0.5 to 5.5)† | +0.6 (−0.6 to 1.8) |
| Not handling demands (unadjusted) | 1.0% | −0.1 | +1.2† | +1.1† |
| Job change because of child care | 7.8% | **+14.6** (9.8 to 19.3) | **+22.2** (12.7 to 31.7) | **+7.3** (3.5 to 11.0) |

† The group's share is flagged by the NSCH reliability rule (CI wider than 1.2× the estimate).

### Comparison 2: full-time mothers, by child's age

Adjusted gap vs. child under 2 (95% CI). **Positive = mothers of older children are worse than mothers of under-2s.**

| Outcome | Child under 2 (adjusted) | 2–5 | 6–11 | 12–17 |
|---|---|---|---|---|
| Mean rating (1–5) | 2.07 | **+0.11** (0.04 to 0.17) | **+0.08** (0.01 to 0.14) | **+0.09** (0.02 to 0.16) |
| Very good or worse | 71.5% | **+4.6** (1.2 to 7.9) | +3.2 (−0.3 to 6.6) | +3.2 (−0.5 to 6.8) |
| Good, fair or poor | 29.7% | **+4.3** (1.2 to 7.5) | **+3.4** (0.3 to 6.6) | **+4.0** (0.7 to 7.2) |
| Fair or poor | 6.0% | +1.2 (−0.5 to 2.9) | +0.6 (−1.2 to 2.3) | +1.4 (−0.4 to 3.2) |
| Parenting aggravation | 1.5% | **+2.8** (1.9 to 3.7) | **+3.8** (2.9 to 4.7) | **+4.3** (3.3 to 5.2) |
| Not handling demands | 1.0% | **+1.3** (0.5 to 2.0) | **+0.8** (0.1 to 1.5) | **+1.0** (0.3 to 1.7) |
| Job change because of child care | 8.2% | −0.8 (−2.4 to 0.9) | — | — |

**Sensitivity, under 3:** the same picture. For example, fair or poor: full-time 7.7% vs. part-time 6.8%, looking 11.1%, not looking 7.7%. Full-time mothers of under-3s vs. older children: gaps of 0.0 to +0.9 points.

## What the results show

1. **No outcome supports the hypothesis.** Among mothers of under-2s, full-time mothers do not report worse mental health or more parenting strain than part-time or non-employed mothers. Among full-time mothers, those with a child under 2 report **better** mental health on the full rating scale (+0.08 to +0.11 points for older children, about 4 percentage points fewer "good or worse" ratings) and **less** parenting aggravation than those with older children.
2. **The full scale is more sensitive than the fair/poor cut-off.** Differences appear in the middle of the scale (excellent/very good vs. good), not at the fair/poor end.
3. **Parenting aggravation is very low for infants** (1.5% for full-time mothers). The items ask whether the child is "much harder to care for than most", "does things that really bother you" or makes the parent angry. They may capture strain with older children better than with babies, so a low value for infants partly reflects the measure.
4. **Return to work: child care problems are where the groups differ most.** Among mothers of under-2s, job changes because of child care problems are reported by 7.8% of full-time mothers but 22.4% of part-time mothers, 30.0% of mothers looking for work and 15.1% of mothers not looking (adjusted). This fits a **selection** explanation for the main finding: mothers who could not arrange child care, or found full-time work with a baby too hard, may have already moved to part-time work or left employment. The full-time mothers who remain may be those for whom the arrangement works ("healthy worker" selection). This cross-sectional data cannot confirm it.

## Limitations

- **Cross-sectional; selection into employment.** See point 4 above. A longitudinal design would be needed to see whether working full-time with an infant changes mental health.
- **No maternal postpartum depression or anxiety measure** in NSCH. `A1_MENTHEALTH` is a single global self-rating. The child depression/anxiety items (`K2Q32*`, `K2Q33*`) are about the child.
- **"Under 2" is the sampled child.** Mothers with a baby and an older sampled child are classified by the older child.
- **`K6Q27` is a family-level item.** The 2024 NSCH guide to topics and questions describes it as whether anyone in the family had to quit, not take, or greatly change a job because of problems with child care in the past 12 months (paraphrase; exact wording `[VERIFY]` in the questionnaire). It is not specific to the mother, and it covers the past year, not the current job.
- **Small groups:** 357 mothers of under-2s are looking for work, and aggravation and "not handling" have few cases. Several estimates are flagged or not estimable.
- **Multiple comparisons:** 8 outcomes × 2 comparisons × 3–4 groups. Isolated borderline results (such as aggravation for part-time mothers) should not be over-read.
