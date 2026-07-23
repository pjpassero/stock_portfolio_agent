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
                company_name = (
                    info.get("longName")
                    or info.get("displayName")
                    or info.get("shortName")
                    or info.get("symbol")
                ),
                sector=info.get("sector"),
                industry=info.get("industry"),
                current_price=info.get("currentPrice"),
                market_cap=info.get("marketCap"),
                trailing_pe=info.get("trailingPE"),
                forward_pe=info.get("forwardPE"),
                beta=info.get("beta"),
                dividend_yield=info.get("dividendYield"),
                profit_margin=info.get("profitMargins"),
                revenue_growth=info.get("revenueGrowth"),
                earnings_growth=info.get("earningsGrowth"),
                debt_to_equity=info.get("debtToEquity"),
                return_on_equity=info.get("returnOnEquity"),
                fifty_two_week_change=info.get("52WeekChange"),
                historicalDataPath="NoSet",
                allocation=position.shares * position.currentBasis / state["portfolioValue"],
                costBasis = position.costBasis
            )
        )

    return {
        "portfolioExpanded": expanded_positions
    }