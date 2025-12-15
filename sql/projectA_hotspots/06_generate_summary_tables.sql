COPY (
    SELECT
        year,
        SUM(total_catch_kg) AS total_catch,
        SUM(vessel_days) AS total_effort,
        SUM(total_catch_kg)/SUM(vessel_days) AS cpue
    FROM analysis.squid_hotspots
    GROUP BY year
    ORDER BY year
) TO '/path/to/projectA_hotspots/outputs/tables/hotspot_summary.csv'
CSV HEADER;

-- \copy (SELECT year, SUM(total_catch_kg) AS total_catch, SUM(vesse
--l_days) AS total_effort, SUM(total_catch_kg)/SUM(vessel_days) AS cpue FROM analy
--sis.squid_hotspots GROUP BY year ORDER BY year) TO 'C:/Users/euchb/OneDrive/Docu
--ments/GitHub/Squid_Fest/Squid_SQL/projectA_hotspots/outputs/tables/hotspot_summa
--ry.csv' WITH CSV HEADER;
