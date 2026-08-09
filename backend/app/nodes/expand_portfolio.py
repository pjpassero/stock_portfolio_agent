from app.state import State
import yfinance as yf 
from app.services.yahoo import get_company_data
from app.models.positionExpanded import PositionExpanded
from app.services.database_connector import get_connection

def expand_position_details(state: State):

    expanded_positions = []

    for position in state["portfolio"]:
        info = get_company_data(position.ticker)

        price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )

        new_postion = PositionExpanded(
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
            allocation=position.shares * position.currentBasis / state["portfolioValue"],
            costBasis=position.costBasis,
            shares=position.shares,
            assetClass=info.get("quoteType")
        )

        expanded_positions.append(new_postion)

        with get_connection() as conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO portfolio_holding (ticker, cost_basis, current_basis, shares, allocation, portfolio_id, asset_class)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                cur.execute(insert_query, (
                    new_postion.ticker,
                    new_postion.costBasis,
                    new_postion.current_price * new_postion.shares,
                    new_postion.shares,
                    new_postion.allocation,
                    state["portfolioId"],
                    new_postion.assetClass
                ))
                conn.commit()

    return {
        "portfolioExpanded": expanded_positions
    }