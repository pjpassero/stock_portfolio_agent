from app.services.database_connector import get_connection
from langchain_core.tools import tool


@tool
def get_model_portfolio(portfolioId: str = ""):
    """
    Fin will run a new simualtion on the portfolio to reallocate funds to raise the score of the portfolio.
    This tool will allow Fin to grab that new data from the database where it is stored.
    
    
    """

    query = """
        SELECT modeled_return,
               modeled_portfolio_score,
               modeled_sharpe_ratio,
               modeled_hhi,
               short_reasoning
        FROM model_portfolio
        WHERE portfolio_id = %s
    """

    position_query = """
        SELECT modeled_allocation,
               ticker
        FROM model_portfolio_position
        WHERE portfolio_id = %s
    """

    values = (portfolioId,)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            result = cur.fetchone()

            cur.execute(position_query, values)
            result_positions = cur.fetchall()

    return {
        "model_portfolio": {
            "modeled_return": result[0],
            "modeled_portfolio_score": result[1],
            "modeled_sharpe_ratio": result[2],
            "modeled_hhi": result[3],
            "short_reasoning": result[4]
        },
        "positions": [
            {
                "modeled_allocation": position[0],
                "ticker": position[1]
            }
            for position in result_positions
        ]
    }