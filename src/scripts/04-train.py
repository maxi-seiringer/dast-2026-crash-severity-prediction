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

# --- Paths ---
REPO_ROOT     = Path(__file__).resolve().parents[2]
PROCESSED     = REPO_ROOT / "data" / "processed"
OUTPUTS_MODEL = REPO_ROOT / "outputs" / "models"
OUTPUTS_MODEL.mkdir(parents=True, exist_ok=True)

TARGET_COL   = "casualty_severity"
TARGET_NAMES = ["Fatal", "Serious", "Slight"]  # codes 1, 2, 3

# --- Load train and validation splits ---
def load(path):
    df = pd.read_csv(path)
    return df.drop(columns=[TARGET_COL]), df[TARGET_COL].astype(int)

X_train, y_train = load(PROCESSED / "stats19-features-train-2023-processed-v1.csv")
X_val,   y_val   = load(PROCESSED / "stats19-features-val-2023-processed-v1.csv")
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