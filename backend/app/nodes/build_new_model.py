from app.state import State
from app.services.reccomend_changes import find_changes
from copy import deepcopy

def build_new_model(state:State):
    model_state = deepcopy(state)

    portfolio = {}
    for stock in state["portfolioExpanded"]:
        portfolio[stock.ticker] = stock.allocation
    analysis_from_fin = state["fin_first_response"]

    new_allocations = find_changes(portfolio, analysis_from_fin)

    proposed = {}
    for change in new_allocations["changes"]:
        proposed[change["ticker"]] = change["proposed_allocation"]

    for stock in model_state["portfolioExpanded"]:
        stock.allocation = proposed[stock.ticker]

    return model_state