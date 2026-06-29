from agents.base import BaseAgent
from domain.graph_state import GraphState
from domain.reflection import ReflectionAnalysis
from services.llm.service import LLMService


class ReflectionAgent(BaseAgent[GraphState, GraphState, ReflectionAnalysis]):
    name = "reflection"

    def __init__(self, llm_service: LLMService) -> None:
        super().__init__()
        self._llm_service = llm_service

    def validate(self, agent_input: GraphState) -> None:
        if agent_input.forecast is None or agent_input.risk is None:
            raise ValueError("forecast and risk are required for reflection")

    async def execute(self, prepared_input: GraphState) -> ReflectionAnalysis:
        result = await self._llm_service.structured(
            "You are a skeptical investment reviewer looking for contradictions.",
            f"Symbol: {prepared_input.symbol}\nState: {prepared_input.model_dump()}\nChallenge the committee inputs.",
            ReflectionAnalysis,
        )
        if result.structured is None:
            raise ValueError("reflection analysis was not returned")
        return result.structured
