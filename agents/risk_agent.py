from agents.base import BaseAgent
from domain.graph_state import GraphState
from domain.risk import RiskAssessment
from services.llm.service import LLMService


class RiskAgent(BaseAgent[GraphState, GraphState, RiskAssessment]):
    name = "risk"

    def __init__(self, llm_service: LLMService) -> None:
        super().__init__()
        self._llm_service = llm_service

    def validate(self, agent_input: GraphState) -> None:
        if agent_input.forecast is None:
            raise ValueError("forecast is required for risk assessment")

    async def execute(self, prepared_input: GraphState) -> RiskAssessment:
        result = await self._llm_service.structured(
            "You are a portfolio risk analyst.",
            f"Symbol: {prepared_input.symbol}\nState: {prepared_input.model_dump()}\nReturn a downside risk assessment.",
            RiskAssessment,
        )
        if result.structured is None:
            raise ValueError("risk assessment was not returned")
        return result.structured
