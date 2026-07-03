from app.state import State
import yfinance as yf 
from app.services.yahoo import get_company_data

def get_stock_data(state:State):
    info = get_company_data(state["ticker"])

    state["company_name"] = info.get("longName")
    state["sector"] = info.get("sector")
    state["industry"] = info.get("industry")

    state["current_price"] = info.get("currentPrice")
    state["market_cap"] = info.get("marketCap")

    state["trailing_pe"] = info.get("trailingPE")
    state["forward_pe"] = info.get("forwardPE")

    state["beta"] = info.get("beta")
    state["dividend_yield"] = info.get("dividendYield")

    state["profit_margin"] = info.get("profitMargins")
    state["revenue_growth"] = info.get("revenueGrowth")
    state["earnings_growth"] = info.get("earningsGrowth")

    state["debt_to_equity"] = info.get("debtToEquity")
    state["return_on_equity"] = info.get("returnOnEquity")

    state["fifty_two_week_change"] = info.get("52WeekChange")    
    return state