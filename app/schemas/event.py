from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SecurityEventRequest(BaseModel):
    """
    Incoming network-security event.

    The event contains the 78 CICIDS2017 feature
    values required by the trained ML models.
    """

    features: dict[str, Any] = Field(
        ...,
        description="Network traffic feature values.",
    )