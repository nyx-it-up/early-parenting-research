-- Weighted employment shares (%) within each child age band, mothers with an employment answer
-- Database: data/processed/nsch.duckdb (built by src/build_db.py)

WITH totals AS (
      SELECT
          b.band_primary          AS band,
          e.label                 AS employment,
          SUM(c.FWC / 3)             AS weighted
      FROM nsch AS c
        JOIN age_bands AS b
            ON c.SC_AGE_YEARS = b.age
        INNER JOIN employment_labels AS e
            ON c.A1_EMPLOYED_R = e.code
        WHERE c.A1_SEX = 2 AND c.A1_RELATION = 1
        GROUP BY band, employment
        ORDER BY band
  )
  SELECT
      band,
      employment,
      ROUND(100 * weighted / SUM(weighted) OVER (PARTITION BY band), 1) AS share_pct
  FROM totals
  ORDER BY band, employment;
