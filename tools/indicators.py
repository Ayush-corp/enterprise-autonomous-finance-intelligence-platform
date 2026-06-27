# tools/indicators.py

import pandas as pd

def compute_indicators(df):
    df["sma20"] = df["Close"].rolling(20).mean()
    df["rsi"] = compute_rsi(df["Close"])
    df["volatility"] = df["Close"].pct_change().rolling(10).std()
    return df

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
