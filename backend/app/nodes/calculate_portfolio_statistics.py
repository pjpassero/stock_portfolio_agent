from app.state import State
import numpy as np
import pandas as pd

sector_weights_with_labels = {} 
sector_volatility = {}
mean_returns = {}

def get_sector_weights(state:State):
    for stock in state["portfolioExpanded"]:
        sector = stock.sector
        if sector not in sector_weights_with_labels:
            sector_weights_with_labels[sector] = 0
        sector_weights_with_labels[sector] += stock.allocation
    print(sector_weights_with_labels)

def calculate_hhi(state:State):
    hhi = 0.0
    for stock in state["portfolioExpanded"]:
        hhi += stock.allocation * stock.allocation
    return hhi


def calculate_portfolio_variance(state:State):
    weights = np.array([
        p.allocation
        for p in state["portfolioExpanded"]
    ])
    cov = state["covarianceMatrix"].values
    portfolio_variance = weights.T @ cov @ weights
    return portfolio_variance

def create_mean_return_list(state:State):
   df = state["returnMatrix"]
   mean_returns = (
    df.drop(columns=["Date"])
      .mean()
      .to_numpy()
    )
   return mean_returns

def sharpe_ratio():
    return "Sharpe"

def portfolio_beta():
    return "Beta"