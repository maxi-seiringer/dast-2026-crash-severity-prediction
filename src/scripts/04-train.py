"""
04-train.py
Train a Random Forest classifier on the training split
and check performance on the validation split.

Run from the repo root:
    python src/scripts/04-train.py
"""

from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from dotenv import load_dotenv
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from utils.dbrepo import DBRepoClient, DBRepoError

load_dotenv()

# --- Paths ---
REPO_ROOT     = Path(__file__).resolve().parents[2]
PROCESSED     = REPO_ROOT / "data" / "processed"
OUTPUTS_MODEL = REPO_ROOT / "outputs" / "models"
OUTPUTS_MODEL.mkdir(parents=True, exist_ok=True)

TARGET_COL   = "casualty_severity"
TARGET_NAMES = ["Fatal", "Serious", "Slight"]  # codes 1, 2, 3

# --- Load train and validation splits ---
def load_from_api_candidates(client: DBRepoClient, name_candidates):
    # Try candidate view names and return the first that exists
    view = client.find_first_existing_view(name_candidates)
    if not view:
        raise DBRepoError(f"No candidate views found for names: {name_candidates}")
    df = client.get_view(view)
    return df.drop(columns=[TARGET_COL]), df[TARGET_COL].astype(int)

client = DBRepoClient()
train_candidates = ["v_features_train", "v_ml_features_train", "ml_features_train", "features_train"]
val_candidates = ["v_features_val", "v_ml_features_val", "ml_features_val", "features_val"]

X_train, y_train = load_from_api_candidates(client, train_candidates)
X_val,   y_val   = load_from_api_candidates(client, val_candidates)
print(f"Train: {len(X_train):,} rows  |  Val: {len(X_val):,} rows")

# --- Train the Random Forest ---
# class_weight="balanced" compensates for the heavy imbalance
# between Slight (most common) and Fatal (very rare)
rf = RandomForestClassifier(
    n_estimators=200,       # number of trees
    min_samples_split=5,    # minimum samples needed to split a node
    min_samples_leaf=2,     # minimum samples required at a leaf node
    class_weight="balanced",
    n_jobs=-1,              # use all CPU cores
    random_state=42,
)
rf.fit(X_train, y_train)
print("Training complete.")

# --- Check performance on the validation set ---
print(f"Validation accuracy: {rf.score(X_val, y_val):.4f}")
print(classification_report(y_val, rf.predict(X_val), target_names=TARGET_NAMES))

# --- Save the trained model ---
model_path = OUTPUTS_MODEL / "model-random-forest-severity-2023-v1.pkl"
joblib.dump(rf, model_path)
print(f"Model saved -> {model_path.relative_to(REPO_ROOT)}")