/* ==========================================================
   05_create_indices_and_cleanup.sql
   ----------------------------------------------------------
   Adds spatial and temporal indexes to improve performance
   for QGIS, notebooks, and dashboards.
   ========================================================== */

-- ----------------------------------------------------------
-- Core table indexes
-- ----------------------------------------------------------

CREATE INDEX IF NOT EXISTS squid_events_geom_idx
ON core.squid_events USING GIST (geom);

CREATE INDEX IF NOT EXISTS squid_events_date_idx
ON core.squid_events (event_date);

CREATE INDEX IF NOT EXISTS squid_events_year_idx
ON core.squid_events (year);

-- ----------------------------------------------------------
-- Polygon grid indexes
-- ----------------------------------------------------------

CREATE INDEX IF NOT EXISTS grid_025deg_poly_geom_idx
ON analysis.grid_025deg_poly
USING GIST (geom);

-- ----------------------------------------------------------
-- Hotspot aggregation indexes
-- ----------------------------------------------------------

CREATE INDEX IF NOT EXISTS squid_hotspots_geom_idx
ON analysis.squid_hotspots
USING GIST (cell_geom);

CREATE INDEX IF NOT EXISTS squid_hotspots_year_idx
ON analysis.squid_hotspots (year);

-- ----------------------------------------------------------
-- Export yearly summary table (unchanged logic) ran in Gitbash
-- ----------------------------------------------------------

/*  \copy (SELECT year, SUM(total_catch_kg) AS total_catch, SUM(vesse
l_days) AS total_effort, SUM(total_catch_kg)/SUM(vessel_days) AS cpue FROM analy
sis.squid_hotspots GROUP BY year ORDER BY year) TO 'hotspot_summary.csv' CSV HEA
DER;*/


