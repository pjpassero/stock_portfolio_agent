from app.states.state import State
from app.services.database_connector import get_connection


def update_all_data(state: State):
    update_fin_database = "INSERT INTO fin_first_response (fin_response, portfolio_id) VALUES (%s, %s)"
    update_query = """
        UPDATE portfolio
        SET
            portfolio_value = %s,
            portfolio_return = %s,
            portfolio_variance = %s,
            sharpe_ratio = %s,
            portfolio_beta = %s,
            hhi = %s,
            portfolio_score = %s,

            cash_weight = %s,
            stock_weight = %s,
            etf_weight = %s,
            crypto_weight = %s,

            sector_risk_score = %s,
            sector_hhi = %s,

            stock_hhi = %s,
            stock_risk_score = %s,
            stock_volatility = %s,

            etf_hhi = %s,
            etf_risk_score = %s,
            etf_sector_hhi = %s,

            base_risk = %s,
            average_corr = %s,
            corr_risk = %s,
            portfolio_risk = %s
        WHERE id = %s
    """

    values = (
        float(state.get("portfolioValue", 0)),
        float(state.get("portfolioReturn", 0)),
        float(state.get("portfolioVariance", 0)),
        float(state.get("sharpeRatio", 0)),
        float(state.get("portfolioBeta", 0)),
        float(state.get("hhi", 0)),
        float(state.get("portfolio_score", 0)),

        float(state.get("cashWeight", 0)),
        float(state.get("stockWeight", 0)),
        float(state.get("etfWeight", 0)),
        float(state.get("cryptoWeight", 0)),

        float(state.get("sector_risk_score", 0)),
        float(state.get("sector_hhi", 0)),

        float(state.get("stockHHI", 0)),
        float(state.get("stockRisk", 0)),
        float(state.get("stockVolatility", 0)),

        float(state.get("etfHHI", 0)),
        float(state.get("etfRisk", 0)),
        float(state.get("etfSectorHHI", 0)),

        float(state.get("baseRisk", 0)),
        float(state.get("averageCorrelation", 0)),
        float(state.get("correlationRisk", 0)),
        float(state.get("portfolioRisk", 0)),

        str(state["portfolioId"])
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(update_query, values)
            cur.execute(update_fin_database, (state["fin_first_response"], state["portfolioId"],))
        conn.commit()

    return {}