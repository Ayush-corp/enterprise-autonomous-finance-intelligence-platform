from infrastructure.market.yfinance_service import YFinanceMarketService


def test_market():

    service = YFinanceMarketService()

    snapshot = service.get_market_snapshot("RELIANCE.NS")

    assert snapshot.symbol == "RELIANCE.NS"

    assert snapshot.current_price > 0