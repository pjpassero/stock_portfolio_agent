from app.states.state import State
import numpy as np
from app.util.sector_mapping import SECTOR_TO_ETF
from app.services.database_connector import get_connection




def build_statistics(state: State):
    positions = state["portfolioExpanded"]
    tickers = [p.ticker for p in positions]

    weights = np.array([p.allocation for p in positions])
    betas = np.array([p.beta for p in positions])
    beta = np.dot(weights,betas)

    sector_weights = {}
    for stock in positions:
        sector_weights[stock.sector] = (
            sector_weights.get(stock.sector, 0)
            + stock.allocation
        )

    hhi = sum(
        stock.allocation ** 2
        for stock in positions
    )

  
    returns_df = state["returnMatrix"].drop(columns=["Date"])
    mean_returns_series = returns_df.mean().reindex(tickers)
    covariance_df = state["covarianceMatrix"].reindex(index=tickers, columns=tickers)

 
    if mean_returns_series.isna().any() or covariance_df.isna().any().any():
        missing = [t for t in tickers if t not in returns_df.columns]
        raise ValueError(
            f"Ticker mismatch between portfolioExpanded and returnMatrix/"
            f"covarianceMatrix: {missing or 'unknown - check both index sets'}"
        )

    mean_returns = mean_returns_series.to_numpy()
    covariance = covariance_df.to_numpy()

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

    with get_connection() as conn:
        with conn.cursor() as cur:
            update_query = """
                    UPDATE portfolio
                    SET sharpe_ratio = %s,
                        portfolio_value = %s,
                        expected_return = %s,
                        volatility = %s,
                        hhi = %s
                    WHERE id = %s
                """

            cur.execute(update_query, (
                float(sharpe_ratio),
                float(state["portfolioValue"]),
                float(portfolio_return),
                float(portfolio_volatility),
                float(hhi),
                str(state["portfolioId"]),
            ))

        conn.commit()

    return {
        "weights": weights.tolist(),
        "sectorWeights": sector_weights,
        "hhi": float(hhi),
        "meanReturns": mean_returns.tolist(),
        "portfolioVariance": float(portfolio_variance),
        "portfolioReturn": float(portfolio_return),
        "portfolioVolatility": float(portfolio_volatility),
        "sharpeRatio": float(sharpe_ratio),
        "portfolioBeta":float(beta)
        # "sector_hhi": float(sector_hhi)
    }