"""H1, first pass: mothers' self-rated mental health by employment status (NSCH).

Research plan H1: "Working mothers' reported mental and emotional health varies
by employment circumstances." This script is descriptive. It estimates, for
each child age band and maternal employment group:

  Table 1  The distribution of the mother's self-rated mental/emotional health
           (A1_MENTHEALTH): excellent or very good / good / fair or poor.
  Table 2  The difference in "fair or poor" between each employment group and
           full-time employment, with a 95% confidence interval.
  Table 3  How many mothers each exclusion removes.
  Sensitivity  Tables 1 and 2 again with retired mothers (A1_EMPLOYED_R = 6)
           left out, side by side with the main estimates.

Applies the decisions in docs/nsch-feasibility.md Section 5:
  - Mothers: Adult 1 female and biological/adoptive parent; estimated as a
    domain, keeping every record in the variance calculation.
  - Employment: four groups. Retired is merged into "not employed, not
    looking"; "working without pay" and missing employment are left out.
  - Complete cases per item; NSCH reliability rules; logit 95% CIs.
  - Results describe children ("X% of children aged 0-5 have a mother who...").

Nothing here is causal: mental health can affect employment as much as the
reverse, and no other factors are adjusted for yet.

Usage (from the repository root, after running src/nsch.py):
    .venv/Scripts/python.exe src/nsch_h1.py
"""

import math
from pathlib import Path

import pandas as pd

from nsch_feasibility import DATA_FILE, logit_ci, prepare, reliability_flags

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "tables" / "nsch_h1"

# Four employment groups (A1_EMPLOYED_R codes -> group). 3 "working without pay" is left out.
EMPLOYMENT_4_CODES = {1: 1, 2: 2, 4: 3, 5: 4, 6: 4}
EMPLOYMENT_4_LABELS = {
    1: "Employed full-time",
    2: "Employed part-time",
    3: "Not employed, looking for work",
    4: "Not employed, not looking (incl. retired)",
}

# A1_MENTHEALTH: 1 Excellent, 2 Very good, 3 Good, 4 Fair, 5 Poor.
MENTAL_HEALTH_GROUPS = {
    "Excellent or very good": [1, 2],
    "Good": [3],
    "Fair or poor": [4, 5],
}

GROUPINGS = {
    "primary": ("BAND", ["0-5", "6-11", "12-17"]),
    "secondary": ("BAND_SECONDARY", ["0-2", "3-5", "6-11", "12-17"]),
    "youngest": ("BAND_YOUNGEST", ["0-5", "6-11", "12-17"]),
}


def employment_4(code):
    """Four-group employment code, or missing for no answer / working without pay."""
    if pd.isna(code) or int(code) not in EMPLOYMENT_4_CODES:
        return float("nan")
    return EMPLOYMENT_4_CODES[int(code)]


def linearized_share(data, in_domain, has_trait, weight="WEIGHT_POOLED"):
    """Weighted share of has_trait in a domain, plus each record's linearized contribution.

    The contributions (z) are what the design-based variance is computed from.
    Keeping them lets two estimates be combined, e.g. for a difference.
    Records outside the domain have z = 0.
    """
    w = data[weight] * in_domain
    total = w.sum()
    share = (w * has_trait).sum() / total
    z = w * (has_trait - share) / total
    return share, z


def design_se(data, z):
    """Standard error from linearized contributions: strata DESIGN_STRATUM, households (HHID) as PSUs.

    Same formula as weighted_share() in nsch_feasibility.py: each record is
    its own household, because NSCH samples one child per household.
    """
    stratum_mean = z.groupby(data["DESIGN_STRATUM"]).transform("mean")
    squared_deviation = (z - stratum_mean) ** 2
    stratum_sum = squared_deviation.groupby(data["DESIGN_STRATUM"]).sum()
    stratum_n = data.groupby("DESIGN_STRATUM").size()
    variance = (stratum_n / (stratum_n - 1) * stratum_sum).sum()
    return math.sqrt(variance)


def distribution_table(data, is_mother, band_column, bands):
    """Table 1: mental health distribution by band x employment group."""
    has_answer = data["A1_MENTHEALTH"].notna()
    rows = []
    for band in bands:
        for code, label in EMPLOYMENT_4_LABELS.items():
            in_domain = is_mother & has_answer & (data[band_column] == band) & (data["EMPLOYMENT_4"] == code)
            n = int(in_domain.sum())
            for group, values in MENTAL_HEALTH_GROUPS.items():
                has_trait = data["A1_MENTHEALTH"].isin(values)
                share, z = linearized_share(data, in_domain, has_trait)
                se = design_se(data, z)
                low, high = logit_ci(share, se)
                ci_width = (high - low) * 100
                rows.append({
                    "band": band,
                    "employment": label,
                    "mental_health": group,
                    "n": n,
                    "share_pct": round(share * 100, 1),
                    "ci_low_pct": round(low * 100, 1),
                    "ci_high_pct": round(high * 100, 1),
                    "flags": reliability_flags(n, share, ci_width),
                })
    return pd.DataFrame(rows)


def difference_table(data, is_mother, band_column, bands):
    """Table 2: difference in 'fair or poor' vs. full-time, by band."""
    has_answer = data["A1_MENTHEALTH"].notna()
    fair_poor = data["A1_MENTHEALTH"].isin(MENTAL_HEALTH_GROUPS["Fair or poor"])
    rows = []
    for band in bands:
        in_band = is_mother & has_answer & (data[band_column] == band)
        full_time = in_band & (data["EMPLOYMENT_4"] == 1)
        share_ft, z_ft = linearized_share(data, full_time, fair_poor)
        for code in [2, 3, 4]:
            group = in_band & (data["EMPLOYMENT_4"] == code)
            share, z = linearized_share(data, group, fair_poor)
            difference = share - share_ft
            # The two groups are separate domains of the same sample, so the
            # difference's contributions are simply z - z_ft.
            se = design_se(data, z - z_ft)
            low = difference - 1.96 * se
            high = difference + 1.96 * se
            rows.append({
                "band": band,
                "employment": EMPLOYMENT_4_LABELS[code],
                "fair_poor_pct": round(share * 100, 1),
                "full_time_fair_poor_pct": round(share_ft * 100, 1),
                "difference_pts": round(difference * 100, 1),
                "ci_low_pts": round(low * 100, 1),
                "ci_high_pts": round(high * 100, 1),
                "ci_excludes_zero": (low > 0) or (high < 0),
                "n_group": int(group.sum()),
                "n_full_time": int(full_time.sum()),
            })
    return pd.DataFrame(rows)


def exclusions(data, is_mother):
    """Table 3: how many mothers each step removes."""
    mothers = data[is_mother]
    code = mothers["A1_EMPLOYED_R"]
    rows = [
        {"step": "Mothers (Adult 1 female, biological/adoptive parent)", "n": len(mothers)},
        {"step": "Retired, merged into 'not employed, not looking'", "n": int((code == 6).sum())},
        {"step": "Excluded: working without pay", "n": int((code == 3).sum())},
        {"step": "Excluded: no employment answer", "n": int(code.isna().sum())},
        {"step": "Excluded: no mental health answer (among the rest)",
         "n": int((mothers["EMPLOYMENT_4"].notna() & mothers["A1_MENTHEALTH"].isna()).sum())},
        {"step": "Analysis sample",
         "n": int((mothers["EMPLOYMENT_4"].notna() & mothers["A1_MENTHEALTH"].notna()).sum())},
    ]
    return pd.DataFrame(rows)


def retired_sensitivity(data, is_mother, band_column, bands):
    """Tables 1 and 2 with retired mothers left out, next to the main estimates."""
    not_retired = is_mother & (data["A1_EMPLOYED_R"] != 6)
    keys = ["band", "employment", "mental_health"]
    main = distribution_table(data, is_mother, band_column, bands)
    check = distribution_table(data, not_retired, band_column, bands)
    shares = main[keys + ["n", "share_pct"]].merge(
        check[keys + ["n", "share_pct", "flags"]], on=keys, suffixes=("_main", "_no_retired"))
    shares = shares.rename(columns={"share_pct_main": "main", "share_pct_no_retired": "no_retired",
                                    "flags": "flags_no_retired"})
    shares.insert(0, "estimate", "% " + shares.pop("mental_health"))

    keys = ["band", "employment"]
    main = difference_table(data, is_mother, band_column, bands)
    check = difference_table(data, not_retired, band_column, bands)
    gaps = main[keys + ["n_group", "difference_pts"]].merge(
        check[keys + ["n_group", "difference_pts", "ci_low_pts", "ci_high_pts"]],
        on=keys, suffixes=("_main", "_no_retired"))
    gaps = gaps.rename(columns={"n_group_main": "n_main", "n_group_no_retired": "n_no_retired",
                                "difference_pts_main": "main", "difference_pts_no_retired": "no_retired",
                                "ci_low_pts": "ci_low_no_retired", "ci_high_pts": "ci_high_no_retired"})
    gaps.insert(0, "estimate", "fair or poor, difference vs. full-time (pts)")

    table = pd.concat([shares, gaps], ignore_index=True)
    table["change_pts"] = (table["no_retired"] - table["main"]).round(1)
    return table


def save(table, name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"  {name}.csv ({len(table)} rows)")


def main():
    data = prepare(pd.read_parquet(DATA_FILE))
    data["EMPLOYMENT_4"] = data["A1_EMPLOYED_R"].apply(employment_4)
    is_mother = (data["A1_SEX"] == 2) & (data["A1_RELATION"] == 1)

    save(exclusions(data, is_mother), "table3_exclusions")
    for name, (column, bands) in GROUPINGS.items():
        save(distribution_table(data, is_mother, column, bands), f"table1_mental_health_{name}")
        save(difference_table(data, is_mother, column, bands), f"table2_fair_poor_difference_{name}")
        save(retired_sensitivity(data, is_mother, column, bands), f"sensitivity_no_retired_{name}")


if __name__ == "__main__":
    main()
