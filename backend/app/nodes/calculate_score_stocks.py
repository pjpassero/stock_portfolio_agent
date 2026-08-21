from app.state import State
from app.services.retrieve_vix import get_vix
from app.services.database_connector import get_connection
from app.util.sector_mapping import SECTOR_TO_ETF

import pandas as pd
import numpy as np


ALPHA = 0.40
BETA = 0.30
GAMMA = 0.30

MAX_SECTOR_VOLATILITY = 0.35
MAX_HHI = 1.0


def calculate_stock_weights(state: State):
    stock_weight = state["stockWeight"]

    if stock_weight == 0:
        return {
            "stockInternalWeights": {}
        }

    stock_internal_weights = {}

    for position in state["stockPositions"]:
        stock_internal_weights[position.ticker] = (
            position.allocation / stock_weight
        )

    return {
        "stockInternalWeights": stock_internal_weights
    }


def calculate_stock_hhi(state: State):
    weights = state["stockInternalWeights"]

    stock_hhi = sum(
        weight ** 2
        for weight in weights.values()
    )

    return {
        "stockHHI": stock_hhi
    }


def get_min_hhi(state: State):
    num_stocks = len(state["stockPositions"])

    if num_stocks == 0:
        return 0.0

    return 1.0 / num_stocks


def calculate_stock_sector_weights(state: State):
    sector_weights = {}

    for position in state["stockPositions"]:
        weight = state["stockInternalWeights"][position.ticker]
        sector = position.sector

        if sector is None:
            continue

        sector_weights[sector] = (
            sector_weights.get(sector, 0.0) + weight
        )

    return {
        "stockSectorWeights": sector_weights
    }


def load_sector_data():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT ticker, volatility
                FROM sector_volatility
            """)

            result = cur.fetchall()

    return {
        ticker: float(volatility)
        for ticker, volatility in result
    }


def get_sector_volatility():
    df = pd.read_csv(
        "app/data/sector_data/sector_returns.csv",
        index_col="Date",
        parse_dates=True
    )

    sector_volatility = df.std() * np.sqrt(252)

    with get_connection() as conn:
        with conn.cursor() as cur:
            for ticker, volatility in sector_volatility.items():
                cur.execute(
                    """
                    INSERT INTO sector_volatility (ticker, volatility)
                    VALUES (%s, %s)
                    ON CONFLICT (ticker)
                    DO UPDATE SET volatility = EXCLUDED.volatility;
                    """,
                    (ticker, float(volatility))
                )

            conn.commit()


def calculate_sector_risk_score(state: State):
    score = 0.0

    sector_volatilities = load_sector_data()
    sector_weights = state["stockSectorWeights"]

    for sector, weight in sector_weights.items():
        etf = SECTOR_TO_ETF.get(sector)

        if etf is None:
            raise ValueError(
                f"No sector ETF mapping found for sector: {sector}"
            )

        volatility = sector_volatilities.get(etf)

        if volatility is None:
            raise ValueError(
                f"No volatility data found for sector ETF: {etf}"
            )

        score += weight * volatility

    return score


def calculate_stock_volatility(state: State):
    stock_weights = state["stockInternalWeights"]

    if not stock_weights:
        return {
            "stockVolatility": 0.0
        }

    stock_tickers = list(stock_weights.keys())

    covariance_matrix = state["covarianceMatrix"]

    stock_covariance = covariance_matrix.loc[
        stock_tickers,
        stock_tickers
    ]

    weights = np.array([
        stock_weights[ticker]
        for ticker in stock_tickers
    ])

    stock_variance = (
        weights.T
        @ stock_covariance.values
        @ weights
    )

    stock_volatility = (
        np.sqrt(stock_variance)
        * np.sqrt(252)
    )

    return {
        "stockVolatility": float(stock_volatility)
    }


def volatility_norm(state: State):
    max_volatility = get_vix() * 1.5

    return (
        state["stockVolatility"]
        / max_volatility
    )


def sector_norm(state: State):
    sector_risk = calculate_sector_risk_score(state)

    return (
        sector_risk
        / MAX_SECTOR_VOLATILITY
    )


def hhi_norm(state: State):
    min_hhi = get_min_hhi(state)

    if min_hhi == MAX_HHI:
        return 1.0

    normalized_hhi = (
        (state["stockHHI"] - min_hhi)
        / (MAX_HHI - min_hhi)
    )

    return normalized_hhi


def calculate_score(state: State):

    if state["stockWeight"] == 0:
        return {
            "stockInternalWeights": {},
            "stockSectorWeights": {},
            "stockHHI": 0.0,
            "stockVolatility": 0.0,
            "stockRisk": 0.0
        }

    weights_result = calculate_stock_weights(state)

    state["stockInternalWeights"] = (
        weights_result["stockInternalWeights"]
    )

    hhi_result = calculate_stock_hhi(state)

    state["stockHHI"] = (
        hhi_result["stockHHI"]
    )

    sector_result = calculate_stock_sector_weights(state)

    state["stockSectorWeights"] = (
        sector_result["stockSectorWeights"]
    )

    volatility_result = calculate_stock_volatility(state)

    state["stockVolatility"] = (
        volatility_result["stockVolatility"]
    )

    vol_score = volatility_norm(state)
    sector_score = sector_norm(state)
    hhi_score = hhi_norm(state)

    stock_risk = (
        ALPHA * vol_score
        + BETA * sector_score
        + GAMMA * hhi_score
    )

    print("\n--- STOCK RISK ---")
    print("Internal Weights:", state["stockInternalWeights"])
    print("Sector Weights:", state["stockSectorWeights"])
    print("HHI:", state["stockHHI"])
    print("Volatility:", state["stockVolatility"])
    print("Vol Score:", vol_score)
    print("Sector Score:", sector_score)
    print("HHI Score:", hhi_score)
    print("Stock Risk:", stock_risk)

    return {
        "stockInternalWeights": state["stockInternalWeights"],
        "stockSectorWeights": state["stockSectorWeights"],
        "stockHHI": state["stockHHI"],
        "stockVolatility": state["stockVolatility"],
        "stockRisk": stock_risk
    }