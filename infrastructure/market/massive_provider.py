from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx

from app.core.exceptions import MarketDataError
from domain.enums import Trend
from domain.market import MarketSnapshot
from infrastructure.market.provider import MarketDataProvider


class MassiveMarketDataProvider(MarketDataProvider):
    name = "massive"

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.polygon.io",
        timeout: float = 30.0,
    ) -> None:
        if not api_key:
            raise MarketDataError("MASSIVE_API_KEY is required for live market data")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def get_snapshot(self, symbol: str, country: str = "US") -> MarketSnapshot:
        ticker = symbol.strip().upper()
        today = datetime.now(UTC).date()
        start = today - timedelta(days=60)
        url = f"{self._base_url}/v2/aggs/ticker/{ticker}/range/1/day/{start}/{today}"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 120,
            "apiKey": self._api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                payload = response.json()
        except Exception as exc:
            raise MarketDataError(f"Massive market data request failed for {ticker}: {exc}") from exc

        if payload.get("status") in {"ERROR", "NOT_AUTHORIZED"}:
            raise MarketDataError(payload.get("error") or payload.get("message") or "Massive API error")

        results = payload.get("results") or []
        if not results:
            raise MarketDataError(f"No market bars returned for {ticker}")

        closes = [float(bar["c"]) for bar in results if "c" in bar]
        if not closes:
            raise MarketDataError(f"No close prices returned for {ticker}")

        current_price = closes[-1]
        sma_window = closes[-20:] if len(closes) >= 20 else closes
        sma20 = sum(sma_window) / len(sma_window)
        latest_volume = float(results[-1].get("v") or 0.0)

        if current_price > sma20 * 1.01:
            trend = Trend.BULLISH
        elif current_price < sma20 * 0.99:
            trend = Trend.BEARISH
        else:
            trend = Trend.SIDEWAYS

        return MarketSnapshot(
            symbol=ticker,
            current_price=current_price,
            sma20=sma20,
            volume=latest_volume,
            trend=trend,
        )
