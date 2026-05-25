CREATE TABLE IF NOT EXISTS casualty (

    casualty_id SERIAL PRIMARY KEY,

    collision_index VARCHAR(20) NOT NULL,

    vehicle_reference INTEGER,

    casualty_reference INTEGER,

    casualty_class VARCHAR(50),

    sex_of_casualty VARCHAR(20),

    age_of_casualty INTEGER,

    age_band_of_casualty VARCHAR(50),

    casualty_severity VARCHAR(50),

    pedestrian_location VARCHAR(100),

    pedestrian_movement VARCHAR(100),

    car_passenger VARCHAR(50),

    bus_or_coach_passenger VARCHAR(50),

    pedestrian_road_maintenance_worker VARCHAR(50),

    casualty_type VARCHAR(100),

    casualty_imd_decile INTEGER,

    lsoa_of_casualty VARCHAR(50),

    enhanced_casualty_severity VARCHAR(50),

    casualty_injury_based BOOLEAN,

    casualty_adjusted_severity_serious BOOLEAN,

    casualty_adjusted_severity_slight BOOLEAN,

    casualty_distance_banding VARCHAR(50),

    FOREIGN KEY (collision_index)
        REFERENCES collision(collision_index)
);