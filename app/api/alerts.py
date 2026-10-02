from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.crud import get_recent_security_events
from app.database.crud import get_security_event
from app.database.database import get_db
from app.schemas.alert import AlertResponse


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get(
    "",
    response_model=list[AlertResponse],
)
def get_alerts(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return get_recent_security_events(
        db,
        limit=limit,
    )


@router.get(
    "/{event_id}",
    response_model=AlertResponse,
)
def get_alert(
    event_id: int,
    db: Session = Depends(get_db),
):
    event = get_security_event(
        db,
        event_id,
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Security event not found.",
        )

    return event