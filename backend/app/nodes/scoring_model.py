from app.states.state import State
import numpy as np
import yfinance as yf

V_MAX = 0.40
D_MAX = 0.50
HHI_MIN = 1 / 11
N_TARGET = 30
ALPHA = 0.40
BETA = 0.30
GAMMA = 0.30
LAMBDA = 0.50


def start_scoring(state: State):
    tickers = []
    weights = []

    portfolio_inital_value = state["portfolioValue"]
    cash_weight = state["cashWeight"]
    sector_map = state["sector_map"]

    for position in state["portfolioExpanded"]:
        tickers.append(position.ticker)
        weights.append(position.allocation)

    weights = np.array(weights)

    etfs = [
        position.ticker
        for position in state["etfPositions"]
    ]

    market_tickers = [
        ticker for ticker in tickers
        if ticker != "CASH"
    ]

    prices = yf.download(
        market_tickers,
        period="5y",
        progress=False
    )["Close"]

    prices = prices[market_tickers]

    returns = prices.pct_change().dropna()

    if "CASH" in tickers:
        returns["CASH"] = 0.0

    returns = returns[tickers]

    risky_weight = 1 - cash_weight

    concentration_weights = {}

    if risky_weight > 0:
        for i, ticker in enumerate(tickers):
            if ticker != "CASH":
                concentration_weights[ticker] = (
                    weights[i] / risky_weight
                )

    covariance_matrix = state["covarianceMatrix"]

    daily_portfolio_varaince = (
        weights.T
        @ covariance_matrix
        @ weights
    )

    v_raw = np.sqrt(
        252 * daily_portfolio_varaince
    )

    v = min(
        v_raw / V_MAX,
        1
    )

    sector_exposure = {}

    for ticker, weight in concentration_weights.items():
        if ticker not in etfs:
            sector = sector_map.get(ticker)

            if sector is not None:
                if sector in sector_exposure:
                    sector_exposure[sector] += weight
                else:
                    sector_exposure[sector] = weight

    for etf_ticker in etfs:
        if etf_ticker not in concentration_weights:
            continue

        etf = yf.Ticker(etf_ticker)

        etf_sector_weights = (
            etf.funds_data.sector_weightings
        )

        etf_weight = concentration_weights[etf_ticker]

        for sector, sector_weight in etf_sector_weights.items():
            sector = sector.lower().replace(" ", "_")

            exposure = (
                etf_weight * sector_weight
            )

            if sector in sector_exposure:
                sector_exposure[sector] += exposure
            else:
                sector_exposure[sector] = exposure

    sector_hhi = sum(
        exposure ** 2
        for exposure in sector_exposure.values()
    )

    if risky_weight > 0:
        C_sector = (
            (sector_hhi - HHI_MIN)
            / (1 - HHI_MIN)
        )

        C_sector = max(
            0,
            min(C_sector, 1)
        )
    else:
        C_sector = 0

    company_exposure = {}

    for ticker, weight in concentration_weights.items():
        if ticker not in etfs:
            company_exposure[ticker] = weight

    residual_portfolio_hhi = 0

    for etf_ticker in etfs:
        if etf_ticker not in concentration_weights:
            continue

        etf = yf.Ticker(etf_ticker)

        top_holdings = (
            etf.funds_data.top_holdings
        )

        if top_holdings is None:
            continue

        N = 500

        top_holdings_weight = (
            top_holdings["Holding Percent"].sum()
        )

        remaining_weight = (
            1 - top_holdings_weight
        )

        remaining_holdings = max(
            N - len(top_holdings),
            1
        )

        etf_weight = (
            concentration_weights[etf_ticker]
        )

        remaining_portfolio_weight = (
            etf_weight * remaining_weight
        )

        residual_portfolio_hhi += (
            remaining_portfolio_weight ** 2
            / remaining_holdings
        )

        for holding_ticker, row in top_holdings.iterrows():
            fund_weight = (
                row["Holding Percent"]
            )

            portfolio_weight = (
                etf_weight * fund_weight
            )

            if holding_ticker in company_exposure:
                company_exposure[holding_ticker] += portfolio_weight
            else:
                company_exposure[holding_ticker] = portfolio_weight

    known_company_hhi = sum(
        weight ** 2
        for weight in company_exposure.values()
    )

    company_hhi = (
        known_company_hhi
        + residual_portfolio_hhi
    )

    if company_hhi > 0:
        N_EFFECTIVE = (
            1 / company_hhi
        )

        C_Comapny = (
            (N_TARGET - N_EFFECTIVE)
            / (N_TARGET - 1)
        )

        company_concentration = max(
            0,
            min(C_Comapny, 1)
        )
    else:
        N_EFFECTIVE = 0
        C_Comapny = 0
        company_concentration = 0

    C = (
        LAMBDA * company_concentration
        + (1 - LAMBDA) * C_sector
    )

    portfolio_daily_returns = (
        returns @ weights
    )

    portfolio_value = (
        portfolio_inital_value
        * (1 + portfolio_daily_returns).cumprod()
    )

    running_peak = (
        portfolio_value.cummax()
    )

    drawdown = (
        (portfolio_value - running_peak)
        / running_peak
    )

    max_drawdown = (
        drawdown.min()
    )

    D_raw = abs(
        max_drawdown
    )

    D = min(
        D_raw / D_MAX,
        1
    )

    risk = (
        ALPHA * v
        + BETA * C
        + GAMMA * D
    )

    final_fin_score = (
        (1 - risk) * 100
    )

    return {
        "portfolio_score": final_fin_score
    }