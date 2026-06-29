from domain.market import MarketSnapshot
from infrastructure.market.provider import MarketDataProvider


class MockMarketDataProvider(MarketDataProvider):
    name = "mock_market"

    async def get_snapshot(self, symbol: str) -> MarketSnapshot:
        normalized_symbol = symbol.upper()
        current_price = 2520.0
        sma20 = 2488.0
        return MarketSnapshot(
            symbol=normalized_symbol,
            current_price=current_price,
            sma20=sma20,
            volume=2_450_000.0,
            trend="bullish" if current_price >= sma20 else "bearish",
        )
