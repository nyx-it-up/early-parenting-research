# Both Ends of the Mental Health Scale (NSCH, Exploratory)

**Status:** v0.1 (2026-11-11). **Exploratory.**
**Code:** `src/nsch_h1_positive.py`. **Table:** `reports/tables/nsch_h1_positive/both_ends.csv`.

**Question:** do employment groups differ at the positive end of the scale (excellent or very good mental health) as well as the negative end (fair or poor)?

**Methods:** same as H1 Part B (`docs/nsch-h1.md`):
- **Model:** M1 covariates, six income imputations, design-based SEs, predictive margins.
- **Sample:** 87,318 mothers.
- **Outcomes:** `A1_MENTHEALTH` 1–2 (excellent or very good) and 4–5 (fair or poor).

## Results (adjusted %, gap vs. full-time with 95% CI)

| Mother's employment | Excellent or very good | Gap | Fair or poor | Gap |
|---|---|---|---|---|
| Full-time | 66.2% | — | 7.3% | — |
| Part-time | 67.3% | +1.1 (−0.6 to 2.8) | 7.3% | 0.0 (−0.9 to 0.9) |
| Not employed, looking | 60.8% | **−5.4** (−8.5 to −2.3) | 10.3% | **+3.0** (1.5 to 4.5) |
| Not employed, not looking | 65.2% | −1.0 (−3.0 to 1.0) | 10.0% | **+2.7** (1.3 to 4.1) |

## What it shows

1. **Mothers looking for work are worse off at both ends.** Fewer report excellent or very good mental health, and more report fair or poor.
2. **Mothers not looking for work are more spread out.** They are about as likely as full-time mothers to report excellent or very good mental health, but more likely to report fair or poor. This fits the H1 finding that this group mixes different situations: for example, an often-chosen arrangement with young children, and health problems or caregiving with older children.
3. **Part-time and full-time mothers do not differ at either end.**

**Limitations:** as in H1. Exploratory and not pre-specified: two outcomes × three comparisons, uncorrected for multiple testing.
