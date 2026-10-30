"""Load NSCH topical files into one analysis-ready table.

Reads the Stata topical files listed in docs/data-acquisition.md, keeps the
variables needed for the research plan, standardizes names to upper case and
stacks the years. No recoding or sample restriction happens here; that is
done in later steps (mother definition, age bands).

Stata extended missing values (.l legitimate skip, .m missing in error,
.n not on this form, .d suppressed, .k don't know; see 2025 NSCH FAQs) are
converted to NaN in the value column, and the missing-value letter is kept in
a companion column named <VAR>__MISS so nonresponse can be told apart from
skips.

Usage (from the repository root):
    .venv/Scripts/python.exe src/nsch.py
"""

from pathlib import Path

import pandas as pd
from pandas.io.stata import StataMissingValue

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "nsch"
PROCESSED_DIR = ROOT / "data" / "processed"

FILES = {
    2023: RAW_DIR / "2023" / "nsch_2023e_topical.dta",
    2024: RAW_DIR / "2024" / "nsch_2024e_topical.dta",
    2025: RAW_DIR / "2025" / "nsch_2025e_topical.dta",
}

# Variables to keep, grouped by inventory category (docs/dataset-inventory.md, Section 2.4).
# T1 = child age 0-5 questionnaire, T2 = 6-11, T3 = 12-17.
VARIABLES = {
    # Survey design: needed for correct weighted estimates and standard errors.
    "design": [
        "HHID",      # Household ID; also the primary sampling unit (PSU)
        "FWC",       # Survey weight for the sampled child
        "FIPSST",    # State FIPS code; also part of the sampling strata
        "STRATUM",   # Sampling stratum within state ("1" or "2A"); text
        "FORMTYPE",  # Questionnaire form: T1 (0-5), T2 (6-11), T3 (12-17); text
        "METRO_YN",  # Lives in a metropolitan area (yes/no)
    ],
    # The sampled child's age and the household's makeup.
    "child_age_family": [
        "SC_AGE_YEARS",  # Sampled child's age in years (0-17)
        "SC_AGE_LT4",    # Child younger than 4 months
        "SC_AGE_LT6",    # Child younger than 6 months
        "SC_AGE_LT9",    # Child younger than 9 months
        "SC_AGE_LT10",   # Child younger than 10 months
        "TOTKIDS_R",     # Number of children in household (1, 2, 3, 4+)
        "TOTAGE_0_5",    # Number of children aged 0-5 in household
        "TOTAGE_6_11",   # Number of children aged 6-11 in household
        "TOTAGE_12_17",  # Number of children aged 12-17 in household
        "AGEPOS4",       # Sampled child's birth order (only, oldest, 2nd, ...)
        "HHCOUNT",       # Number of people living at the address
        "FAMCOUNT",      # Number of household members who are family
        "FAMILY_R",      # Family structure (e.g., two married bio/adoptive parents, single mother)
    ],
    # Adult 1 = the person who filled in the survey (self-reported).
    "adult1": [
        "A1_SEX",         # Sex (1 male, 2 female)
        "A1_RELATION",    # Relationship to child (1 = biological or adoptive parent)
        "A1_AGE",         # Age
        "A1_MARITAL",     # Marital status
        "A1_GRADE",       # Highest education completed
        "A1_EMPLOYED_R",  # Current employment: full-time, part-time, looking, etc. (2023+)
        "A1_MENTHEALTH",  # Rating of own mental/emotional health (excellent ... poor)
        "A1_PHYSHEALTH",  # Rating of own physical health (excellent ... poor)
    ],
    # Adult 2 = a second caregiver, described BY Adult 1 (proxy report).
    "adult2": [
        "A2_SEX",         # Sex
        "A2_RELATION",    # Relationship to child (8 = no second caregiver)
        "A2_AGE",         # Age
        "A2_MARITAL",     # Marital status
        "A2_GRADE",       # Highest education completed
        "A2_EMPLOYED_R",  # Current employment
        "A2_MENTHEALTH",  # Mental/emotional health, as rated by Adult 1
        "A2_PHYSHEALTH",  # Physical health, as rated by Adult 1
    ],
    # Parenting aggravation, emotional support and family resilience.
    "aggravation_support": [
        "K8Q30",      # How well handling day-to-day demands of raising children
        "K8Q31",      # Past month: child much harder to care for than most
        "K8Q32",      # Past month: child does things that really bother you
        "K8Q34",      # Past month: felt angry with this child
        "K8Q35",      # Past 12 months: someone to turn to for emotional support with parenting
        "TALKABOUT",  # Resilience: family talks together about what to do
        "WKTOSOLVE",  # Resilience: family works together to solve problems
        "STRENGTHS",  # Resilience: family knows it has strengths to draw on
        "HOPEFUL",    # Resilience: family stays hopeful in difficult times
    ],
    # Family income, hardship and housing.
    "economic_housing": [
        "FPL_I1", "FPL_I2", "FPL_I3",  # Family income as % of poverty line:
        "FPL_I4", "FPL_I5", "FPL_I6",  # six imputed versions, to be combined
        "FPL_IF",        # Flag: income was imputed
        "ACE1",          # How often hard to cover basics like food or housing
        "FOODSIT",       # Household's ability to afford needed food, past 12 months
        "TENURE",        # Own with mortgage / own free and clear / rent / no rent (2018+)
        "TENURE_IF",     # Flag: tenure was imputed
        "MISSMORTGAGE",  # Past 12 months: unable to pay mortgage or rent on time
        "HOMEEVIC",      # How often worried about eviction or foreclosure
    ],
    # Child sleep and childcare.
    "sleep_childcare": [
        "HOURSLEEP05",  # Child's sleep per 24 hours incl. naps (T1 only, ages 0-5)
        "HOURSLEEP",    # Child's sleep on most weeknights (T2/T3 only, ages 6-17)
        "BEDTIME",      # How often child goes to bed at the same time
        "HOURSOFCARE",  # Weekly hours of non-parental care (T1 only; 2025 only)
        "K6Q27",        # Family member quit/changed job due to childcare problems (T1 only)
    ],
}

# Kept as text rather than numbers (STRATUM: "1"/"2A"; FORMTYPE: "T1"/"T2"/"T3").
STRING_VARIABLES = {"STRATUM", "FORMTYPE"}


def all_variables():
    """Flatten VARIABLES into one list of variable names, in order."""
    names = []
    for group in VARIABLES.values():
        for name in group:
            names.append(name)
    return names


def is_stata_code(value):
    """True if a cell holds a Stata missing code such as .m, .l or .n."""
    return isinstance(value, StataMissingValue)

# Examples:
#   is_stata_code(2)      # False: an ordinary number
#   is_stata_code(".m")   # False: plain text that happens to look like a code
#   is_stata_code(<the .m object pandas created>)   # True


def load_year(year):
    """Read one NSCH year and return the kept variables plus SURVEY_YEAR.

    Variables not fielded in that year are added as empty columns so the
    years stack cleanly. Returns (data, unavailable variables, all column
    names in the file); the full column list is used by load_nsch to find
    variables that are new or dropped compared with the previous year.
    """
    raw = pd.read_stata(FILES[year], convert_categoricals=False, convert_missing=True)
    raw.columns = raw.columns.str.upper()
    all_columns = list(raw.columns)

    keep = all_variables()

    # Note which of our variables this year's file does not have.
    # (Brand-new variables are found in load_nsch, which compares each year's
    # full column list with the previous year's.)
    unavailable = []
    for name in keep:
        if name not in raw.columns:
            unavailable.append(name)

    # Keep only our variables; reindex adds empty columns for the unavailable ones.
    df = raw.reindex(columns=keep)

    for name in keep:
        if name in STRING_VARIABLES:
            df[name] = df[name].astype("string")
            continue

        is_code = df[name].apply(is_stata_code)

        # True if this variable has at least one Stata missing code in this year.
        is_missingStataCode = is_code.any()

        # Companion column with the missing-value letter, e.g. "m" for missing in error.
        if is_missingStataCode:
            letters = df[name].where(is_code).astype(str).str.lstrip(".")
            df[name + "__MISS"] = letters.where(is_code).astype("string")

        # Missing codes become NaN; to_numeric raises an error if any text is left,
        # so a text column missing from STRING_VARIABLES cannot be wiped out silently.
        df[name] = pd.to_numeric(df[name].mask(is_code))

    df["SURVEY_YEAR"] = year
    return df, unavailable, all_columns


def load_nsch(years=None):
    """Load and stack NSCH years (default: every year listed in FILES).

    Returns (data, unavailable, changes):
      unavailable: {year: our variables not in that year's file}
      changes:     {year: {"new": [...], "dropped": [...]}} comparing each
                   year's full file with the previous year's
    """
    if years is None:
        years = sorted(FILES)

    frames = []
    unavailable = {}
    columns_by_year = {}
    for year in years:
        df, missing_vars, all_columns = load_year(year)
        frames.append(df)
        unavailable[year] = missing_vars
        columns_by_year[year] = all_columns

    # Compare each year's full file with the previous year's: which variables
    # are brand new, and which were dropped. Covers every column in the file,
    # not only the ones we keep, so new questions worth adding are visible.
    changes = {}
    previous_year = None
    for year in years:
        if previous_year is not None:
            new = []
            for column in columns_by_year[year]:
                if column not in columns_by_year[previous_year]:
                    new.append(column)
            dropped = []
            for column in columns_by_year[previous_year]:
                if column not in columns_by_year[year]:
                    dropped.append(column)
            changes[year] = {"new": new, "dropped": dropped}
        previous_year = year

    data = pd.concat(frames, ignore_index=True)

    # A __MISS column that exists in only some years gets blanks for the others
    # after concat; set all of them to the same text type.
    for column in data.columns:
        if column.endswith("__MISS"):
            data[column] = data[column].astype("string")

    return data, unavailable, changes


def main():
    data, unavailable, changes = load_nsch()

    # Output file name follows the years loaded, e.g. nsch_2023_2025.parquet.
    first_year = data["SURVEY_YEAR"].min()
    last_year = data["SURVEY_YEAR"].max()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"nsch_{first_year}_{last_year}.parquet"
    data.to_parquet(out_path, index=False)

    print(f"Wrote {out_path.relative_to(ROOT)}: {len(data):,} rows, {data.shape[1]} columns")
    print(data.groupby("SURVEY_YEAR").size().rename("rows").to_string())

    print("\nOur variables not in a year's file:")
    for year, missing_vars in unavailable.items():
        print(f"  {year}: {', '.join(missing_vars) or 'none'}")

    # Variables marked * are in VARIABLES (ones we keep).
    keep = all_variables()
    print("\nChanges from the previous year's file (* = a variable we keep):")
    for year, change in changes.items():
        for kind in ["new", "dropped"]:
            labeled = []
            for column in change[kind]:
                if column in keep:
                    labeled.append(column + "*")
                else:
                    labeled.append(column)
            print(f"  {year} {kind} ({len(labeled)}): {', '.join(labeled) or 'none'}")


if __name__ == "__main__":
    main()
