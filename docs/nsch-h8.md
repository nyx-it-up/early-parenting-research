# H8: Employment and Mental Health in Mothers vs. Fathers (NSCH)

**Status:** v0.1 (2026-11-11). **Exploratory comparison.** The project focuses on mothers; fathers are a comparison group, used to see whether patterns are specific to mothers or apply to parents generally.
**Data:** NSCH 2023–2025 topical files, pooled. **Code:** `src/nsch_h8.py` (uses `src/nsch_h1_models.py` and `src/survey_logit.py`). **Tables:** `reports/tables/nsch_h8/`.

**Hypothesis (research plan H8):** associations between employment and well-being differ between mothers and fathers.

**All results are associations.** Poor mental health can lead to non-employment as much as the reverse.

## Methods

Same outcome, design and estimation as H1 (`docs/nsch-h1.md`), with these differences:

- **Parents:** Adult 1 is the sampled child's biological or adoptive parent (`A1_RELATION = 1`). Mothers: `A1_SEX = 2` (88,047 with employment and mental health answers). Fathers: `A1_SEX = 1` (43,550).
- **Employment, collapsed** (`docs/nsch-feasibility.md` decision 11): full-time; part-time; not employed (looking, not looking or retired). "Working without pay" and missing answers are left out. The main comparison is **not employed vs. full-time**, because about 90% of fathers work full-time. Part-time is shown with reliability flags.
- **Outcome:** the parent's self-rated mental or emotional health is fair or poor (`A1_MENTHEALTH` 4–5).
- **Adjusted models:** the H1 main model (M1: income across six imputations, education, marital status, number of children, age, child age band, survey year), fitted **separately for mothers and fathers**. That is equivalent to letting every covariate's association differ by sex. Model samples: 87,318 mothers and 43,157 fathers, after dropping those missing marital status, age or physical health. This is the same complete-case rule as every H1 model, applied to fathers' own answers (`A1_MARITAL`, `A1_AGE`, `A1_PHYSHEALTH`), even though physical health is not a covariate in M1.
- **Difference between mothers and fathers:** mothers' gap minus fathers' gap (a "difference in differences"). Mothers and fathers are separate domains of the same sample, so the variance comes from the difference of the records' linearized contributions, keeping the shared strata in the calculation.
- **By band:** the same models with employment × band terms.
- **Sensitivity:** retired parents left out (865 mothers; 1,192 fathers in the model samples, mostly fathers of teenagers). This three-group check is separate from the four-group check for mothers in `docs/nsch-h1.md`.

## Results

### Fair or poor mental health (`partA_fair_poor_by_sex.csv`)

The share of children whose parent rates their own mental health as fair or poor, with 95% CIs:

| Parent's employment | Child 0–5 | Child 6–11 | Child 12–17 |
|---|---|---|---|
| **Mothers**, full-time | 7.4% (6.6–8.3) | 6.7% (5.9–7.7) | 6.7% (6.1–7.4) |
| Mothers, part-time | 8.4% (7.0–10.0) | 7.6% (6.2–9.2) | 6.9% (5.8–8.1) |
| Mothers, not employed | 9.6% (8.3–11.1) | 10.9% (9.4–12.7) | 12.1% (10.2–14.3) |
| **Fathers**, full-time | 4.4% (3.8–5.1) | 3.5% (3.0–4.1) | 3.4% (2.9–4.1) |
| Fathers, part-time | 4.6% (1.6–12.3)† | 10.4% (6.2–17.0) | 6.5% (3.5–11.6)† |
| Fathers, not employed | 8.0% (5.5–11.6) | 12.8% (9.5–17.1) | 13.6% (8.8–20.4) |

† Flagged: the CI is wider than 1.2 times the estimate (NSCH reliability rule). Interpret with caution.

**Fathers who work full-time** report fair or poor mental health about half as often as mothers who work full-time (3–4% vs. 7%). **Non-employed fathers** report it at similar rates to non-employed mothers (8–14% vs. 10–12%).

### Gaps vs. full-time, adjusted (`partB_adjusted_gaps.csv`)

Percentage points, 95% CI. M1 covariates.

| Employment vs. full-time | Mothers | Fathers | Difference (mothers − fathers) |
|---|---|---|---|
| Not employed | **+2.8** (1.7 to 3.9) | **+6.6** (4.4 to 8.8) | **−3.8** (−6.3 to −1.3) |
| Part-time | 0.0 (−0.9 to 0.9) | +2.3 (0.0 to 4.6) | −2.3 (−4.8 to 0.1) |

### By child age band, adjusted (`partB_adjusted_gaps_by_band.csv`)

Gap for not employed vs. full-time:

| | Child 0–5 | Child 6–11 | Child 12–17 |
|---|---|---|---|
| Mothers | +0.7 (−0.9 to 2.3) | **+3.2** (1.3 to 5.0) | **+4.6** (2.5 to 6.6) |
| Fathers | +2.9 (−0.1 to 6.0) | **+7.5** (3.9 to 11.2) | **+7.9** (3.9 to 12.0) |
| Difference | −2.2 (−5.7 to 1.2) | **−4.3** (−8.4 to −0.3) | −3.4 (−7.9 to 1.2) |

### Sensitivity: retired parents left out (`sensitivity_adjusted_gaps_no_retired.csv`)

Not employed vs. full-time: mothers +2.9 (1.7 to 4.0), fathers **+8.7** (5.5 to 11.9), difference **−5.8** (−9.2 to −2.5). Retired fathers dilute the fathers' gap, so leaving them out **widens** the mother-father difference.

## What the results show

1. **For non-employment, mothers and fathers differ.** After adjustment, the mental health gap between non-employed and full-time parents is **more than twice as large for fathers** (+6.6 points) as for mothers (+2.8). The difference (−3.8 points) excludes zero, and it widens when retired parents are left out.
2. **Relative to their baseline, the fathers' gap is even larger.** Full-time fathers start at about 3.5–4.4%, so non-employed fathers have roughly 2–4 times the rate of full-time fathers. Non-employed mothers have about 1.3–1.8 times the rate of full-time mothers.
3. **By band,** the pattern is the same in every band. The mother-father difference is clearest for children 6–11. The band-specific differences have wide intervals, so the data do not show that the mother-father difference changes with child age.
4. **Part-time:** no gap for mothers. For fathers, a borderline gap (+2.3, CI 0.0 to 4.6). Part-time fathers are few (389–573 per band) and two of three band estimates are flagged, so this is not interpreted further.

**A possible reading, which this data cannot test:** not being employed is a more common and more socially accepted arrangement for mothers (for example, caring for children at home), while for fathers it more often coincides with job loss, health problems or financial strain. That would fit both the smaller gap for mothers and the H1 finding that mothers' gap is absent when children are 0–5.

## Limitations

- All H1 limitations apply: cross-sectional, direction unknown, single self-rating, no job-quality measures.
- **Respondent selection differs by sex.** Fathers answer the survey less often than mothers (43,550 vs. 88,047 parents here). Fathers who answer may differ from those who do not, and the selection may itself depend on employment.
- **"Not employed" mixes different situations** (looking, not looking, retired), and the mix differs between mothers and fathers. The collapsed scheme was needed for fathers' sample sizes.
- **Multiple comparisons.** The band-specific differences are secondary and not corrected for multiple testing.
- **Comparing gaps on the percentage-point scale.** Fathers' lower baseline means the same relative difference would produce a smaller point gap, so the point-scale difference understates the relative difference rather than overstating it.

## Next steps

1. If wanted: split fathers' "not employed" into looking / not looking for the pooled bands only, where the sample allows.
2. ATUS part of H8 (time use of full-time fathers vs. mothers), after the replicate weights are downloaded.
