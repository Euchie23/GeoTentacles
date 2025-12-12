/* ==========================================================
   04_create_views_for_apps.sql
   ----------------------------------------------------------
   Provides simple public-facing views for visualization
   layers in QGIS and data access in Shiny dashboards.
   ========================================================== */

DROP VIEW IF EXISTS public.squid_hotspots;

CREATE VIEW public.squid_hotspots AS
SELECT *
FROM analysis.squid_grid_025;

COMMENT ON VIEW public.squid_hotspots IS 
'View used by QGIS and Shiny for hotspot visualization.';
