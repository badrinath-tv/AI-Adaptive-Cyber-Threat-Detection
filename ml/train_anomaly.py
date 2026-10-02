from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "binary_dataset.csv"
)

MODEL_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_FILE = (
    MODEL_DIR
    / "isolation_forest.joblib"
)

FEATURE_FILE = (
    MODEL_DIR
    / "anomaly_features.joblib"
)


RANDOM_STATE = 42

# Keep the first prototype computationally manageable.
# The benign class contains more than 2 million records.
TRAIN_SAMPLE_SIZE = 200_000


def load_dataset():
    print("\nLoading dataset...")

    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_FILE}"
        )

    df = pd.read_csv(
        DATASET_FILE,
        low_memory=False
    )

    print(f"Loaded {len(df):,} rows.")

    return df


def prepare_benign_data(df):
    print("\nSelecting BENIGN traffic...")

    if "Binary_Label" not in df.columns:
        raise ValueError(
            "'Binary_Label' column not found."
        )

    feature_columns = [
        column
        for column in df.columns
        if column not in {
            "Label",
            "Binary_Label",
        }
    ]

    benign = df[
        df["Binary_Label"] == 0
    ].copy()

    print(
        f"Available BENIGN rows: {len(benign):,}"
    )

    if len(benign) > TRAIN_SAMPLE_SIZE:
        benign = benign.sample(
            n=TRAIN_SAMPLE_SIZE,
            random_state=RANDOM_STATE
        )

    X = benign[feature_columns].copy()

    print(
        f"Training anomaly detector on "
        f"{len(X):,} BENIGN rows."
    )

    print(
        f"Features: {len(feature_columns)}"
    )

    return X, feature_columns


def train_model(X):
    print("\nTraining Isolation Forest...")
    print("This may take some time.")

    model = IsolationForest(
        n_estimators=200,
        contamination=0.01,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model.fit(X)

    print("Isolation Forest training complete.")

    return model


def save_model(model, feature_columns):
    print("\nSaving anomaly detector...")

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_FILE
    )

    joblib.dump(
        feature_columns,
        FEATURE_FILE
    )

    print(
        f"Model saved   : {MODEL_FILE}"
    )

    print(
        f"Features saved: {FEATURE_FILE}"
    )


def main():
    print("=" * 70)
    print("ISOLATION FOREST ANOMALY DETECTOR")
    print("=" * 70)

    df = load_dataset()

    X, feature_columns = prepare_benign_data(
        df
    )

    model = train_model(X)

    save_model(
        model,
        feature_columns
    )

    print("\n" + "=" * 70)
    print("ANOMALY DETECTOR TRAINING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()