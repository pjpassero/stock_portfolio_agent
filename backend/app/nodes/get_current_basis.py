from app.extraction_state import ExtractionState
from app.services.yahoo import get_company_data


def update_current_basis(state: ExtractionState):
    portfolio = state["portfolio"]

    for position in portfolio["positions"]:
        ticker = position["ticker"].upper()

        if ticker == "CASH":
            continue

        position_info = get_company_data(ticker)

        price = (
            position_info.get("currentPrice")
            or position_info.get("regularMarketPrice")
            or position_info.get("previousClose")
        )

        position["currentBasis"] = price

    return {
        "portfolio": portfolio
    }