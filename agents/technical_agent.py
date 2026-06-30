from agents.base import BaseAgent
from domain.graph_state import GraphState
from domain.technical import TechnicalAnalysis
from services.llm.service import LLMService


class TechnicalAgent(BaseAgent[GraphState, GraphState, TechnicalAnalysis]):
    name = "technical"

    def __init__(self, llm: LLMService) -> None:
        super().__init__()
        self.llm = llm

    async def execute(self, prepared_input: GraphState) -> TechnicalAnalysis:
        result = await self.llm.structured(
            "You are a technical analyst.",
            f"Symbol: {prepared_input.symbol}\n\nState:\n{prepared_input.model_dump_json(indent=2)}",
            TechnicalAnalysis,
        )
        if result.structured is None:
            raise ValueError("LLM provider returned no technical analysis")
        return result.structured
