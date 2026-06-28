import yfinance as yf

from domain import MarketSnapshot
from domain.enums import Trend

from services.market.interface import MarketDataService
from app.core.exceptions import MarketDataError
from app.config.constants import SMA_WINDOW



class YFinanceMarketService(MarketDataService):

    async def get_market_snapshot(self, symbol: str) -> MarketSnapshot:

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
            sma20 = float(close_series.rolling(SMA_WINDOW).mean().iloc[-1])
            volume = float(volume_series.iloc[-1])

            trend = Trend.BULLISH if close >= sma20 else Trend.BEARISH

            return MarketSnapshot(
                symbol=symbol,
                current_price=close,
                sma20=sma20,
                volume=volume,
                trend=trend,
            )

        except Exception as e:
            raise MarketDataError(str(e)) from e
        