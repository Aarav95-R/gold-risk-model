import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from gold_risk.data import fetch_gold_data, GoldData


def _mock_ticker(n: int = 500):
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    np.random.seed(42)
    prices = 1800 + np.cumsum(np.random.randn(n) * 5)
    df = pd.DataFrame({"Close": prices}, index=dates)
    mock = MagicMock()
    mock.history.return_value = df
    return mock


def test_fetch_gold_data_returns_golddata():
    with patch("gold_risk.data.yf.Ticker", return_value=_mock_ticker()):
        result = fetch_gold_data(years=5)
    assert isinstance(result, GoldData)


def test_fetch_gold_data_prices_nonempty():
    with patch("gold_risk.data.yf.Ticker", return_value=_mock_ticker()):
        result = fetch_gold_data(years=5)
    assert len(result.prices) > 0


def test_fetch_gold_data_log_returns_one_shorter():
    with patch("gold_risk.data.yf.Ticker", return_value=_mock_ticker(500)):
        result = fetch_gold_data(years=5)
    assert len(result.log_returns) == len(result.prices) - 1


def test_fetch_gold_data_sigma_positive():
    with patch("gold_risk.data.yf.Ticker", return_value=_mock_ticker()):
        result = fetch_gold_data(years=5)
    assert result.sigma_global > 0


def test_fetch_gold_data_mu_is_float():
    with patch("gold_risk.data.yf.Ticker", return_value=_mock_ticker()):
        result = fetch_gold_data(years=5)
    assert isinstance(result.mu_global, float)
