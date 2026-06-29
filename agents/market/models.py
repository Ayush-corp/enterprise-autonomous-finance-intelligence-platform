from pydantic import BaseModel, Field


class MarketAgentInput(BaseModel):
    symbol: str = Field(min_length=1)


class MarketAgentOutput(BaseModel):
    summary: str
    market_sentiment: str
    confidence: float