from pydantic import BaseModel

from domain.forecast import Forecast
from domain.fundamental import FundamentalAnalysis
from domain.macro import MacroAnalysis
from domain.recommendation import Recommendation
from domain.reflection import ReflectionAnalysis
from domain.risk import RiskAssessment


class AnalysisSynthesis(BaseModel):
    fundamental: FundamentalAnalysis
    macro: MacroAnalysis
    forecast: Forecast
    risk: RiskAssessment
    reflection: ReflectionAnalysis
    recommendation: Recommendation
