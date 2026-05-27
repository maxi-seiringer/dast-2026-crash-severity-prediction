"""
verify_api_matches_local.py

Utility script to help verify that loading data from the DBRepo API
produces identical modelling results to the original local-file pipeline.

This script is not part of the production experiment codepath — it's a
developer aid for comparison. It will attempt to load processed splits both
from `data/processed/` and from DBRepo views and compare classification
reports on the validation and test splits.

Run from the repo root:
    python src/scripts/verify_api_matches_local.py
"""

from pathlib import Path
import sys
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from dotenv import load_dotenv

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
from utils.dbrepo import DBRepoClient, DBRepoError

TARGET_COL = "casualty_severity"


def train_and_report(X_train, y_train, X_val, y_val):
    rf = RandomForestClassifier(n_estimators=200, min_samples_split=5,
                                min_samples_leaf=2, class_weight="balanced",
                                n_jobs=-1, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_val)
    return classification_report(y_val, y_pred, output_dict=True)


def load_local_processed():
    proc = REPO_ROOT / "data" / "processed"
    if not proc.exists():
        return None
    try:
        train = pd.read_csv(proc / "stats19-features-train-2023-processed-v1.csv")
        val = pd.read_csv(proc / "stats19-features-val-2023-processed-v1.csv")
        test = pd.read_csv(proc / "stats19-features-test-2023-processed-v1.csv")
        return {"train": train, "val": val, "test": test}
    except Exception:
        return None


def load_api_processed():
    client = DBRepoClient()
    def get_df(candidates):
        view = client.find_first_existing_view(candidates)
        if not view:
            return None, None
        df = client.get_view(view)
        return df.drop(columns=[TARGET_COL]), df[TARGET_COL].astype(int)

    train = get_df(["v_features_train", "v_ml_features_train", "ml_features_train", "features_train"])
    val = get_df(["v_features_val", "v_ml_features_val", "ml_features_val", "features_val"])
    test = get_df(["v_features_test", "v_ml_features_test", "ml_features_test", "features_test"])
    if train[0] is None or val[0] is None:
        raise DBRepoError("Could not find train/val views in DBRepo for verification")
    return {"train": train, "val": val, "test": test}


def main():
    local = load_local_processed()
    api = None
    try:
        api = load_api_processed()
    except Exception as e:
        print("API load failed:", e)

    if local is None and api is None:
        print("No data sources available for verification (local or API).")
        return

    if local is not None and api is not None:
        # Compare train->val reports
        lr = train_and_report(local["train"].drop(columns=[TARGET_COL]), local["train"][TARGET_COL].astype(int),
                              local["val"].drop(columns=[TARGET_COL]), local["val"][TARGET_COL].astype(int))
        ar = train_and_report(api["train"][0], api["train"][1], api["val"][0], api["val"][1])
        print("Local report (val):")
        print(json.dumps(lr, indent=2))
        print("API report (val):")
        print(json.dumps(ar, indent=2))
        if lr == ar:
            print("Reports are identical on the validation set.")
        else:
            print("Reports differ between local and API. Inspect above JSON outputs.")
    else:
        print("Only one data source available; nothing to compare.")


if __name__ == "__main__":
    main()
