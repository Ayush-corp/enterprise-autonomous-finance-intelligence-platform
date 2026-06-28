from pydantic import BaseModel
from domain.enums import RiskLevel

class RiskAssessment(BaseModel):
    level: RiskLevel
    score: float
    reasoning: str