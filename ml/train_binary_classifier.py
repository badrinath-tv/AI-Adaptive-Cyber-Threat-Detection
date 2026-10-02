from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "binary_dataset.csv"
)

MODEL_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_FILE = MODEL_DIR / "binary_random_forest.joblib"
FEATURE_FILE = MODEL_DIR / "binary_features.joblib"


RANDOM_STATE = 42
TEST_SIZE = 0.20


def load_dataset() -> pd.DataFrame:
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


def prepare_data(df: pd.DataFrame):
    print("\nPreparing features and labels...")

    if "Binary_Label" not in df.columns:
        raise ValueError(
            "'Binary_Label' column not found."
        )

    if "Label" not in df.columns:
        raise ValueError(
            "'Label' column not found."
        )

    # Do not use the original text label as a feature.
    feature_columns = [
        column
        for column in df.columns
        if column not in {
            "Label",
            "Binary_Label",
        }
    ]

    X = df[feature_columns].copy()
    y = df["Binary_Label"].copy()

    print(f"Features: {len(feature_columns)}")
    print(f"Samples : {len(X):,}")

    return X, y, feature_columns


def split_data(X, y):
    print("\nCreating train/test split...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(f"Training samples : {len(X_train):,}")
    print(f"Testing samples  : {len(X_test):,}")

    print("\nTraining class distribution:")
    print(y_train.value_counts().sort_index())

    print("\nTesting class distribution:")
    print(y_test.value_counts().sort_index())

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    print("\nTraining Random Forest...")
    print("This may take some time.")

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",
        max_features="sqrt",
    )

    model.fit(X_train, y_train)

    print("Training complete.")

    return model


def evaluate_model(model, X_test, y_test):
    print("\n" + "=" * 70)
    print("MODEL EVALUATION")
    print("=" * 70)

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    print(f"\nAccuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")

    print("\nClassification Report")
    print("-" * 70)

    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "BENIGN",
                "ATTACK",
            ],
            zero_division=0,
        )
    )

    print("Confusion Matrix")
    print("-" * 70)

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    print(matrix)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
    }


def save_model(model, feature_columns):
    print("\nSaving model artifacts...")

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

    print(f"Model saved   : {MODEL_FILE}")
    print(f"Features saved: {FEATURE_FILE}")


def main():
    print("=" * 70)
    print("BINARY CYBER THREAT CLASSIFIER")
    print("=" * 70)

    df = load_dataset()

    X, y, feature_columns = prepare_data(
        df
    )

    X_train, X_test, y_train, y_test = split_data(
        X,
        y
    )

    model = train_model(
        X_train,
        y_train
    )

    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    save_model(
        model,
        feature_columns
    )

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)

    print("\nFinal metrics:")
    for name, value in metrics.items():
        print(f"{name:>10}: {value:.4f}")


if __name__ == "__main__":
    main()