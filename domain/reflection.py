from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Reflection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    assumptions: list[str]
    weaknesses: list[str]
    contradictions: list[str]
    confidence_adjustment: float
    revised_confidence: float
    summary: str
