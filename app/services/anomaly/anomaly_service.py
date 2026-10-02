from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

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


class AnomalyDetector:
    """
    Loads the trained Isolation Forest and
    detects unusual network-security events.
    """

    def __init__(self):
        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Anomaly model not found: {MODEL_FILE}"
            )

        if not FEATURE_FILE.exists():
            raise FileNotFoundError(
                f"Anomaly feature file not found: {FEATURE_FILE}"
            )

        self.model = joblib.load(
            MODEL_FILE
        )

        self.feature_columns = joblib.load(
            FEATURE_FILE
        )

    def predict(self, event: dict) -> dict:
        """
        Detect whether one event is anomalous.
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

        score = float(
            self.model.decision_function(dataframe)[0]
        )

        is_anomaly = prediction == -1

        return {
            "prediction": prediction,
            "is_anomaly": is_anomaly,
            "anomaly_score": score,
        }