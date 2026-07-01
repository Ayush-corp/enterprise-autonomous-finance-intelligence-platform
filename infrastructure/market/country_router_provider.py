from __future__ import annotations

from app.core.exceptions import MarketDataError
from domain.market import MarketSnapshot
from infrastructure.market.provider import MarketDataProvider


class CountryRouterMarketDataProvider(MarketDataProvider):
    name = "country_router"

    def __init__(
        self,
        *,
        us_provider: MarketDataProvider,
        india_provider: MarketDataProvider,
        default_provider: MarketDataProvider,
    ) -> None:
        self._us_provider = us_provider
        self._india_provider = india_provider
        self._default_provider = default_provider

    async def get_snapshot(self, symbol: str, country: str = "US") -> MarketSnapshot:
        country_code = country.strip().upper()
        if country_code == "US":
            return await self._us_provider.get_snapshot(symbol, country_code)
        if country_code == "IN":
            return await self._india_provider.get_snapshot(symbol, country_code)
        try:
            return await self._default_provider.get_snapshot(symbol, country_code)
        except MarketDataError as exc:
            raise MarketDataError(
                f"No configured market data provider could fetch {symbol} for country {country_code}: {exc}"
            ) from exc
