import yfinance as yf
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "history"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_historical_data(tickerName:str) -> str:
    tickerHistoricalData = yf.Ticker(tickerName)

    print(tickerHistoricalData)

    df = tickerHistoricalData.history(period="5y")

    save_path = DATA_DIR / f"{tickerName}.csv"

    df.to_csv(save_path)

    return save_path
