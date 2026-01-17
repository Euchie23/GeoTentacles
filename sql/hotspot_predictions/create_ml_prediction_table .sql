-- ML prediction table derived from the squid_hotspots dataset
-- first check if any table already exists
DROP TABLE IF EXISTS analysis.ml_prediction;

-- Create base table to store machine learning features
CREATE TABLE analysis.ml_prediction AS
SELECT
    cell_geom,                						   -- Spatial grid cell geometry
    year,                      					   -- Year of observation
    SUM(total_catch_kg) AS total_catch_kg,            -- Total squid catch in kilograms
    SUM(vessel_days)    AS vessel_days,			   -- Total fishing effort (vessel-days)
    
    -- Catch Per Unit Effort (CPUE); avoids division by zero
    SUM(total_catch_kg) / NULLIF(SUM(vessel_days), 0) AS cpue
FROM analysis.squid_hotspots_monthly
GROUP BY cell_geom, year;

-- Add a column to store the hotspot classification label
ALTER TABLE analysis.ml_prediction
ADD COLUMN hotspot_class INTEGER;

-- Classifying Hotspots
WITH ranked AS (
    SELECT
        cell_geom,
        year,
        NTILE(4) OVER (
            PARTITION BY year
            ORDER BY total_catch_kg DESC
        ) AS catch_quartile
    FROM analysis.ml_prediction
)
UPDATE analysis.ml_prediction mp
SET hotspot_class = CASE
    WHEN r.catch_quartile = 1 THEN 1
    ELSE 0
END
FROM ranked r
WHERE
    mp.cell_geom = r.cell_geom
    AND mp.year = r.year;

-- Adding columns to analysis.ml_prediction
ALTER TABLE analysis.ml_prediction
ADD COLUMN mean_depth DOUBLE PRECISION,
ADD COLUMN mean_sst DOUBLE PRECISION,
ADD COLUMN mean_ssh DOUBLE PRECISION,
ADD COLUMN mean_chlor_a DOUBLE PRECISION;

---Adding month to table
ALTER TABLE analysis.ml_prediction
ADD COLUMN month INTEGER;

/*UPDATE analysis.ml_prediction mp
SET month = shm.month
FROM analysis.squid_hotspots_monthly shm
JOIN analysis.grid_025deg_poly g
  ON ST_Intersects(shm.cell_geom, g.geom)
WHERE
    ST_Intersects(mp.cell_geom, g.geom)
    AND mp.year = shm.year;*/

	WITH month_ranked AS (
  SELECT
    cell_geom,
    year,
    month,
    ROW_NUMBER() OVER (
      PARTITION BY cell_geom, year
      ORDER BY total_catch_kg DESC
    ) AS rn
  FROM analysis.squid_hotspots_monthly
)
UPDATE analysis.ml_prediction t
SET month = m.month
FROM month_ranked m
WHERE t.cell_geom = m.cell_geom
  AND t.year = m.year
  AND m.rn = 1;


WITH vessel_day_means AS (
    SELECT
        g.geom AS cell_geom,
        EXTRACT(YEAR FROM se.event_date) AS year,
        AVG(se.depth) AS mean_depth,
        AVG(se.water_temp) AS mean_sst
    FROM core.squid_events se
    JOIN analysis.grid_025deg_poly g
      ON ST_Intersects(se.geom, g.geom)
    GROUP BY g.geom, EXTRACT(YEAR FROM se.event_date)
)
UPDATE analysis.ml_prediction mp
SET
    mean_depth = vdm.mean_depth,
    mean_sst   = vdm.mean_sst
FROM vessel_day_means vdm
WHERE mp.cell_geom = vdm.cell_geom
    AND mp.year = vdm.year;

	WITH monthly_env AS (
    SELECT
        g.geom AS cell_geom,
        se.year,
        AVG(se.ssh)     AS mean_ssh,
        AVG(se.chlor_a) AS mean_chlor_a
    FROM core.squid_events se
    JOIN analysis.grid_025deg_poly g
      ON ST_Intersects(se.geom, g.geom)
    GROUP BY g.geom, se.year
)
UPDATE analysis.ml_prediction mp
SET
    mean_ssh     = me.mean_ssh,
    mean_chlor_a = me.mean_chlor_a
FROM monthly_env me
WHERE
    ST_Intersects(mp.cell_geom, me.cell_geom)
    AND mp.year = me.year;


-- Checking class balance  
/*SELECT
    year,
    COUNT(*) AS cells,
    SUM(hotspot_class) AS hotspots
FROM analysis.ml_prediction
GROUP BY year
ORDER BY year;*/

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
FROM analysis.ml_prediction;*/

select * from analysis.ml_prediction;
select * from analysis.ml_features LIMIT 10;
select * from analysis.squid_hotspots;