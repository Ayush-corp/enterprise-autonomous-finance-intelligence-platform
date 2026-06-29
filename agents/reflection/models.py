from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from agents.forecast.models import ForecastAgentOutput
from agents.risk.models import RiskAgentOutput


class ReflectionAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str

    forecast: ForecastAgentOutput

    risk: RiskAgentOutput


class ReflectionAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assumptions: list[str]

    weaknesses: list[str]

    contradictions: list[str]

    confidence_adjustment: float

    revised_confidence: float

    summary: str