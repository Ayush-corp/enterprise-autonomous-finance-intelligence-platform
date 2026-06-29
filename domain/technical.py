from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TechnicalAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    trend: str
    momentum: str
    support: float
    resistance: float
    confidence: float
    summary: str
