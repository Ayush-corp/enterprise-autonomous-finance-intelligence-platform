from pydantic import BaseModel


class Recommendation(BaseModel):
    action: str
    confidence: float
    reasoning: str