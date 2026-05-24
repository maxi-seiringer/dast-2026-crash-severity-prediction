-- joins collision, vehicle and casualty into one flat table with all features and the target label, ready for model training.
CREATE OR REPLACE VIEW v_ml_features AS
SELECT
    cas.casualty_id,
    c.collision_index,
    cas.casualty_severity,
    c.road_type,
    c.speed_limit,
    c.weather_conditions,
    c.light_conditions,
    c.road_surface_conditions,
    c.time,
    c.day_of_week,
    c.number_of_vehicles,
    v.vehicle_type
FROM casualty cas
         JOIN collision c ON cas.collision_index = c.collision_index
         JOIN vehicle v ON cas.collision_index = v.collision_index
    AND cas.vehicle_reference = v.vehicle_reference;

--Shows how many casualties fall into each severity class (Slight, Serious, Fatal) and what percentage each class makes up.
CREATE OR REPLACE VIEW v_severity_distribution AS
SELECT
    casualty_severity,
    COUNT(*) AS total_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM casualty
GROUP BY casualty_severity
ORDER BY total_count DESC;

--One row per collision with the most important scene conditions and the worst severity recorded among all casualties involved.
CREATE OR REPLACE VIEW v_collision_summary AS
SELECT
    c.collision_index,
    c.date,
    c.day_of_week,
    c.time,
    c.road_type,
    c.speed_limit,
    c.weather_conditions,
    c.light_conditions,
    c.road_surface_conditions,
    c.number_of_vehicles,
    c.number_of_casualties,
    CASE
        WHEN bool_or(cas.casualty_severity = 'Fatal')   THEN 'Fatal'
        WHEN bool_or(cas.casualty_severity = 'Serious') THEN 'Serious'
        ELSE 'Slight'
        END AS worst_severity
FROM collision c
         JOIN casualty cas ON c.collision_index = cas.collision_index
GROUP BY
    c.collision_index, c.date, c.day_of_week, c.time,
    c.road_type, c.speed_limit, c.weather_conditions,
    c.light_conditions, c.road_surface_conditions,
    c.number_of_vehicles, c.number_of_casualties;

--Counts missing values for each ML feature column so data quality issues can be spotted before training.
CREATE OR REPLACE VIEW v_feature_null_check AS
SELECT
    'road_type'              AS feature, COUNT(*) FILTER (WHERE road_type IS NULL)              AS null_count, COUNT(*) AS total FROM collision
UNION ALL SELECT 'speed_limit',          COUNT(*) FILTER (WHERE speed_limit IS NULL),          COUNT(*) FROM collision
UNION ALL SELECT 'weather_conditions',   COUNT(*) FILTER (WHERE weather_conditions IS NULL),   COUNT(*) FROM collision
UNION ALL SELECT 'light_conditions',     COUNT(*) FILTER (WHERE light_conditions IS NULL),     COUNT(*) FROM collision
UNION ALL SELECT 'road_surface_conditions', COUNT(*) FILTER (WHERE road_surface_conditions IS NULL), COUNT(*) FROM collision
UNION ALL SELECT 'time',                 COUNT(*) FILTER (WHERE time IS NULL),                 COUNT(*) FROM collision
UNION ALL SELECT 'day_of_week',          COUNT(*) FILTER (WHERE day_of_week IS NULL),          COUNT(*) FROM collision
UNION ALL SELECT 'number_of_vehicles',   COUNT(*) FILTER (WHERE number_of_vehicles IS NULL),   COUNT(*) FROM collision
UNION ALL SELECT 'vehicle_type',         COUNT(*) FILTER (WHERE vehicle_type IS NULL),         COUNT(*) FROM vehicle
UNION ALL SELECT 'casualty_severity',    COUNT(*) FILTER (WHERE casualty_severity IS NULL),    COUNT(*) FROM casualty;