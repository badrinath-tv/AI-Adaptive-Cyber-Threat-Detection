from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "binary_random_forest.joblib"
)

FEATURE_FILE = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "binary_features.joblib"
)


class ThreatClassifier:
    """
    Loads the trained Random Forest model and
    classifies network-security events as
    BENIGN or ATTACK.
    """

    def __init__(self):
        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Model not found: {MODEL_FILE}"
            )

        if not FEATURE_FILE.exists():
            raise FileNotFoundError(
                f"Feature file not found: {FEATURE_FILE}"
            )

        self.model = joblib.load(
            MODEL_FILE
        )

        self.feature_columns = joblib.load(
            FEATURE_FILE
        )

    def predict(self, event: dict) -> dict:
        """
        Predict the threat class for one event.
        """

        dataframe = pd.DataFrame(
            [event]
        )

        missing_features = [
            feature
            for feature in self.feature_columns
            if feature not in dataframe.columns
        ]

        if missing_features:
            raise ValueError(
                "Missing required features: "
                + ", ".join(missing_features)
            )

        dataframe = dataframe[
            self.feature_columns
        ]

        prediction = int(
            self.model.predict(dataframe)[0]
        )

        probabilities = (
            self.model.predict_proba(dataframe)[0]
        )

        benign_probability = float(
            probabilities[0]
        )

        attack_probability = float(
            probabilities[1]
        )

        label = (
            "ATTACK"
            if prediction == 1
            else "BENIGN"
        )

        return {
            "prediction": prediction,
            "label": label,
            "benign_probability": benign_probability,
            "attack_probability": attack_probability,
        }