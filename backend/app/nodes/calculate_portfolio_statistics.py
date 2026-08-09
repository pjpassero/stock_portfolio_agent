from app.state import State
import numpy as np
from app.util.sector_mapping import SECTOR_TO_ETF

def build_statistics(state: State):
    weights = np.array([
        position.allocation
        for position in state["portfolioExpanded"]
    ])

    sector_weights = {}
    for stock in state["portfolioExpanded"]:
        sector_weights[stock.sector] = (
            sector_weights.get(stock.sector, 0)
            + stock.allocation
        )

    hhi = sum(
        stock.allocation ** 2
        for stock in state["portfolioExpanded"]
    )

    mean_returns = (
        state["returnMatrix"]
        .drop(columns=["Date"])
        .mean()
        .to_numpy()
    )

    covariance = state["covarianceMatrix"].values

    portfolio_variance = weights.T @ covariance @ weights

    portfolio_return = (
        np.dot(weights, mean_returns)
        * 252
    )

    portfolio_volatility = (
        np.sqrt(portfolio_variance)
        * np.sqrt(252)
    )

    risk_free = 0.04

    sharpe_ratio = (
        portfolio_return - risk_free
    ) / portfolio_volatility

    
    
    return {
        "weights": weights.tolist(),
        "sectorWeights": sector_weights,
        "hhi": float(hhi),
        "meanReturns": mean_returns.tolist(),
        "portfolioVariance": float(portfolio_variance),
        "portfolioReturn": float(portfolio_return),
        "portfolioVolatility": float(portfolio_volatility),
        "sharpeRatio": float(sharpe_ratio),
    }