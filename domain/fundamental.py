from pydantic import BaseModel, Field


class FinancialRatios(BaseModel):
    pe: float
    pb: float
    roe: float
    roce: float
    debt_to_equity: float
    eps: float


class FundamentalAnalysis(BaseModel):
    symbol: str
    valuation: str
    quality: str
    growth: str
    financial_health: str
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    ratios: FinancialRatios | None = None
