from app.services.openai_service import ask_fin

test_portfolio = {
    "username": "Philip",
    "experienceLevel": "intermediate",
    "portfolioValue": 125000.00,
    "holdings": [
        {
            "ticker": "AAPL",
            "assetClass": "EQUITY",
            "shares": 100,
            "currentValue": 30000.00,
            "allocation": 0.24,
            "sector": "Technology"
        },
        {
            "ticker": "MU",
            "assetClass": "EQUITY",
            "shares": 50,
            "currentValue": 25000.00,
            "allocation": 0.20,
            "sector": "Technology"
        },
        {
            "ticker": "VOO",
            "assetClass": "ETF",
            "shares": 75,
            "currentValue": 50000.00,
            "allocation": 0.40
        },
        {
            "ticker": "VXUS",
            "assetClass": "ETF",
            "shares": 100,
            "currentValue": 10000.00,
            "allocation": 0.08
        },
        {
            "ticker": "CASH",
            "assetClass": "CASH",
            "shares": 1,
            "currentValue": 10000.00,
            "allocation": 0.08
        }
    ]
}


test_metrics = {
    "expectedReturn": 0.112,
    "portfolioVolatility": 0.218,
    "sharpeRatio": 0.82,

    "stockWeight": 0.44,
    "etfWeight": 0.48,
    "cashWeight": 0.08,

    "stockRisk": 0.61,
    "stockHHI": 0.504,

    "stockSectorWeights": {
        "Technology": 1.0
    },

    "etfRisk": 0.29,
    "etfVolatility": 0.164,
    "etfHoldingsHHI": 0.035,
    "etfSectorHHI": 0.14
}


test_history = [
    {
        "role": "user",
        "content": "Is my portfolio diversified?"
    },
    {
        "role": "assistant",
        "content": (
            "Your portfolio has exposure to individual stocks, "
            "ETFs, and cash."
        )
    }
]


test_question = (
    "What is the biggest risk in my portfolio and what is causing it?"
)


response = ask_fin(
    portfolio=test_portfolio,
    level=test_portfolio["experienceLevel"],
    metrics=test_metrics,
    history=test_history,
    question=test_question
)


print("\n--- FIN RESPONSE ---\n")
print(response)