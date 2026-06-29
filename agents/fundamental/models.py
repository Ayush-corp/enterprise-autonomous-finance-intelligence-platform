from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FundamentalAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str


class FinancialRatios(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pe: float
    pb: float
    roe: float
    roce: float
    debt_to_equity: float
    eps: float


class FundamentalAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valuation: str
    quality: str
    growth: str
    financial_health: str
    confidence: float
    summary: str