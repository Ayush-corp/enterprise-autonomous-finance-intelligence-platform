from agents.base import BaseAgent
from domain.graph_state import GraphState
from domain.recommendation import Recommendation
from services.llm.service import LLMService


class CommitteeAgent(BaseAgent[GraphState, GraphState, Recommendation]):
    name = "committee"

    def __init__(self, llm_service: LLMService) -> None:
        super().__init__()
        self._llm_service = llm_service

    def validate(self, agent_input: GraphState) -> None:
        if not all([agent_input.forecast, agent_input.risk, agent_input.reflection]):
            raise ValueError("forecast, risk, and reflection are required for recommendation")

    async def execute(self, prepared_input: GraphState) -> Recommendation:
        result = await self._llm_service.structured(
            "You are the chair of an investment committee. Return BUY, HOLD, or SELL only as action.",
            f"Symbol: {prepared_input.symbol}\nState: {prepared_input.model_dump()}\nReturn final recommendation.",
            Recommendation,
        )
        if result.structured is None:
            raise ValueError("recommendation was not returned")
        return result.structured
