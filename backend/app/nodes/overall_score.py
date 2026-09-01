from app.state import State

THETA = 0.20


def calculate_portfolio_risk(state: State):

    base_risk = (
        state["stockWeight"] * state["stockRisk"]
        + state["etfWeight"] * state["etfRisk"]
    )

    correlation_matrix = state["correlationMatrix"]
    weights = state["weights"]

    weighted_correlation = 0.0
    weight_sum = 0.0

    for i in range(len(weights)):
        for j in range(i + 1, len(weights)):

            weight_pair = weights[i] * weights[j]

            weighted_correlation += (
                weight_pair * correlation_matrix.iloc[i, j]
            )

            weight_sum += weight_pair

    if weight_sum > 0:
        average_correlation = weighted_correlation / weight_sum
    else:
        average_correlation = 0.0

    correlation_risk = (average_correlation + 1) / 2

    portfolio_risk = (
        (1 - THETA) * base_risk
        + THETA * correlation_risk
    )

    portfolioScore = (1 - portfolio_risk) * 100
    return {
        "baseRisk": float(base_risk),
        "averageCorrelation": float(average_correlation),
        "correlationRisk": float(correlation_risk),
        "portfolioRisk": float(portfolio_risk),
        "portfolio_score": float(portfolioScore)
    }