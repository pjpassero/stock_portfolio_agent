from app.state import State
from app.services.retrieve_vix import get_vix
from app.services.database_connector import get_connection
from app.constants.sectors import SECTOR_TO_ETF
import pandas as pd
import numpy as np


ALPHA = 0.40
BETA = 0.30
GAMMA = 0.30

MAX_SECTOR_VOLATILITY = 0.35
MAX_HHI = 1.0


def get_min_hhi(state: State):
    num_stocks = len(state["portfolioExpanded"])
    return 1.0 / num_stocks


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

    sector_weights = state["sectorWeights"]

    for sector, weight in sector_weights.items():
        etf = SECTOR_TO_ETF.get(sector)
        volatility = sector_volatilities.get(etf)

        score += weight * volatility

    return score


def volatility_norm(state: State):
    max_volatility = get_vix() * 1.5

    return state["portfolioVolatility"] / max_volatility


def sector_norm(state: State):
    sector_risk = calculate_sector_risk_score(state)

    return sector_risk / MAX_SECTOR_VOLATILITY


def hhi_norm(state: State):
    min_hhi = get_min_hhi(state)

    return (
        (state["hhi"] - min_hhi)
        / (MAX_HHI - min_hhi)
    )
def calculate_score(state: State):
    vol_score = volatility_norm(state)
    sector_score = sector_norm(state)
    hhi_score = hhi_norm(state)

    overall_stock_score = (
        ALPHA * vol_score
        + BETA * sector_score
        + GAMMA * hhi_score
    )

    return {
        "overall_stock_score": overall_stock_score
    }