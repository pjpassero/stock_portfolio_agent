import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "temp" / "returnsMatricies"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR_GET_TEST = Path(__file__).resolve().parent.parent / "data" / "history"
DATA_DIR_GET_TEST.mkdir(parents=True, exist_ok=True)


def load_and_compute_returns(ticker):
    get_path = DATA_DIR_GET_TEST / f"{ticker}.csv"
    save_path = DATA_DIR / f"{ticker}.csv"

    df = pd.read_csv(get_path)

    df["Date"] = pd.to_datetime(df["Date"], utc=True)
    df = df.sort_values("Date")

    df[ticker] = df["Close"].pct_change()

    returns_df = df[["Date", ticker]].dropna()

    returns_df["Date"] = returns_df["Date"].dt.strftime("%Y-%m-%d")

    returns_df.to_csv(save_path, index=False)

    return returns_df