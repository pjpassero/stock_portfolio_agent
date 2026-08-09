from app.services.retrieve_vix import get_vix
from state import State

def min_hhi(state:State):
    return len(state["portfolioExpanded"])


alpha = 0.40
beta = 0.30
gamma = 0.30

max_volatility = get_vix() * 1.5
max_sector_volatility = 0.35
max_hhi = 1.0
min_hhi = 1.0/min_hhi()



def volatility_norm(state:State):
    return state["portfolioVolatility"] / max_volatility

def hhi_norm(state:State):
    return (state["hhi"] - min_hhi) / (max_hhi - min_hhi)
