# agents/market_agent.py

from tools.market_tools import get_stock_data
import pandas as pd

def market_agent(state):
    print("Market agent processing state:", state)
    stock = state["stock"]

    df = get_stock_data(stock)

    # safety: flatten columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna()

    close_series = df["Close"]

    latest_close = float(close_series.iloc[-1])
    latest_volume = float(df["Volume"].iloc[-1])

    sma20 = float(close_series.rolling(20).mean().iloc[-1])

    state["market_data"] = {
        "close": latest_close,
        "volume": latest_volume,
        "sma20": sma20
    }

    return state