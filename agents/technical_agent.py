# agents/technical_agent.py

from tools.market_tools import get_stock_data
from tools.indicators import compute_indicators

def technical_agent(state):
    print("Technical agent processing state:", state)
    df = get_stock_data(state["stock"])
    df = compute_indicators(df)

    latest = df.iloc[-1]

    state["technical_data"] = {
        "sma20": latest["sma20"],
        "rsi": latest["rsi"],
        "volatility": latest["volatility"],
        "close": latest["Close"]
    }

    return state