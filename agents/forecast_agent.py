from agents.base import BaseAgent
from domain.forecast import Forecast
from domain.graph_state import GraphState
from services.llm.service import LLMService


class ForecastAgent(BaseAgent[GraphState, GraphState, Forecast]):
    name = "forecast"

    def __init__(self, llm_service: LLMService) -> None:
        super().__init__()
        self._llm_service = llm_service

    def validate(self, agent_input: GraphState) -> None:
        if not all([agent_input.market, agent_input.news, agent_input.technical, agent_input.fundamental, agent_input.macro]):
            raise ValueError("market, news, technical, fundamental, and macro analyses are required")

    async def execute(self, prepared_input: GraphState) -> Forecast:
        result = await self._llm_service.structured(
            "You are a forecast analyst synthesizing multi-factor equity signals.",
            f"Symbol: {prepared_input.symbol}\nState: {prepared_input.model_dump()}\nReturn a 5 trading day forecast.",
            Forecast,
        )
        if result.structured is None:
            raise ValueError("forecast was not returned")
        return result.structured
