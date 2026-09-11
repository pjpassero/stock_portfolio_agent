from app.states.state import State
from app.services.yahoo import get_company_data
from app.models.positionExpanded import PositionExpanded


def add_position(state: State):

    new_positions = state["new_positions"]
    portfolio = state["portfolioExpanded"]

    for ticker, shares in new_positions.items():
        print("Position: " + ticker + " will be added.")

        info = get_company_data(ticker)

        price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )

        new_position = PositionExpanded(
            ticker=info["symbol"],
            company_name=(
                info.get("longName")
                or info.get("displayName")
                or info.get("shortName")
                or info.get("symbol")
            ),
            sector=info.get("sector"),
            industry=info.get("industry"),
            current_price=price,
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
            allocation=(
                shares * price
                / state["portfolioValue"]
            ),
            costBasis=price,
            shares=shares,
            assetClass=info.get("quoteType")
        )

        portfolio.append(new_position)


    #need to add DB entry
    return {
        "portfolioExpanded": portfolio
    }