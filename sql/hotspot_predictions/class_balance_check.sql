
--Sanity Check for class balance
SELECT
    year,
    COUNT(*) AS cells,
    SUM(hotspot_class) AS hotspots
FROM analysis.ml_features
GROUP BY year
ORDER BY year;
