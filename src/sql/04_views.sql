-- DBRepo-compatible views used by the ML pipeline.
-- These are documented here for reproducibility even if the DBRepo backend
-- only supports a subset of the SQL shown in the notebook.

-- Severity class distribution for sanity checks and reporting.
CREATE OR REPLACE VIEW v_severity_distribution AS
SELECT
    casualty_severity,
    COUNT(*) AS total_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM casualty
GROUP BY casualty_severity
ORDER BY total_count DESC;

-- Collision-level scene summary used as the main collision feature source.
CREATE OR REPLACE VIEW v_collision_summary AS
SELECT
    collision_index,
    date,
    day_of_week,
    time,
    road_type,
    speed_limit,
    weather_conditions,
    light_conditions,
    road_surface_conditions,
    number_of_vehicles,
    number_of_casualties
FROM collision;

-- Basic data-quality check for the casualty table.
CREATE OR REPLACE VIEW v_feature_null_check AS
SELECT
    'casualty_id' AS feature,
    COUNT(*) FILTER (WHERE casualty_id IS NULL) AS null_count,
    COUNT(*) AS total_count
FROM casualty
UNION ALL SELECT 'casualty_severity', COUNT(*) FILTER (WHERE casualty_severity IS NULL), COUNT(*) FROM casualty
UNION ALL SELECT 'age_of_casualty', COUNT(*) FILTER (WHERE age_of_casualty IS NULL), COUNT(*) FROM casualty
UNION ALL SELECT 'casualty_type', COUNT(*) FILTER (WHERE casualty_type IS NULL), COUNT(*) FROM casualty;
