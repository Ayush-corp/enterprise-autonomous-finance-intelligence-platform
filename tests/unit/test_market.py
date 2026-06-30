import pytest

from infrastructure.market.mock_provider import MockMarketDataProvider


@pytest.mark.asyncio
async def test_market_provider_returns_snapshot():
    provider = MockMarketDataProvider()

    snapshot = await provider.get_snapshot("RELIANCE.NS")

    assert snapshot.symbol == "RELIANCE.NS"
    assert snapshot.current_price > 0
