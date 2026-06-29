from pydantic import BaseModel


class RiskAssessment(BaseModel):
    symbol: str
    level: str
    score: float
    downside: str = ""
    uncertainty: str = ""
    explanation: str
