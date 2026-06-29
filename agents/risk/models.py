from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from agents.forecast.models import ForecastAgentOutput


class RiskAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    forecast: ForecastAgentOutput


class RiskAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_level: str

    volatility: str

    max_drawdown: float

    recommendation: str

    confidence: float

    summary: str