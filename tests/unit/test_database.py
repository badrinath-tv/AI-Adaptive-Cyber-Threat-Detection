from app.database.crud import (
    create_security_event,
    get_recent_security_events,
    get_security_event,
)
from app.database.database import SessionLocal, init_database


def test_security_event_crud():
    init_database()

    db = SessionLocal()

    try:
        event = create_security_event(
            db=db,
            classification="ATTACK",
            attack_probability=0.95,
            anomaly=True,
            anomaly_score=-0.08,
            risk_score=82.5,
            risk_level="HIGH",
            response_actions=[
                "LOG_EVENT",
                "CREATE_INCIDENT",
                "SIMULATE_CONTAINMENT",
            ],
            response_simulation=True,
        )

        assert event.id is not None
        assert event.classification == "ATTACK"
        assert event.risk_level == "HIGH"

        retrieved = get_security_event(
            db,
            event.id,
        )

        assert retrieved is not None
        assert retrieved.id == event.id
        assert retrieved.attack_probability == 0.95

        recent = get_recent_security_events(
            db,
            limit=10,
        )

        assert len(recent) >= 1
        assert any(
            item.id == event.id
            for item in recent
        )

    finally:
        db.close()