"""H1, exploratory: both ends of the mental health scale (NSCH).

Compares mothers' "excellent or very good" mental health (A1_MENTHEALTH 1-2)
with "fair or poor" (4-5) across employment groups, so the story covers
flourishing as well as struggling. Same sample, covariates (M1), imputations
and design-based estimation as src/nsch_h1_models.py.

Output: reports/tables/nsch_h1_positive/both_ends.csv
  outcome, employment, adjusted %, 95% CI, gap vs. full-time and its CI.

Exploratory; associations only.

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch_h1_positive.py
"""

from pathlib import Path

import pandas as pd

from nsch_feasibility import DATA_FILE, prepare
from nsch_h1_models import IMPUTATIONS, MODELS, add_covariates, combine_margins, fit_once

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "tables" / "nsch_h1_positive"

OUTCOMES = {
    "EXC_VG": "Excellent or very good",
    "FAIR_POOR": "Fair or poor",
}


def main():
    data = add_covariates(prepare(pd.read_parquet(DATA_FILE))).reset_index(drop=True)
    data["EXC_VG"] = (data["A1_MENTHEALTH"] <= 2).astype(float)
    is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    complete = (is_mother & data["EMP"].notna() & data["A1_MENTHEALTH"].notna()
                & data["MARITAL"].notna() & data["AGE"].notna() & data["PHYS"].notna())

    tables = []
    for outcome, label in OUTCOMES.items():
        print(f"Fitting M1 for {label}")
        fits = [fit_once(data, complete, MODELS["M1"], column, outcome=outcome) for column in IMPUTATIONS]
        table = combine_margins(fits, data)
        table.insert(0, "outcome", label)
        tables.append(table)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = pd.concat(tables, ignore_index=True)
    result.to_csv(OUT_DIR / "both_ends.csv", index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
