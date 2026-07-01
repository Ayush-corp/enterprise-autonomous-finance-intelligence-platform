from __future__ import annotations

from app.core.exceptions import MarketDataError
from domain.market import MarketSnapshot
from infrastructure.market.provider import MarketDataProvider


class FallbackMarketDataProvider(MarketDataProvider):
    name = "fallback_market"

    def __init__(self, providers: list[MarketDataProvider]) -> None:
        if not providers:
            raise ValueError("At least one market data provider is required")
        self._providers = providers

    async def get_snapshot(self, symbol: str, country: str = "US") -> MarketSnapshot:
        errors: list[str] = []
        for provider in self._providers:
            try:
                return await provider.get_snapshot(symbol, country)
            except MarketDataError as exc:
                errors.append(f"{provider.name}: {exc}")
        raise MarketDataError("; ".join(errors))
