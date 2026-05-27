"""
01-load-merge-api.py
Fetch the merged feature table directly from the DBRepo view.
No local CSV files needed.
"""

from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
API_BASE = "https://test.dbrepo.tuwien.ac.at/api/v1"   # fill in when available
DB_ID    = "3d81c073-e5fd-49b9-9536-b75ed490ca3e"             # fill in when available
USERNAME = os.getenv("DBREPO_USER")
PASSWORD = os.getenv("DBREPO_PASSWORD")

REPO_ROOT = Path(__file__).resolve().parents[2]
INTERIM   = REPO_ROOT / "data" / "interim"
INTERIM.mkdir(parents=True, exist_ok=True)

# --- Fetch the view from DBRepo ---
# v_ml_features already contains the merged collision + vehicle + casualty data
response = requests.get(
    f"{API_BASE}/database/{DB_ID}/subset/v_ml_features",
    auth=(USERNAME, PASSWORD),
)
response.raise_for_status()  # stops the script if something goes wrong

# --- Convert to DataFrame and save ---
df = pd.DataFrame(response.json()["data"])
print(f"Fetched {len(df):,} rows from v_ml_features")

df.to_csv(INTERIM / "stats19-collision-vehicle-casualty-2023-interim-v1.csv", index=False)
print("Saved -> data/interim/")