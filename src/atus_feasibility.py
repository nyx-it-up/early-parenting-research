"""ATUS feasibility check: mother definition, pooling window, sample sizes, missing data.

Reads the processed file written by src/atus.py and runs research plan
Section 11 (next step 1) for ATUS:

  Step 1  Define "mother" (female respondent with own household children
          under 18) and count respondents at each filter, by year. From 2007,
          split mothers by whether the CPS lists their children as
          biological/adopted or step-children.
  Step 2  Diary coverage by year and month (2020 and 2025 have gaps).
  Step 3  Unweighted sample sizes and weighted employment shares by the
          youngest own child's age band x employment status, pooled
          2022-2025. Mothers and, as a comparison group, fathers.
  Step 4  Precision of mean diary-day minutes (sleep, childcare, paid work)
          by band x employment, with approximate standard errors.
  Step 5  Missing data among mothers.

Results are written as CSV files to reports/tables/atus_feasibility/ and
summarized in docs/atus-feasibility.md. Nothing here is a finding about
mothers' time use; the numbers only say which comparisons the data can support.

Usage (from the repository root, after running src/atus.py):
    .venv/Scripts/python.exe src/atus_feasibility.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "atus_2003_2025.parquet"
OUT_DIR = ROOT / "reports" / "tables" / "atus_feasibility"

# Pooling window. 2022-2025 is the main window: 2021 is left out as too close to
# the COVID-19 pandemic, and 2020 (diaries from March 18 to May 9 not collected,
# separate weight TU20FWGT) is excluded. Pre-pandemic / pandemic / post-pandemic
# comparisons are planned for a later pass.
WINDOWS = {
    "2022-2025": [2022, 2023, 2024, 2025],
}

# Employment status from TELFS (labor force status) and TRDPFTPT (full/part time).
EMPLOYMENT_LABELS = {
    1: "Employed full-time",
    2: "Employed part-time",
    3: "Employed, hours status unknown",
    4: "Unemployed",
    5: "Not in labor force",
}
# Collapsed: unemployed and not in labor force combined, as for NSCH fathers.
EMPLOYMENT_3_LABELS = {
    1: "Employed full-time",
    2: "Employed part-time",
    3: "Not employed (unemployed or not in labor force)",
}

OUTCOMES = {
    "SLEEP": "Sleeping (010101), minutes",
    "CHILDCARE_HH": "Caring for household children (0301-0303), minutes",
    "PAID_WORK": "Working at a job (0501), minutes",
}

BAND_ORDER = ["0-2", "3-5", "0-5", "6-11", "12-17"]

# Provisional reliability rules for this check. BLS applies its own publication
# criteria (ATUS User's Guide, Appendix N), which have not been checked yet.
MIN_N = 30
MAX_RSE = 0.30


def employment(row):
    """Employment code (see EMPLOYMENT_LABELS) from TELFS and TRDPFTPT."""
    if row["TELFS"] in (1, 2):
        if row["TRDPFTPT"] == 1:
            return 1
        if row["TRDPFTPT"] == 2:
            return 2
        return 3
    if row["TELFS"] in (3, 4):
        return 4
    if row["TELFS"] == 5:
        return 5
    return None


def employment_3(code):
    """Collapse the employment code to full-time / part-time / not employed."""
    if code == 1:
        return 1
    if code == 2:
        return 2
    if code in (4, 5):
        return 3
    return None


def primary_band(age):
    """Primary age band of the youngest own child: 0-5, 6-11 or 12-17."""
    if pd.isna(age):
        return None
    if age <= 5:
        return "0-5"
    if age <= 11:
        return "6-11"
    return "12-17"


def secondary_band(age):
    """Secondary age band: 0-2, 3-5, 6-11 or 12-17."""
    if pd.isna(age):
        return None
    if age <= 2:
        return "0-2"
    if age <= 5:
        return "3-5"
    return primary_band(age)


def child_type_group(row):
    """Mother's children by CPS parent type (2007+ only)."""
    if row["TUYEAR"] < 2007:
        return "Not available before 2007"
    if row["N_CHILD_BIO_ADOPT"] > 0:
        return "At least one biological/adopted child"
    if row["N_CHILD_STEP"] > 0:
        return "Only step-children"
    return "No CPS parent type for any child"


def prepare(data):
    """Add the derived grouping columns used in the tables."""
    data = data.copy()
    data["EMPLOYMENT"] = data.apply(employment, axis=1)
    data["EMPLOYMENT_3"] = data["EMPLOYMENT"].apply(employment_3)
    data["BAND"] = data["YOUNGEST_OWN_AGE"].apply(primary_band)
    data["BAND_SECONDARY"] = data["YOUNGEST_OWN_AGE"].apply(secondary_band)
    data["CHILD_TYPE"] = data.apply(child_type_group, axis=1)
    data["WEEKEND"] = data["TUDIARYDAY"].isin([1, 7])
    return data


def weighted_mean(data, in_domain, values, weight="WEIGHT"):
    """Weighted mean of values among records in in_domain, with an approximate standard error.

    The standard error uses Taylor linearization and treats every respondent as
    an independent unit (ATUS selects one person per household). It ignores the
    CPS strata and clusters, so it is only an approximation; final results will
    use the 160 replicate weights as the ATUS User's Guide specifies.
    Records outside the domain stay in with zero weight (domain estimation).
    Returns (mean, standard_error).
    """
    w = data[weight] * in_domain
    total = w.sum()
    mean = (w * values).sum() / total
    z = w * (values - mean) / total
    n = len(data)
    variance = n / (n - 1) * ((z - z.mean()) ** 2).sum()
    return mean, variance ** 0.5


def reliability_flags(n, mean, se):
    """Return the provisional rule(s) an estimate breaks, as text ('' if none)."""
    flags = []
    if n < MIN_N:
        flags.append(f"n<{MIN_N}")
    if mean > 0 and se / mean > MAX_RSE:
        flags.append(f"RSE>{int(MAX_RSE * 100)}%")
    return "; ".join(flags)


def mother_flow(data):
    """Step 1: respondents per year at each step of the mother definition."""
    rows = []
    for year, group in data.groupby("TUYEAR"):
        female = group["RESP_SEX"] == 2
        mothers = female & (group["N_OWN_CHILDREN"] > 0)
        fathers = (group["RESP_SEX"] == 1) & (group["N_OWN_CHILDREN"] > 0)
        row = {
            "year": year,
            "all_respondents": len(group),
            "female": int(female.sum()),
            "mothers": int(mothers.sum()),
            "fathers": int(fathers.sum()),
        }
        for child_type in ["At least one biological/adopted child", "Only step-children",
                           "No CPS parent type for any child"]:
            row[f"mothers: {child_type}"] = int((mothers & (group["CHILD_TYPE"] == child_type)).sum())
        rows.append(row)
    return pd.DataFrame(rows)


def child_types_by_window(mothers):
    """Step 1: share of mothers by CPS parent type of their children, per window (2007+)."""
    rows = []
    for window, years in WINDOWS.items():
        group = mothers[mothers["TUYEAR"].isin(years)]
        for child_type, count in group["CHILD_TYPE"].value_counts().items():
            rows.append({
                "window": window,
                "children": child_type,
                "n": int(count),
                "pct_of_mothers": round(100 * count / len(group), 1),
                "mothers_with_any_step_child": int((group["N_CHILD_STEP"] > 0).sum()),
            })
    return pd.DataFrame(rows)


def diary_coverage(data):
    """Step 2: completed diaries by year and month, 2018 onward."""
    recent = data[data["TUYEAR"] >= 2018]
    table = pd.crosstab(recent["TUYEAR"], recent["TUMONTH"])
    table.columns = [f"month_{m}" for m in table.columns]
    return table.reset_index().rename(columns={"TUYEAR": "year"})


def weekend_share(parents):
    """Step 2: share of diary days on a weekend, per window (design: 50%)."""
    rows = []
    for window, years in WINDOWS.items():
        group = parents[parents["TUYEAR"].isin(years)]
        rows.append({
            "window": window,
            "n": len(group),
            "weekend_diaries_pct": round(100 * group["WEEKEND"].mean(), 1),
        })
    return pd.DataFrame(rows)


def sample_sizes(parents, band_column):
    """Step 3: unweighted n by band x employment status for each window."""
    rows = []
    for window, years in WINDOWS.items():
        group = parents[parents["TUYEAR"].isin(years)]
        for band in BAND_ORDER:
            in_band = group[group[band_column] == band]
            if len(in_band) == 0:
                continue
            for code, label in EMPLOYMENT_LABELS.items():
                rows.append({
                    "window": window,
                    "band": band,
                    "employment": label,
                    "n": int((in_band["EMPLOYMENT"] == code).sum()),
                })
            rows.append({"window": window, "band": band, "employment": "Total", "n": len(in_band)})
    return pd.DataFrame(rows)


def employment_shares(data, is_group, band_column):
    """Step 3: weighted employment shares (%) within each band, per window."""
    rows = []
    for window, years in WINDOWS.items():
        in_window = data["TUYEAR"].isin(years)
        known = data["EMPLOYMENT"].isin([1, 2, 4, 5])
        for band in BAND_ORDER:
            in_band = is_group & in_window & known & (data[band_column] == band)
            if not in_band.any():
                continue
            band_weight = data.loc[in_band, "WEIGHT"].sum()
            for code in [1, 2, 4, 5]:
                share_weight = data.loc[in_band & (data["EMPLOYMENT"] == code), "WEIGHT"].sum()
                rows.append({
                    "window": window,
                    "band": band,
                    "employment": EMPLOYMENT_LABELS[code],
                    "share_pct": round(100 * share_weight / band_weight, 1),
                })
    return pd.DataFrame(rows)


def outcome_precision(data, is_group, band_column):
    """Step 4: weighted mean minutes by band x collapsed employment, with approximate precision."""
    rows = []
    for window, years in WINDOWS.items():
        window_data = data[data["TUYEAR"].isin(years)]
        in_group = is_group[window_data.index]
        for band in BAND_ORDER:
            if not (in_group & (window_data[band_column] == band)).any():
                continue
            for code, label in EMPLOYMENT_3_LABELS.items():
                in_domain = in_group & (window_data[band_column] == band) & (window_data["EMPLOYMENT_3"] == code)
                n = int(in_domain.sum())
                for outcome, outcome_label in OUTCOMES.items():
                    if n < 2:
                        continue
                    mean, se = weighted_mean(window_data, in_domain, window_data[outcome])
                    rows.append({
                        "window": window,
                        "band": band,
                        "employment": label,
                        "outcome": outcome_label,
                        "n": n,
                        "mean_minutes": round(mean, 1),
                        "approx_se": round(se, 1),
                        "ci_low": round(mean - 1.96 * se, 1),
                        "ci_high": round(mean + 1.96 * se, 1),
                        "rse_pct": round(100 * se / mean, 1) if mean > 0 else None,
                        "flags": reliability_flags(n, mean, se),
                    })
    return pd.DataFrame(rows)


def missingness(mothers):
    """Step 5: negative (blank / don't know / refused) codes among mothers, by window."""
    checks = {
        "TELFS (labor force status)": mothers["TELFS"] < 0,
        "TRDPFTPT (full/part time), employed only": mothers["TELFS"].isin([1, 2]) & (mothers["TRDPFTPT"] < 0),
        "TEHRUSLT (usual hours), employed only, -4 'hours vary' excluded":
            mothers["TELFS"].isin([1, 2]) & (mothers["TEHRUSLT"] < 0) & (mothers["TEHRUSLT"] != -4),
        "TEHRUSLT = -4 'hours vary', employed only": mothers["TELFS"].isin([1, 2]) & (mothers["TEHRUSLT"] == -4),
        "RESP_AGE (respondent age)": mothers["RESP_AGE"] < 0,
    }
    rows = []
    for window, years in WINDOWS.items():
        in_window = mothers["TUYEAR"].isin(years)
        employed = in_window & mothers["TELFS"].isin([1, 2])
        for name, is_missing in checks.items():
            base = employed if "employed only" in name else in_window
            count = int((is_missing & in_window).sum())
            rows.append({
                "window": window,
                "variable": name,
                "base_n": int(base.sum()),
                "n_missing": count,
                "pct": round(100 * count / base.sum(), 2),
            })
    return pd.DataFrame(rows)


def roster_age_problems():
    """Step 5: roster lines coded as own household child with a negative (missing) age or relationship."""
    roster = pd.read_csv(ROOT / "data" / "raw" / "atus" / "atusrost_0325.dat", dtype={"TUCASEID": str})
    return pd.DataFrame([{
        "roster_lines": len(roster),
        "TERRP_negative": int((roster["TERRP"] < 0).sum()),
        "TEAGE_negative": int((roster["TEAGE"] < 0).sum()),
        "own_child_TEAGE_negative": int(((roster["TERRP"] == 22) & (roster["TEAGE"] < 0)).sum()),
    }])


def save(table, name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"  {name}.csv ({len(table)} rows)")


def main():
    data = prepare(pd.read_parquet(DATA_FILE))
    has_child = data["N_OWN_CHILDREN"] > 0
    is_mother = (data["RESP_SEX"] == 2) & has_child
    is_father = (data["RESP_SEX"] == 1) & has_child
    mothers = data[is_mother]

    print("Step 1: mother definition")
    save(mother_flow(data), "step1_mother_flow")
    save(child_types_by_window(mothers), "step1_child_types_by_window")

    print("Step 2: diary coverage")
    save(diary_coverage(data), "step2_diary_coverage")
    save(weekend_share(mothers), "step2_weekend_share_mothers")

    print("Step 3: sample sizes and employment shares")
    parent_groups = {"mothers": is_mother, "fathers": is_father}
    groupings = {"primary": "BAND", "secondary": "BAND_SECONDARY"}
    for group_name, is_group in parent_groups.items():
        for grouping_name, column in groupings.items():
            suffix = f"{group_name}_{grouping_name}"
            save(sample_sizes(data[is_group], column), f"step3_sizes_{suffix}")
            save(employment_shares(data, is_group, column), f"step3_employment_shares_{suffix}")

    print("Step 4: precision of mean minutes")
    for group_name, is_group in parent_groups.items():
        for grouping_name, column in groupings.items():
            save(outcome_precision(data, is_group, column), f"step4_minutes_precision_{group_name}_{grouping_name}")

    print("Step 5: missing data among mothers")
    save(missingness(mothers), "step5_missingness")
    save(roster_age_problems(), "step5_roster_codes")


if __name__ == "__main__":
    main()
