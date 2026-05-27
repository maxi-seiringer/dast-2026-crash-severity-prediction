"""
01-load-merge-api.py
Fetch the merged feature table directly from the DBRepo view.
No local CSV files needed.
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

load_dotenv()

# --- Config ---
# Prefer environment variables: DBREPO_API_BASE, DBREPO_DB_ID, DBREPO_USER, DBREPO_PASSWORD
INTERIM   = REPO_ROOT / "data" / "interim"
INTERIM.mkdir(parents=True, exist_ok=True)

def main():
    client = DBRepoClient()
    # Try the common view name for the merged ML features
    view_candidates = ["v_ml_features", "v_ml_merged", "ml_features", "v_features"]
    view = client.find_first_existing_view(view_candidates)
    if not view:
        raise DBRepoError(f"None of the candidate views found: {view_candidates}")
    df = client.get_view(view)
    print(f"Fetched {len(df):,} rows from view '{view}'")
    df.to_csv(INTERIM / "stats19-collision-vehicle-casualty-2023-interim-v1.csv", index=False)
    print("Saved -> data/interim/")


if __name__ == "__main__":
    main()