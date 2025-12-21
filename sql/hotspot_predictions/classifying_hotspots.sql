-- Rank spatial cells by total catch within each year
-- and classify the top quartile (top 25%) as fishing hotspots
WITH ranked AS (
    SELECT
        cell_geom,               -- Spatial grid cell geometry
        year,                    -- Year of observation
        total_catch_kg,          -- Total catch used for ranking

        -- Assign quartiles (1 = highest catch, 4 = lowest)
        NTILE(4) OVER (
            PARTITION BY year    -- Compute quartiles separately for each year
            ORDER BY total_catch_kg DESC
        ) AS catch_quartile
    FROM analysis.ml_features
)

-- Update the hotspot_class label in the main table
UPDATE analysis.ml_features mf
SET hotspot_class = CASE
    WHEN r.catch_quartile = 1 THEN 1   -- Top 25% of catches = hotspot
    ELSE 0                             -- Remaining 75% = non-hotspot
END
FROM ranked r
WHERE
    mf.cell_geom = r.cell_geom         -- Match the same spatial cell
    AND mf.year = r.year;              -- Match the same year
