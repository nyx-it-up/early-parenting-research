-- Missing-data codes per variable among mothers (pooled 2023-2025)
-- Database: data/processed/nsch.duckdb (built by src/build_db.py)

 WITH mothers AS (
      SELECT COLUMNS( '.*_MISS')
      FROM nsch
      WHERE A1_SEX = 2 AND A1_RELATION = 1
  ),
  long AS (
      UNPIVOT mothers
      ON COLUMNS(*)
      INTO NAME variable VALUE code
  )
  SELECT
      REPLACE(variable, '__MISS', '')   AS variable,
      code,
      COUNT(*)                         AS n
  FROM long
  GROUP BY variable, code
  ORDER BY variable, code;
