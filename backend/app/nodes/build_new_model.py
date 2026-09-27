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
    new_positions = {}

    for change in new_allocations["changes"]:
        ticker = change["ticker"]
        proposed_allocation = float(change["proposed_allocation"])

        proposed[ticker] = proposed_allocation

        if ticker not in portfolio:
            new_positions[ticker] = proposed_allocation

    for stock in model_positions:
        stock.allocation = proposed[stock.ticker]

    model_portfolio = ModelPortfolio(
        positions=model_positions,
        portfolio_value=state["portfolioValue"]
    )

    return {
        "model_portfolio": model_portfolio,
        "need_new_calculations": bool(
            new_allocations["need_new_calculations"]
        ),
        "new_positions": new_positions,
        "short_explanation": str(
            new_allocations["short-explanation"]
        )
    }