from app.state import State
import numpy as np

from app.services.etf_service import get_etf_holdings, get_holding_sector
from app.services.retrieve_vix import get_vix


ALPHA = 0.40
BETA = 0.30
GAMMA = 0.30


def calculate_etf_weights(state: State):
    etf_weight = state["etfWeight"]

    if etf_weight == 0:
        return {
            "etfInternalWeights": {}
        }

    etf_internal_weights = {}

    for position in state["etfPositions"]:
        etf_internal_weights[position.ticker] = (
            position.allocation / etf_weight
        )

    return {
        "etfInternalWeights": etf_internal_weights
    }


def calculate_etf_volatility(state: State):
    etf_weights = state["etfInternalWeights"]

    if not etf_weights:
        return {
            "etfVolatility": 0.0
        }

    etf_tickers = list(etf_weights.keys())

    covariance_matrix = state["covarianceMatrix"]

    etf_covariance = covariance_matrix.loc[
        etf_tickers,
        etf_tickers
    ]

    weights = np.array([
        etf_weights[ticker]
        for ticker in etf_tickers
    ])

    etf_variance = (
        weights.T
        @ etf_covariance.values
        @ weights
    )

    etf_volatility = (
        np.sqrt(etf_variance)
        * np.sqrt(252)
    )

    return {
        "etfVolatility": float(etf_volatility)
    }


def calculate_underlying_hhi(ticker: str):
    holdings = get_etf_holdings(ticker)

    weights = holdings["Holding Percent"]

    hhi = sum(
        weight ** 2
        for weight in weights
    )

    return float(hhi)


def calculate_etf_holdings_concentration(state: State):
    score = 0.0

    for position in state["etfPositions"]:
        etf_weight = state["etfInternalWeights"][position.ticker]

        underlying_hhi = calculate_underlying_hhi(
            position.ticker
        )

        score += etf_weight * underlying_hhi

    return {
        "etfHoldingsHHI": score
    }


def calculate_etf_sector_concentration(state: State):
    combined_sector_weights = {}

    for position in state["etfPositions"]:
        etf_weight = state["etfInternalWeights"][position.ticker]

        holdings = get_etf_holdings(position.ticker)

        for ticker, holding in holdings.iterrows():
            sector = get_holding_sector(ticker)

            if sector is None:
                continue

            holding_weight = holding["Holding Percent"]

            combined_sector_weights[sector] = (
                combined_sector_weights.get(sector, 0.0)
                + etf_weight * holding_weight
            )

    total_weight = sum(combined_sector_weights.values())

    if total_weight > 0:
        combined_sector_weights = {
            sector: weight / total_weight
            for sector, weight in combined_sector_weights.items()
        }

    sector_hhi = sum(
        weight ** 2
        for weight in combined_sector_weights.values()
    )

    return {
        "etfSectorWeights": combined_sector_weights,
        "etfSectorHHI": sector_hhi
    }


def etf_volatility_norm(state: State):
    max_volatility = get_vix() * 1.5

    return (
        state["etfVolatility"]
        / max_volatility
    )


def etf_holdings_hhi_norm(state: State):
    hhi = state["etfHoldingsHHI"]

    return min(max(hhi, 0.0), 1.0)


def etf_sector_hhi_norm(state: State):
    sector_weights = state["etfSectorWeights"]

    if not sector_weights:
        return 0.0

    num_sectors = len(sector_weights)

    if num_sectors == 1:
        return 1.0

    min_hhi = 1.0 / num_sectors

    normalized_hhi = (
        (state["etfSectorHHI"] - min_hhi)
        / (1.0 - min_hhi)
    )

    return min(max(normalized_hhi, 0.0), 1.0)


def calculate_etf_score(state: State):
    if state["etfWeight"] == 0:
        return {
            "etfInternalWeights": {},
            "etfVolatility": 0.0,
            "etfHoldingsHHI": 0.0,
            "etfSectorWeights": {},
            "etfSectorHHI": 0.0,
            "etfRisk": 0.0
        }

    weights_result = calculate_etf_weights(state)
    state["etfInternalWeights"] = (
        weights_result["etfInternalWeights"]
    )

    volatility_result = calculate_etf_volatility(state)
    state["etfVolatility"] = (
        volatility_result["etfVolatility"]
    )

    holdings_result = calculate_etf_holdings_concentration(state)
    state["etfHoldingsHHI"] = (
        holdings_result["etfHoldingsHHI"]
    )

    sector_result = calculate_etf_sector_concentration(state)
    state["etfSectorWeights"] = (
        sector_result["etfSectorWeights"]
    )
    state["etfSectorHHI"] = (
        sector_result["etfSectorHHI"]
    )

    volatility_score = etf_volatility_norm(state)
    holdings_score = etf_holdings_hhi_norm(state)
    sector_score = etf_sector_hhi_norm(state)

    etf_risk = (
        ALPHA * volatility_score
        + BETA * holdings_score
        + GAMMA * sector_score
    )

    print("\n--- ETF RISK ---")
    print("Internal Weights:", state["etfInternalWeights"])
    print("Volatility:", state["etfVolatility"])
    print("Holdings HHI:", state["etfHoldingsHHI"])
    print("Sector Weights:", state["etfSectorWeights"])
    print("Sector HHI:", state["etfSectorHHI"])
    print("Volatility Score:", volatility_score)
    print("Holdings Score:", holdings_score)
    print("Sector Score:", sector_score)
    print("ETF Risk:", etf_risk)

    return {
        "etfInternalWeights": state["etfInternalWeights"],
        "etfVolatility": state["etfVolatility"],
        "etfHoldingsHHI": state["etfHoldingsHHI"],
        "etfSectorWeights": state["etfSectorWeights"],
        "etfSectorHHI": state["etfSectorHHI"],
        "etfRisk": etf_risk
    }