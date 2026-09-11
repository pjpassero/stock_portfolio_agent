from app.states.state import State
from app.services.database_connector import get_connection


def update_database(state: State):

    insert_query = """
        INSERT INTO model_portfolio (
            portfolio_id,
            modeled_return,
            modeled_portfolio_score,
            modeled_sharpe_ratio,
            modeled_portfolio_varaince,
            modeled_hhi
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """

    values = (
        str(state["portfolioId"]),
        float(state.get("portfolioReturn", 0)),
        float(state.get("portfolio_score", 0)),
        float(state.get("sharpeRatio", 0)),
        float(state.get("portfolioVariance", 0)),
        float(state.get("hhi", 0))
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(insert_query, values)
            model_portfolio_id = cur.fetchone()[0]

        conn.commit()

    return {}

    insert_query = """
        INSERT INTO model_portfolio (
            portfolio_id,
            modeled_return,
            modeled_portfolio_score,
            modeled_sharpe_ratio,
            modeled_portfolio_varaince
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """

    values = (
        str(state["portfolioId"]),
        float(state.get("portfolioReturn", 0)),
        float(state.get("portfolio_score", 0)),
        float(state.get("sharpeRatio", 0)),
        float(state.get("portfolioVariance", 0))
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(insert_query, values)

            model_portfolio_id = cur.fetchone()[0]

        conn.commit()

    return {}