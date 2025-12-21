
--- CPUE value check
SELECT
    MIN(cpue),
    MAX(cpue),
    AVG(cpue)
FROM analysis.ml_features;
