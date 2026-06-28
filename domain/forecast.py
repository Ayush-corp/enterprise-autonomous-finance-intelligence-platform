from pydantic import BaseModel

class Forecast(BaseModel):
    predicted_price: float
    confidence: float
    horizon_days: int
    reasoning: str