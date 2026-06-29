from __future__ import annotations

from agents.base import BaseAgent
from agents.fundamental.models import (
    FundamentalAgentInput,
    FundamentalAgentOutput,
)
from agents.fundamental.prompt import FUNDAMENTAL_PROMPT
from infrastructure.market.provider import MarketDataProvider
from infrastructure.llm.models import LLMMessage
from services.llm.service import LLMService


class FundamentalAgent(
    BaseAgent[
        FundamentalAgentInput,
        FundamentalAgentOutput,
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
        state: FundamentalAgentInput,
    ) -> str:

        financials = await self.market_provider.fundamentals(
            state.symbol,
        )

        return FUNDAMENTAL_PROMPT.render(
            symbol=state.symbol,
            financials=financials,
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
            response_model=FundamentalAgentOutput,
        )

    async def parse(
        self,
        result,
    ) -> FundamentalAgentOutput:
        return result