from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.event import SecurityEventRequest
from app.services.detection.pipeline_service import DetectionPipeline


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


pipeline = DetectionPipeline()


@router.post("/analyze")
def analyze_event(
    request: SecurityEventRequest,
    db: Session = Depends(get_db),
):
    result = pipeline.analyze(
        request.features
    )

    saved_event = pipeline.save_result(
        db,
        result,
    )

    return {
        "event_id": saved_event.id,
        "classification": result["classification"],
        "anomaly": result["anomaly"],
        "risk": result["risk"],
        "response": result["response"],
        "explanation": result["explanation"],
    }