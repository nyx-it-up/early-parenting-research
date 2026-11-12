"""Export the data used by the interactive stories (viz/).

Writes two JavaScript files so the pages open straight from disk:
  viz/data.js         window.STORY_DATA: estimates from the CSV tables written by
                      the analysis scripts (nothing re-estimated here).
  viz/respondents.js  window.RESPONDENTS: one record per parent who answered
                      (employment, child's age, mental health rating, survey
                      year, pooled weight), for the room of circles in
                      people.html. Rows are shuffled; no IDs or geography.

Usage (from the repository root, after the analysis scripts have run):
    .venv/Scripts/python.exe src/build_viz_data.py
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "reports" / "tables"
OUT_FILE = ROOT / "viz" / "data.js"
RESPONDENTS_FILE = ROOT / "viz" / "respondents.js"
SHUFFLE_SEED = 20261111

SHORT_EMPLOYMENT = {
    "Employed full-time": "Full-time",
    "Employed part-time": "Part-time",
    "Not employed, looking for work": "Looking for work",
    "Not employed, not looking (incl. retired)": "Not looking for work",
    "Not employed (looking, not looking or retired)": "Not employed",
}


def short(label):
    return SHORT_EMPLOYMENT.get(label, label)


def parse_ci(text):
    """'1.5 to 4.5' -> [1.5, 4.5]; missing -> None."""
    if not isinstance(text, str) or " to " not in text:
        return None
    low, high = text.split(" to ")
    return [float(low), float(high)]


def fair_poor_by_band():
    table = pd.read_csv(TABLES / "nsch_h1" / "table1_mental_health_primary.csv")
    table = table[table["mental_health"] == "Fair or poor"]
    rows = []
    for _, row in table.iterrows():
        rows.append({"band": row["band"], "group": short(row["employment"]), "n": int(row["n"]),
                     "pct": row["share_pct"], "ci": [row["ci_low_pct"], row["ci_high_pct"]]})
    return rows


def adjusted_gaps():
    table = pd.read_csv(TABLES / "nsch_h1_models" / "adjusted_gaps.csv")
    rows = []
    for _, row in table.iterrows():
        rows.append({"model": row["model"], "group": short(row["employment"]),
                     "gap": row["gap_vs_full_time_pts"], "ci": [row["gap_ci_low_pts"], row["gap_ci_high_pts"]]})
    return rows


def gaps_by_band():
    table = pd.read_csv(TABLES / "nsch_h1_models" / "adjusted_gaps_by_band.csv")
    table = table[table["gap_vs_full_time_pts"].notna()]
    rows = []
    for _, row in table.iterrows():
        rows.append({"band": row["band"], "group": short(row["employment"]),
                     "gap": row["gap_vs_full_time_pts"], "ci": [row["gap_ci_low_pts"], row["gap_ci_high_pts"]]})
    return rows


def decomposition():
    totals = pd.read_csv(TABLES / "nsch_h1_fairlie" / "fairlie_totals.csv")
    parts = pd.read_csv(TABLES / "nsch_h1_fairlie" / "fairlie_contributions.csv")
    names = {"MARITAL": "Marital status", "AGE": "Mother's age", "INCOME": "Family income",
             "EDUCATION": "Education", "KIDS": "Number of children", "BAND": "Child's age", "YEAR": "Survey year"}
    result = []
    for _, total in totals.iterrows():
        comparison = total["comparison"]
        contributions = []
        for _, part in parts[parts["comparison"] == comparison].iterrows():
            contributions.append({"name": names.get(part["covariate"], part["covariate"]), "pts": part["contribution_pts"]})
        result.append({"group": short(comparison.split(" vs. ")[0]), "raw": total["raw_gap_pts"],
                       "explained": total["explained_pts"], "unexplained": total["unexplained_pts"],
                       "contributions": contributions})
    return result


def under2():
    table = pd.read_csv(TABLES / "nsch_h1_under2" / "under2_all_outcomes.csv")
    table = table[table["scheme"] == "under2"]
    keep = {
        "Mental health fair or poor": "Fair or poor mental health",
        "Mental health good, fair or poor": "Good, fair or poor mental health",
        "Parenting aggravation (usually/always on K8Q31, K8Q32 or K8Q34)": "Frequent parenting aggravation",
        "Job change because of problems with child care (K6Q27), child 0-5": "Family job change because of child care",
    }
    rows = []
    for _, row in table.iterrows():
        if row["outcome"] not in keep or str(row["adjusted"]).startswith("not estimable"):
            continue
        rows.append({
            "outcome": keep[row["outcome"]],
            "comparison": "employment" if row["comparison"].startswith("1") else "child age",
            "group": short(row["group"]),
            "n": int(row["n"]),
            "pct": float(row["adjusted"]),
            "ci": parse_ci(row["adjusted_ci"]),
            "gap": None if pd.isna(row["adjusted_gap"]) else float(row["adjusted_gap"]),
            "gap_ci": parse_ci(row["adjusted_gap_ci"]),
            "flag": "" if pd.isna(row["flags"]) else row["flags"],
        })
    return rows


def fathers():
    levels = pd.read_csv(TABLES / "nsch_h8" / "partA_fair_poor_by_sex.csv")
    gaps = pd.read_csv(TABLES / "nsch_h8" / "partB_adjusted_gaps.csv")
    level_rows = []
    for _, row in levels.iterrows():
        level_rows.append({"parent": row["parent"], "band": row["band"], "group": short(row["employment"]),
                           "n": int(row["n"]), "pct": row["fair_poor_pct"],
                           "ci": [row["ci_low_pct"], row["ci_high_pct"]],
                           "flag": "" if pd.isna(row["flags"]) else row["flags"]})
    gap_rows = []
    for _, row in gaps.iterrows():
        for parent in ["mothers", "fathers", "difference"]:
            gap_rows.append({"group": short(row["employment"]), "parent": parent, "gap": row[f"{parent}_pts"],
                             "ci": [row[f"{parent}_ci_low"], row[f"{parent}_ci_high"]]})
    return {"levels": level_rows, "gaps": gap_rows}


def odds_ratios():
    """Odds ratios of the main model (M1) with 95% CIs."""
    table = pd.read_csv(TABLES / "nsch_h1_models" / "odds_ratios_M1.csv")
    rows = []
    for _, row in table.iterrows():
        variable, level = row["term"].split(": ", 1)
        rows.append({"variable": variable, "level": short(level), "or": row["odds_ratio"],
                     "ci": [row["ci_low"], row["ci_high"]], "p": row["p_value"]})
    return rows


def respondents():
    """One record per mother or father in the analysis samples (H1 and H8).

    Encoded compactly: digit strings for employment (0 full-time, 1 part-time,
    2 looking, 3 not looking), mental health rating (1 excellent ... 5 poor) and
    survey year (last digit); child's age as one base-36 character (0-h);
    pooled weights as rounded integers.
    """
    from nsch_feasibility import DATA_FILE, prepare
    from nsch_h1 import employment_4

    data = prepare(pd.read_parquet(DATA_FILE))
    data["EMPLOYMENT_4"] = data["A1_EMPLOYED_R"].apply(employment_4)
    parents = data[(data["A1_RELATION"] == 1) & data["A1_SEX"].isin([1, 2])
                   & data["EMPLOYMENT_4"].notna() & data["A1_MENTHEALTH"].notna()]
    parents = parents.sample(frac=1, random_state=SHUFFLE_SEED)

    result = {}
    for sex, name in [(2, "mothers"), (1, "fathers")]:
        group = parents[parents["A1_SEX"] == sex]
        result[name] = {
            "employment": "".join(str(int(v) - 1) for v in group["EMPLOYMENT_4"]),
            "age": "".join("0123456789abcdefgh"[int(v)] for v in group["SC_AGE_YEARS"]),
            "rating": "".join(str(int(v)) for v in group["A1_MENTHEALTH"]),
            "year": "".join(str(int(v) % 10) for v in group["SURVEY_YEAR"]),
            "weight": [int(round(v)) for v in group["WEIGHT_POOLED"]],
        }
    return result


def main():
    data = {
        "fairPoorByBand": fair_poor_by_band(),
        "adjustedGaps": adjusted_gaps(),
        "gapsByBand": gaps_by_band(),
        "decomposition": decomposition(),
        "under2": under2(),
        "oddsRatios": odds_ratios(),
        "fathers": fathers(),
    }
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    text = "// Generated by src/build_viz_data.py from reports/tables/. Do not edit by hand.\n"
    text += "window.STORY_DATA = " + json.dumps(data, indent=1) + ";\n"
    OUT_FILE.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT_FILE.relative_to(ROOT)}")
    for key, value in data.items():
        print(f"  {key}: {len(value) if isinstance(value, list) else {k: len(v) for k, v in value.items()}}")

    people = respondents()
    text = "// Generated by src/build_viz_data.py. One record per parent who answered; do not edit by hand.\n"
    text += "window.RESPONDENTS = " + json.dumps(people, separators=(",", ":")) + ";\n"
    RESPONDENTS_FILE.write_text(text, encoding="utf-8")
    sizes = {name: len(group["rating"]) for name, group in people.items()}
    print(f"Wrote {RESPONDENTS_FILE.relative_to(ROOT)}: {sizes}, {RESPONDENTS_FILE.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
