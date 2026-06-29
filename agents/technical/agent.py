from __future__ import annotations

from agents.base import BaseAgent
from agents.technical.models import (
    TechnicalAgentInput,
    TechnicalAgentOutput,
)
from agents.technical.prompt import TECHNICAL_PROMPT
from infrastructure.market.provider import MarketDataProvider
from infrastructure.llm.models import LLMMessage
from services.llm.service import LLMService


class TechnicalAgent(
    BaseAgent[
        TechnicalAgentInput,
        TechnicalAgentOutput,
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
        state: TechnicalAgentInput,
    ):

        indicators = await self.market_provider.technical_indicators(
            state.symbol,
        )

        return TECHNICAL_PROMPT.render(
            symbol=state.symbol,
            indicators=indicators,
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
            response_model=TechnicalAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> TechnicalAgentOutput:
        return result