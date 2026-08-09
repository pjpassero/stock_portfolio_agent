from app.state import State
from app.services.get_covariance_matrix_service import calculate_covariance_matrix
import pandas as pd
from app.services.database_connector import get_connection
from psycopg2.extras import Json
def build_covariance_matrix(state: State):
    df = state["returnMatrix"]
    df = df.drop(columns=["Date"])
    cov = df.cov()

    with get_connection() as conn:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO matrix (portfolio_id, type, ticker_a, ticker_b, value)
                VALUES (%s, %s, %s, %s, %s)
            """

            rows = [
                (state["portfolioId"], "covariance", a, b, float(cov.loc[a, b]))
                for a in cov.index
                for b in cov.columns
            ]

            cur.executemany(insert_query, rows)
            conn.commit()

    return {
        "covarianceMatrix": cov
    }