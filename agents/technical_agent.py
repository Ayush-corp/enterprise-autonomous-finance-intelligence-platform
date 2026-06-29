from agents.base import BaseAgent
from domain.graph_state import GraphState
from domain.technical import TechnicalAnalysis
from services.llm.service import LLMService


class TechnicalAgent(BaseAgent[GraphState, GraphState, TechnicalAnalysis]):
    name = "technical"

    def __init__(self, llm_service: LLMService) -> None:
        super().__init__()
        self._llm_service = llm_service

    def validate(self, agent_input: GraphState) -> None:
        if agent_input.market is None:
            raise ValueError("market snapshot is required for technical analysis")

    async def execute(self, prepared_input: GraphState) -> TechnicalAnalysis:
        result = await self._llm_service.structured(
            "You are an institutional technical analyst for Indian equities.",
            (
                f"Symbol: {prepared_input.symbol}\n"
                f"Market snapshot: {prepared_input.market.model_dump() if prepared_input.market else {}}\n"
                "Return a conservative technical analysis."
            ),
            TechnicalAnalysis,
        )
        if result.structured is None:
            raise ValueError("technical analysis was not returned")
        return result.structured
