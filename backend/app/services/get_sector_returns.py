import yfinance as yf
import pandas as pd
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sector_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

tickers = [
    "XLC", "XLY", "XLP", "XLE", "XLF",
    "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"
]

prices = yf.download(
    tickers,
    period="5y",
    interval="1d",
    auto_adjust=True,
    progress=False
)["Close"]

returns = prices.pct_change().dropna()

print(returns.head())


returns.to_csv(DATA_DIR / "sector_returns.csv", index=True)
