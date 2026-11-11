"""H1, second pass: adjusted logistic regression of mothers' fair/poor mental health (NSCH).

Builds on src/nsch_h1.py (same sample, outcome and employment groups) and adds
survey-weighted logistic regression with design-based standard errors
(src/survey_logit.py). Income is multiply imputed in NSCH (FPL_I1-FPL_I6), so
every model is fitted six times and combined with Rubin's rules.

Models (all on the same complete-case sample):
  M0  employment + child age band + survey year
  M1  M0 + income, education, marital status, number of children, mother's age
  M2  M1 + mother's physical health (sensitivity: health may be a cause or a
      consequence of both employment and mental health)
  M1x M1 + employment x child age band (does the employment gap differ by band?)

Outputs (reports/tables/nsch_h1_models/):
  odds_ratios_<model>.csv        odds ratios with 95% CIs (appendix)
  adjusted_percentages.csv       predicted % fair/poor by employment group, M0-M2
  adjusted_gaps.csv              percentage-point gaps vs. full-time, M0-M2
  adjusted_gaps_by_band.csv      gaps vs. full-time within each band, from M1x
  interaction_test.csv           Wald test of the employment x band terms
  sample.csv                     sample size and exclusions

Exploratory (src/nsch_h1_fairlie.py): Fairlie decomposition of the gap
between "not employed, looking" and full-time mothers.

All results are associations. Nothing here estimates an effect of employment.

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch_h1_models.py
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from nsch_feasibility import DATA_FILE, prepare
from nsch_h1 import EMPLOYMENT_4_LABELS, employment_4
from survey_logit import (coefficient_influence, design_covariance, fit_logit,
                          predictive_margin, rubin)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "tables" / "nsch_h1_models"
IMPUTATIONS = ["FPL_I1", "FPL_I2", "FPL_I3", "FPL_I4", "FPL_I5", "FPL_I6"]

# Covariate groupings. Codes are from the 2023-2025 Stata label files (.do),
# identical in all three years. The first category of each is the reference.
CATEGORIES = {
    "EMP": ["Employed full-time", "Employed part-time",
            "Not employed, looking for work", "Not employed, not looking (incl. retired)"],
    "BAND": ["0-5", "6-11", "12-17"],
    "YEAR": ["2023", "2024", "2025"],
    "INCOME": ["400%+ FPL", "<100% FPL", "100-199% FPL", "200-399% FPL"],
    "EDUCATION": ["Bachelor's degree", "High school or less", "Some college, vocational or associate",
                  "Graduate degree"],
    "MARITAL": ["Married", "Living with a partner", "Never married", "Divorced, separated or widowed"],
    "KIDS": ["1 child", "2 children", "3 children", "4+ children"],
    "AGE": ["35-44", "18-24", "25-34", "45+"],
    "PHYS": ["Excellent or very good", "Good", "Fair or poor"],
}

MODELS = {
    "M0": ["EMP", "BAND", "YEAR"],
    "M1": ["EMP", "BAND", "YEAR", "INCOME", "EDUCATION", "MARITAL", "KIDS", "AGE"],
    "M2": ["EMP", "BAND", "YEAR", "INCOME", "EDUCATION", "MARITAL", "KIDS", "AGE", "PHYS"],
}


def income_group(fpl):
    """Income-to-poverty ratio (FPL_I*, percent of the federal poverty level) in four groups."""
    if fpl < 100:
        return "<100% FPL"
    if fpl < 200:
        return "100-199% FPL"
    if fpl < 400:
        return "200-399% FPL"
    return "400%+ FPL"


def education_group(code):
    """A1_GRADE: 1-3 high school or less; 4-6 vocational/some college/associate; 7 bachelor's; 8-9 graduate."""
    if code <= 3:
        return "High school or less"
    if code <= 6:
        return "Some college, vocational or associate"
    if code == 7:
        return "Bachelor's degree"
    return "Graduate degree"


def marital_group(code):
    """A1_MARITAL: 1 married; 2 living with a partner; 3 never married; 4-6 divorced/separated/widowed."""
    if pd.isna(code):
        return None
    if code == 1:
        return "Married"
    if code == 2:
        return "Living with a partner"
    if code == 3:
        return "Never married"
    return "Divorced, separated or widowed"


def kids_group(code):
    """TOTKIDS_R: 1, 2, 3, 4+ children in the household."""
    return CATEGORIES["KIDS"][int(code) - 1]


def age_group(age):
    """Mother's age (A1_AGE) in four groups."""
    if pd.isna(age):
        return None
    if age < 25:
        return "18-24"
    if age < 35:
        return "25-34"
    if age < 45:
        return "35-44"
    return "45+"


def health_group(code):
    """A1_PHYSHEALTH: 1-2 excellent/very good; 3 good; 4-5 fair/poor."""
    if pd.isna(code):
        return None
    if code <= 2:
        return "Excellent or very good"
    if code == 3:
        return "Good"
    return "Fair or poor"


def add_covariates(data):
    """Add the grouped covariates (income is added per imputation in design_matrix)."""
    data["EMPLOYMENT_4"] = data["A1_EMPLOYED_R"].apply(employment_4)
    employment_names = {}
    for code, label in EMPLOYMENT_4_LABELS.items():
        employment_names[code] = label
    data["EMP"] = data["EMPLOYMENT_4"].map(employment_names)
    data["YEAR"] = data["SURVEY_YEAR"].astype(str)
    data["EDUCATION"] = data["A1_GRADE"].apply(education_group)
    data["MARITAL"] = data["A1_MARITAL"].apply(marital_group)
    data["KIDS"] = data["TOTKIDS_R"].apply(kids_group)
    data["AGE"] = data["A1_AGE"].apply(age_group)
    data["PHYS"] = data["A1_PHYSHEALTH"].apply(health_group)
    data["FAIR_POOR"] = data["A1_MENTHEALTH"].isin([4, 5]).astype(float)
    return data


def design_matrix(frame, variables, interaction=False):
    """Intercept + one 0/1 column per non-reference category of each variable.

    With interaction=True, adds employment x band columns.
    Returns (array, list of column names).
    """
    columns = {"Intercept": np.ones(len(frame))}
    for variable in variables:
        for category in CATEGORIES[variable][1:]:
            columns[f"{variable}: {category}"] = (frame[variable] == category).astype(float).values
    if interaction:
        for employment in CATEGORIES["EMP"][1:]:
            for band in CATEGORIES["BAND"][1:]:
                columns[f"EMP x BAND: {employment} x {band}"] = (
                    (frame["EMP"] == employment) & (frame["BAND"] == band)).astype(float).values
    names = list(columns.keys())
    return np.column_stack([columns[name] for name in names]), names


def set_employment(frame, employment):
    """Copy of frame with every record's employment set to one group (for predictive margins)."""
    changed = frame.copy()
    changed["EMP"] = employment
    return changed


def fit_once(data, domain, variables, income_column, interaction=False):
    """Fit one model on one imputation. Returns a dict with everything later steps need."""
    frame = data.loc[domain].copy()
    frame["INCOME"] = frame[income_column].apply(income_group)
    X, names = design_matrix(frame, variables, interaction)
    y = frame["FAIR_POOR"].values
    w = frame["WEIGHT_POOLED"].values
    beta = fit_logit(X, y, w)

    # Influence of every record in the FILE (zeros outside the domain).
    influence = np.zeros((len(data), len(beta)))
    domain_rows = np.flatnonzero(domain.values)
    influence[domain_rows] = coefficient_influence(X, y, w, beta)
    covariance = design_covariance(influence, data["DESIGN_STRATUM"])
    return {"frame": frame, "names": names, "beta": beta, "influence": influence,
            "covariance": covariance, "w": w, "domain_rows": domain_rows,
            "variables": variables, "interaction": interaction}


def margins(fit, data, subset=None):
    """Predictive margin and contributions for each employment group (optionally within a subset)."""
    frame = fit["frame"]
    w = fit["w"]
    rows = fit["domain_rows"]
    if subset is not None:
        keep = subset(frame).values
        frame = frame[keep]
        w = w[keep]
        rows = rows[keep]
    results = {}
    for employment in CATEGORIES["EMP"]:
        X, _ = design_matrix(set_employment(frame, employment), fit["variables"], fit["interaction"])
        results[employment] = predictive_margin(X, w, fit["beta"], fit["influence"], rows, len(data))
    return results


def variance_of(contributions, data):
    """Design-based variance of one estimate from its per-record contributions."""
    return float(design_covariance(contributions[:, None], data["DESIGN_STRATUM"])[0, 0])


def combine_margins(fits, data, subset=None):
    """Adjusted % and gaps vs. full-time, combined across imputations."""
    per_imputation = []
    for fit in fits:
        per_imputation.append(margins(fit, data, subset))

    rows = []
    reference = CATEGORIES["EMP"][0]
    for employment in CATEGORIES["EMP"]:
        levels, level_vars, gaps, gap_vars = [], [], [], []
        for result in per_imputation:
            level, z = result[employment]
            ref_level, z_ref = result[reference]
            levels.append(level)
            level_vars.append(variance_of(z, data))
            gaps.append(level - ref_level)
            gap_vars.append(variance_of(z - z_ref, data))
        level, level_se = rubin(levels, level_vars)
        gap, gap_se = rubin(gaps, gap_vars)
        rows.append({
            "employment": employment,
            "adjusted_pct": round(100 * level, 1),
            "ci_low_pct": round(100 * (level - 1.96 * level_se), 1),
            "ci_high_pct": round(100 * (level + 1.96 * level_se), 1),
            "gap_vs_full_time_pts": round(100 * gap, 1) if employment != reference else None,
            "gap_ci_low_pts": round(100 * (gap - 1.96 * gap_se), 1) if employment != reference else None,
            "gap_ci_high_pts": round(100 * (gap + 1.96 * gap_se), 1) if employment != reference else None,
        })
    return pd.DataFrame(rows)


def combine_coefficients(fits):
    """Rubin's rules for the whole coefficient vector. Returns (beta, covariance, names)."""
    m = len(fits)
    betas = np.array([fit["beta"] for fit in fits])
    within = np.mean([fit["covariance"] for fit in fits], axis=0)
    between = np.cov(betas, rowvar=False, ddof=1)
    total = within + (1 + 1 / m) * between
    return betas.mean(axis=0), total, fits[0]["names"]


def odds_ratio_table(fits):
    beta, covariance, names = combine_coefficients(fits)
    se = np.sqrt(np.diag(covariance))
    rows = []
    for i, name in enumerate(names):
        if name == "Intercept":
            continue
        rows.append({
            "term": name,
            "odds_ratio": round(math.exp(beta[i]), 2),
            "ci_low": round(math.exp(beta[i] - 1.96 * se[i]), 2),
            "ci_high": round(math.exp(beta[i] + 1.96 * se[i]), 2),
            "p_value": round(2 * stats.norm.sf(abs(beta[i] / se[i])), 4),
        })
    return pd.DataFrame(rows)


def interaction_test(fits):
    """Wald chi-square test that all employment x band terms are zero (on Rubin-combined estimates)."""
    beta, covariance, names = combine_coefficients(fits)
    index = [i for i, name in enumerate(names) if name.startswith("EMP x BAND")]
    b = beta[index]
    V = covariance[np.ix_(index, index)]
    chi2 = float(b @ np.linalg.solve(V, b))
    return pd.DataFrame([{"terms": len(index), "chi_square": round(chi2, 2),
                          "p_value": round(stats.chi2.sf(chi2, len(index)), 4)}])


def save(table, name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"  {name}.csv ({len(table)} rows)")


def main():
    data = add_covariates(prepare(pd.read_parquet(DATA_FILE))).reset_index(drop=True)
    is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    in_h1 = is_mother & data["EMP"].notna() & data["A1_MENTHEALTH"].notna()
    complete = in_h1 & data["MARITAL"].notna() & data["AGE"].notna() & data["PHYS"].notna()

    save(pd.DataFrame([
        {"step": "H1 sample (nsch_h1.py)", "n": int(in_h1.sum())},
        {"step": "Missing marital status", "n": int((in_h1 & data["MARITAL"].isna()).sum())},
        {"step": "Missing mother's age", "n": int((in_h1 & data["AGE"].isna()).sum())},
        {"step": "Missing physical health", "n": int((in_h1 & data["PHYS"].isna()).sum())},
        {"step": "Model sample (complete cases, same for all models)", "n": int(complete.sum())},
    ]), "sample")

    percentages = []
    for model, variables in MODELS.items():
        print(f"Fitting {model} on {len(IMPUTATIONS)} imputations")
        fits = []
        for column in IMPUTATIONS:
            fits.append(fit_once(data, complete, variables, column))
        save(odds_ratio_table(fits), f"odds_ratios_{model}")
        table = combine_margins(fits, data)
        table.insert(0, "model", model)
        percentages.append(table)
    combined = pd.concat(percentages, ignore_index=True)
    save(combined[["model", "employment", "adjusted_pct", "ci_low_pct", "ci_high_pct"]], "adjusted_percentages")
    gaps = combined[combined["gap_vs_full_time_pts"].notna()]
    save(gaps[["model", "employment", "gap_vs_full_time_pts", "gap_ci_low_pts", "gap_ci_high_pts"]], "adjusted_gaps")

    print("Fitting M1x (employment x band)")
    fits = []
    for column in IMPUTATIONS:
        fits.append(fit_once(data, complete, MODELS["M1"], column, interaction=True))
    save(odds_ratio_table(fits), "odds_ratios_M1x")
    save(interaction_test(fits), "interaction_test")
    by_band = []
    for band in CATEGORIES["BAND"]:
        def in_band(frame, band=band):
            return frame["BAND"] == band
        table = combine_margins(fits, data, subset=in_band)
        table.insert(0, "band", band)
        by_band.append(table)
    save(pd.concat(by_band, ignore_index=True), "adjusted_gaps_by_band")


if __name__ == "__main__":
    main()
