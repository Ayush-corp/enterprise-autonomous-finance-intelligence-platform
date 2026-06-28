from pydantic import BaseModel


class Forecast(BaseModel):
    predicted_price: float
    confidence: float
    reasoning: str