from app.state import State
from app.services.get_historical_data import get_historical_data

def query_historical_data(state:State):
    for stock in state['portfolioExpanded']:
        stockTicker = stock.ticker
        stock.historicalDataPath = get_historical_data(stockTicker)
    return state