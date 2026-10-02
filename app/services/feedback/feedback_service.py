from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.crud import get_feedback_for_event
from app.database.models import AnalystFeedback


class FeedbackService:

    @staticmethod
    def get_event_feedback(
        db: Session,
        event_id: int,
    ) -> list[AnalystFeedback]:
        return get_feedback_for_event(
            db,
            event_id,
        )

    @staticmethod
    def calculate_feedback_statistics(
        db: Session,
    ) -> dict:

        feedback_records = (
            db.query(AnalystFeedback)
            .order_by(AnalystFeedback.created_at.desc())
            .all()
        )

        total = len(feedback_records)

        benign_count = sum(
            1
            for feedback in feedback_records
            if feedback.analyst_label == "BENIGN"
        )

        attack_count = sum(
            1
            for feedback in feedback_records
            if feedback.analyst_label == "ATTACK"
        )

        return {
            "total_feedback": total,
            "benign_feedback": benign_count,
            "attack_feedback": attack_count,
            "adaptation_status": (
                "READY_FOR_MODEL_REVIEW"
                if total >= 5
                else "COLLECTING_ANALYST_FEEDBACK"
            ),
        }