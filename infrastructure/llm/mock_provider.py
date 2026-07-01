import re
from typing import TypeVar

from pydantic import BaseModel

from domain.analysis import AnalysisSynthesis
from domain.forecast import Forecast
from domain.fundamental import FundamentalAnalysis
from domain.macro import MacroAnalysis
from domain.recommendation import Recommendation
from domain.reflection import ReflectionAnalysis
from domain.risk import RiskAssessment
from domain.technical import TechnicalAnalysis
from infrastructure.llm.models import LLMResult
from infrastructure.llm.provider import LLMProvider


T = TypeVar("T", bound=BaseModel)


class MockLLMProvider(LLMProvider):
    name = "mock"

    async def complete(self, system_prompt: str, user_prompt: str) -> LLMResult[BaseModel]:
        return LLMResult(
            content="Deterministic mock response for local development.",
            metadata={"provider": self.name},
        )

    async def structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> LLMResult[T]:
        symbol = self._extract_symbol(user_prompt)
        payload = self._payload_for(response_model, symbol)
        return LLMResult(
            structured=response_model.model_validate(payload),
            metadata={"provider": self.name, "mock": True},
        )

    def _extract_symbol(self, prompt: str) -> str:
        match = re.search(r"Symbol:\s*([A-Z0-9.\-]+)", prompt, flags=re.IGNORECASE)
        return match.group(1).upper() if match else "UNKNOWN.NS"

    def _payload_for(self, response_model: type[T], symbol: str) -> dict[str, object]:
        if response_model is AnalysisSynthesis:
            return {
                "fundamental": self._payload_for(FundamentalAnalysis, symbol),
                "macro": self._payload_for(MacroAnalysis, symbol),
                "forecast": self._payload_for(Forecast, symbol),
                "risk": self._payload_for(RiskAssessment, symbol),
                "reflection": self._payload_for(ReflectionAnalysis, symbol),
                "recommendation": self._payload_for(Recommendation, symbol),
            }
        if response_model is TechnicalAnalysis:
            return {
                "symbol": symbol,
                "trend": "uptrend",
                "momentum": "moderate",
                "support": 2475.0,
                "resistance": 2625.0,
                "confidence": 0.64,
                "summary": "Mock technical read indicates price is above short-term support with moderate momentum.",
            }
        if response_model is FundamentalAnalysis:
            return {
                "symbol": symbol,
                "valuation": "fair",
                "quality": "high",
                "growth": "steady",
                "financial_health": "sound",
                "confidence": 0.61,
                "summary": "Mock fundamental read assumes stable earnings quality and manageable leverage.",
                "ratios": {
                    "pe": 22.5,
                    "pb": 3.1,
                    "roe": 14.2,
                    "roce": 15.4,
                    "debt_to_equity": 0.32,
                    "eps": 98.4,
                },
            }
        if response_model is MacroAnalysis:
            return {
                "symbol": symbol,
                "market_cycle": "mid-cycle expansion",
                "inflation_impact": "manageable input-cost pressure",
                "interest_rate_impact": "neutral to mildly restrictive",
                "currency_impact": "limited near-term currency pressure",
                "sector_outlook": "constructive",
                "confidence": 0.58,
                "summary": "Mock macro view is broadly supportive but not aggressive.",
            }
        if response_model is Forecast:
            return {
                "symbol": symbol,
                "horizon": "5 trading days",
                "direction": "up",
                "predicted_price": 2580.0,
                "confidence": 0.62,
                "reasoning": "Mock synthesis weights market trend, technical support, and neutral news positively.",
            }
        if response_model is RiskAssessment:
            return {
                "symbol": symbol,
                "level": "medium",
                "score": 42.0,
                "downside": "Support break could pull price toward the lower trading range.",
                "uncertainty": "Mock data limits confidence and should be replaced with live providers.",
                "explanation": "Risk is medium due to mixed signal quality and development data sources.",
            }
        if response_model is ReflectionAnalysis:
            return {
                "symbol": symbol,
                "assumptions": ["Mock providers approximate market, news, and financial context."],
                "weaknesses": ["No live filings, order book, or real-time news are included."],
                "contradictions": [],
                "confidence_adjustment": -0.05,
                "revised_confidence": 0.57,
                "summary": "Recommendation confidence should be discounted until live providers are configured.",
            }
        if response_model is Recommendation:
            return {
                "symbol": symbol,
                "action": "HOLD",
                "confidence": 0.57,
                "risk_score": 42.0,
                "position_size": 0.0,
                "reasoning": "Mock committee output favors waiting because production data providers are not active.",
            }
        raise ValueError(f"No mock structured payload for {response_model.__name__}")
