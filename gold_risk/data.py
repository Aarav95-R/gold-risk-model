from dataclasses import dataclass

import numpy as np
import pandas as pd
import yfinance as yf


@dataclass
class GoldData:
    prices: pd.Series          # daily closing prices
    log_returns: pd.Series     # log(P_t / P_{t-1}), length = len(prices) - 1
    mu_global: float           # annualised mean log-return
    sigma_global: float        # annualised std of log-returns


def fetch_gold_data(years: int = 5) -> GoldData:
    """Fetch GC=F (gold futures) and calibrate global GBM parameters."""
    end = pd.Timestamp.today()
    start = end - pd.DateOffset(years=years)

    ticker = yf.Ticker("GC=F")
    df = ticker.history(start=start, end=end)
    prices = df["Close"].dropna()

    log_returns = np.log(prices / prices.shift(1)).dropna()

    mu_global = float(log_returns.mean() * 252)
    sigma_global = float(log_returns.std() * np.sqrt(252))

    return GoldData(
        prices=prices,
        log_returns=log_returns,
        mu_global=mu_global,
        sigma_global=sigma_global,
    )
