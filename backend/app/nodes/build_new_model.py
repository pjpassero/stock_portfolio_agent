from app.states.state import State
from app.services.reccomend_changes import find_changes
from app.models.model_portfolio import ModelPortfolio
from copy import deepcopy

def build_new_model(state: State):
    model_positions = deepcopy(state["portfolioExpanded"])

    portfolio = {}

    for stock in state["portfolioExpanded"]:
        portfolio[stock.ticker] = stock.allocation

    new_allocations = find_changes(
        portfolio,
        state["fin_first_response"]
    )

    proposed = {}

    for change in new_allocations["changes"]:
        proposed[change["ticker"]] = change["proposed_allocation"]

    for stock in model_positions:
        stock.allocation = proposed[stock.ticker]

    model_portfolio = ModelPortfolio(
        positions=model_positions,
        portfolio_value=state["portfolioValue"]
    )

    return {
        "model_portfolio": model_portfolio,
        "need_new_calculations": bool(new_allocations["need_new_calculations"]),
        "new_positions": new_allocations["tickers_added"]
    }