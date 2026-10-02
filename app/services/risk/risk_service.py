from __future__ import annotations


class RiskEngine:
    """
    Combines supervised classification and anomaly
    detection signals into a normalized risk score.
    """

    def __init__(
        self,
        classifier_weight: float = 0.70,
        anomaly_weight: float = 0.30,
    ):
        if classifier_weight < 0:
            raise ValueError(
                "classifier_weight cannot be negative."
            )

        if anomaly_weight < 0:
            raise ValueError(
                "anomaly_weight cannot be negative."
            )

        total = classifier_weight + anomaly_weight

        if total == 0:
            raise ValueError(
                "At least one risk weight must be greater than zero."
            )

        self.classifier_weight = (
            classifier_weight / total
        )

        self.anomaly_weight = (
            anomaly_weight / total
        )

    @staticmethod
    def normalize_anomaly_score(
        anomaly_score: float
    ) -> float:
        """
        Convert an Isolation Forest decision score
        into an anomaly-risk value from 0 to 1.

        Lower Isolation Forest scores indicate
        more anomalous observations.

        The mapping is intentionally bounded and
        simple for the first prototype.
        """

        # Scores below zero are treated as strongly
        # anomalous; positive scores gradually reduce
        # the anomaly contribution.
        risk = 0.5 - anomaly_score

        return max(
            0.0,
            min(1.0, risk)
        )

    @staticmethod
    def classify_risk_level(
        risk_score: float
    ) -> str:
        if risk_score >= 70:
            return "HIGH"

        if risk_score >= 40:
            return "MEDIUM"

        return "LOW"

    def calculate_risk(
        self,
        attack_probability: float,
        anomaly_score: float,
    ) -> dict:
        if not 0.0 <= attack_probability <= 1.0:
            raise ValueError(
                "attack_probability must be between 0 and 1."
            )

        anomaly_risk = (
            self.normalize_anomaly_score(
                anomaly_score
            )
        )

        combined_risk = (
            (
                attack_probability
                * self.classifier_weight
            )
            +
            (
                anomaly_risk
                * self.anomaly_weight
            )
        )

        risk_score = round(
            combined_risk * 100,
            2
        )

        risk_level = self.classify_risk_level(
            risk_score
        )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "attack_probability": round(
                attack_probability,
                4
            ),
            "anomaly_risk": round(
                anomaly_risk,
                4
            ),
        }