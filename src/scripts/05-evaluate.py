"""
05-evaluate.py
Evaluate the trained model on the held-out test set
and save all output artefacts.

Run from the repo root:
    python src/scripts/05-evaluate.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from dotenv import load_dotenv
 

load_dotenv()

# --- Paths ---
REPO_ROOT      = Path(__file__).resolve().parents[2]
PROCESSED      = REPO_ROOT / "data" / "processed"
OUTPUTS_FIG    = REPO_ROOT / "outputs" / "figures"
OUTPUTS_MODEL  = REPO_ROOT / "outputs" / "models"
OUTPUTS_REPORT = REPO_ROOT / "outputs" / "reports"
for p in (OUTPUTS_FIG, OUTPUTS_REPORT):
    p.mkdir(parents=True, exist_ok=True)

TARGET_COL   = "casualty_severity"
TARGET_NAMES = ["Fatal", "Serious", "Slight"]  # codes 1, 2, 3
SEVERITY_MAP = {1: "Fatal", 2: "Serious", 3: "Slight"}

# --- Load the trained model ---
rf = joblib.load(OUTPUTS_MODEL / "model-random-forest-severity-2023-v1.pkl")

test_path = PROCESSED / "stats19-features-test-2023-processed-v1.csv"
if test_path.exists():
    df_test = pd.read_csv(test_path)
    print(f"Loaded test split from {test_path.relative_to(REPO_ROOT)}")
    X_test = df_test.drop(columns=[TARGET_COL])
    y_test = df_test[TARGET_COL].astype(int)
else:
    raise FileNotFoundError("Missing processed test split. Run src/scripts/03-prepare-features.py first.")
y_pred   = rf.predict(X_test)
print(f"Test rows: {len(X_test):,}")

# --- Classification report (precision, recall, F1 per class) ---
report_dict = classification_report(y_test, y_pred, target_names=TARGET_NAMES, output_dict=True)
pd.DataFrame(report_dict).transpose().to_csv(
    OUTPUTS_REPORT / "report-classification-metrics-2023-v1.csv"
)
print(classification_report(y_test, y_pred, target_names=TARGET_NAMES))

# --- Confusion matrix plot ---
fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay(
    confusion_matrix(y_test, y_pred, labels=[1, 2, 3]),
    display_labels=TARGET_NAMES
).plot(ax=ax, cmap="Blues")
ax.set_title("Confusion matrix - test set")
fig.tight_layout()
fig.savefig(OUTPUTS_FIG / "fig-confusion-matrix-2023-v1.png", dpi=150)
plt.close(fig)
print("Saved: fig-confusion-matrix-2023-v1.png")

# --- Feature importance plot ---
import pandas as _pd  # avoid conflict with the pd alias for the classification report
importances = pd.Series(rf.feature_importances_, index=X_test.columns).sort_values()
fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(importances.index, importances.values, color="#4C9BE8")
ax.set_title("Feature importance - Random Forest")
ax.set_xlabel("Mean decrease in impurity")
fig.tight_layout()
fig.savefig(OUTPUTS_FIG / "fig-feature-importance-2023-v1.png", dpi=150)
plt.close(fig)
print("Saved: fig-feature-importance-2023-v1.png")

# --- Predictions CSV: predicted vs actual label for every test row ---
pred_df = X_test.copy()
pred_df["actual_severity"]    = y_test.values
pred_df["predicted_severity"] = y_pred
pred_df["actual_label"]       = pred_df["actual_severity"].map(SEVERITY_MAP)
pred_df["predicted_label"]    = pred_df["predicted_severity"].map(SEVERITY_MAP)
pred_df.to_csv(OUTPUTS_REPORT / "report-predictions-test-2023-v1.csv", index=False)
print("Saved: report-predictions-test-2023-v1.csv")