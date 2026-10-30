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
# Anchored to the repo root so every notebook reads the same file regardless of cwd.
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "prices.parquet")

# Pinned study window (last trading day 2026-07-21). yfinance treats `end` as exclusive.
START = "2016-07-22"
END = "2026-07-22"


def _download(start=START, end=END):
    tickers = sorted({t for p in PAIRS for t in p})
    raw = {}
    for t in tickers:
        s = yf.Ticker(t).history(start=start, end=end, auto_adjust=True)["Close"]
        s.index = s.index.tz_localize(None).normalize()
        raw[t] = s
    return pd.DataFrame(raw).dropna()


def load_panel(start=START, end=END, refresh=False):
    """Aligned adjusted-close panel for every ticker in PAIRS.
    Builds and caches on first call; reads the cache afterwards.
    Returns (prices, log_prices)."""
    if refresh or not os.path.exists(CACHE):
        prices = _download(start, end)
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        prices.to_parquet(CACHE)
    else:
        prices = pd.read_parquet(CACHE)
    return prices, np.log(prices)