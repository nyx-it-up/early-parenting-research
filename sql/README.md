# SQL exercises (DuckDB)

These exercises rebuild parts of the NSCH feasibility check (`docs/nsch-feasibility.md`) in SQL. The pandas pipeline already produced the answers, so every query can be checked automatically. When the SQL and pandas results agree, each confirms the other.

## Setup

From the repository root:

```
.venv/Scripts/python.exe src/nsch.py        # only if data/processed/nsch_2023_2025.parquet is missing
.venv/Scripts/python.exe src/build_db.py    # builds data/processed/nsch.duckdb
```

**Check an exercise:**

```
.venv/Scripts/python.exe src/check_sql.py sql/01_mother_flow.sql
```

The checker prints your result, then either `Match` or the rows that differ. Column names are compared in lower case, and row order does not matter.

**Explore interactively.** Open a Python shell:

```python
import duckdb
con = duckdb.connect("data/processed/nsch.duckdb", read_only=True)
con.sql("DESCRIBE nsch").show()
con.sql("SELECT * FROM employment_labels").show()
```

## Tables

| Table | Rows | What it holds |
|---|---|---|
| `nsch` | 151,676 | One row per sampled child, 2023–2025. Same columns as the parquet file: `SURVEY_YEAR`, `FWC`, `SC_AGE_YEARS`, `A1_SEX`, `A1_RELATION`, `A1_EMPLOYED_R`, … and `<VAR>__MISS` columns holding the missing-code letter. |
| `employment_labels` | 6 | `code` → `label` for `A1_EMPLOYED_R` |
| `relation_labels` | 7 | `code` → `label` for `A1_RELATION` / `A2_RELATION` |
| `sex_labels` | 2 | `code` → `label` for `A1_SEX` / `A2_SEX` |
| `missing_codes` | 4 | `code` (`m`, `l`, `n`, `d`) → meaning |
| `age_bands` | 18 | `age` 0–17 → `band_primary` (`0-5`, `6-11`, `12-17`) and `band_secondary` (`0-2`, `3-5`, `6-11`, `12-17`) |

**Mother definition used throughout:** `A1_SEX = 2 AND A1_RELATION = 1`.

**Missing values:** a missing answer is `NULL` in the value column. Its reason is in the matching `__MISS` column.

---

## Exercise 01: the mother filter (`sql/01_mother_flow.sql`)

**Goal:** for each survey year, count all sampled children, children whose respondent is female, and children whose respondent is their mother.

**Output columns:** `survey_year`, `all_children`, `female_respondent`, `mothers` (3 rows).

**Check against:** pooled totals 151,676 / 99,011 / 90,415. For 2025: 45,139 / 29,021 / 26,421.

**Skills:** `GROUP BY`, conditional counting.

<details><summary>Hint</summary>

One query, one `GROUP BY`. Count conditionally inside the `SELECT` with `COUNT(*) FILTER (WHERE …)` (DuckDB/PostgreSQL), or the portable `SUM(CASE WHEN … THEN 1 ELSE 0 END)`.
</details>

## Exercise 02: sample sizes (`sql/02_sample_sizes.sql`)

**Goal:** number of mothers in each primary age band × employment status, using the **labels**, not the codes. Mothers with no employment answer appear as `'Missing'`.

**Output columns:** `band`, `employment`, `n` (21 rows: 3 bands × 7 employment values).

**Check against:** 0–5 full-time = 16,552; 0–5 retired = 62; 12–17 missing = 385.

**Skills:** `JOIN` to lookup tables, `LEFT JOIN` vs. `INNER JOIN`, `COALESCE`.

<details><summary>Hint</summary>

Join `nsch` to `age_bands` on the child's age. Join to `employment_labels` on the employment code. Ask yourself which join type keeps mothers whose employment code is `NULL`, then what turns their `NULL` label into `'Missing'`.
</details>

## Exercise 03: weighted shares (`sql/03_employment_shares.sql`)

**Goal:** among mothers **with** an employment answer, the weighted share (%) in each employment status **within** each primary band, rounded to 1 decimal. Use the pooled weight `FWC / 3` (the 3 cancels in a share, but write it anyway).

**Output columns:** `band`, `employment`, `share_pct` (18 rows).

**Check against:** 0–5 full-time = 51.6; 12–17 full-time = 59.9.

**Skills:** CTEs (`WITH`), window functions (`SUM(...) OVER (PARTITION BY ...)`).

<details><summary>Hint</summary>

First sum the weights per band × employment in a CTE. Then divide each row by the band total. A window function gives you the band total on every row without a second `GROUP BY`.
</details>

## Exercise 04: missing codes (`sql/04_missing_codes.sql`)

**Goal:** among mothers, count how often each missing code appears for each variable, using **all** `__MISS` columns. Report the variable name **without** the `__MISS` suffix, and only codes that occur.

**Output columns:** `variable`, `code`, `n` (44 rows).

**Check against:** `A1_EMPLOYED_R` / `m` = 821; `HOURSLEEP05` / `n` = 61,809. There is also one surprise that the first pandas version missed; see `docs/nsch-feasibility.md` Section 3.

**Skills:** `UNPIVOT` (wide → long), selecting columns by pattern, string functions.

<details><summary>Hint</summary>

DuckDB can select columns by pattern: `COLUMNS('.*__MISS')`. `UNPIVOT … ON … INTO NAME … VALUE …` turns those columns into rows. `UNPIVOT` drops `NULL` values by default, which here is what you want.
</details>

---

## Ideas for later (no automatic check yet)

- **State-level summary:** weighted share of children 0–5 whose mother works full-time, by state (`FIPSST`), with unweighted n. Flag states with n < 30 using `CASE`. Rank states with `RANK() OVER (...)`.
- **Joining sources at the area level:** once ACS and BEA RPP data are loaded, join the state-level NSCH summary to state price levels on the state code. This joins **state summaries**, not people, as the research plan requires.
- **Year-over-year change:** `LAG()` over `SURVEY_YEAR` for a weighted share.
