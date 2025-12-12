/* ==========================================================
   03_create_analysis_tables.sql
   ----------------------------------------------------------
   Aggregates fishing events into a 0.25-degree grid for
   spatio-temporal hotspot analysis.
   ========================================================== */

DROP TABLE IF EXISTS analysis.squid_grid_025;

CREATE TABLE analysis.squid_grid_025 AS
SELECT
    ST_SnapToGrid(geom, 0.25, 0.25) AS cell_geom,
    year,
    SUM(squid_kg) AS total_catch,
    COUNT(DISTINCT ctno || '-' || event_date) AS vessel_days
FROM core.squid_events
GROUP BY cell_geom, year;

COMMENT ON TABLE analysis.squid_grid_025 IS 
'Yearly squid catch aggregated into 0.25-degree grid cells.';
