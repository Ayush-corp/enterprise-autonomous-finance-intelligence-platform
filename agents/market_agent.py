from domain.market import MarketSnapshot
from infrastructure.market.provider import MarketDataProvider
from agents.base import BaseAgent


class MarketAgent(BaseAgent[str, str, MarketSnapshot]):
    name = "market"

    def __init__(self, provider: MarketDataProvider) -> None:
        super().__init__()
        self._provider = provider

    def validate(self, agent_input: str) -> None:
        if not agent_input.strip():
            raise ValueError("symbol is required")

    async def execute(self, prepared_input: str) -> MarketSnapshot:
        return await self._provider.get_snapshot(prepared_input.upper())
