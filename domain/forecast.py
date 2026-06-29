from pydantic import BaseModel


class Forecast(BaseModel):
    symbol: str
    horizon: str = "5 trading days"
    direction: str
    predicted_price: float
    confidence: float
    reasoning: str
