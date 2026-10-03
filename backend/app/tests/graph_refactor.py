from app.agents.graph import app_graph
from app.models.portfolioRequest import PortfolioRequest
import uuid


config = {
    "configurable": {
        "thread_id": "test-thread-2"
    }
}

portfolio_test = PortfolioRequest(
    portfolio=[
        {
            "ticker": "AAPL",
            "shares": 20,
            "costBasis": 180.00,
            "currentBasis": 255.00
        },
        {
            "ticker": "NVDA",
            "shares": 25,
            "costBasis": 140.00,
            "currentBasis": 180.00
        },
        {
            "ticker": "JPM",
            "shares": 15,
            "costBasis": 210.00,
            "currentBasis": 300.00
        },
        {
            "ticker": "XOM",
            "shares": 30,
            "costBasis": 105.00,
            "currentBasis": 115.00
        },
        {
            "ticker": "VOO",
            "shares": 20,
            "costBasis": 500.00,
            "currentBasis": 600.00
        }
    ],
    username="Test User",
    level="intermediate"
)

result = app_graph.invoke(
    {
        "portfolio": portfolio_test.portfolio,
        "portfolioValue": 100000,
        "portfolioId": "test-case#1-id",
        "username": portfolio_test.username,
        "interpretation_level": portfolio_test.level,
    },
    config=config
)

#print(result)

state = app_graph.get_state(config)

print("\nSAVED THREAD STATE:")
print(state.values)