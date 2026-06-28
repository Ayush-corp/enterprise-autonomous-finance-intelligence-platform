from pydantic import BaseModel, Field

from domain.forecast import Forecast
from domain.market import MarketSnapshot
from domain.news import NewsAnalysis
from domain.recommendation import Recommendation
from domain.risk import RiskAssessment


class GraphState(BaseModel):
    symbol: str
    market: MarketSnapshot | None = None
    news: NewsAnalysis | None = None
    forecast: Forecast | None = None
    risk: RiskAssessment | None = None
    recommendation: Recommendation | None = None
    metadata: dict = Field(default_factory=dict)