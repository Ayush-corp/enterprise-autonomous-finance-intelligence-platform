from agents.base import BaseAgent
from domain.graph_state import GraphState
from domain.macro import MacroAnalysis
from services.llm.service import LLMService


class MacroAgent(BaseAgent[GraphState, GraphState, MacroAnalysis]):
    name = "macro"

    def __init__(self, llm_service: LLMService) -> None:
        super().__init__()
        self._llm_service = llm_service

    async def execute(self, prepared_input: GraphState) -> MacroAnalysis:
        result = await self._llm_service.structured(
            "You are a macro strategist covering India.",
            f"Symbol: {prepared_input.symbol}\nReturn macro context for this Indian equity.",
            MacroAnalysis,
        )
        if result.structured is None:
            raise ValueError("macro analysis was not returned")
        return result.structured
