import asyncio

from domain import MarketSnapshot
from infrastructure.market.mock_provider import MockMarketDataProvider
from services.market.interface import MarketDataService


class YFinanceMarketService(MarketDataService):
    """Compatibility adapter; live yfinance support will be added as an explicit provider."""

    def get_market_snapshot(self, symbol: str) -> MarketSnapshot:
        return asyncio.run(MockMarketDataProvider().get_snapshot(symbol))
