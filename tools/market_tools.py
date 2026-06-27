import yfinance as yf
import pandas as pd

def get_stock_data(symbol: str):
    df = yf.download(symbol, period="6mo", interval="1d")
    df = df.reset_index()
    return df