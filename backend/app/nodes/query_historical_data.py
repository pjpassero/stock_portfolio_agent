from app.state import State
from app.services.get_historical_data import get_historical_data


def query_historical_data(state: State):
    for position in state["portfolioExpanded"]:

        if position.assetClass == "CASH":
            position.historicalDataPath = None
            continue

        position.historicalDataPath = get_historical_data(
            position.ticker
        )

    return state