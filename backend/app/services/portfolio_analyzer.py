import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "returns"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR_GET_TEST = Path(__file__).resolve().parent.parent / "data" / "history"
DATA_DIR_GET_TEST.mkdir(parents=True, exist_ok=True)


def load_and_compute_returns(filename, ticker):
    df = pd.read_csv(filename)

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df[ticker] = df["Close"].pct_change()

    return df[["Date", ticker]].dropna()




ticker = "MU"

get_path = DATA_DIR_GET_TEST / f"{ticker}.csv"
save_path = DATA_DIR / f"{ticker}.csv"

returns_df = load_and_compute_returns(get_path, ticker)

returns_df.to_csv(save_path, index=False)