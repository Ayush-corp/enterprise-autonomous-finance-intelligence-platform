from pydantic import BaseModel


class Recommendation(BaseModel):
    symbol: str
    action: str
    confidence: float
    risk_score: float
    position_size: float
    reasoning: str
