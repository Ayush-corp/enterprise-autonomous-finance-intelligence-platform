from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from agents.forecast.models import ForecastAgentOutput
from agents.reflection.models import ReflectionAgentOutput
from agents.risk.models import RiskAgentOutput


class CommitteeAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str

    forecast: ForecastAgentOutput

    risk: RiskAgentOutput

    reflection: ReflectionAgentOutput


class CommitteeAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: str

    conviction: float

    target_horizon: str

    investment_thesis: str

    key_risks: list[str]

    action_items: list[str]