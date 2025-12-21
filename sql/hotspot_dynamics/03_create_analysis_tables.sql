/* ==========================================================
   03a_create_polygon_grid.sql
   ----------------------------------------------------------
   Creates an origin-aligned 0.25-degree POLYGON grid.

   Why polygons?
   - Defines real spatial areas (not snapped points)
   - Enables proper point-in-polygon aggregation
   - Aligns with environmental raster data
   - Is reproducible and defensible for analysis
   ========================================================== */

DROP TABLE IF EXISTS analysis.grid_025deg_poly;

-- Build a grid that fully covers the spatial extent of squid events
CREATE TABLE analysis.grid_025deg_poly AS
WITH bounds AS (
    -- Determine spatial bounds of the dataset
    SELECT
        floor(ST_XMin(extent) / 0.25)::numeric * 0.25 AS xmin,
        ceil(ST_XMax(extent) / 0.25)::numeric * 0.25 AS xmax,
        floor(ST_YMin(extent) / 0.25)::numeric * 0.25 AS ymin,
        ceil(ST_YMax(extent) / 0.25)::numeric * 0.25 AS ymax
    FROM (
        SELECT ST_Extent(geom) AS extent
        FROM core.squid_events
    ) e
)

-- Generate grid cells as polygons
SELECT
    -- Stable unique identifier for each grid cell
    row_number() OVER () AS cell_id,

 -- Create a 0.25° x 0.25° polygon
    ST_SetSRID(
        ST_MakePolygon(
            ST_MakeLine(ARRAY[
                ST_MakePoint(x::double precision, y::double precision),
                ST_MakePoint((x + 0.25)::double precision, y::double precision),
                ST_MakePoint((x + 0.25)::double precision, (y + 0.25)::double precision),
                ST_MakePoint(x::double precision, (y + 0.25)::double precision),
                ST_MakePoint(x::double precision, y::double precision)
            ])
        ),
        4326
    ) AS geom

FROM bounds,
     -- Generate grid coordinates aligned to 0.25° origin
     generate_series(xmin, xmax - 0.25, 0.25) AS x,
     generate_series(ymin, ymax - 0.25, 0.25) AS y;

COMMENT ON TABLE analysis.grid_025deg_poly IS
'Origin-aligned 0.25-degree polygon grid used for spatial aggregation.';

/* ==========================================================
   03b_create_squid_hotspots.sql
   ----------------------------------------------------------
   Aggregates squid fishing events into polygon grid cells.

   - Events remain POINTS
   - Grid cells are POLYGONS
   - Aggregation uses ST_Within (point-in-polygon)
   ========================================================== */

DROP TABLE analysis.squid_hotspots CASCADE;

CREATE TABLE analysis.squid_hotspots AS
SELECT
    -- Grid cell identifier
    g.cell_id,

    -- Polygon geometry for mapping and analysis
    g.geom AS cell_geom,

    -- Temporal dimension
    e.year,

    -- Total squid catch per cell per year
    SUM(e.squid_kg) AS total_catch_kg,

    -- Fishing effort measured as vessel-days
    COUNT(DISTINCT e.ctno || '-' || e.event_date)::INTEGER AS vessel_days,

	-- Squid CPUE calculation using vessel-days
	SUM(e.squid_kg) / NULLIF(COUNT(DISTINCT e.ctno || '-' || e.event_date),0) AS cpue,

	-- Log-transformed CPUE for visualization (base 10)
	CASE 
	    WHEN COUNT(DISTINCT e.ctno || '-' || e.event_date) > 0
	         AND SUM(e.squid_kg) / COUNT(DISTINCT e.ctno || '-' || e.event_date) > 0
	    THEN LN(SUM(e.squid_kg)::double precision / COUNT(DISTINCT e.ctno || '-' || e.event_date)::double precision) / LN(10.0)
	    ELSE NULL
	END AS cpue_log

FROM analysis.grid_025deg_poly g

-- Spatial join: assign each event to the polygon it falls within
JOIN core.squid_events e
    ON ST_Intersects(e.geom, g.geom)

GROUP BY
    g.cell_id,
    g.geom,
    e.year;

COMMENT ON TABLE analysis.squid_hotspots IS
'Yearly squid catch aggregated into 0.25-degree polygon grid cells.';

SELECT * FROM analysis.squid_hotspots;
--SELECT * FROM core.squid_events;
---SELECT * FROM analysis.grid_025deg_poly;