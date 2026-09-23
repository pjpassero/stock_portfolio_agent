from app.states.fin_state import FinState
from app.services.database_connector import get_connection
from app.models.fin_position import FinPosition


def collect_user_data(state: FinState):

    quick_snapshot = """
        SELECT
            portfolio_value,
            expected_return,
            volatility,
            sharpe_ratio,
            username,
            interpretation_level,
            hhi,
            cash_weight,
            portfolio_score,
            portfolio_return,
            portfolio_beta,
            sortino_ratio
        FROM portfolio
        WHERE id = %s
    """

    positions_query = """
        SELECT
            ticker,
            cost_basis,
            current_basis,
            shares,
            allocation,
            asset_class
        FROM portfolio_holding
        WHERE portfolio_id = %s
    """

    portfolio_id = str(state["portfolioId"])
    values = (portfolio_id,)

    with get_connection() as conn:
        with conn.cursor() as cur:

            cur.execute(quick_snapshot, values)
            row = cur.fetchone()

            if row is None:
                raise ValueError(
                    f"Portfolio {portfolio_id} was not found."
                )

            cur.execute(positions_query, values)
            result_positions = cur.fetchall()

    metrics = {
        "portfolio_value": row[0],
        "expected_return": row[1],
        "volatility": row[2],
        "sharpe_ratio": row[3],
        "username": row[4],
        "hhi": row[6],
        "cash_weight": row[7],
        "portfolio_score": row[8],
        "portfolio_return": row[9],
        "portfolio_beta": row[10],
        "sortino_ratio": row[11]
    }

    positions = []

    for result_row in result_positions:
        positions.append(
            FinPosition(
                ticker=result_row[0],
                costBasis=result_row[1],
                currentBasis=result_row[2],
                shares=result_row[3],
                allocation=result_row[4],
                assetClass=result_row[5]
            )
        )

    return {
        "metrics": metrics,
        "portfolio": positions,
        "interpretation_level": row[5]

    }