-- Exercise 01 - the mother filter
-- Instructions and hints: sql/README.md
-- Expected output columns: survey_year, all_children, female_respondent, mothers
-- Check: .venv/Scripts/python.exe src/check_sql.py sql/01_mother_flow.sql

-- Write your query below.

SELECT
      SURVEY_YEAR AS survey_year,
      COUNT(*)                              AS all_children,
      COUNT(*) FILTER (WHERE A1_SEX = 2)        AS female_respondent,
      COUNT(*) FILTER (WHERE A1_SEX = 2 AND A1_RELATION = 1)        AS mothers
  FROM nsch
  GROUP BY survey_year
  ORDER BY survey_year;

