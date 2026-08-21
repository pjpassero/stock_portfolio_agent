from app.state import State
from pathlib import Path
from app.services.get_stock_returns import load_and_compute_returns
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "temp"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def build_returns_matrix(state: State) -> str:
    save_path = DATA_DIR / "returns.csv"
    returnsMatrix = None
    has_cash = False

    for position in state["portfolioExpanded"]:

        if position.assetClass == "CASH":
            has_cash = True
            continue

        returns = load_and_compute_returns(
            position.ticker
        )

        if returnsMatrix is None:
            returnsMatrix = returns
        else:
            returnsMatrix = returnsMatrix.merge(
                returns,
                on="Date"
            )

    if returnsMatrix is None:
        return {
            "returnMatrix": None
        }

    returnsMatrix = returnsMatrix.dropna()

    if has_cash:
        returnsMatrix["CASH"] = 0.0

    returnsMatrix.to_csv(
        save_path,
        index=False
    )

    return {
        "returnMatrix": returnsMatrix
    }