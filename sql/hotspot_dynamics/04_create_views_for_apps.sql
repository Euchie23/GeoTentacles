/* ==========================================================
   04_create_views_for_apps.sql
   ----------------------------------------------------------
   Public-facing views for QGIS and dashboards.
   ========================================================== */

DROP VIEW IF EXISTS public.squid_hotspots;

CREATE VIEW public.squid_hotspots AS
SELECT *
FROM analysis.squid_hotspots;

COMMENT ON VIEW public.squid_hotspots IS
'Polygon-based squid catch hotspots for visualization and apps.';

