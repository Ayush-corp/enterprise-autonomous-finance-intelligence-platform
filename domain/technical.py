from pydantic import BaseModel, Field


class TechnicalAnalysis(BaseModel):
    symbol: str
    trend: str
    momentum: str
    support: float
    resistance: float
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
