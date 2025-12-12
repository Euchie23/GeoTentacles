/* ==========================================================
   02_build_core_tables.sql
   ----------------------------------------------------------
   Creates the cleaned core table:
   - fixes data types
   - adds event_date
   - creates geometry (EPSG:4326)
   ========================================================== */

DROP TABLE IF EXISTS core.squid_events;

CREATE TABLE core.squid_events AS
SELECT
    pointid,
    ctno,
    year,
    month,
    day,
    make_date(year, month, day) AS event_date,
    lon,
    lat,
    water_temp,
    ssh,
    depth,
    chlor_a_mg_m3 AS chlor_a,
    sqcatch_kg AS squid_kg,
    ST_SetSRID(ST_MakePoint(lon, lat), 4326) AS geom
FROM raw.squid_raw;

COMMENT ON TABLE core.squid_events IS 
'Cleaned squid fishing log data with geometry for spatio-temporal analysis.';

/* Basic cleaning */
DELETE FROM core.squid_events
WHERE lon IS NULL OR lat IS NULL OR sqcatch_kg IS NULL;
