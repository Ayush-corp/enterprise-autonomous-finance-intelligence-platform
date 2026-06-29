from __future__ import annotations

from agents.base import BaseAgent
from agents.committee.models import (
    CommitteeAgentInput,
    CommitteeAgentOutput,
)
from agents.committee.prompt import COMMITTEE_PROMPT
from infrastructure.llm.models import LLMMessage
from services.llm.service import LLMService


class CommitteeAgent(
    BaseAgent[
        CommitteeAgentInput,
        CommitteeAgentOutput,
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
        state: CommitteeAgentInput,
    ) -> str:

        return COMMITTEE_PROMPT.render(
            forecast=state.forecast.model_dump_json(indent=2),
            risk=state.risk.model_dump_json(indent=2),
            reflection=state.reflection.model_dump_json(indent=2),
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
            response_model=CommitteeAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> CommitteeAgentOutput:
        return result