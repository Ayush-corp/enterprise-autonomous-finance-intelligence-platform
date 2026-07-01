from pydantic import BaseModel, field_validator


class Recommendation(BaseModel):
    symbol: str
    action: str
    confidence: float
    risk_score: float
    position_size: float
    reasoning: str

    @field_validator("action")
    @classmethod
    def normalize_action(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in {"BUY", "HOLD", "SELL", "AVOID"}:
            raise ValueError("action must be BUY, HOLD, SELL, or AVOID")
        return normalized
