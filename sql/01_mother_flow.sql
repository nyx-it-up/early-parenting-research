-- Mother definition: children per survey year at each step
-- Database: data/processed/nsch.duckdb (built by src/build_db.py)

SELECT
      SURVEY_YEAR AS survey_year,
      COUNT(*)                              AS all_children,
      COUNT(*) FILTER (WHERE A1_SEX = 2)        AS female_respondent,
      COUNT(*) FILTER (WHERE A1_SEX = 2 AND A1_RELATION = 1)        AS mothers
  FROM nsch
  GROUP BY survey_year
  ORDER BY survey_year;
