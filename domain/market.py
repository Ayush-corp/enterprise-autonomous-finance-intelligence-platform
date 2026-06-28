from pydantic import BaseModel, Field
from domain.enums import Trend


class MarketSnapshot(BaseModel):
    symbol: str
    current_price: float = Field(gt=0)
    sma20: float = Field(gt=0)
    volume: float = Field(ge=0)
    trend: Trend