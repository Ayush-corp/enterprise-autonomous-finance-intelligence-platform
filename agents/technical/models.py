from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TechnicalAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str


class TechnicalAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trend: str
    momentum: str
    support: float
    resistance: float
    confidence: float
    summary: str