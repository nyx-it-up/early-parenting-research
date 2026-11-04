# SQL queries (DuckDB)

SQL queries on the pooled 2023–2025 NSCH topical files. The notebook `notebooks/nsch_sql.ipynb` runs the same queries and shows their results.

## Setup

From the repository root:

```
.venv/Scripts/python.exe src/nsch.py        # only if data/processed/nsch_2023_2025.parquet is missing
.venv/Scripts/python.exe src/build_db.py    # builds data/processed/nsch.duckdb
```

## Tables

| Table | Rows | What it holds |
|---|---|---|
| `nsch` | 151,676 | One row per sampled child, 2023–2025. Value columns (`SURVEY_YEAR`, `FWC`, `SC_AGE_YEARS`, `A1_SEX`, `A1_RELATION`, `A1_EMPLOYED_R`, …) and `<VAR>__MISS` columns holding the missing-code letter. |
| `employment_labels` | 6 | `code` → `label` for `A1_EMPLOYED_R` |
| `relation_labels` | 7 | `code` → `label` for `A1_RELATION` / `A2_RELATION` |
| `sex_labels` | 2 | `code` → `label` for `A1_SEX` / `A2_SEX` |
| `missing_codes` | 4 | `code` (`m`, `l`, `n`, `d`) → meaning |
| `age_bands` | 18 | `age` 0–17 → `band_primary` (`0-5`, `6-11`, `12-17`) and `band_secondary` (`0-2`, `3-5`, `6-11`, `12-17`) |

**Mother definition:** `A1_SEX = 2 AND A1_RELATION = 1`.

**Missing values:** a missing answer is `NULL` in the value column. Its reason is in the matching `__MISS` column.

## Queries

| File | What it returns |
|---|---|
| `01_mother_flow.sql` | Children per survey year at each step of the mother definition |
| `02_sample_sizes.sql` | Mothers by child age band × employment status (unweighted n) |
| `03_employment_shares.sql` | Weighted employment shares (%) within each child age band |
| `04_missing_codes.sql` | Missing-data codes per variable among mothers |
