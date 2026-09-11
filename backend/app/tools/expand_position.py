from app.models.positionExpanded import PositionExpanded
from app.services.yahoo import get_company_data
from app.models.positionExpanded import PositionExpanded
from app.services.yahoo import get_company_data


def expand_tickers(positions: list[dict]) -> list[PositionExpanded]:

    expanded_positions = []

    for position in positions:

        ticker = position["ticker"]

        if ticker.upper() == "CASH":

            new_position = PositionExpanded(
                ticker="CASH",
                company_name="Cash",
                sector=None,
                industry=None,
                current_price=position["currentBasis"],
                market_cap=None,
                trailing_pe=None,
                forward_pe=None,
                beta=0.0,
                dividend_yield=None,
                profit_margin=None,
                revenue_growth=None,
                earnings_growth=None,
                debt_to_equity=None,
                return_on_equity=None,
                fifty_two_week_change=None,
                historicalDataPath="NoSet",
                allocation=position["allocation"],
                costBasis=position["costBasis"],
                currentBasis=position["currentBasis"],
                shares=position["shares"],
                assetClass="CASH"
            )

        else:

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
                allocation=position["allocation"],
                costBasis=position["costBasis"],
                currentBasis=position["currentBasis"],
                shares=position["shares"],
                assetClass=info.get("quoteType")
            )

        expanded_positions.append(new_position)

    return expanded_positions