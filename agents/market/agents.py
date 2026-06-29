from __future__ import annotations

from agents.base import BaseAgent
from agents.market.models import (
    MarketAgentInput,
    MarketAgentOutput,
)
from agents.market.prompts import MARKET_AGENT_PROMPT
from infrastructure.llm.client import LLMClient


class MarketAgent(
    BaseAgent[
        MarketAgentInput,
        MarketAgentOutput,
    ]
):
    def __init__(self, llm: LLMClient):
        super().__init__()
        self.llm = llm

    async def prepare(
        self,
        state: MarketAgentInput,
    ) -> str:

        return f"""
{MARKET_AGENT_PROMPT}

Ticker:
{state.symbol}
"""

    async def execute(
        self,
        prepared: str,
    ):

        return await self.llm.complete(prepared)

    async def parse(
        self,
        result,
    ) -> MarketAgentOutput:

        return MarketAgentOutput.model_validate(result)