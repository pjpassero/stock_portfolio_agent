from app.states.state import State
from app.services.database_connector import get_connection

def build_correlation_matrix(state: State):
    df = state["returnMatrix"]

    df = df.drop(
        columns=["CASH"],
        errors="ignore"
    )

    corr = df.corr()

    with get_connection() as conn:
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO matrix (portfolio_id, type, ticker_a, ticker_b, value)
                VALUES (%s, %s, %s, %s, %s)
            """

            rows = [
                (
                    state["portfolioId"],
                    "correlation",
                    a,
                    b,
                    float(corr.loc[a, b])
                )
                for a in corr.index
                for b in corr.columns
            ]

            cur.executemany(insert_query, rows)
            conn.commit()

    return {
        "correlationMatrix": corr
    }