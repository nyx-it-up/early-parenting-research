"""Load the ATUS 2003-2025 multi-year files into one row per respondent.

Reads four files from data/raw/atus/ (see docs/data-acquisition.md):

  atusresp_0325.dat   Respondent file: year, diary day, weights, labor force status
  atusrost_0325.dat   Roster file: age, sex and relationship of household members
  atussum_0325.dat    Activity summary file: minutes per activity on the diary day
  atuscps_0325.dat    ATUS-CPS file: whether each child is a biological, step or
                      adopted child (2007+), from the CPS interview 2-5 months earlier

and writes data/processed/atus_2003_2025.parquet with one row per respondent.

Derived columns
  RESP_SEX, RESP_AGE     respondent's sex and age (roster line 1)
  WEIGHT                 TUFNWGTP, or TU20FWGT for 2020 (the only year without TUFNWGTP)
  N_OWN_CHILDREN         own household children under 18 (roster TERRP = 22, TEAGE < 18)
  YOUNGEST_OWN_AGE       age of the youngest of them (missing if none)
  N_CHILD_BIO_ADOPT      own children the CPS lists as biological or adopted child of the respondent
  N_CHILD_STEP           own children the CPS lists as step-child of the respondent
  N_CHILD_NO_TYPE        own children with no CPS parent type (before 2007, or no link)
  SLEEP, SLEEPLESSNESS   minutes in activities 010101 and 010102
  CHILDCARE_HH           minutes caring for and helping household children (0301xx-0303xx)
  PAID_WORK              minutes working at a job (0501xx)

Variable names and codes are from the Stata label files (.do) in the zips and the
2003-2025 Interview and ATUS-CPS data dictionaries.

Usage (from the repository root):
    .venv/Scripts/python.exe src/atus.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "atus"
OUT_FILE = ROOT / "data" / "processed" / "atus_2003_2025.parquet"

RESPONDENT_COLUMNS = [
    "TUCASEID", "TUYEAR", "TUMONTH", "TUDIARYDAY", "TRHOLIDAY",
    "TUFNWGTP", "TU20FWGT",
    "TELFS", "TRDPFTPT", "TEHRUSLT",
    "TROHHCHILD", "TRNHHCHILD", "TRCHILDNUM", "TRYHHCHILD", "TRSPPRES",
]

CPS_COLUMNS = [
    "TUCASEID", "TULINENO", "PULINENO",
    "PELNMOM", "PEMOMTYP", "PELNDAD", "PEDADTYP",      # 2007-2019 (and part of 2020)
    "PEPAR1", "PEPAR2", "PEPAR1TYP", "PEPAR2TYP",      # 2020+
]

OWN_HOUSEHOLD_CHILD = 22  # TERRP code
BIOLOGICAL, STEP, ADOPTED = 1, 2, 3  # PEMOMTYP / PEDADTYP / PEPAR1TYP / PEPAR2TYP codes


def read_dat(name, columns=None):
    """Read one comma-separated .dat file, keeping TUCASEID as text."""
    return pd.read_csv(RAW / name, usecols=columns, dtype={"TUCASEID": str})


def activity_minutes():
    """Minutes per respondent for the activity groups used in the check."""
    header = pd.read_csv(RAW / "atussum_0325.dat", nrows=0).columns.tolist()
    groups = {
        "SLEEP": ["t010101"],
        "SLEEPLESSNESS": ["t010102"],
        "CHILDCARE_HH": [],
        "PAID_WORK": [],
    }
    for column in header:
        if column.startswith(("t0301", "t0302", "t0303")):
            groups["CHILDCARE_HH"].append(column)
        if column.startswith("t0501"):
            groups["PAID_WORK"].append(column)

    needed = ["TUCASEID"]
    for columns in groups.values():
        needed.extend(columns)
    summary = read_dat("atussum_0325.dat", needed)

    minutes = summary[["TUCASEID"]].copy()
    for name, columns in groups.items():
        minutes[name] = summary[columns].sum(axis=1)
    return minutes


def child_parent_types():
    """Parent type (1 biological, 2 step, 3 adopted) of each child relative to the respondent.

    The respondent is ATUS line 1. In the ATUS-CPS file every person has a CPS
    line number (PULINENO). A child belongs to the respondent if the child's
    mother/father line (PELNMOM/PELNDAD, 2007-2019) or first/second parent line
    (PEPAR1/PEPAR2, 2020+) equals the respondent's PULINENO.
    Returns one row per linked child: TUCASEID, TULINENO, PARENT_TYPE.
    """
    parts = []
    for chunk in pd.read_csv(RAW / "atuscps_0325.dat", usecols=CPS_COLUMNS,
                             dtype={"TUCASEID": str}, chunksize=300_000):
        parts.append(chunk)
    cps = pd.concat(parts, ignore_index=True)

    respondent_line = cps.loc[cps["TULINENO"] == 1, ["TUCASEID", "PULINENO"]]
    respondent_line = respondent_line.rename(columns={"PULINENO": "RESP_PULINENO"})
    cps = cps.merge(respondent_line, on="TUCASEID", how="inner")

    links = [
        ("PELNMOM", "PEMOMTYP"),
        ("PELNDAD", "PEDADTYP"),
        ("PEPAR1", "PEPAR1TYP"),
        ("PEPAR2", "PEPAR2TYP"),
    ]
    found = []
    for line_column, type_column in links:
        is_child_of_respondent = (cps[line_column] == cps["RESP_PULINENO"]) & (cps[type_column] > 0)
        rows = cps.loc[is_child_of_respondent, ["TUCASEID", "TULINENO", type_column]]
        found.append(rows.rename(columns={type_column: "PARENT_TYPE"}))
    types = pd.concat(found, ignore_index=True)
    # A child linked twice (e.g. PELNMOM and PEPAR1 in a 2020 case) keeps the first type.
    return types.drop_duplicates(["TUCASEID", "TULINENO"])


def own_children_summary(roster, types):
    """Per respondent: number of own household children < 18, youngest age, parent types."""
    is_own_child = (roster["TERRP"] == OWN_HOUSEHOLD_CHILD) & (roster["TEAGE"] >= 0) & (roster["TEAGE"] < 18)
    children = roster.loc[is_own_child, ["TUCASEID", "TULINENO", "TEAGE"]]
    children = children.merge(types, on=["TUCASEID", "TULINENO"], how="left")

    children["IS_BIO_ADOPT"] = children["PARENT_TYPE"].isin([BIOLOGICAL, ADOPTED])
    children["IS_STEP"] = children["PARENT_TYPE"] == STEP
    children["NO_TYPE"] = children["PARENT_TYPE"].isna()

    summary = children.groupby("TUCASEID").agg(
        N_OWN_CHILDREN=("TULINENO", "size"),
        YOUNGEST_OWN_AGE=("TEAGE", "min"),
        N_CHILD_BIO_ADOPT=("IS_BIO_ADOPT", "sum"),
        N_CHILD_STEP=("IS_STEP", "sum"),
        N_CHILD_NO_TYPE=("NO_TYPE", "sum"),
    )
    return summary.reset_index()


def main():
    print("Reading respondent file")
    respondents = read_dat("atusresp_0325.dat", RESPONDENT_COLUMNS)

    print("Reading roster file")
    roster = read_dat("atusrost_0325.dat")
    self_rows = roster.loc[roster["TULINENO"] == 1, ["TUCASEID", "TESEX", "TEAGE", "TERRP"]]
    self_rows = self_rows.rename(columns={"TESEX": "RESP_SEX", "TEAGE": "RESP_AGE", "TERRP": "RESP_TERRP"})

    print("Reading ATUS-CPS file (large; read in chunks)")
    types = child_parent_types()

    print("Reading activity summary file")
    minutes = activity_minutes()

    data = respondents.merge(self_rows, on="TUCASEID", how="left")
    data = data.merge(own_children_summary(roster, types), on="TUCASEID", how="left")
    for column in ["N_OWN_CHILDREN", "N_CHILD_BIO_ADOPT", "N_CHILD_STEP", "N_CHILD_NO_TYPE"]:
        data[column] = data[column].fillna(0).astype(int)
    data = data.merge(minutes, on="TUCASEID", how="left")

    # TUFNWGTP is the final weight for 2003-2019 and 2021+; 2020 has only TU20FWGT.
    data["WEIGHT"] = data["TUFNWGTP"].where(data["TUYEAR"] != 2020, data["TU20FWGT"])

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(OUT_FILE, index=False)
    print(f"Wrote {OUT_FILE.relative_to(ROOT)}: {len(data):,} respondents, {data.shape[1]} columns")


if __name__ == "__main__":
    main()
