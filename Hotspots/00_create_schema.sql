
/* ==========================================================
   00_setup_schemas.sql
   ----------------------------------------------------------
   Creates the schema structure for Project A.
   This script is safe to run multiple times.
   ========================================================== */

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS analysis;
CREATE SCHEMA IF NOT EXISTS metadata;
CREATE SCHEMA IF NOT EXISTS public;

