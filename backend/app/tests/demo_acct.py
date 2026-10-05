from copy import deepcopy
from uuid import UUID

from app.agents.graph import app_graph
from app.agents.reanalyze_graph import app_graph_analysis
from app.models.portfolioRequest import PortfolioRequest


portfolio_test = PortfolioRequest(
    portfolio=[
        {
            "ticker": "AAPL",
            "shares": 20,
            "costBasis": 180.00,
            "currentBasis": 255.00,
            "allocation": 0.172589
        },
        {
            "ticker": "NVDA",
            "shares": 25,
            "costBasis": 140.00,
            "currentBasis": 180.00,
            "allocation": 0.152284
        },
        {
            "ticker": "JPM",
            "shares": 15,
            "costBasis": 210.00,
            "currentBasis": 300.00,
            "allocation": 0.152284
        },
        {
            "ticker": "XOM",
            "shares": 30,
            "costBasis": 105.00,
            "currentBasis": 115.00,
            "allocation": 0.116751
        },
        {
            "ticker": "VOO",
            "shares": 20,
            "costBasis": 500.00,
            "currentBasis": 600.00,
            "allocation": 0.406092
        }
    ],
    username="Test User",
    level="intermediate",
    user_uuid=UUID("00000000-0000-0000-0000-000000000000")
)

result = app_graph.invoke(
    {
        "portfolio": portfolio_test.portfolio,
        "portfolioValue": 100000,

        # This remains "demo".
        "portfolioId": "demo",

        "username": portfolio_test.username,
        "interpretation_level": portfolio_test.level,
    }
)


model_state = deepcopy(result)

model_state["portfolioExpanded"] = deepcopy(
    result["model_portfolio"].positions
)


model_result = app_graph_analysis.invoke(model_state)


result["model_portfolio"].expected_return = model_result["portfolioReturn"]
result["model_portfolio"].volatility = model_result["portfolioVolatility"]
result["model_portfolio"].sharpe_ratio = model_result["sharpeRatio"]
result["model_portfolio"].portfolio_score = model_result["portfolio_score"]
result["model_portfolio"].hhi = model_result["hhi"]


print(result)