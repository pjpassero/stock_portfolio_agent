from app.states.state import State
from pathlib import Path
from app.services.get_stock_returns import load_and_compute_returns
import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "temp"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def build_returns_matrix(state: State):
    tickers = [
        position.ticker
        for position in state["portfolioExpanded"]
    ]

    market_tickers = [
        ticker
        for ticker in tickers
        if ticker != "CASH"
    ]

    prices = yf.download(
        market_tickers,
        period="5y",
        progress=False
    )["Close"]

    prices = prices[market_tickers]

    returnsMatrix = (
        prices
        .pct_change()
        .dropna()
    )

    if state["cashWeight"] > 0:
        returnsMatrix["CASH"] = 0.0

    returnsMatrix = returnsMatrix[tickers]

    return {
        "returnMatrix": returnsMatrix
    }