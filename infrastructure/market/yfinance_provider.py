from __future__ import annotations

import asyncio

from app.core.exceptions import MarketDataError
from domain.enums import Trend
from domain.market import MarketSnapshot
from infrastructure.market.provider import MarketDataProvider


class YFinanceMarketDataProvider(MarketDataProvider):
    name = "yfinance"

    _country_suffixes = {
        "IN": ".NS",
        "AU": ".AX",
        "CA": ".TO",
        "DE": ".DE",
        "HK": ".HK",
        "JP": ".T",
        "UK": ".L",
    }

    async def get_snapshot(self, symbol: str, country: str = "US") -> MarketSnapshot:
        ticker = self._normalize_symbol(symbol, country)
        try:
            return await asyncio.to_thread(self._get_snapshot_sync, ticker)
        except Exception as exc:
            raise MarketDataError(f"yfinance market data request failed for {ticker}: {exc}") from exc

    def _get_snapshot_sync(self, ticker: str) -> MarketSnapshot:
        import yfinance as yf

        data = yf.Ticker(ticker).history(period="3mo", interval="1d", auto_adjust=False)
        if data.empty:
            raise MarketDataError(f"No yfinance market data returned for {ticker}")

        closes = data["Close"].dropna()
        if closes.empty:
            raise MarketDataError(f"No yfinance close prices returned for {ticker}")

        current_price = float(closes.iloc[-1])
        sma_window = closes.tail(20)
        sma20 = float(sma_window.mean())
        volume = float(data["Volume"].dropna().iloc[-1]) if "Volume" in data and not data["Volume"].dropna().empty else 0.0

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
            volume=volume,
            trend=trend,
        )

    def _normalize_symbol(self, symbol: str, country: str) -> str:
        ticker = symbol.strip().upper()
        country_code = country.strip().upper()
        if country_code == "US":
            return ticker

        if "." in ticker:
            return ticker

        suffix = self._country_suffixes.get(country_code)
        if suffix:
            return f"{ticker}{suffix}"

        return ticker
