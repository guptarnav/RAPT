# Regime Aware Pairs Trading

## What This Project Is About
Standard pairs trading tests (like the full-sample Engle-Granger test) often miss good trading pairs. When two stocks drift over time, static tests treat them like random noise and throw them out - especially once you adjust for testing multiple pairs. 

This project proves that static tests lose power when hedge ratios ($\beta$) change over time, and demonstrates how state-space models (Kalman Filters) can track changing parameters in real time to trade these dynamic relationships effectively.

---

## How to Run the Notebooks

Run the notebooks in order:

1. `notebooks/01_coint_tests.ipynb`
   Run the static vs. rolling cointegration scans on the 20-pair universe and view the Static-Power Paradox exhibit (V/MA case study).

2. `notebooks/02_ols_benchmarks.ipynb`
   Evaluate static and rolling OLS baselines on out-of-sample data to quantify parameter lag and execution drag.


---

## Setup & Installation

1. Clone the repo:
   git clone <https://github.com/guptarnav/RAPT>
   cd RAPT

2. Install dependencies (Python 3.13):
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. Data: prices are not committed. On first run, `models/data.py` downloads adjusted closes from Yahoo Finance for the pinned window 2016-07-22 → 2026-07-21 and caches them to `data/prices.parquet`; later runs read the cache. Yahoo back-adjusts history for later dividends and splits, so a fresh download has the same dates but slightly different adjusted prices, and results may differ a little from the saved notebook outputs.