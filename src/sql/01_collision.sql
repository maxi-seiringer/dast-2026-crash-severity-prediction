CREATE TABLE IF NOT EXISTS collision (
    collision_index VARCHAR(20) PRIMARY KEY,

    collision_year INTEGER NOT NULL,
    collision_ref_no VARCHAR(20),

    location_easting_osgr INTEGER,
    location_northing_osgr INTEGER,

    longitude DECIMAL(10,6),
    latitude DECIMAL(10,6),

    police_force VARCHAR(100),

    collision_severity VARCHAR(50),

    number_of_vehicles INTEGER,
    number_of_casualties INTEGER,

    date DATE,
    day_of_week VARCHAR(20),
    time TIME,

    local_authority_district VARCHAR(100),
    local_authority_ons_district VARCHAR(100),
    local_authority_highway VARCHAR(100),
    local_authority_highway_current VARCHAR(100),

    first_road_class VARCHAR(50),
    first_road_number INTEGER,

    road_type VARCHAR(100),

    speed_limit INTEGER,

    junction_detail VARCHAR(100),
    junction_control VARCHAR(100),

    second_road_class VARCHAR(50),
    second_road_number INTEGER,

    pedestrian_crossing VARCHAR(100),

    light_conditions VARCHAR(100),

    weather_conditions VARCHAR(100),

    road_surface_conditions VARCHAR(100),

    special_conditions_at_site VARCHAR(100),

    carriageway_hazards VARCHAR(100),

    urban_or_rural_area VARCHAR(50),

    did_police_officer_attend_scene_of_accident BOOLEAN,

    trunk_road_flag BOOLEAN,

    lsoa_of_accident_location VARCHAR(50),

    enhanced_severity_collision VARCHAR(50),

    collision_injury_based BOOLEAN,

    collision_adjusted_severity_serious BOOLEAN,
    collision_adjusted_severity_slight BOOLEAN
);