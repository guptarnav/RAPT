import os
import numpy as np
import pandas as pd
import yfinance as yf

PAIRS = [
    ("GLD","SLV"), ("GLD","IAU"), ("SPY","IVV"),
    ("XLE","XOP"), ("EEM","EMB"),
    ("KO","PEP"), ("XOM","CVX"), ("HD","LOW"),
    ("V","MA"), ("EWA","EWC"), ("USO","BNO"),
    ("TLT","IEF"), ("XLK","QQQ"), ("GDX","GDXJ"),
    ("XLP","XLU"), ("IWM","IWO"), ("EFA","VEA"),
    ("LQD","HYG"), ("XLI","XLB"), ("MSFT","AAPL"),
]

ADF_MAXLAG = 1
CACHE = "data/prices.parquet"


def _download(period="10y"):
    tickers = sorted({t for p in PAIRS for t in p})
    raw = {}
    for t in tickers:
        s = yf.Ticker(t).history(period=period, auto_adjust=True)["Close"]
        s.index = s.index.tz_localize(None).normalize()
        raw[t] = s
    return pd.DataFrame(raw).dropna()


def load_panel(period="10y", refresh=False):
    """Aligned adjusted-close panel for every ticker in PAIRS.
    Builds and caches on first call; reads the cache afterwards.
    Returns (prices, log_prices)."""
    if refresh or not os.path.exists(CACHE):
        prices = _download(period)
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        prices.to_parquet(CACHE)
    else:
        prices = pd.read_parquet(CACHE)
    return prices, np.log(prices)