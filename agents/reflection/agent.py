from __future__ import annotations

from agents.base import BaseAgent
from agents.reflection.models import (
    ReflectionAgentInput,
    ReflectionAgentOutput,
)
from agents.reflection.prompt import REFLECTION_PROMPT
from infrastructure.llm.models import LLMMessage
from services.llm.service import LLMService


class ReflectionAgent(
    BaseAgent[
        ReflectionAgentInput,
        ReflectionAgentOutput,
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
        state: ReflectionAgentInput,
    ) -> str:

        return REFLECTION_PROMPT.render(
            forecast=state.forecast.model_dump_json(indent=2),
            risk=state.risk.model_dump_json(indent=2),
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
            response_model=ReflectionAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> ReflectionAgentOutput:
        return result