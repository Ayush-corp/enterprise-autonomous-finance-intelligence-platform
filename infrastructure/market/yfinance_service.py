import yfinance as yf

from domain import MarketSnapshot
from services.market.interface import MarketDataService
from app.core.exceptions import MarketDataError


class YFinanceMarketService(MarketDataService):

    def get_market_snapshot(self, symbol: str) -> MarketSnapshot:

        try:

            df = yf.download(
                symbol,
                period="3mo",
                auto_adjust=True,
                progress=False,
            )

            if df.empty:
                raise MarketDataError(f"No data found for {symbol}")

            # Handle MultiIndex columns returned by newer yfinance versions
            if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
                df.columns = df.columns.get_level_values(0)

            close_series = df["Close"]
            volume_series = df["Volume"]

            if close_series.empty:
                raise MarketDataError("Close price missing")
        
            if volume_series.empty:
                raise MarketDataError("Volume data missing")

            close = float(close_series.iloc[-1])
            sma20 = float(close_series.rolling(20).mean().iloc[-1])
            volume = float(volume_series.iloc[-1])

            trend = "bullish" if close >= sma20 else "bearish"

            return MarketSnapshot(
                symbol=symbol,
                current_price=close,
                sma20=sma20,
                volume=volume,
                trend=trend,
            )

        except Exception as e:
            raise MarketDataError(str(e)) from e
        