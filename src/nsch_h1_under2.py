"""H1 focus: are full-time working mothers of children under 2 worse off? (NSCH)

The user's hypothesis: mothers who work full-time and whose (sampled) child is
under 2 years old have worse mental health. Two comparisons test it:

  Comparison 1  Among mothers of children under 2: full-time vs. part-time,
                not employed and looking, and not employed and not looking.
                The hypothesis predicts the other groups do BETTER than full-time.
  Comparison 2  Among full-time mothers: child under 2 vs. child 2-5, 6-11 and
                12-17. The hypothesis predicts the older-child groups do BETTER.

Outcomes (higher = worse for every outcome):
  Mental health, full rating scale (A1_MENTHEALTH: 1 excellent ... 5 poor):
    MH_SCORE          mean rating (1-5)
    MH_NOT_EXCELLENT  very good or worse (2-5)
    MH_GOOD_OR_WORSE  good, fair or poor (3-5)
    FAIR_POOR         fair or poor (4-5)
    MH_POOR           poor (5); descriptive only, too rare for an adjusted model
    The four cut-offs together show whether the pattern is the same along the
    whole scale (an informal check of what an ordinal model would assume).
  Parenting strain:
    AGGRAVATION       "usually" or "always" felt at least one of: the child is
                      much harder to care for than most (K8Q31), the child does
                      things that really bother you a lot (K8Q32), angry with
                      the child (K8Q34)
    NOT_HANDLING      handling the day-to-day demands of raising children
                      "not very well" or "not well at all" (K8Q30)
  Return to work / child care (children 0-5 only):
    JOB_CHANGE_CC     job change because of problems with child care (K6Q27 = 1)

Each comparison is shown unadjusted and adjusted (H1 main model covariates,
six income imputations, design-based SEs). Binary outcomes use logistic
regression with predictive margins; the mean score uses weighted least squares.
Sensitivity: "under 3" (ages 0-2) for the headline outcomes.

"Under 2" uses the sampled child's exact age (SC_AGE_YEARS 0 or 1). A mother
with an older sampled child may also have a baby; NSCH cannot identify that.

Associations only.

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch_h1_under2.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from nsch_feasibility import DATA_FILE, logit_ci, prepare, reliability_flags
from nsch_h1 import design_se, linearized_share
from nsch_h1_models import (CATEGORIES, IMPUTATIONS, MODELS, NOT_ESTIMABLE, add_covariates, combine,
                            combine_margins, design_matrix, fit_imputations, has_covariates, income_group,
                            is_mother, set_employment, variance_of)
from survey_logit import NotEstimable, fit_linear, linear_influence

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "tables" / "nsch_h1_under2"

OUTCOMES = {
    "MH_SCORE": ("Mental health rating, mean (1 excellent - 5 poor)", "mean"),
    "MH_NOT_EXCELLENT": ("Mental health very good or worse", "binary"),
    "MH_GOOD_OR_WORSE": ("Mental health good, fair or poor", "binary"),
    "FAIR_POOR": ("Mental health fair or poor", "binary"),
    "MH_POOR": ("Mental health poor", "binary_descriptive"),  # too rare to model (46 mothers of under-2s)
    "AGGRAVATION": ("Parenting aggravation (usually/always on K8Q31, K8Q32 or K8Q34)", "binary"),
    "NOT_HANDLING": ("Handling demands of raising children not very well / not at all (K8Q30)", "binary"),
    "JOB_CHANGE_CC": ("Job change because of problems with child care (K6Q27), child 0-5", "binary"),
}
HEADLINE = ["MH_SCORE", "FAIR_POOR", "AGGRAVATION"]
AGE_SCHEMES = {
    "under2": ["Under 2", "2-5", "6-11", "12-17"],
    "under3": ["Under 3", "3-5", "6-11", "12-17"],
}
FULL_TIME = CATEGORIES["EMP"][0]
OTHER_COVARIATES = MODELS["M1"][2:]  # year, income, education, marital, kids, mother's age


def add_outcomes(data):
    """Add the outcome columns (missing where the item is missing)."""
    rating = data["A1_MENTHEALTH"]
    data["MH_SCORE"] = rating
    thresholds = {"MH_NOT_EXCELLENT": 2, "MH_GOOD_OR_WORSE": 3, "FAIR_POOR": 4, "MH_POOR": 5}
    for name, cut in thresholds.items():
        data[name] = (rating >= cut).astype(float).where(rating.notna())

    items = data[["K8Q31", "K8Q32", "K8Q34"]]
    usually_or_always = (items >= 4).any(axis=1).astype(float)
    data["AGGRAVATION"] = usually_or_always.where(items.notna().all(axis=1))
    data["NOT_HANDLING"] = (data["K8Q30"] >= 3).astype(float).where(data["K8Q30"].notna())
    data["JOB_CHANGE_CC"] = (data["K6Q27"] == 1).astype(float).where(data["K6Q27"].notna())
    return data


def child_age_group(age, cutoff):
    """Child age group for a cut-off of 2 or 3 years."""
    if age < cutoff:
        return f"Under {cutoff}"
    if age <= 5:
        return f"{cutoff}-5"
    if age <= 11:
        return "6-11"
    return "12-17"


def descriptive(data, domain, group_column, groups, outcome, kind):
    """Unadjusted share (or mean) per group, plus the gap vs. the first group."""
    values = data[outcome].fillna(0)
    reference = domain & (data[group_column] == groups[0])
    ref_value, z_ref = linearized_share(data, reference, values)
    rows = []
    for group in groups:
        in_group = domain & (data[group_column] == group)
        n = int(in_group.sum())
        value, z = linearized_share(data, in_group, values)
        se = design_se(data, z)
        if kind != "mean":
            low, high = logit_ci(value, se)
            flags = reliability_flags(n, value, (high - low) * 100)
            scale = 100
        else:
            low, high = value - 1.96 * se, value + 1.96 * se
            flags = "" if n >= 30 else "n<30"
            scale = 1
        row = {"group": group, "n": n,
               "unadjusted": round(scale * value, 2 if kind == "mean" else 1),
               "unadjusted_ci": f"{scale * low:.{2 if kind == 'mean' else 1}f} to {scale * high:.{2 if kind == 'mean' else 1}f}",
               "flags": flags}
        if group != groups[0]:
            gap_se = design_se(data, z - z_ref)
            gap = value - ref_value
            row["unadjusted_gap"] = round(scale * gap, 2 if kind == "mean" else 1)
            row["unadjusted_gap_ci"] = (f"{scale * (gap - 1.96 * gap_se):.{2 if kind == 'mean' else 1}f} to "
                                        f"{scale * (gap + 1.96 * gap_se):.{2 if kind == 'mean' else 1}f}")
        rows.append(row)
    return pd.DataFrame(rows)


def adjusted_binary(data, domain, exposure, outcome):
    fits = fit_imputations(data, domain, [exposure] + OTHER_COVARIATES, outcome=outcome)
    table = combine_margins(fits, data)
    table["adjusted_ci"] = table["ci_low_pct"].astype(str) + " to " + table["ci_high_pct"].astype(str)
    table["adjusted_gap_ci"] = table["gap_ci_low_pts"].astype(str) + " to " + table["gap_ci_high_pts"].astype(str)
    table.loc[table["gap_vs_full_time_pts"].isna(), "adjusted_gap_ci"] = ""
    return table.rename(columns={"employment": "group", "adjusted_pct": "adjusted",
                                 "gap_vs_full_time_pts": "adjusted_gap"})[
        ["group", "adjusted", "adjusted_ci", "adjusted_gap", "adjusted_gap_ci"]]


def adjusted_mean(data, domain, exposure, outcome):
    """Adjusted mean score per group (weighted least squares), Rubin-combined."""
    variables = [exposure] + OTHER_COVARIATES
    groups = CATEGORIES[exposure]
    levels = {}
    gaps = {}
    for group in groups:
        levels[group] = ([], [])
        gaps[group] = ([], [])
    domain_rows = np.flatnonzero(domain.values)
    for column in IMPUTATIONS:
        frame = data.loc[domain].copy()
        frame["INCOME"] = frame[column].apply(income_group)
        X, _ = design_matrix(frame, variables)
        y = frame[outcome].values
        w = frame["WEIGHT_POOLED"].values
        beta = fit_linear(X, y, w)
        influence = np.zeros((len(data), len(beta)))
        influence[domain_rows] = linear_influence(X, y, w, beta)

        margin = {}
        contribution = {}
        for group in groups:
            X_group, _ = design_matrix(set_employment(frame, group, exposure), variables)
            predicted = X_group @ beta
            margin[group] = (w * predicted).sum() / w.sum()
            z = influence @ ((X_group * w[:, None]).sum(axis=0) / w.sum())
            z[domain_rows] += w * (predicted - margin[group]) / w.sum()
            contribution[group] = z
        for group in groups:
            levels[group][0].append(margin[group])
            levels[group][1].append(variance_of(contribution[group], data))
            gaps[group][0].append(margin[group] - margin[groups[0]])
            gaps[group][1].append(variance_of(contribution[group] - contribution[groups[0]], data))

    rows = []
    for group in groups:
        level, low, high = combine(*levels[group], data)
        row = {"group": group, "adjusted": round(level, 2), "adjusted_ci": f"{low:.2f} to {high:.2f}",
               "adjusted_gap": None, "adjusted_gap_ci": ""}
        if group != groups[0]:
            gap, low, high = combine(*gaps[group], data)
            row["adjusted_gap"] = round(gap, 2)
            row["adjusted_gap_ci"] = f"{low:.2f} to {high:.2f}"
        rows.append(row)
    return pd.DataFrame(rows)


def run_comparison(data, domain, exposure, outcome, comparison, scheme):
    label, kind = OUTCOMES[outcome]
    has_outcome = data[outcome].notna()
    complete = domain & has_outcome & has_covariates(data)
    table = descriptive(data, domain & has_outcome, exposure, CATEGORIES[exposure], outcome, kind)
    events = int(data.loc[complete, outcome].sum()) if kind == "binary" else None
    table["outcome_events"] = events
    try:
        if kind == "binary":
            table = table.merge(adjusted_binary(data, complete, exposure, outcome), on="group", how="left")
        elif kind == "mean":
            table = table.merge(adjusted_mean(data, complete, exposure, outcome), on="group", how="left")
    except NotEstimable:
        table["adjusted"] = NOT_ESTIMABLE
    table.insert(0, "group_type", "employment" if exposure == "EMP" else "child age")
    table.insert(0, "comparison", comparison)
    table.insert(0, "outcome", label)
    table.insert(0, "scheme", scheme)
    return table


def main():
    data = add_outcomes(add_covariates(prepare(pd.read_parquet(DATA_FILE)))).reset_index(drop=True)
    usable = is_mother(data) & data["EMP"].notna()

    results = []
    for scheme, groups in AGE_SCHEMES.items():
        cutoff = 2 if scheme == "under2" else 3
        column = f"CHILD_AGE_{scheme.upper()}"
        data[column] = data["SC_AGE_YEARS"].apply(child_age_group, cutoff=cutoff)
        CATEGORIES[column] = groups  # register the groups so design_matrix() can use them
        young_column = column + "_0_5"
        data[young_column] = data[column]
        CATEGORIES[young_column] = groups[:2]  # child care item: children 0-5 only

        outcomes = list(OUTCOMES) if scheme == "under2" else HEADLINE
        for outcome in outcomes:
            print(f"{scheme}: {outcome}")
            in_young = data[column] == groups[0]
            results.append(run_comparison(data, usable & in_young, "EMP", outcome,
                                          "1: employment, child " + groups[0].lower(), scheme))
            full_time = data["EMP"] == FULL_TIME
            if outcome == "JOB_CHANGE_CC":
                in_0_5 = data[column].isin(groups[:2])
                results.append(run_comparison(data, usable & full_time & in_0_5, young_column, outcome,
                                              "2: child age, full-time mothers", scheme))
            else:
                results.append(run_comparison(data, usable & full_time, column, outcome,
                                              "2: child age, full-time mothers", scheme))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old_file in OUT_DIR.glob("*.csv"):
        old_file.unlink()
    pd.concat(results, ignore_index=True).to_csv(OUT_DIR / "under2_all_outcomes.csv", index=False)
    print("  under2_all_outcomes.csv")


if __name__ == "__main__":
    main()
