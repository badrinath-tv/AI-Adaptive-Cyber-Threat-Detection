from __future__ import annotations

from sqlalchemy.orm import Session

from app.database.models import AnalystFeedback
from app.database.models import SecurityEvent


def create_security_event(
    db: Session,
    classification: str,
    attack_probability: float,
    anomaly: bool,
    anomaly_score: float,
    risk_score: float,
    risk_level: str,
    response_actions: list[str],
    response_simulation: bool = True,
) -> SecurityEvent:
    """
    Store one analyzed security event.
    """

    event = SecurityEvent(
        classification=classification,
        attack_probability=attack_probability,
        anomaly=anomaly,
        anomaly_score=anomaly_score,
        risk_score=risk_score,
        risk_level=risk_level,
        response_actions=response_actions,
        response_simulation=response_simulation,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def get_security_event(
    db: Session,
    event_id: int,
) -> SecurityEvent | None:
    """
    Retrieve one security event by ID.
    """

    return db.get(
        SecurityEvent,
        event_id,
    )


def get_recent_security_events(
    db: Session,
    limit: int = 50,
) -> list[SecurityEvent]:
    """
    Retrieve the most recent security events.
    """

    if limit < 1:
        raise ValueError(
            "limit must be greater than zero."
        )

    return (
        db.query(SecurityEvent)
        .order_by(
            SecurityEvent.created_at.desc()
        )
        .limit(limit)
        .all()
    )


def create_analyst_feedback(
    db: Session,
    event_id: int,
    analyst_label: str,
    analyst_comment: str | None = None,
) -> AnalystFeedback:
    """
    Store analyst feedback for a security event.
    """

    feedback = AnalystFeedback(
        event_id=event_id,
        analyst_label=analyst_label,
        analyst_comment=analyst_comment,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


def get_feedback_for_event(
    db: Session,
    event_id: int,
) -> list[AnalystFeedback]:
    """
    Retrieve all analyst feedback associated
    with a security event.
    """

    return (
        db.query(AnalystFeedback)
        .filter(
            AnalystFeedback.event_id == event_id
        )
        .order_by(
            AnalystFeedback.created_at.desc()
        )
        .all()
    )