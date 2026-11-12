"""H8: Do the employment-mental health associations differ between mothers and fathers? (NSCH)

Research plan H8: "Associations between employment and well-being differ
between mothers and fathers." Outcome as in H1: the parent's self-rated
mental/emotional health is fair or poor (A1_MENTHEALTH 4-5).

Parents: Adult 1 is the sampled child's biological or adoptive parent
(A1_RELATION = 1); mothers A1_SEX = 2, fathers A1_SEX = 1.

Employment uses the collapsed scheme (docs/nsch-feasibility.md decision 11):
full-time / part-time / not employed (looking, not looking or retired). About
90% of fathers work full-time, so the main comparison is NOT EMPLOYED vs.
FULL-TIME. Part-time results are shown, with the reliability flags where they
apply.

  Part A (descriptive)  fair/poor % by sex x band x employment, gaps vs.
                        full-time, and the mother-father difference in gaps.
  Part B (adjusted)     the H1 main model (M1 covariates) fitted separately for
                        mothers and fathers; adjusted gaps and their
                        difference ("difference in differences"), overall and
                        by band (with employment x band terms).
  Sensitivity           the same adjusted comparison with retired parents
                        left out.

Model samples use the same complete-case rule for mothers and fathers as
every H1 model (has_covariates in nsch_h1_models.py: marital status, the
parent's own age and physical health answered).

Mothers and fathers are separate domains of the same sample, so the variance
of a difference is computed from the difference of the records'
contributions; this keeps the shared strata in the calculation.

All results are associations, not effects.

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch_h8.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

from nsch_feasibility import DATA_FILE, logit_ci, prepare, reliability_flags
from nsch_h1 import design_se, linearized_share
from nsch_h1_models import (CATEGORIES, IMPUTATIONS, MODELS, add_covariates, combine, fit_imputations,
                            has_covariates, margins, variance_of)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "tables" / "nsch_h8"

EMPLOYMENT = CATEGORIES["EMP3"]
FULL_TIME = EMPLOYMENT[0]
BANDS = CATEGORIES["BAND"]
COVARIATES = ["EMP3"] + MODELS["M1"][1:]  # M1 with the collapsed employment groups


def descriptive(data, parents):
    """Part A: fair/poor % by sex x band x employment, with reliability flags."""
    fair_poor = data["FAIR_POOR"]
    rows = []
    for sex, is_sex in parents.items():
        for band in BANDS:
            for employment in EMPLOYMENT:
                in_domain = is_sex & (data["BAND"] == band) & (data["EMP3"] == employment)
                n = int(in_domain.sum())
                share, z = linearized_share(data, in_domain, fair_poor)
                se = design_se(data, z)
                low, high = logit_ci(share, se)
                rows.append({
                    "parent": sex,
                    "band": band,
                    "employment": employment,
                    "n": n,
                    "fair_poor_pct": round(100 * share, 1),
                    "ci_low_pct": round(100 * low, 1),
                    "ci_high_pct": round(100 * high, 1),
                    "flags": reliability_flags(n, share, (high - low) * 100),
                })
    return pd.DataFrame(rows)


def descriptive_gaps(data, parents):
    """Part A: gap vs. full-time for each sex and band, and mothers' gap minus fathers' gap."""
    fair_poor = data["FAIR_POOR"]
    rows = []
    for band in BANDS:
        for employment in EMPLOYMENT[1:]:
            gaps = {}
            contributions = {}
            for sex, is_sex in parents.items():
                in_band = is_sex & (data["BAND"] == band)
                share_ft, z_ft = linearized_share(data, in_band & (data["EMP3"] == FULL_TIME), fair_poor)
                share, z = linearized_share(data, in_band & (data["EMP3"] == employment), fair_poor)
                gaps[sex] = share - share_ft
                contributions[sex] = z - z_ft
            row = {"band": band, "employment": employment}
            for sex in parents:
                se = design_se(data, contributions[sex])
                row[f"{sex}_gap_pts"] = round(100 * gaps[sex], 1)
                row[f"{sex}_ci"] = f"{100 * (gaps[sex] - 1.96 * se):.1f} to {100 * (gaps[sex] + 1.96 * se):.1f}"
            difference = gaps["mothers"] - gaps["fathers"]
            se = design_se(data, contributions["mothers"] - contributions["fathers"])
            row["difference_pts"] = round(100 * difference, 1)
            row["difference_ci_low"] = round(100 * (difference - 1.96 * se), 1)
            row["difference_ci_high"] = round(100 * (difference + 1.96 * se), 1)
            rows.append(row)
    return pd.DataFrame(rows)


def fit_by_sex(data, domains, interaction=False):
    """Fit the model for each sex on all six imputations."""
    fits = {}
    for sex, domain in domains.items():
        print(f"  fitting {sex}{' (with employment x band)' if interaction else ''}")
        fits[sex] = fit_imputations(data, domain, COVARIATES, interaction)
    return fits


def adjusted_gaps(fits, data, subset=None):
    """Adjusted gaps vs. full-time per sex, and the mother-father difference (Rubin-combined)."""
    per_imputation = []
    for i in range(len(IMPUTATIONS)):
        per_imputation.append({
            "mothers": margins(fits["mothers"][i], data, subset),
            "fathers": margins(fits["fathers"][i], data, subset),
        })

    rows = []
    for employment in EMPLOYMENT[1:]:
        values = {"mothers": [], "fathers": [], "difference": []}
        variances = {"mothers": [], "fathers": [], "difference": []}
        for result in per_imputation:
            contribution = {}
            for sex in ["mothers", "fathers"]:
                level, z = result[sex][employment]
                level_ft, z_ft = result[sex][FULL_TIME]
                values[sex].append(level - level_ft)
                contribution[sex] = z - z_ft
                variances[sex].append(variance_of(contribution[sex], data))
            values["difference"].append(values["mothers"][-1] - values["fathers"][-1])
            variances["difference"].append(variance_of(contribution["mothers"] - contribution["fathers"], data))
        row = {"employment": employment}
        for key in ["mothers", "fathers", "difference"]:
            estimate, low, high = combine(values[key], variances[key], data)
            row[f"{key}_pts"] = round(100 * estimate, 1)
            row[f"{key}_ci_low"] = round(100 * low, 1)
            row[f"{key}_ci_high"] = round(100 * high, 1)
        rows.append(row)
    return pd.DataFrame(rows)


def save(table, name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"  {name}.csv ({len(table)} rows)")


def main():
    data = add_covariates(prepare(pd.read_parquet(DATA_FILE))).reset_index(drop=True)
    is_parent = data["A1_RELATION"] == 1
    usable = is_parent & data["EMP3"].notna() & data["A1_MENTHEALTH"].notna()
    parents = {
        "mothers": usable & (data["A1_SEX"] == 2),
        "fathers": usable & (data["A1_SEX"] == 1),
    }

    print("Part A: descriptive")
    save(descriptive(data, parents), "partA_fair_poor_by_sex")
    save(descriptive_gaps(data, parents), "partA_gaps_by_sex")

    complete = {}
    for sex, domain in parents.items():
        complete[sex] = domain & has_covariates(data)
    sample_rows = []
    for sex in parents:
        sample_rows.append({"parent": sex, "descriptive_n": int(parents[sex].sum()),
                            "model_n": int(complete[sex].sum()),
                            "retired": int((complete[sex] & (data["A1_EMPLOYED_R"] == 6)).sum())})
    save(pd.DataFrame(sample_rows), "sample")

    print("Part B: adjusted (M1 covariates)")
    fits = fit_by_sex(data, complete)
    save(adjusted_gaps(fits, data), "partB_adjusted_gaps")

    fits = fit_by_sex(data, complete, interaction=True)
    by_band = []
    for band in BANDS:
        def in_band(frame, band=band):
            return frame["BAND"] == band
        table = adjusted_gaps(fits, data, subset=in_band)
        table.insert(0, "band", band)
        by_band.append(table)
    save(pd.concat(by_band, ignore_index=True), "partB_adjusted_gaps_by_band")

    print("Sensitivity: retired parents left out")
    not_retired = {}
    for sex, domain in complete.items():
        not_retired[sex] = domain & (data["A1_EMPLOYED_R"] != 6)
    fits = fit_by_sex(data, not_retired)
    save(adjusted_gaps(fits, data), "sensitivity_adjusted_gaps_no_retired")


if __name__ == "__main__":
    main()
