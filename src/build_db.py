"""Build a DuckDB database from the processed NSCH file, for SQL analysis.

Creates data/processed/nsch.duckdb (not under version control) with:

  nsch               one row per sampled child, 2023-2025 (from src/nsch.py output)
  employment_labels  code -> label for A1_EMPLOYED_R / A2_EMPLOYED_R
  relation_labels    code -> label for A1_RELATION / A2_RELATION
  sex_labels         code -> label for A1_SEX / A2_SEX
  missing_codes      Stata missing-code letter -> meaning (for the __MISS columns)
  age_bands          child age 0-17 -> primary and secondary age band

Labels are copied from the 2023-2025 Stata label files (.do); they are
identical in all three years. The queries in sql/ use these tables.

Usage (from the repository root, after running src/nsch.py):
    .venv/Scripts/python.exe src/build_db.py
"""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
PARQUET_FILE = ROOT / "data" / "processed" / "nsch_2023_2025.parquet"
DB_FILE = ROOT / "data" / "processed" / "nsch.duckdb"

EMPLOYMENT_LABELS = {
    1: "Employed full-time",
    2: "Employed part-time",
    3: "Working without pay",
    4: "Not employed, looking for work",
    5: "Not employed, not looking for work",
    6: "Retired",
}
RELATION_LABELS = {
    1: "Biological or adoptive parent",
    2: "Step-parent",
    3: "Grandparent",
    4: "Foster parent",
    6: "Other relative",
    7: "Other non-relative",
    8: "No second caregiver",  # A2_RELATION only
}
SEX_LABELS = {
    1: "Male",
    2: "Female",
}
MISSING_CODES = {
    "m": "No valid response",
    "l": "Logical skip",
    "n": "Not in universe",
    "d": "Suppressed for confidentiality",
}


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
    return primary_band(age)


def create_lookup(con, table, key_column, key_type, labels):
    """Create a two-column lookup table (key, label) from a dict."""
    con.execute(f"CREATE TABLE {table} ({key_column} {key_type} PRIMARY KEY, label VARCHAR NOT NULL)")
    for key, label in labels.items():
        con.execute(f"INSERT INTO {table} VALUES (?, ?)", [key, label])


def create_age_bands(con):
    """Create age_bands: one row per age 0-17 with both band schemes."""
    con.execute(
        "CREATE TABLE age_bands (age INTEGER PRIMARY KEY, band_primary VARCHAR, band_secondary VARCHAR)"
    )
    for age in range(18):
        con.execute(
            "INSERT INTO age_bands VALUES (?, ?, ?)",
            [age, primary_band(age), secondary_band(age)],
        )


def main():
    # Rebuild from scratch each time so the database always matches the parquet file.
    if DB_FILE.exists():
        DB_FILE.unlink()

    con = duckdb.connect(str(DB_FILE))
    con.execute("CREATE TABLE nsch AS SELECT * FROM read_parquet(?)", [str(PARQUET_FILE)])

    create_lookup(con, "employment_labels", "code", "INTEGER", EMPLOYMENT_LABELS)
    create_lookup(con, "relation_labels", "code", "INTEGER", RELATION_LABELS)
    create_lookup(con, "sex_labels", "code", "INTEGER", SEX_LABELS)
    create_lookup(con, "missing_codes", "code", "VARCHAR", MISSING_CODES)
    create_age_bands(con)

    print(f"Wrote {DB_FILE.relative_to(ROOT)}")
    for (table,) in con.execute("SELECT table_name FROM information_schema.tables ORDER BY table_name").fetchall():
        rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {rows:,} rows")
    con.close()


if __name__ == "__main__":
    main()
