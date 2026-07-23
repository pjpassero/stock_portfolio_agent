from app.state import State
from pathlib import Path
from app.services.get_stock_returns import load_and_compute_returns
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "temp"
DATA_DIR.mkdir(parents=True, exist_ok=True)



def build_returns_matrix(state:State) -> str:
    save_path = DATA_DIR / "returns.csv"
    returnsMatrix = None
    for stock in state["portfolioExpanded"]:
        df = pd.read_csv(stock.historicalDataPath)
        returns = load_and_compute_returns(
            stock.ticker

        )

        if returnsMatrix is None:
            returnsMatrix = returns 
        else:
            returnsMatrix = returnsMatrix.merge(returns, on="Date")

        returnsMatrix = returnsMatrix.dropna()

        returnsMatrix.to_csv(save_path, index=False)
    return {
            "returnMatrix":returnsMatrix
        }


        