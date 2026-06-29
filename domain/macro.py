from pydantic import BaseModel, Field


class MacroAnalysis(BaseModel):
    symbol: str
    market_cycle: str
    inflation_impact: str
    interest_rate_impact: str
    currency_impact: str
    sector_outlook: str
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
