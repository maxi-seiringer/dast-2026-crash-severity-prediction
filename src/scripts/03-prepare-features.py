"""
03-prepare-features.py
Clean the merged dataset, engineer features, and split into train/val/test.

Run from the repo root:
    python src/scripts/03-prepare-features.py
"""

from pathlib import Path
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import sys
# Ensure `src/` is importable when running this script from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from utils.dbrepo import DBRepoClient, DBRepoError

load_dotenv()

EXPECTED_DB_ID = "3d81c073-e5fd-49b9-9536-b75ed490ca3e"
os.environ.setdefault("DBREPO_DB_ID", EXPECTED_DB_ID)

# --- Paths ---
REPO_ROOT = Path(__file__).resolve().parents[2]
INTERIM   = REPO_ROOT / "data" / "interim"
PROCESSED = REPO_ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

# --- Feature and target column names ---
FEATURE_COLS = [
    "road_type", "speed_limit", "weather_conditions", "light_conditions",
    "road_surface_conditions", "day_of_week", "hour_of_day",
    "number_of_vehicles", "vehicle_type",
]
TARGET_COL = "casualty_severity"

def load_merged_from_api():
    interim_file = INTERIM / "stats19-collision-vehicle-casualty-2023-interim-v1.csv"
    if interim_file.exists():
        df = pd.read_csv(interim_file)
        print(f"Loaded {len(df):,} rows from {interim_file.relative_to(REPO_ROOT)}")
        return df

    client = DBRepoClient()
    if client.db_id != EXPECTED_DB_ID:
        raise DBRepoError(
            f"DBREPO_DB_ID={client.db_id} does not match expected {EXPECTED_DB_ID}."
        )

    required_views = ["v_severity_distribution", "v_collision_summary", "v_feature_null_check"]
    available_views = set(client.list_views())
    missing = [v for v in required_views if v not in available_views]
    if missing:
        raise DBRepoError(f"Missing required DBRepo views: {missing}")

    collision_view = client.get_view("v_collision_summary")
    casualty = client.get_table("casualty")
    vehicle = client.get_table("vehicle")

    df = casualty.merge(
        collision_view[["collision_index", "road_type", "speed_limit", "weather_conditions",
                        "light_conditions", "road_surface_conditions", "time", "day_of_week", "number_of_vehicles"]],
        on="collision_index", how="inner"
    )
    df = df.merge(
        vehicle[["collision_index", "vehicle_reference", "vehicle_type"]],
        on=["collision_index", "vehicle_reference"], how="inner"
    )
    print(f"Fetched and merged {len(df):,} rows from DBRepo views/tables")
    return df


# --- Load the merged interim data from DBRepo view ---
df = load_merged_from_api()

# --- Derive hour of day from the time column (format HH:MM) ---
df["hour_of_day"] = pd.to_datetime(df["time"], format="%H:%M", errors="coerce").dt.hour

# --- Replace STATS19 sentinel codes with NaN ---
# -1, 9, and 99 are used in STATS19 to indicate unknown or missing values
for col in FEATURE_COLS:
    if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].replace([-1, 9, 99], np.nan)

# --- Drop rows that are missing any feature or the target label ---
features = [c for c in FEATURE_COLS if c in df.columns]
df = df.dropna(subset=features + [TARGET_COL])
print(f"Rows after cleaning: {len(df):,}")

# --- Build feature matrix and target vector ---
# Fill any remaining NaN with the column median as a safety net
X = df[features].fillna(df[features].median(numeric_only=True))
y = df[TARGET_COL].astype(int)

# --- Split 70 / 15 / 15 ---
# First split off 30% as a temporary pool, then split that equally into val and test
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
X_val,   X_test, y_val,   y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

print(f"Train : {len(X_train):,} rows")
print(f"Val   : {len(X_val):,} rows")
print(f"Test  : {len(X_test):,} rows")

# --- Save each split as a CSV file ---
for name, Xs, ys in [("train", X_train, y_train), ("val", X_val, y_val), ("test", X_test, y_test)]:
    out = Xs.copy()
    out[TARGET_COL] = ys.values
    out.to_csv(PROCESSED / f"stats19-features-{name}-2023-processed-v1.csv", index=False)
    print(f"Saved: stats19-features-{name}-2023-processed-v1.csv")