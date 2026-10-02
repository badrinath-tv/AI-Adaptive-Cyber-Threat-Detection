from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: int
    created_at: datetime
    classification: str
    attack_probability: float
    anomaly: bool
    anomaly_score: float
    risk_score: float
    risk_level: str
    response_actions: list[str]
    response_simulation: bool

    class Config:
        from_attributes = True