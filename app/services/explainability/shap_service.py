from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import shap


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_FILE = PROJECT_ROOT / "ml" / "models" / "binary_random_forest.joblib"
FEATURE_FILE = PROJECT_ROOT / "ml" / "models" / "binary_features.joblib"


class ShapExplainer:
    def __init__(self):
        if not MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Model not found: {MODEL_FILE}"
            )

        if not FEATURE_FILE.exists():
            raise FileNotFoundError(
                f"Feature file not found: {FEATURE_FILE}"
            )

        self.model = joblib.load(MODEL_FILE)
        self.feature_columns = joblib.load(FEATURE_FILE)

        self.explainer = shap.TreeExplainer(self.model)

    def explain(
        self,
        event: dict,
        top_n: int = 10,
    ) -> dict:

        dataframe = pd.DataFrame([event])

        missing_features = [
            feature
            for feature in self.feature_columns
            if feature not in dataframe.columns
        ]

        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features}"
            )

        dataframe = dataframe[self.feature_columns]

        shap_values = self.explainer.shap_values(dataframe)

        # RandomForest binary classification normally returns
        # one SHAP array per class.
        if isinstance(shap_values, list):
            values = shap_values[1][0]
        else:
            values = shap_values[0]

        explanations = []

        for feature, shap_value in zip(
            self.feature_columns,
            values,
        ):
            value = dataframe.iloc[0][feature]

            explanations.append(
                {
                    "feature": feature,
                    "value": float(value),
                    "shap_value": float(shap_value),
                    "impact": (
                        "increases_attack_risk"
                        if shap_value > 0
                        else "decreases_attack_risk"
                    ),
                }
            )

        explanations.sort(
            key=lambda item: abs(item["shap_value"]),
            reverse=True,
        )

        return {
            "top_features": explanations[:top_n]
        }