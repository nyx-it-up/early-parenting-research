"""H1, exploratory: Fairlie decomposition of the fair/poor mental health gap (NSCH).

Question: how much of the gap in fair/poor mental health between mothers who
are not employed and mothers employed full-time is accounted for by measured
differences in income, education, marital status, number of children, age,
child age band and survey year? The rest is "unexplained" (it may reflect
unmeasured differences, or a different relationship within each group).

Method (Fairlie, 2005), for a logistic model:
  1. Fit one logistic regression on both groups together, with the M1
     covariates and an indicator for the employment group, so the group
     difference itself is not absorbed into the covariate coefficients.
  2. Explained gap = average predicted probability using group A's
     characteristics minus that using group B's, both with the same
     coefficients and the group indicator set to 0.
  3. Contribution of each covariate: draw equal-sized weighted samples from
     both groups, pair records by predicted probability, and swap one
     covariate at a time from A's value to its B partner's value. The order of
     swapping affects each contribution, so the order is randomized in every
     replication and contributions are averaged over 100 replications.
  4. Repeated for each of the six income imputations and averaged.

Exploratory: point estimates only. The survey-design variance of the detailed
contributions is not computed, so differences between contributions should
not be over-read.

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch_h1_fairlie.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from nsch_feasibility import DATA_FILE, prepare
from nsch_h1_models import CATEGORIES, IMPUTATIONS, add_covariates, design_matrix, income_group
from survey_logit import fit_logit

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "tables" / "nsch_h1_fairlie"

COVARIATES = ["BAND", "YEAR", "INCOME", "EDUCATION", "MARITAL", "KIDS", "AGE"]
REFERENCE_GROUP = "Employed full-time"
COMPARISONS = ["Not employed, looking for work", "Not employed, not looking (incl. retired)"]
REPLICATIONS = 100
SEED = 2026


def predicted(frame, beta):
    """Predicted probability with the group indicator set to 0 (covariate part only)."""
    X, _ = design_matrix(frame, COVARIATES)
    return 1 / (1 + np.exp(-X @ beta))


def weighted_mean(values, weights):
    return float((values * weights).sum() / weights.sum())


def decompose_once(group_a, group_b, rng):
    """Fairlie decomposition for one imputation. Returns totals and contributions per covariate."""
    both = pd.concat([group_a, group_b], ignore_index=True)
    X, _ = design_matrix(both, COVARIATES)
    indicator = np.r_[np.ones(len(group_a)), np.zeros(len(group_b))]
    X_with_group = np.column_stack([X, indicator])
    beta_all = fit_logit(X_with_group, both["FAIR_POOR"].values, both["WEIGHT_POOLED"].values)
    beta = beta_all[:-1]  # coefficients without the group indicator

    w_a = group_a["WEIGHT_POOLED"].values
    w_b = group_b["WEIGHT_POOLED"].values
    raw_gap = weighted_mean(group_a["FAIR_POOR"].values, w_a) - weighted_mean(group_b["FAIR_POOR"].values, w_b)
    explained = weighted_mean(predicted(group_a, beta), w_a) - weighted_mean(predicted(group_b, beta), w_b)

    contributions = {}
    for variable in COVARIATES:
        contributions[variable] = []

    size = len(group_a)
    for _ in range(REPLICATIONS):
        # Weighted draws of equal size from each group.
        sample_a = group_a.iloc[rng.choice(len(group_a), size, p=w_a / w_a.sum())].reset_index(drop=True)
        sample_b = group_b.iloc[rng.choice(len(group_b), size, p=w_b / w_b.sum())].reset_index(drop=True)
        # Pair records by rank of predicted probability.
        sample_a = sample_a.iloc[np.argsort(predicted(sample_a, beta))].reset_index(drop=True)
        sample_b = sample_b.iloc[np.argsort(predicted(sample_b, beta))].reset_index(drop=True)

        current = sample_a.copy()
        previous_mean = predicted(current, beta).mean()
        order = rng.permutation(COVARIATES)
        for variable in order:
            current[variable] = sample_b[variable].values
            new_mean = predicted(current, beta).mean()
            contributions[variable].append(previous_mean - new_mean)
            previous_mean = new_mean

    averaged = {}
    for variable, values in contributions.items():
        averaged[variable] = float(np.mean(values))
    return raw_gap, explained, averaged


def main():
    data = add_covariates(prepare(pd.read_parquet(DATA_FILE))).reset_index(drop=True)
    is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    complete = (is_mother & data["EMP"].notna() & data["A1_MENTHEALTH"].notna()
                & data["MARITAL"].notna() & data["AGE"].notna() & data["PHYS"].notna())
    rng = np.random.default_rng(SEED)

    totals = []
    details = []
    for comparison in COMPARISONS:
        print(f"Decomposing: {comparison} vs. {REFERENCE_GROUP}")
        gaps, explained_parts = [], []
        per_variable = {}
        for variable in COVARIATES:
            per_variable[variable] = []
        for column in IMPUTATIONS:
            frame = data.loc[complete].copy()
            frame["INCOME"] = frame[column].apply(income_group)
            group_a = frame[frame["EMP"] == comparison].reset_index(drop=True)
            group_b = frame[frame["EMP"] == REFERENCE_GROUP].reset_index(drop=True)
            gap, explained, contributions = decompose_once(group_a, group_b, rng)
            gaps.append(gap)
            explained_parts.append(explained)
            for variable, value in contributions.items():
                per_variable[variable].append(value)

        gap = float(np.mean(gaps))
        explained = float(np.mean(explained_parts))
        totals.append({
            "comparison": f"{comparison} vs. {REFERENCE_GROUP}",
            "n_group": int((complete & (data["EMP"] == comparison)).sum()),
            "n_full_time": int((complete & (data["EMP"] == REFERENCE_GROUP)).sum()),
            "raw_gap_pts": round(100 * gap, 1),
            "explained_pts": round(100 * explained, 1),
            "unexplained_pts": round(100 * (gap - explained), 1),
            "explained_pct_of_gap": round(100 * explained / gap, 0),
        })
        for variable in COVARIATES:
            value = float(np.mean(per_variable[variable]))
            details.append({
                "comparison": f"{comparison} vs. {REFERENCE_GROUP}",
                "covariate": variable,
                "contribution_pts": round(100 * value, 2),
                "pct_of_raw_gap": round(100 * value / gap, 0),
            })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(totals).to_csv(OUT_DIR / "fairlie_totals.csv", index=False)
    pd.DataFrame(details).to_csv(OUT_DIR / "fairlie_contributions.csv", index=False)
    print("  fairlie_totals.csv, fairlie_contributions.csv")


if __name__ == "__main__":
    main()
