"""NSCH feasibility check: mother definition, sample sizes and missing data.

Reads the processed file written by src/nsch.py and runs research plan
Section 11, step 5 for NSCH:

  Step 3  Define "mother" and count the children dropped at each filter.
  Step 4  Unweighted and weighted sample sizes by age band x employment
          status, checked against the NSCH reliability rules. Run for
          mothers and, as a comparison group, fathers. Also by the
          youngest child's age band, the number of children aged 0-5, and
          a "baby plus another young child" group.
  Step 5  Missing data among mothers, using the <VAR>__MISS columns.

Results are written as CSV files to reports/tables/nsch_feasibility/ and
summarized in docs/nsch-feasibility.md. Nothing here is a finding about
mothers' well-being; the numbers only say which comparisons the data can
support.

Usage (from the repository root, after running src/nsch.py):
    .venv/Scripts/python.exe src/nsch_feasibility.py
"""

import math
from pathlib import Path

import pandas as pd

from nsch import VARIABLES

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "nsch_2023_2025.parquet"
OUT_DIR = ROOT / "reports" / "tables" / "nsch_feasibility"

# Value labels, copied from the 2023-2025 Stata label files (.do); identical in all three years.
RELATION_LABELS = {
    1: "Biological or adoptive parent",
    2: "Step-parent",
    3: "Grandparent",
    4: "Foster parent",
    6: "Other relative",
    7: "Other non-relative",
}
EMPLOYMENT_LABELS = {
    1: "Employed full-time",
    2: "Employed part-time",
    3: "Working without pay",
    4: "Not employed, looking for work",
    5: "Not employed, not looking for work",
    6: "Retired",
}

# Collapsed employment for the mothers vs fathers comparison: few fathers are
# part-time or not employed, so the not-employed groups (codes 4, 5, 6) are
# combined. "Working without pay" (3) is left out.
EMPLOYMENT_3_CODES = {1: 1, 2: 2, 4: 3, 5: 3, 6: 3}
EMPLOYMENT_3_LABELS = {
    1: "Employed full-time",
    2: "Employed part-time",
    3: "Not employed (looking, not looking or retired)",
}

# NSCH reliability guidance (2025 NSCH Methodology Report, "Estimation,
# Hypothesis Testing, and Data Use Guidelines"): only present estimates with
# an unweighted denominator of 30 or more; flag estimates whose 95% CI is wider
# than 20 percentage points or wider than 1.2 times the estimate (the report
# notes this is about the same as a relative standard error above 30%).
MIN_N = 30
MAX_CI_WIDTH = 20.0
MAX_RELATIVE_CI_WIDTH = 1.2


def primary_band(age):
    """Primary age band, matching the NSCH forms T1/T2/T3."""
    if age <= 5:
        return "0-5"
    if age <= 11:
        return "6-11"
    return "12-17"


def secondary_band(age):
    """Secondary age band: splits early childhood into 0-2 and 3-5."""
    if age <= 2:
        return "0-2"
    if age <= 5:
        return "3-5"
    if age <= 11:
        return "6-11"
    return "12-17"


def youngest_band(row):
    """Age band of the YOUNGEST child in the household, from the TOTAGE counts.

    The public file has only counts of children per band (which include the
    sampled child), not each child's exact age. So this can say "there is a
    child aged 0-5" but not "there is a child under 3".
    """
    if row["TOTAGE_0_5"] > 0:
        return "0-5"
    if row["TOTAGE_6_11"] > 0:
        return "6-11"
    return "12-17"


def young_children_group(count):
    """Number of children aged 0-5 in the household, grouped."""
    if count == 0:
        return "No child 0-5"
    if count == 1:
        return "1 child 0-5"
    return "2+ children 0-5"


def baby_group(row):
    """Is the sampled child under 3, and is there another child aged 0-5?

    The closest the public file gets to "two children under 3": the sampled
    child's exact age is known, but other children are only counted by band.
    TOTAGE_0_5 includes the sampled child, so 2+ means at least one more
    child aged 0-5 (who may be 0, 1, 2, 3, 4 or 5).
    """
    if row["SC_AGE_YEARS"] > 2:
        return "Sampled child 3+"
    if row["TOTAGE_0_5"] >= 2:
        return "Child 0-2 + another 0-5"
    return "Child 0-2, no other 0-5"


def employment_3(code):
    """Collapsed employment code (1-3), or missing for no answer / working without pay."""
    if pd.isna(code) or int(code) not in EMPLOYMENT_3_CODES:
        return float("nan")
    return EMPLOYMENT_3_CODES[int(code)]


def employment_label(code):
    """Employment label, or 'Missing' when there is no valid answer."""
    if pd.isna(code):
        return "Missing"
    return EMPLOYMENT_LABELS[int(code)]


def prepare(data):
    """Add age bands, design strata and the pooled weight."""
    number_of_years = data["SURVEY_YEAR"].nunique()

    data["BAND"] = data["SC_AGE_YEARS"].apply(primary_band)
    data["BAND_SECONDARY"] = data["SC_AGE_YEARS"].apply(secondary_band)
    data["BAND_YOUNGEST"] = data.apply(youngest_band, axis=1)
    data["YOUNG_CHILDREN"] = data["TOTAGE_0_5"].apply(young_children_group)
    data["BABY_GROUP"] = data.apply(baby_group, axis=1)
    data["EMPLOYMENT"] = data["A1_EMPLOYED_R"].apply(employment_label)
    data["EMPLOYMENT_3"] = data["A1_EMPLOYED_R"].apply(employment_3)

    # Pooled weight: divide by the number of years (NSCH multi-year guidance).
    data["WEIGHT_POOLED"] = data["FWC"] / number_of_years

    # Each year is a separate sample, so year is part of the stratum.
    data["DESIGN_STRATUM"] = (
        data["SURVEY_YEAR"].astype(str) + "_"
        + data["FIPSST"].astype(str) + "_"
        + data["STRATUM"].astype(str)
    )
    return data


def weighted_share(data, in_domain, has_trait, weight="WEIGHT_POOLED"):
    """Weighted share of has_trait among records in in_domain, with its standard error.

    The standard error uses Taylor linearization for a ratio, with strata
    DESIGN_STRATUM and each household (HHID) as its own primary sampling unit,
    as the NSCH design specifies. Records outside the domain stay in the
    calculation with zero weight, which is the correct way to estimate a
    subgroup ("domain") from a survey without deleting records.

    in_domain and has_trait are True/False Series aligned with data.
    Returns (share, standard_error).
    """
    w = data[weight] * in_domain
    total = w.sum()
    share = (w * has_trait).sum() / total

    # Each record's contribution to the estimate (zero outside the domain).
    z = w * (has_trait - share) / total

    # Variance: within each stratum, spread of contributions around the stratum mean.
    stratum_mean = z.groupby(data["DESIGN_STRATUM"]).transform("mean")
    squared_deviation = (z - stratum_mean) ** 2
    stratum_sum = squared_deviation.groupby(data["DESIGN_STRATUM"]).sum()
    stratum_n = data.groupby("DESIGN_STRATUM").size()
    variance = (stratum_n / (stratum_n - 1) * stratum_sum).sum()

    return share, variance ** 0.5


def logit_ci(share, se):
    """95% confidence interval for a share, computed on the logit (log-odds) scale.

    A plain share +/- 1.96 SE interval is symmetric, so for a small share with
    a large SE its lower end can fall below 0%. Working on the log-odds scale,
    log(p / (1 - p)), and converting back keeps both ends between 0 and 1 and
    makes the interval lopsided near 0, as it should be.
    Returns (low, high) as shares between 0 and 1.
    """
    if share <= 0 or share >= 1:
        return float("nan"), float("nan")
    logit = math.log(share / (1 - share))
    logit_se = se / (share * (1 - share))  # SE on the log-odds scale (delta method)
    low = logit - 1.96 * logit_se
    high = logit + 1.96 * logit_se
    return 1 / (1 + math.exp(-low)), 1 / (1 + math.exp(-high))


def reliability_flags(n, share, ci_width):
    """Return the NSCH reliability rule(s) an estimate breaks, as text ('' if none).

    ci_width is in percentage points; share is between 0 and 1.
    """
    flags = []
    if n < MIN_N:
        flags.append(f"n<{MIN_N}")
    if ci_width > MAX_CI_WIDTH:
        flags.append("CI>20pts")
    if ci_width > MAX_RELATIVE_CI_WIDTH * share * 100:
        flags.append("CI>1.2x estimate")
    return "; ".join(flags)


def precision_row(data, in_domain, has_trait):
    """Share, logit 95% CI, RSE and reliability flags for one domain."""
    n = int(in_domain.sum())
    share, se = weighted_share(data, in_domain, has_trait)
    rse = se / share if share > 0 else float("nan")
    low, high = logit_ci(share, se)
    ci_width = (high - low) * 100
    return {
        "n": n,
        "share_pct": round(share * 100, 1),
        "ci_low_pct": round(low * 100, 1),
        "ci_high_pct": round(high * 100, 1),
        "ci_width_pts": round(ci_width, 1),
        "rse_pct": round(rse * 100, 1),
        "flags": reliability_flags(n, share, ci_width),
    }


# ---------------------------------------------------------------------------
# Step 3: who counts as a mother
# ---------------------------------------------------------------------------

def mother_flow(data):
    """Children remaining after each filter, by year and primary band.

    Filter 1: Adult 1 (the respondent) is female (A1_SEX = 2).
    Filter 2: Adult 1 is the child's biological or adoptive parent (A1_RELATION = 1).
    """
    is_female = data["A1_SEX"] == 2
    is_parent = data["A1_RELATION"] == 1
    steps = {
        "1. All sampled children": pd.Series(True, index=data.index),
        "2. Adult 1 is female": is_female,
        "3. ...and biological/adoptive parent (mother)": is_female & is_parent,
    }

    rows = []
    for step, keep in steps.items():
        for year in sorted(data["SURVEY_YEAR"].unique()):
            for band in ["0-5", "6-11", "12-17", "All"]:
                in_cell = keep & (data["SURVEY_YEAR"] == year)
                if band != "All":
                    in_cell = in_cell & (data["BAND"] == band)
                rows.append({"step": step, "year": year, "band": band, "n": int(in_cell.sum())})
    flow = pd.DataFrame(rows)

    # Add pooled totals across years.
    pooled = flow.groupby(["step", "band"], as_index=False)["n"].sum()
    pooled["year"] = "Pooled"
    return pd.concat([flow, pooled], ignore_index=True)


def exclusion_reasons(data):
    """Why children were dropped: Adult 1's sex and relationship, pooled years."""
    rows = []

    sex_labels = {1: "Adult 1 male", 2: "Adult 1 female"}
    for code, label in sex_labels.items():
        rows.append({"filter": "sex", "reason": label, "n": int((data["A1_SEX"] == code).sum())})
    rows.append({"filter": "sex", "reason": "Adult 1 sex missing", "n": int(data["A1_SEX"].isna().sum())})

    female = data[data["A1_SEX"] == 2]
    for code, label in RELATION_LABELS.items():
        n = int((female["A1_RELATION"] == code).sum())
        rows.append({"filter": "relation (female Adult 1 only)", "reason": label, "n": n})
    rows.append({
        "filter": "relation (female Adult 1 only)",
        "reason": "Relationship missing",
        "n": int(female["A1_RELATION"].isna().sum()),
    })
    return pd.DataFrame(rows)


def adult2_mothers(data):
    """Mothers who appear only as Adult 2 (described by proxy), by primary band.

    These are excluded from the main sample because their mental health and
    employment are reported by someone else (usually the father).
    """
    a1_is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    a2_is_mother = (data["A2_SEX"] == 2) & (data["A2_RELATION"] == 1)
    only_a2 = a2_is_mother & ~a1_is_mother

    rows = []
    for band in ["0-5", "6-11", "12-17"]:
        in_band = data["BAND"] == band
        rows.append({
            "band": band,
            "mother_is_adult1": int((a1_is_mother & in_band).sum()),
            "mother_only_adult2": int((only_a2 & in_band).sum()),
            "no_mother_identified": int((~a1_is_mother & ~a2_is_mother & in_band).sum()),
        })
    return pd.DataFrame(rows)


def employment_adult1_vs_adult2(data):
    """Employment mix of self-reporting mothers vs proxy-reported Adult 2 mothers.

    Shows whether dropping Adult 2 mothers changes the employment picture.
    Weighted shares among valid answers, pooled years.
    """
    a1_is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    only_a2 = (data["A2_SEX"] == 2) & (data["A2_RELATION"] == 1) & ~a1_is_mother

    groups = {
        "Adult 1 mother (self-report)": (a1_is_mother, "A1_EMPLOYED_R"),
        "Adult 2 mother (proxy report)": (only_a2, "A2_EMPLOYED_R"),
    }
    rows = []
    for group, (is_group, column) in groups.items():
        for band in ["0-5", "6-11", "12-17"]:
            in_domain = is_group & (data["BAND"] == band) & data[column].notna()
            for code, label in EMPLOYMENT_LABELS.items():
                row = {"group": group, "band": band, "employment": label}
                row.update(precision_row(data, in_domain, data[column] == code))
                rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Step 4: sample sizes and reliability
# ---------------------------------------------------------------------------

def sample_sizes(parents, band_column):
    """Unweighted n (per year and pooled) and weighted N by band x employment.

    parents is the subset of records for one parent group (mothers or fathers).
    """
    rows = []
    bands = list(parents[band_column].unique())
    bands.sort(key=band_sort_key)
    employment_values = list(EMPLOYMENT_LABELS.values()) + ["Missing"]

    for band in bands:
        for employment in employment_values:
            in_cell = (parents[band_column] == band) & (parents["EMPLOYMENT"] == employment)
            row = {"band": band, "employment": employment}
            for year in sorted(parents["SURVEY_YEAR"].unique()):
                row[f"n_{year}"] = int((in_cell & (parents["SURVEY_YEAR"] == year)).sum())
            row["n_pooled"] = int(in_cell.sum())
            # Weighted count = estimated number of CHILDREN (not parents), yearly average.
            row["weighted_children"] = round(parents.loc[in_cell, "WEIGHT_POOLED"].sum())
            row["meets_n30_pooled"] = row["n_pooled"] >= MIN_N
            row["meets_n30_every_year"] = True
            for year in sorted(parents["SURVEY_YEAR"].unique()):
                if row[f"n_{year}"] < MIN_N:
                    row["meets_n30_every_year"] = False
            rows.append(row)
    return pd.DataFrame(rows)


# Display order for the grouping columns used in step 4.
GROUP_ORDER = [
    "0-2", "3-5", "0-5", "6-11", "12-17",
    "No child 0-5", "1 child 0-5", "2+ children 0-5",
    "Child 0-2, no other 0-5", "Child 0-2 + another 0-5", "Sampled child 3+",
]


def band_sort_key(band):
    """Sort bands in GROUP_ORDER ('12-17' after '6-11')."""
    return GROUP_ORDER.index(band)


def employment_shares(data, is_group, band_column):
    """Employment share within each band, with precision and reliability flags."""
    rows = []
    bands = list(data.loc[is_group, band_column].unique())
    bands.sort(key=band_sort_key)
    has_employment = data["A1_EMPLOYED_R"].notna()

    for band in bands:
        in_domain = is_group & (data[band_column] == band) & has_employment
        for code, label in EMPLOYMENT_LABELS.items():
            row = {"band": band, "employment": label}
            row.update(precision_row(data, in_domain, data["A1_EMPLOYED_R"] == code))
            rows.append(row)
    return pd.DataFrame(rows)


def outcome_precision(data, is_group, band_column,
                      employment_column="A1_EMPLOYED_R", labels=EMPLOYMENT_LABELS):
    """Precision test with a real outcome: fair/poor mental health (A1_MENTHEALTH 4-5).

    Enough cases (n >= 30) does not guarantee a usable estimate when the
    outcome is uncommon, so this checks CI width and RSE for an outcome the
    analysis will actually use. The shares are a feasibility test only, not
    results, and say nothing about cause.

    employment_column and labels choose the employment scheme: the six
    original codes (default) or the collapsed EMPLOYMENT_3.
    """
    rows = []
    bands = list(data.loc[is_group, band_column].unique())
    bands.sort(key=band_sort_key)
    has_outcome = data["A1_MENTHEALTH"].notna()
    fair_or_poor = data["A1_MENTHEALTH"] >= 4

    for band in bands:
        for code, label in labels.items():
            in_domain = (
                is_group
                & (data[band_column] == band)
                & (data[employment_column] == code)
                & has_outcome
            )
            row = {"band": band, "employment": label}
            if in_domain.sum() < 2:
                row.update({"n": int(in_domain.sum()), "flags": f"n<{MIN_N}"})
            else:
                row.update(precision_row(data, in_domain, fair_or_poor))
            rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Step 5: missing data among mothers
# ---------------------------------------------------------------------------

# Stata missing codes defined in the 2023-2025 label files (.do). The NSCH FAQ
# also mentions .k ("don't know"), but no 2023-2025 file defines it.
MISSING_CODE_NAMES = {
    "m": "no_valid_response",
    "l": "logical_skip",
    "n": "not_in_universe",
    "d": "suppressed",
}

# Variables that store "don't know" as an ordinary answer code instead of a
# missing code (from the label files). These answers are not substantive and
# are counted as nonresponse; the analysis must recode them to missing.
NUMERIC_DONT_KNOW = {
    "MISSMORTGAGE": 3,  # 1 Yes, 2 No, 3 Don't know
}


def missing_status(data, name):
    """Status of each cell of one variable: 'valid', a missing-code name, or 'not_in_file'."""
    status = pd.Series("not_in_file", index=data.index)
    status[data[name].notna()] = "valid"
    if name in NUMERIC_DONT_KNOW:
        status[data[name] == NUMERIC_DONT_KNOW[name]] = "dont_know"
    miss_column = name + "__MISS"
    if miss_column in data.columns:
        for letter, label in MISSING_CODE_NAMES.items():
            status[data[miss_column] == letter] = label
    return status


def missingness(mothers):
    """Counts of valid and missing codes per variable, by year and pooled."""
    analysis_variables = []
    for group, names in VARIABLES.items():
        if group != "design":
            for name in names:
                analysis_variables.append(name)

    columns = ["valid"] + list(MISSING_CODE_NAMES.values()) + ["dont_know", "not_in_file"]
    rows = []
    for name in analysis_variables:
        status = missing_status(mothers, name)
        for year in sorted(mothers["SURVEY_YEAR"].unique()) + ["Pooled"]:
            if year == "Pooled":
                year_status = status
            else:
                year_status = status[mothers["SURVEY_YEAR"] == year]
            counts = year_status.value_counts()
            row = {"variable": name, "year": year}
            for column in columns:
                row[column] = int(counts.get(column, 0))
            # Item nonresponse among those who should have answered:
            # no valid response / suppressed / don't know, out of everyone asked.
            nonresponse = row["no_valid_response"] + row["suppressed"] + row["dont_know"]
            asked = row["valid"] + nonresponse
            row["asked"] = asked
            row["nonresponse_pct"] = round(100 * nonresponse / asked, 1) if asked else None
            rows.append(row)
    return pd.DataFrame(rows)


def missing_by_band(mothers, names):
    """Item nonresponse (%) for selected variables by primary band, pooled years."""
    rows = []
    for name in names:
        status = missing_status(mothers, name)
        for band in ["0-5", "6-11", "12-17"]:
            band_status = status[mothers["BAND"] == band]
            asked = band_status.isin(["valid", "no_valid_response", "suppressed", "dont_know"]).sum()
            nonresponse = band_status.isin(["no_valid_response", "suppressed", "dont_know"]).sum()
            rows.append({
                "variable": name,
                "band": band,
                "asked": int(asked),
                "nonresponse_pct": round(100 * nonresponse / asked, 1) if asked else None,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------

def save(table, name):
    """Write one result table to OUT_DIR as CSV."""
    table.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"  wrote {(OUT_DIR / f'{name}.csv').relative_to(ROOT)}")


def main():
    data = prepare(pd.read_parquet(DATA_FILE))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)
    is_father = (data["A1_SEX"] == 1) & (data["A1_RELATION"] == 1)
    mothers = data[is_mother]

    print("Step 3: mother definition")
    save(mother_flow(data), "step3_mother_flow")
    save(exclusion_reasons(data), "step3_exclusion_reasons")
    save(adult2_mothers(data), "step3_adult2_mothers")
    save(employment_adult1_vs_adult2(data), "step3_employment_adult1_vs_adult2")

    # Fathers (male biological/adoptive parent respondents) are the comparison group.
    parent_groups = {"mothers": is_mother, "fathers": is_father}
    # primary = sampled child's band; secondary = with 0-2 / 3-5 split;
    # youngest = youngest child in the household; young_children = number of children 0-5.
    groupings = {
        "primary": "BAND",
        "secondary": "BAND_SECONDARY",
        "youngest": "BAND_YOUNGEST",
        "young_children": "YOUNG_CHILDREN",
        "baby": "BABY_GROUP",
    }

    print("Step 4: sample sizes and reliability")
    for group_name, is_group in parent_groups.items():
        for grouping_name, column in groupings.items():
            suffix = f"{group_name}_{grouping_name}"
            save(sample_sizes(data[is_group], column), f"step4_sizes_{suffix}")
            save(employment_shares(data, is_group, column), f"step4_employment_shares_{suffix}")
            save(outcome_precision(data, is_group, column), f"step4_mentalhealth_precision_{suffix}")
            collapsed = outcome_precision(data, is_group, column, "EMPLOYMENT_3", EMPLOYMENT_3_LABELS)
            save(collapsed, f"step4_mentalhealth_precision_{suffix}_emp3")

    print("Step 5: missing data among mothers")
    save(missingness(mothers), "step5_missingness")
    key_items = ["A1_EMPLOYED_R", "A1_MENTHEALTH", "A1_PHYSHEALTH", "K8Q30", "K8Q31",
                 "K8Q32", "K8Q34", "K8Q35", "ACE1", "FOODSIT", "TENURE", "BEDTIME"]
    save(missing_by_band(mothers, key_items), "step5_missing_by_band")


if __name__ == "__main__":
    main()
