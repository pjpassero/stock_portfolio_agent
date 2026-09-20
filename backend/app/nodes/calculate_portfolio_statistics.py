from app.states.state import State
import numpy as np
from app.services.database_connector import get_connection


def build_statistics(state: State):
    positions = state["portfolioExpanded"]
    tickers = [p.ticker for p in positions]

    weights = np.array([p.allocation for p in positions])
    betas = np.array([p.beta for p in positions])
    beta = np.dot(weights, betas)

    sector_weights = {}

    for stock in positions:
        if stock.assetClass == "CASH":
            continue

        if stock.sector is not None:
            sector_weights[stock.sector] = (
                sector_weights.get(stock.sector, 0)
                + stock.allocation
            )

    hhi = sum(
        position.allocation ** 2
        for position in positions
        if position.assetClass != "CASH"
    )

    returns_df = state["returnMatrix"]

    mean_returns_series = (
        returns_df.mean().reindex(tickers)
    )

    covariance_df = (
        state["covarianceMatrix"]
        .reindex(index=tickers, columns=tickers)
    )

    if mean_returns_series.isna().any() or covariance_df.isna().any().any():
        missing = [
            ticker
            for ticker in tickers
            if ticker not in returns_df.columns
        ]

        raise ValueError(
            f"Ticker mismatch between portfolioExpanded and returnMatrix/"
            f"covarianceMatrix: {missing or 'unknown - check both index sets'}"
        )

    mean_returns = mean_returns_series.to_numpy()
    covariance = covariance_df.to_numpy()

    portfolio_variance = (
        weights.T
        @ covariance
        @ weights
    )

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
        "portfolioBeta": float(beta)
    }