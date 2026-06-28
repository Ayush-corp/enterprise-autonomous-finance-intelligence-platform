from pydantic import BaseModel


class MarketSnapshot(BaseModel):
    symbol: str
    current_price: float
    sma20: float
    volume: float
    trend: str