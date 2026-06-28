from pydantic import BaseModel


class RiskAssessment(BaseModel):
    level: str
    score: float
    explanation: str