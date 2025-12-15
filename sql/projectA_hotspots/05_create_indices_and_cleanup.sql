/* ==========================================================
   05_create_indices_and_cleanup.sql
   ----------------------------------------------------------
   Adds spatial and temporal indexes to dramatically improve
   performance for QGIS, R, and Shiny.
   ========================================================== */

-- Core table indexes
CREATE INDEX IF NOT EXISTS squid_events_geom_idx 
ON core.squid_events USING GIST (geom);

CREATE INDEX IF NOT EXISTS squid_events_date_idx 
ON core.squid_events (event_date);

CREATE INDEX IF NOT EXISTS squid_events_year_idx 
ON core.squid_events (year);

-- Analysis table indexes
CREATE INDEX IF NOT EXISTS squid_grid_025_geom_idx 
ON analysis.squid_grid_025 USING GIST (cell_geom);

CREATE INDEX IF NOT EXISTS squid_grid_025_year_idx 
ON analysis.squid_grid_025 (year);

