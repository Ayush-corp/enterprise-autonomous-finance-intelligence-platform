from __future__ import annotations

from agents.base import BaseAgent
from agents.forecast.models import (
    ForecastAgentInput,
    ForecastAgentOutput,
)
from agents.forecast.prompt import FORECAST_PROMPT
from infrastructure.llm.models import LLMMessage
from services.llm.service import LLMService


class ForecastAgent(
    BaseAgent[
        ForecastAgentInput,
        ForecastAgentOutput,
    ]
):

    def __init__(
        self,
        llm: LLMService,
    ):
        super().__init__()
        self.llm = llm

    async def prepare(
        self,
        state: ForecastAgentInput,
    ) -> str:

        return FORECAST_PROMPT.render(
            news=state.news.model_dump_json(indent=2),
            technical=state.technical.model_dump_json(indent=2),
            macro=state.macro.model_dump_json(indent=2),
            fundamental=state.fundamental.model_dump_json(indent=2),
        )

    async def execute(
        self,
        prepared: str,
    ):

        return await self.llm.structured_chat(
            messages=[
                LLMMessage(
                    role="user",
                    content=prepared,
                )
            ],
            response_model=ForecastAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> ForecastAgentOutput:
        return result