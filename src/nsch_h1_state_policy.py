"""State-policy extension: does state paid family leave go with a smaller strain on
full-time working mothers of children under 2? (NSCH, exploratory)

Question: among mothers whose sampled child is under 2, is the difference in
fair/poor mental health (and parenting strain) between full-time and other
mothers different in states where paid family leave (PFL) bonding benefits
were available when the child was born?

Policy data: data/reference/state_paid_family_leave.csv (mandatory state
programs and the date bonding benefits first became payable; sources in the
file). Voluntary programs (NH, VT) are not counted.

Exposure
  PFL_AT_BIRTH   (main) the state's program paid bonding benefits by the
                 child's birth month (birth date taken as the 15th).
  PFL_IN_YEAR    (sensitivity) benefits were payable by July 1 of the survey
                 year, i.e. for the whole fieldwork period.

Groups: employment collapsed to full-time / part-time / not employed, crossed
with PFL (6 groups). The model has the M1 covariates (year, income across six
imputations, education, marital status, number of children, mother's age).

Estimates (predictive margins):
  - adjusted % in each employment group, separately in PFL and non-PFL states;
  - the full-time minus other gaps within PFL states and within non-PFL states;
  - the difference between those gaps. This compares mothers within the same
    states, so it is less affected by other ways the PFL states differ.

Standard errors are clustered by state (51 clusters), because the policy
varies by state. Stratified household-level SEs are shown alongside.

Exploratory and associational: PFL states differ from other states in many
ways (income, prices, other policies), and the comparison is cross-sectional.

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch_h1_state_policy.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from nsch_feasibility import DATA_FILE, prepare
from nsch_h1_models import (CATEGORIES, IMPUTATIONS, MODELS, add_covariates, fit_once, margins,
                            rubin, variance_of)
from nsch_h1_under2 import add_outcomes
from survey_logit import cluster_variance

ROOT = Path(__file__).resolve().parents[1]
POLICY_FILE = ROOT / "data" / "reference" / "state_paid_family_leave.csv"
OUT_DIR = ROOT / "reports" / "tables" / "nsch_h1_state_policy"

OUTCOMES = {
    "FAIR_POOR": "Mental health fair or poor",
    "AGGRAVATION": "Parenting aggravation (usually/always)",
}
EMPLOYMENT = CATEGORIES["EMP3"]
FULL_TIME = EMPLOYMENT[0]
OTHER_COVARIATES = MODELS["M1"][2:]


def program_starts():
    """Start date of bonding benefits for each state with a mandatory program, keyed by FIPS code."""
    policy = pd.read_csv(POLICY_FILE)
    policy = policy[policy["program_type"] == "mandatory"]
    starts = {}
    for _, row in policy.iterrows():
        starts[int(row["fipsst"])] = pd.Timestamp(row["bonding_benefits_start"])
    return starts


def pfl_at_birth(row, starts):
    """True if the state's program paid bonding benefits by the child's birth (15th of the birth month)."""
    state = int(row["FIPSST"])
    if state not in starts or pd.isna(row["BIRTH_YR"]) or pd.isna(row["BIRTH_MO"]):
        return False
    birth = pd.Timestamp(int(row["BIRTH_YR"]), int(row["BIRTH_MO"]), 15)
    return starts[state] <= birth


def pfl_in_year(row, starts):
    """True if the state's program paid bonding benefits by July 1 of the survey year."""
    state = int(row["FIPSST"])
    if state not in starts:
        return False
    return starts[state] <= pd.Timestamp(int(row["SURVEY_YEAR"]), 7, 1)


def combined_group(employment, has_pfl):
    return f"{employment} | {'PFL' if has_pfl else 'no PFL'}"


def estimate(data, domain, exposure_column, outcome):
    """Adjusted %, within-policy gaps and the difference in gaps, combined across imputations."""
    groups = []
    for has_pfl in [False, True]:
        for employment in EMPLOYMENT:
            groups.append(combined_group(employment, has_pfl))
    data["EMP3_PFL"] = [combined_group(e, p) if isinstance(e, str) else None
                        for e, p in zip(data["EMP3"], data[exposure_column])]
    CATEGORIES["EMP3_PFL"] = groups  # reference group: full-time, no PFL

    def pfl_states(frame):
        return frame[exposure_column]

    def other_states(frame):
        return ~frame[exposure_column]

    collected = {}
    for column in IMPUTATIONS:
        fit = fit_once(data, domain, ["EMP3_PFL"] + OTHER_COVARIATES, column, outcome=outcome)
        by_policy = {True: margins(fit, data, pfl_states), False: margins(fit, data, other_states)}
        for has_pfl in [False, True]:
            for employment in EMPLOYMENT:
                key = ("level", has_pfl, employment)
                value, z = by_policy[has_pfl][combined_group(employment, has_pfl)]
                collected.setdefault(key, []).append((value, z))
        for employment in EMPLOYMENT[1:]:
            gap_z = {}
            for has_pfl in [False, True]:
                value_ft, z_ft = by_policy[has_pfl][combined_group(FULL_TIME, has_pfl)]
                value, z = by_policy[has_pfl][combined_group(employment, has_pfl)]
                # Full-time minus the other group: positive = full-time mothers worse off.
                collected.setdefault(("gap", has_pfl, employment), []).append((value_ft - value, z_ft - z))
                gap_z[has_pfl] = (value_ft - value, z_ft - z)
            difference = gap_z[True][0] - gap_z[False][0]
            collected.setdefault(("difference", None, employment), []).append(
                (difference, gap_z[True][1] - gap_z[False][1]))

    rows = []
    for (kind, has_pfl, employment), draws in collected.items():
        values = [draw[0] for draw in draws]
        state_vars = [cluster_variance(draw[1], data["FIPSST"]) for draw in draws]
        household_vars = [variance_of(draw[1], data) for draw in draws]
        value, se_state = rubin(values, state_vars)
        _, se_household = rubin(values, household_vars)
        rows.append({
            "estimate": kind,
            "states": {None: "PFL minus no PFL", True: "PFL", False: "no PFL"}[has_pfl],
            "employment": employment if kind == "level" else f"full-time minus {employment.lower()}",
            "pct_or_pts": round(100 * value, 1),
            "ci_state_clustered": f"{100 * (value - 1.96 * se_state):.1f} to {100 * (value + 1.96 * se_state):.1f}",
            "ci_household_stratified": f"{100 * (value - 1.96 * se_household):.1f} to {100 * (value + 1.96 * se_household):.1f}",
        })
    return pd.DataFrame(rows)


def main():
    data = add_outcomes(add_covariates(prepare(pd.read_parquet(DATA_FILE)))).reset_index(drop=True)
    starts = program_starts()
    data["PFL_AT_BIRTH"] = data.apply(pfl_at_birth, axis=1, starts=starts)
    data["PFL_IN_YEAR"] = data.apply(pfl_in_year, axis=1, starts=starts)

    is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    under_2 = data["SC_AGE_YEARS"] < 2
    good_birth_date = data["BIRTH_YR_F"] == 0
    base = (is_mother & under_2 & data["EMP3"].notna() & data["MARITAL"].notna() & data["AGE"].notna())

    sizes = []
    results = []
    for exposure, extra in [("PFL_AT_BIRTH", good_birth_date), ("PFL_IN_YEAR", None)]:
        for outcome, label in OUTCOMES.items():
            domain = base & data[outcome].notna()
            if extra is not None:
                domain = domain & extra
            print(f"{exposure}: {outcome}")
            try:
                table = estimate(data, domain, exposure, outcome)
            except RuntimeError:
                print("  not estimable (too few cases)")
                continue
            table.insert(0, "outcome", label)
            table.insert(0, "exposure", exposure)
            results.append(table)
            if outcome == "FAIR_POOR":
                counts = data[domain].groupby([exposure, "EMP3"]).size().reset_index(name="n")
                counts.insert(0, "exposure", exposure)
                counts["states"] = int(data.loc[domain & data[exposure], "FIPSST"].nunique())
                sizes.append(counts)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pd.concat(results, ignore_index=True).to_csv(OUT_DIR / "pfl_gaps.csv", index=False)
    pd.concat(sizes, ignore_index=True).to_csv(OUT_DIR / "sample_sizes.csv", index=False)
    print("  pfl_gaps.csv, sample_sizes.csv")


if __name__ == "__main__":
    main()
