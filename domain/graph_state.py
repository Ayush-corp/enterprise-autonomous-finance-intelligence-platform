from pydantic import BaseModel, Field

from domain.forecast import Forecast
from domain.fundamental import FundamentalAnalysis
from domain.macro import MacroAnalysis
from domain.market import MarketSnapshot
from domain.news import NewsAnalysis
from domain.recommendation import Recommendation
from domain.reflection import ReflectionAnalysis
from domain.risk import RiskAssessment
from domain.technical import TechnicalAnalysis


class GraphState(BaseModel):
    symbol: str

    market: MarketSnapshot | None = None
    news: NewsAnalysis | None = None
    technical: TechnicalAnalysis | None = None
    fundamental: FundamentalAnalysis | None = None
    macro: MacroAnalysis | None = None
    forecast: Forecast | None = None
    risk: RiskAssessment | None = None
    reflection: ReflectionAnalysis | None = None
    recommendation: Recommendation | None = None

    metadata: dict[str, object] = Field(default_factory=dict)