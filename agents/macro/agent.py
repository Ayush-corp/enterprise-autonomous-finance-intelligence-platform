from __future__ import annotations

from agents.base import BaseAgent
from agents.macro.models import (
    MacroAgentInput,
    MacroAgentOutput,
)
from agents.macro.prompt import MACRO_PROMPT
from infrastructure.market.provider import MarketDataProvider
from infrastructure.llm.models import LLMMessage
from services.llm.service import LLMService


class MacroAgent(
    BaseAgent[
        MacroAgentInput,
        MacroAgentOutput,
    ]
):

    def __init__(
        self,
        market_provider: MarketDataProvider,
        llm: LLMService,
    ):
        super().__init__()
        self.market_provider = market_provider
        self.llm = llm

    async def prepare(
        self,
        state: MacroAgentInput,
    ) -> str:

        macro = await self.market_provider.macro_data()

        return MACRO_PROMPT.render(
            symbol=state.symbol,
            macro=macro,
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
            response_model=MacroAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> MacroAgentOutput:
        return result