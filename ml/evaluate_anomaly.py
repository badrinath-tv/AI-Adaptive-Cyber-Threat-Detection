from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "binary_dataset.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "isolation_forest.joblib"
)

FEATURE_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "anomaly_features.joblib"
)

RANDOM_STATE = 42

# Evaluate a manageable, balanced sample.
SAMPLE_PER_CLASS = 10_000


def load_artifacts():
    print("\nLoading Isolation Forest...")

    model = joblib.load(MODEL_FILE)
    feature_columns = joblib.load(FEATURE_FILE)

    return model, feature_columns


def load_evaluation_data(feature_columns):
    print("\nLoading evaluation data...")

    columns = feature_columns + [
        "Binary_Label"
    ]

    df = pd.read_csv(
        DATASET_FILE,
        usecols=columns,
        low_memory=False
    )

    benign = df[
        df["Binary_Label"] == 0
    ]

    attack = df[
        df["Binary_Label"] == 1
    ]

    benign = benign.sample(
        n=min(SAMPLE_PER_CLASS, len(benign)),
        random_state=RANDOM_STATE
    )

    attack = attack.sample(
        n=min(SAMPLE_PER_CLASS, len(attack)),
        random_state=RANDOM_STATE
    )

    evaluation = pd.concat(
        [benign, attack],
        ignore_index=True
    )

    evaluation = evaluation.sample(
        frac=1,
        random_state=RANDOM_STATE
    ).reset_index(drop=True)

    print(
        f"BENIGN evaluation samples: "
        f"{len(benign):,}"
    )

    print(
        f"ATTACK evaluation samples: "
        f"{len(attack):,}"
    )

    print(
        f"Total evaluation samples: "
        f"{len(evaluation):,}"
    )

    return evaluation


def evaluate(model, df, feature_columns):
    X = df[feature_columns]
    y_true = df["Binary_Label"]

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly
    raw_predictions = model.predict(X)

    # Convert to our binary convention:
    # 0 = BENIGN
    # 1 = ATTACK/anomaly
    y_pred = (
        raw_predictions == -1
    ).astype(int)

    anomaly_scores = (
        model.decision_function(X)
    )

    print("\n" + "=" * 70)
    print("ISOLATION FOREST EVALUATION")
    print("=" * 70)

    print("\nConfusion Matrix")
    print("-" * 70)

    matrix = confusion_matrix(
        y_true,
        y_pred
    )

    print(matrix)

    print("\nClassification Report")
    print("-" * 70)

    print(
        classification_report(
            y_true,
            y_pred,
            target_names=[
                "BENIGN",
                "ATTACK",
            ],
            zero_division=0,
        )
    )

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    print(f"Attack precision : {precision:.4f}")
    print(f"Attack recall    : {recall:.4f}")
    print(f"Attack F1        : {f1:.4f}")

    print("\nAnomaly detection rates")
    print("-" * 70)

    benign_mask = y_true == 0
    attack_mask = y_true == 1

    benign_anomaly_rate = (
        y_pred[benign_mask].mean()
    )

    attack_detection_rate = (
        y_pred[attack_mask].mean()
    )

    print(
        f"BENIGN flagged anomalous : "
        f"{benign_anomaly_rate:.4%}"
    )

    print(
        f"ATTACK flagged anomalous : "
        f"{attack_detection_rate:.4%}"
    )

    print("\nAnomaly score statistics")
    print("-" * 70)

    print(
        "BENIGN:"
    )

    print(
        pd.Series(
            anomaly_scores[benign_mask]
        ).describe()
    )

    print(
        "\nATTACK:"
    )

    print(
        pd.Series(
            anomaly_scores[attack_mask]
        ).describe()
    )


def main():
    print("=" * 70)
    print("ANOMALY DETECTOR EVALUATION")
    print("=" * 70)

    model, feature_columns = load_artifacts()

    df = load_evaluation_data(
        feature_columns
    )

    evaluate(
        model,
        df,
        feature_columns
    )


if __name__ == "__main__":
    main()