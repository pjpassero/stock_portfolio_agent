import numpy as np
import pandas as pd
import yfinance as yf

tickers = [
    "DNUT",
    "KO",
    "MARA",
    "MU",
    "NVDA",
    "RIOT",
    "RR",
    "RZLV",
    "VOO",
    "VTI"
]


market_tickers = [
    ticker for ticker in tickers
    if ticker != "CASH"
]

current_weights = {
    "CASH": 0.5174204862819815,
    "DNUT": 0.0031897385793884583,
    "KO": 0.023616636965435242,
    "MARA": 0.013984151917583837,
    "MU": 0.161159237084668,
    "NVDA": 0.07153687380399794,
    "RIOT": 0.02508486465578672,
    "RR": 0.0035277241242243217,
    "RZLV": 0.0035963774380191062,
    "VOO": 0.14912674065878673,
    "VTI": 0.027757168490128024
}

prices = yf.download(
    market_tickers,
    period="5y",
    progress=False
)["Close"]

returns = prices.pct_change().dropna()
print(returns)

mean_daily_returns = returns.mean()
annual_returns = mean_daily_returns * 252

cov_maxtrix = returns.cov()
annual_cov_matrix = cov_maxtrix * 252
