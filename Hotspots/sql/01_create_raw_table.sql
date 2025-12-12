/* ==========================================================
   01_create_raw_table.sql
   ----------------------------------------------------------
   Raw import table with NO cleaning and NO geometry.
   This mirrors the CSV exactly.
   ========================================================== */

DROP TABLE IF EXISTS raw.squid_raw;

CREATE TABLE raw.squid_raw (
    pointid INTEGER,
    ctno INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    lon DOUBLE PRECISION,
    lat DOUBLE PRECISION,
    water_temp DOUBLE PRECISION,
    ssh DOUBLE PRECISION,
    depth DOUBLE PRECISION,
    chlor_a_mg_m3 DOUBLE PRECISION,
    sqcatch_kg DOUBLE PRECISION
);

-- Load data (adjust path)
-- \copy raw.squid_raw FROM 'data_raw/squid_20years.csv' CSV HEADER;

