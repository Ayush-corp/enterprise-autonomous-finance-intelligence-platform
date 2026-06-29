from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from agents.fundamental.models import FundamentalAgentOutput
from agents.macro.models import MacroAgentOutput
from agents.news.models import NewsAgentOutput
from agents.technical.models import TechnicalAgentOutput


class ForecastAgentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str

    news: NewsAgentOutput
    technical: TechnicalAgentOutput
    fundamental: FundamentalAgentOutput
    macro: MacroAgentOutput


class ForecastAgentOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    direction: str = Field(
        description="Bullish | Bearish | Neutral"
    )

    horizon: str

    confidence: float

    reasoning: str

    expected_return: float