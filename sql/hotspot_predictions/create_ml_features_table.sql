-- ML features table derived from the squid_hotspots dataset
-- first check if any table already exists
DROP TABLE IF EXISTS analysis.ml_features;

-- Create base table to store machine learning features
CREATE TABLE analysis.ml_features AS
SELECT
    cell_geom,                 -- Spatial grid cell geometry
    year,                      -- Year of observation
    total_catch_kg,            -- Total squid catch in kilograms
    vessel_days,               -- Total fishing effort (vessel-days)
    
    -- Catch Per Unit Effort (CPUE); avoids division by zero
    total_catch_kg / NULLIF(vessel_days, 0) AS cpue
FROM analysis.squid_hotspots;

-- Add a column to store the hotspot classification label
ALTER TABLE analysis.ml_features
ADD COLUMN hotspot_class INTEGER;

-- Classifying Hotspots
WITH ranked AS (
    SELECT
        cell_geom,
        year,
        total_catch_kg,
        NTILE(4) OVER (
            PARTITION BY year
            ORDER BY total_catch_kg DESC
        ) AS catch_quartile
    FROM analysis.ml_features
)
UPDATE analysis.ml_features mf
SET hotspot_class = CASE
    WHEN r.catch_quartile = 1 THEN 1
    ELSE 0
END
FROM ranked r
WHERE
    mf.cell_geom = r.cell_geom
    AND mf.year = r.year;

-- Adding columns to analysis.ml_features
ALTER TABLE analysis.ml_features
ADD COLUMN mean_depth DOUBLE PRECISION,
ADD COLUMN mean_sst DOUBLE PRECISION,
ADD COLUMN mean_ssh DOUBLE PRECISION,
ADD COLUMN mean_chlor_a DOUBLE PRECISION;

-- Checking class balance  
SELECT
    year,
    COUNT(*) AS cells,
    SUM(hotspot_class) AS hotspots
FROM analysis.ml_features
GROUP BY year
ORDER BY year;

/*upon first glance i can see that the year 2000 had the most 
number of hotspots which decreased slightly in 2001 and then 
consiserably the years after up until 2020.. indicating either 
reduced numbers in squid population or more enforced regulation on 
squid fishing in that region or change in squid migration path. */ 

-- Checing CPUE values
/*SELECT
    MIN(cpue),
    MAX(cpue),
    AVG(cpue)
FROM analysis.ml_features;*/

