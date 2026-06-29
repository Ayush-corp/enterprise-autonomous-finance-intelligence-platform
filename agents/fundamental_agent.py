from agents.base import BaseAgent
from domain.fundamental import FundamentalAnalysis
from domain.graph_state import GraphState
from services.llm.service import LLMService


class FundamentalAgent(BaseAgent[GraphState, GraphState, FundamentalAnalysis]):
    name = "fundamental"

    def __init__(self, llm_service: LLMService) -> None:
        super().__init__()
        self._llm_service = llm_service

    async def execute(self, prepared_input: GraphState) -> FundamentalAnalysis:
        result = await self._llm_service.structured(
            "You are an institutional fundamental analyst for Indian equities.",
            f"Symbol: {prepared_input.symbol}\nReturn a conservative fundamental analysis.",
            FundamentalAnalysis,
        )
        if result.structured is None:
            raise ValueError("fundamental analysis was not returned")
        return result.structured
