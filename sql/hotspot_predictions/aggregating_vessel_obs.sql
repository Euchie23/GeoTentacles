-- Create a Common Table Expression (CTE) that aggregates environmental variables
-- Step 1: Aggregate environmental variables per month (Jan–June)
WITH env_monthly AS (
    SELECT
        g.geom AS cell_geom,
        e.year,
        e.month,
        AVG(e.depth) AS mean_depth_month,
        AVG(e.water_temp) AS mean_sst_month,
        AVG(DISTINCT e.ssh) AS ssh_month,
        AVG(DISTINCT e.chlor_a) AS chlor_a_month
    FROM core.squid_events e
    JOIN analysis.grid_025deg_poly g
      ON ST_Intersects(e.geom, g.geom)
    WHERE e.month BETWEEN 1 AND 6
    GROUP BY g.geom, e.year, e.month
),

-- Step 2: Aggregate monthly values to annual per grid cell
annual_agg AS (
    SELECT
        cell_geom,
        year,
        AVG(mean_depth_month) AS mean_depth,
        AVG(mean_sst_month) AS mean_sst,
        AVG(ssh_month) AS mean_ssh,
        AVG(chlor_a_month) AS mean_chlor_a
    FROM env_monthly
    GROUP BY cell_geom, year
)

-- Step 3: Update ML features table
UPDATE analysis.ml_features mf
SET
    mean_depth = aa.mean_depth,
    mean_sst = aa.mean_sst,
    mean_ssh = aa.mean_ssh,
    mean_chlor_a = aa.mean_chlor_a
FROM annual_agg aa
WHERE mf.cell_geom = aa.cell_geom
  AND mf.year = aa.year;

-- Step 4: Global median imputation for missing values
UPDATE analysis.ml_features
SET
    mean_depth = COALESCE(
        mean_depth,
        (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mean_depth)
         FROM analysis.ml_features)
    ),
    mean_sst = COALESCE(
        mean_sst,
        (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mean_sst)
         FROM analysis.ml_features)
    ),
    mean_ssh = COALESCE(
        mean_ssh,
        (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mean_ssh)
         FROM analysis.ml_features)
    ),
    mean_chlor_a = COALESCE(
        mean_chlor_a,
        (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mean_chlor_a)
         FROM analysis.ml_features)
    );

-- Optional: check missing values
SELECT
    COUNT(*) FILTER (WHERE mean_depth IS NULL) AS missing_depth,
    COUNT(*) FILTER (WHERE mean_sst IS NULL) AS missing_sst,
    COUNT(*) FILTER (WHERE mean_ssh IS NULL) AS missing_ssh,
    COUNT(*) FILTER (WHERE mean_chlor_a IS NULL) AS missing_chlor
FROM analysis.ml_features;

-- Before imputation depth has 36 missing values, sst has 0, ssh has 11 and chlor_a has 23


-- Checking ranges
/*SELECT
    MIN(mean_sst), MAX(mean_sst),
    MIN(mean_depth), MAX(mean_depth),
    MIN(mean_chlor_a), MAX(mean_chlor_a)
FROM analysis.ml_features;*/
