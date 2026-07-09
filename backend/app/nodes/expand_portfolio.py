from app.state import State
import yfinance as yf 
from app.services.yahoo import get_company_data
from app.models.positionExpanded import PositionExpanded

def expand_position_details(state: State):

    expanded_positions = []

    for position in state["portfolio"]:
        info = get_company_data(position.ticker)

        expanded_positions.append(
            PositionExpanded(
                ticker=info["symbol"],
                company_name=info["longName"],
                sector=info["sector"],
                industry=info["industry"],
                current_price=info["currentPrice"],
                market_cap=info["marketCap"],
                trailing_pe=info["trailingPE"],
                forward_pe=info["forwardPE"],
                beta=info["beta"],
                dividend_yield=info["dividendYield"],
                profit_margin=info["profitMargins"],
                revenue_growth=info["revenueGrowth"],
                earnings_growth=info["earningsGrowth"],
                debt_to_equity=info["debtToEquity"],
                return_on_equity=info["returnOnEquity"],
                fifty_two_week_change=info["52WeekChange"],
            )
        )

    return {
        "portfolioExpanded": expanded_positions
    }