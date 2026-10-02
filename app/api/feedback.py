from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.crud import create_analyst_feedback
from app.database.crud import get_feedback_for_event
from app.database.crud import get_security_event
from app.database.database import get_db
from app.schemas.feedback import FeedbackRequest
from app.schemas.feedback import FeedbackResponse
from app.services.feedback.feedback_service import FeedbackService


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post(
    "",
    response_model=FeedbackResponse,
)
def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db),
):
    event = get_security_event(
        db,
        request.event_id,
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Security event not found.",
        )

    analyst_label = request.analyst_label.upper()

    if analyst_label not in {
        "BENIGN",
        "ATTACK",
    }:
        raise HTTPException(
            status_code=400,
            detail="analyst_label must be BENIGN or ATTACK.",
        )

    feedback = create_analyst_feedback(
        db=db,
        event_id=request.event_id,
        analyst_label=analyst_label,
        analyst_comment=request.analyst_comment,
    )

    return feedback


@router.get(
    "/event/{event_id}",
    response_model=list[FeedbackResponse],
)
def get_event_feedback(
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

    return get_feedback_for_event(
        db,
        event_id,
    )


@router.get("/stats")
def get_feedback_statistics(
    db: Session = Depends(get_db),
):
    """
    Return analyst feedback statistics used by the
    adaptive learning component.
    """

    return FeedbackService.calculate_feedback_statistics(
        db
    )