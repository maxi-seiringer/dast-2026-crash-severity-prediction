CREATE TABLE IF NOT EXISTS vehicle(
    vehicle_id SERIAL PRIMARY KEY,

    collision_index VARCHAR(20) NOT NULL,

    vehicle_reference INTEGER,

    vehicle_type VARCHAR(100),

    towing_and_articulation VARCHAR(100),

    vehicle_manoeuvre VARCHAR(100),

    vehicle_direction_from VARCHAR(50),
    vehicle_direction_to VARCHAR(50),

    vehicle_location_restricted_lane VARCHAR(100),

    junction_location VARCHAR(100),

    skidding_and_overturning VARCHAR(100),

    hit_object_in_carriageway VARCHAR(100),

    vehicle_leaving_carriageway VARCHAR(100),

    hit_object_off_carriageway VARCHAR(100),

    first_point_of_impact VARCHAR(100),

    vehicle_left_hand_drive BOOLEAN,

    journey_purpose_of_driver VARCHAR(100),

    sex_of_driver VARCHAR(20),

    age_of_driver INTEGER,

    age_band_of_driver VARCHAR(50),

    engine_capacity_cc INTEGER,

    propulsion_code VARCHAR(50),

    age_of_vehicle INTEGER,

    generic_make_model VARCHAR(100),

    driver_imd_decile INTEGER,

    lsoa_of_driver VARCHAR(50),

    escooter_flag BOOLEAN,

    driver_distance_banding VARCHAR(50),

    FOREIGN KEY (collision_index)
        REFERENCES collision(collision_index)
);