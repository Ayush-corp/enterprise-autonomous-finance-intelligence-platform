from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MacroAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str


class MacroAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    market_cycle: str
    inflation_impact: str
    interest_rate_impact: str
    currency_impact: str
    sector_outlook: str
    confidence: float
    summary: str