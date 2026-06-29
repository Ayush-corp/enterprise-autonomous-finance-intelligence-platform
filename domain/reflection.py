from pydantic import BaseModel, Field


class ReflectionAnalysis(BaseModel):
    symbol: str
    assumptions: list[str]
    weaknesses: list[str]
    contradictions: list[str]
    confidence_adjustment: float
    revised_confidence: float = Field(ge=0.0, le=1.0)
    summary: str
