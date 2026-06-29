from __future__ import annotations

from agents.base import BaseAgent
from agents.risk.models import (
    RiskAgentInput,
    RiskAgentOutput,
)
from agents.risk.prompt import RISK_PROMPT
from infrastructure.llm.models import LLMMessage
from services.llm.service import LLMService


class RiskAgent(
    BaseAgent[
        RiskAgentInput,
        RiskAgentOutput,
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
        state: RiskAgentInput,
    ) -> str:

        return RISK_PROMPT.render(
            forecast=state.forecast.model_dump_json(indent=2),
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
            response_model=RiskAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> RiskAgentOutput:
        return result