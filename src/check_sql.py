"""Check a SQL exercise against the pandas results.

Runs one of the queries in sql/ against data/processed/nsch.duckdb and
compares the result with the numbers already produced by
src/nsch_feasibility.py (reports/tables/nsch_feasibility/). If both agree,
the SQL and the pandas pipeline confirm each other.

Usage (from the repository root, after running src/build_db.py):
    .venv/Scripts/python.exe src/check_sql.py sql/01_mother_flow.sql

The expected output columns for each exercise are listed in sql/README.md.
Column names are compared in lower case; row order does not matter.
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_FILE = ROOT / "data" / "processed" / "nsch.duckdb"
TABLES = ROOT / "reports" / "tables" / "nsch_feasibility"


def expected_mother_flow():
    """Exercise 01: children per year at each step of the mother definition."""
    flow = pd.read_csv(TABLES / "step3_mother_flow.csv")
    flow = flow[(flow["band"] == "All") & (flow["year"] != "Pooled")]
    step_names = {
        "1. All sampled children": "all_children",
        "2. Adult 1 is female": "female_respondent",
        "3. ...and biological/adoptive parent (mother)": "mothers",
    }
    flow["step"] = flow["step"].map(step_names)
    table = flow.pivot(index="year", columns="step", values="n").reset_index()
    table = table.rename(columns={"year": "survey_year"})
    table["survey_year"] = table["survey_year"].astype(int)
    return table[["survey_year", "all_children", "female_respondent", "mothers"]], ["survey_year"]


def expected_sample_sizes():
    """Exercise 02: mothers by primary band x employment label (pooled n)."""
    sizes = pd.read_csv(TABLES / "step4_sizes_mothers_primary.csv")
    table = sizes[["band", "employment", "n_pooled"]].rename(columns={"n_pooled": "n"})
    return table, ["band", "employment"]


def expected_employment_shares():
    """Exercise 03: weighted employment share (%) within each primary band, mothers."""
    shares = pd.read_csv(TABLES / "step4_employment_shares_mothers_primary.csv")
    return shares[["band", "employment", "share_pct"]], ["band", "employment"]


def expected_missing_codes():
    """Exercise 04: count of each Stata missing code per variable, mothers (pooled)."""
    missing = pd.read_csv(TABLES / "step5_missingness.csv")
    missing = missing[missing["year"] == "Pooled"]
    code_columns = {
        "no_valid_response": "m",
        "logical_skip": "l",
        "not_in_universe": "n",
        "suppressed": "d",
    }
    rows = []
    for _, row in missing.iterrows():
        for column, code in code_columns.items():
            if row[column] > 0:
                rows.append({"variable": row["variable"], "code": code, "n": int(row[column])})
    return pd.DataFrame(rows), ["variable", "code"]


EXERCISES = {
    "01_mother_flow.sql": expected_mother_flow,
    "02_sample_sizes.sql": expected_sample_sizes,
    "03_employment_shares.sql": expected_employment_shares,
    "04_missing_codes.sql": expected_missing_codes,
}


def compare(result, expected, keys):
    """Print whether result matches expected; return True if it does."""
    result.columns = result.columns.str.lower()
    missing_columns = []
    for column in expected.columns:
        if column not in result.columns:
            missing_columns.append(column)
    if missing_columns:
        print(f"Missing column(s): {', '.join(missing_columns)}. Got: {', '.join(result.columns)}")
        return False

    result = result[list(expected.columns)]
    merged = expected.merge(result, on=keys, how="outer", suffixes=("_expected", "_yours"), indicator=True)

    problems = merged[merged["_merge"] != "both"]
    value_columns = []
    for column in expected.columns:
        if column not in keys:
            value_columns.append(column)

    both = merged[merged["_merge"] == "both"]
    for column in value_columns:
        # Allow a rounding difference of 0.05 (shares are rounded to 1 decimal).
        difference = (both[column + "_expected"].astype(float) - both[column + "_yours"].astype(float)).abs()
        problems = pd.concat([problems, both[difference > 0.05]])

    if len(problems) == 0:
        print(f"Match: all {len(expected)} rows agree with the pandas results.")
        return True
    print(f"{len(problems)} row(s) differ (left_only = missing from your result, right_only = extra):")
    print(problems.to_string(index=False))
    return False


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sql_path = Path(sys.argv[1])
    if sql_path.name not in EXERCISES:
        print(f"No check defined for {sql_path.name}. Known: {', '.join(EXERCISES)}")
        sys.exit(1)

    query = sql_path.read_text(encoding="utf-8")

    # Stop early if the file still only holds the template comments.
    code_lines = []
    for line in query.splitlines():
        if line.strip() and not line.strip().startswith("--"):
            code_lines.append(line)
    if not code_lines:
        print(f"{sql_path} has no query yet. Write one below the comments, then run this again.")
        sys.exit(1)

    con = duckdb.connect(str(DB_FILE), read_only=True)
    result = con.execute(query).df()
    con.close()

    print(result.to_string(index=False, max_rows=40))
    print()
    expected, keys = EXERCISES[sql_path.name]()
    matched = compare(result, expected, keys)
    sys.exit(0 if matched else 1)


if __name__ == "__main__":
    main()
