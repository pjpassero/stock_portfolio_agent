from app.states.state import State
from app.services.database_connector import get_connection


def update_database(state: State):
    print(state["portfolioExpanded"])


    insert_query = """
        INSERT INTO model_portfolio (
            portfolio_id,
            modeled_return,
            modeled_portfolio_score,
            modeled_sharpe_ratio,
            modeled_portfolio_varaince,
            modeled_hhi,
            short_reasoning
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """

    update_model_positions_query = """
        INSERT INTO model_portfolio_position (portfolio_id, modeled_allocation, ticker) VALUES(%s, %s, %s)
    """



    values = (
        str(state["portfolioId"]),
        float(state.get("portfolioReturn", 0)),
        float(state.get("portfolio_score", 0)),
        float(state.get("sharpeRatio", 0)),
        float(state.get("portfolioVariance", 0)),
        float(state.get("hhi", 0)),
        str(state.get("short_explanation"))
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(insert_query, values)
            model_portfolio_id = cur.fetchone()[0]

            for position in state["portfolioExpanded"]:
                cur.execute(update_model_positions_query, (str(state["portfolioId"]), float(position.allocation), str(position.ticker),))
        conn.commit()

    return {}


    