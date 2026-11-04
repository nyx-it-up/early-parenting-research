-- Mothers by child age band x employment status (unweighted n, pooled 2023-2025)
-- Database: data/processed/nsch.duckdb (built by src/build_db.py)

SELECT
    b.band_primary                 AS band,
    COALESCE(e.label, 'Missing')     AS employment,
    COUNT(*)                       AS n
FROM nsch AS c
JOIN age_bands AS b
    ON c.SC_AGE_YEARS = b.age
LEFT JOIN employment_labels AS e
    ON c.A1_EMPLOYED_R = e.code
WHERE c.A1_SEX = 2 AND c.A1_RELATION = 1
GROUP BY band, employment
ORDER BY band;
