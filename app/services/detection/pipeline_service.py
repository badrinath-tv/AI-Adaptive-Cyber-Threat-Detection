from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.crud import create_security_event
from app.services.anomaly.anomaly_service import AnomalyDetector
from app.services.detection.classifier_service import ThreatClassifier
from app.services.explainability.shap_service import ShapExplainer
from app.services.response.response_service import ResponseService
from app.services.risk.risk_service import RiskEngine


class DetectionPipeline:
    def __init__(self):
        self.classifier = ThreatClassifier()
        self.anomaly_detector = AnomalyDetector()
        self.shap_explainer = ShapExplainer()
        self.risk_engine = RiskEngine()
        self.response_service = ResponseService()

    def analyze(self, event: dict) -> dict:

        classification = self.classifier.predict(event)

        anomaly = self.anomaly_detector.predict(event)

        risk = self.risk_engine.calculate_risk(
            attack_probability=classification["attack_probability"],
            anomaly_score=anomaly["anomaly_score"],
        )

        response = self.response_service.generate_response(
            risk["risk_level"]
        )

        explanation = self.shap_explainer.explain(
            event,
            top_n=10,
        )

        return {
            "classification": classification,
            "anomaly": anomaly,
            "risk": risk,
            "response": response,
            "explanation": explanation,
        }

    def save_result(
        self,
        db: Session,
        result: dict,
    ):
        classification = result["classification"]
        anomaly = result["anomaly"]
        risk = result["risk"]
        response = result["response"]

        event = create_security_event(
            db=db,
            classification=classification["label"],
            attack_probability=classification["attack_probability"],
            anomaly=anomaly["is_anomaly"],
            anomaly_score=anomaly["anomaly_score"],
            risk_score=risk["risk_score"],
            risk_level=risk["risk_level"],
            response_actions=response["actions"],
            response_simulation=response["simulation"],
        )

        return event