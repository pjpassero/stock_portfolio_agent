from backend.app.services.openai_chat_service import ask_fin


test_portfolio = {
    "username": "PJ",
    "portfolioValue": 185000.00,

    "portfolioExpanded": [
        {
            "ticker": "MU",
            "company_name": "Micron Technology, Inc.",
            "shares": 60,
            "sector": "Technology",
            "allocation": 0.30,
            "current_price": 925.00,
            "assetClass": "EQUITY"
        },
        {
            "ticker": "CVX",
            "company_name": "Chevron Corporation",
            "shares": 100,
            "sector": "Energy",
            "allocation": 0.11,
            "current_price": 203.50,
            "assetClass": "EQUITY"
        },
        {
            "ticker": "VOO",
            "company_name": "Vanguard S&P 500 ETF",
            "shares": 100,
            "sector": None,
            "allocation": 0.38,
            "current_price": 710.00,
            "assetClass": "ETF"
        },
        {
            "ticker": "VXUS",
            "company_name": "Vanguard Total International Stock ETF",
            "shares": 100,
            "sector": None,
            "allocation": 0.05,
            "current_price": 87.00,
            "assetClass": "ETF"
        },
        {
            "ticker": "CASH",
            "company_name": "Cash",
            "shares": 1,
            "sector": None,
            "allocation": 0.16,
            "current_price": 29600.00,
            "assetClass": "CASH"
        }
    ],

    "assetClassBreakdown": {
        "EQUITY": 0.41,
        "ETF": 0.43,
        "CASH": 0.16
    }
}


test_metrics = {
    "portfolioReturn": 0.124,
    "portfolioVariance": 0.0529,
    "portfolioVolatility": 0.23,
    "sharpeRatio": 0.91,
    "portfolioBeta": 1.08,

    "stockWeight": 0.41,
    "etfWeight": 0.43,
    "cryptoWeight": 0.0,
    "cashWeight": 0.16,

    "stockInternalWeights": {
        "MU": 0.7317,
        "CVX": 0.2683
    },

    "stockSectorWeights": {
        "Technology": 0.7317,
        "Energy": 0.2683
    },

    "stockHHI": 0.6073,
    "stockVolatility": 0.41,
    "stockRisk": 0.57,

    "etfInternalWeights": {
        "VOO": 0.8837,
        "VXUS": 0.1163
    },

    "etfHHI": 0.7945,
    "etfVolatility": 0.17,
    "etfRisk": 0.25,

    "etfSectorWeights": {
        "Technology": 0.27,
        "Financial Services": 0.15,
        "Industrials": 0.13,
        "Healthcare": 0.11,
        "Consumer Cyclical": 0.10,
        "Communication Services": 0.08,
        "Consumer Defensive": 0.06,
        "Energy": 0.04,
        "Basic Materials": 0.03,
        "Utilities": 0.02,
        "Real Estate": 0.01
    },

    "etfSectorHHI": 0.134
}


test_history = [
    {
        "role": "user",
        "content": "How risky is my portfolio?"
    },
    {
        "role": "assistant",
        "content": (
            "Your portfolio has a mixture of individual stocks, "
            "ETFs, and cash. The risk is not distributed evenly "
            "between those groups."
        )
    },
    {
        "role": "user",
        "content": "Which part should I be paying the most attention to?"
    },
    {
        "role": "assistant",
        "content": (
            "Your individual stock allocation deserves closer attention "
            "because its calculated risk is higher than your ETF allocation."
        )
    }
]


test_question = (
    "Why is my stock portfolio considered riskier than my ETFs?"
)


response = ask_fin(
    portfolio=test_portfolio,
    level="beginner",
    metrics=test_metrics,
    history=test_history,
    question=test_question
)


print("\n--- FIN RESPONSE ---\n")
print(response)