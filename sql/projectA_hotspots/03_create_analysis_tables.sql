/* ==========================================================
   03_create_analysis_tables.sql
   ----------------------------------------------------------
   Aggregates fishing events into a 0.25-degree grid for
   spatio-temporal hotspot analysis.
   ========================================================== */

-- 1. Create 0.25° grid from squid events
DROP TABLE IF EXISTS analysis.grid_025deg;

CREATE TABLE analysis.grid_025deg AS
SELECT DISTINCT
    ST_SnapToGrid(geom, 0.25, 0.25) AS geom
FROM core.squid_events;


--2. Aggregate catch per grid cell per year
DROP TABLE IF EXISTS analysis.squid_hotspots;

CREATE TABLE analysis.squid_hotspots AS
SELECT
    ST_SnapToGrid(geom, 0.25, 0.25) AS cell_geom,
    year,
    SUM(squid_kg) AS total_catch_kg,
    COUNT(DISTINCT ctno || '-' || event_date) AS vessel_days
FROM core.squid_events
GROUP BY year, ST_SnapToGrid(geom, 0.25, 0.25);

COMMENT ON TABLE analysis.squid_hotspots IS 
'Yearly squid catch aggregated into 0.25-degree grid cells.';
