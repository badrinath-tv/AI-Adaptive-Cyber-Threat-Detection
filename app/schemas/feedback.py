from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class FeedbackRequest(BaseModel):
    event_id: int = Field(
        ...,
        description="ID of the security event being reviewed.",
    )

    analyst_label: str = Field(
        ...,
        description="Analyst's final classification.",
    )

    analyst_comment: str | None = Field(
        default=None,
        description="Optional analyst explanation.",
    )


class FeedbackResponse(BaseModel):
    id: int
    event_id: int
    analyst_label: str
    analyst_comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True