"""
01-load-merge-api.py
Fetch the merged feature table directly from DBRepo (table or view).
Falls back to local CSV merge if DBRepo is unavailable.
"""

from pathlib import Path
import os
import pandas as pd
from dotenv import load_dotenv

import sys
from pathlib import Path as _Path
# Ensure `src/` is importable when running this script from the repo root
REPO_ROOT = _Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
from utils.dbrepo import DBRepoClient, DBRepoError

load_dotenv(dotenv_path=REPO_ROOT / ".env")

DEFAULT_API_BASE = "https://test.dbrepo.tuwien.ac.at"
EXPECTED_DB_ID = "3d81c073-e5fd-49b9-9536-b75ed490ca3e"
os.environ.setdefault("DBREPO_DB_ID", EXPECTED_DB_ID)

# --- Config ---
# Prefer environment variables: DBREPO_API_BASE, DBREPO_DB_ID, DBREPO_USER, DBREPO_PASSWORD
INTERIM   = REPO_ROOT / "data" / "interim"
INTERIM.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "data" / "raw"

def main():
    client = DBRepoClient(api_base=DEFAULT_API_BASE, db_id=EXPECTED_DB_ID)
    if client.db_id != EXPECTED_DB_ID:
        raise DBRepoError(
            f"DBREPO_DB_ID={client.db_id} does not match expected {EXPECTED_DB_ID}."
        )
    print(f"Using DBRepo database ID: {client.db_id}")

    required_views = ["v_severity_distribution", "v_collision_summary", "v_feature_null_check"]
    dbrepo_ready = True
    try:
        available_views = set(client.list_views())
        missing = [v for v in required_views if v not in available_views]
        if missing:
            print(f"Warning: missing required DBRepo views: {missing}")
            dbrepo_ready = False
    except DBRepoError as e:
        print(f"Warning: DBRepo view check failed ({e}).")
        print("Continuing with local fallback. Set DBREPO_USER and DBREPO_PASSWORD to enable DBRepo access.")
        dbrepo_ready = False

    df = None
    
    # Strategy 1: Try to fetch t_ml_features table (materialized ML features)
    if dbrepo_ready:
        print("Strategy 1: Attempting to load t_ml_features table from DBRepo...")
        try:
            df = client.get_table("t_ml_features")
            if not df.empty:
                print(f"✓ Loaded {len(df):,} rows from DBRepo table 't_ml_features'")
            else:
                print("  ✗ t_ml_features is empty")
                df = None
        except DBRepoError as e:
            print(f"  ✗ Table not available: {e}")
    
    # Strategy 2: Build the merge from DBRepo new views + base tables
    if df is None and dbrepo_ready:
        print("\nStrategy 2: Attempting to load and merge from DBRepo views and tables...")
        try:
            # New view used here for collision-level explanatory features.
            collision_view = client.get_view("v_collision_summary")
            print(
                "  Using views: v_collision_summary (data source), "
                "v_feature_null_check (presence check), v_severity_distribution (presence check)"
            )

            casualty = client.get_table("casualty")
            vehicle = client.get_table("vehicle")

            print(f"  Loaded tables: casualty ({len(casualty):,}), vehicle ({len(vehicle):,})")

            df = casualty.merge(
                collision_view[["collision_index", "road_type", "speed_limit", "weather_conditions",
                                "light_conditions", "road_surface_conditions", "time", "day_of_week", "number_of_vehicles"]],
                on="collision_index", how="inner"
            )
            df = df.merge(
                vehicle[["collision_index", "vehicle_reference", "vehicle_type"]],
                on=["collision_index", "vehicle_reference"], how="inner"
            )
            print(f"✓ Merged from DBRepo tables: {len(df):,} rows")
        except DBRepoError as e:
            print(f"  ✗ Could not merge DBRepo tables: {e}")

    # Strategy 3: Fall back to local CSV merge
    if df is None:
        print("\nStrategy 3: Falling back to local CSV merge...")
        print("  Loading casualty, collision, vehicle from data/raw/...")
        try:
            casualty = pd.read_csv(RAW_DIR / "stats19-casualty-2023-raw-v1.csv")
            collision = pd.read_csv(RAW_DIR / "stats19-collision-2023-raw-v1.csv")
            vehicle = pd.read_csv(RAW_DIR / "stats19-vehicle-2023-raw-v1.csv")
            
            print(f"  Loaded: casualty ({len(casualty):,}), collision ({len(collision):,}), vehicle ({len(vehicle):,})")
            
            # Join: casualty -> collision -> vehicle
            df = casualty.merge(
                collision[['collision_index', 'road_type', 'speed_limit', 'weather_conditions',
                          'light_conditions', 'road_surface_conditions', 'time', 'day_of_week', 'number_of_vehicles']],
                on='collision_index', how='inner'
            )
            df = df.merge(
                vehicle[['collision_index', 'vehicle_reference', 'vehicle_type']],
                on=['collision_index', 'vehicle_reference'], how='inner'
            )
            print(f"✓ Merged locally: {len(df):,} rows")
        except FileNotFoundError as e:
            raise DBRepoError(f"Local CSV files not found: {e}")
    
    if df is None:
        raise DBRepoError("Failed to load merged features from any source")
    
    # Save to interim
    output_file = INTERIM / "stats19-collision-vehicle-casualty-2023-interim-v1.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✓ Saved {len(df):,} rows -> {output_file.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()