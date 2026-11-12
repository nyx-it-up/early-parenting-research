"""Table 1 for the manuscript: characteristics of mothers by employment status (NSCH 2023-2025).

Weighted column percentages (FWC / 3) and unweighted n for the H1 model sample
(mothers with employment, mental health, marital status and age answers).
Income-to-poverty groups are averaged across the six imputations (FPL_I1-I6).

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch_table1.py
"""

from pathlib import Path

import pandas as pd

from nsch_feasibility import DATA_FILE, prepare
from nsch_h1_models import CATEGORIES, IMPUTATIONS, add_covariates, income_group

ROOT = Path(__file__).resolve().parents[1]
OUT_FILE = ROOT / "reports" / "tables" / "manuscript" / "table1_characteristics.csv"

ROWS = {
    "BAND": "Sampled child's age (years)",
    "AGE": "Mother's age (years)",
    "MARITAL": "Marital status",
    "EDUCATION": "Education",
    "KIDS": "Children in household",
    "INCOME": "Family income (% of federal poverty level)",
}


def weighted_percent(frame, column, category):
    weights = frame["WEIGHT_POOLED"]
    return 100 * weights[frame[column] == category].sum() / weights.sum()


def main():
    data = add_covariates(prepare(pd.read_parquet(DATA_FILE)))
    is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    sample = data[is_mother & data["EMP"].notna() & data["A1_MENTHEALTH"].notna()
                  & data["MARITAL"].notna() & data["AGE"].notna()].copy()

    groups = ["All mothers"] + CATEGORIES["EMP"]
    rows = [{"characteristic": "Unweighted n", "category": ""}]
    for group in groups:
        in_group = sample if group == "All mothers" else sample[sample["EMP"] == group]
        rows[0][group] = f"{len(in_group):,}"

    for variable, label in ROWS.items():
        categories = CATEGORIES[variable]
        if variable == "AGE":
            categories = ["18-24", "25-34", "35-44", "45+"]
        if variable == "INCOME":
            categories = ["<100% FPL", "100-199% FPL", "200-399% FPL", "400%+ FPL"]
        if variable == "EDUCATION":
            categories = ["High school or less", "Some college, vocational or associate",
                          "Bachelor's degree", "Graduate degree"]
        for category in categories:
            row = {"characteristic": label, "category": category}
            for group in groups:
                in_group = sample if group == "All mothers" else sample[sample["EMP"] == group]
                if variable == "INCOME":
                    values = []
                    for column in IMPUTATIONS:
                        frame = in_group.copy()
                        frame["INCOME"] = frame[column].apply(income_group)
                        values.append(weighted_percent(frame, "INCOME", category))
                    row[group] = f"{sum(values) / len(values):.1f}"
                else:
                    row[group] = f"{weighted_percent(in_group, variable, category):.1f}"
            rows.append(row)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT_FILE, index=False)
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
