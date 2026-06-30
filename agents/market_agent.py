from agents.base import BaseAgent
from domain.market import MarketSnapshot
from infrastructure.market.provider import MarketDataProvider


class MarketAgent(BaseAgent[str, str, MarketSnapshot]):
    name = "market"

    def __init__(self, market_provider: MarketDataProvider) -> None:
        super().__init__()
        self.market_provider = market_provider

    async def execute(self, prepared_input: str) -> MarketSnapshot:
        return await self.market_provider.get_snapshot(prepared_input.strip().upper())
