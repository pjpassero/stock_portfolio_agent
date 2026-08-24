import numpy as np
import pandas as pd

from app.state import State
from app.nodes.portfolio_summary import summarize_details

test_state: State = {

    "portfolio": [
        {
            "ticker": "MU",
            "shares": 100,
            "costBasis": 150,
            "currentBasis": 911.495
        },
        {
            "ticker": "NVDA",
            "shares": 100,
            "costBasis": 105,
            "currentBasis": 210.5231
        },
        {
            "ticker": "VOO",
            "shares": 100,
            "costBasis": 450,
            "currentBasis": 702.71
        },
        {
            "ticker": "CASH",
            "shares": 1,
            "costBasis": 45000,
            "currentBasis": 45000
        },
        {
            "ticker": "VXUS",
            "shares": 100,
            "costBasis": 45,
            "currentBasis": 87.205
        },
        {
            "ticker": "CVX",
            "shares": 100,
            "costBasis": 95,
            "currentBasis": 202.285
        },
        {
            "ticker": "JPM",
            "shares": 100,
            "costBasis": 150,
            "currentBasis": 356.72
        }
    ],

    "username": "Philip",
    "interpretation_level": "advanced",
    "portfolioValue": 292093.81,
    "portfolioId": "119cf06f-80a3-42b4-b7f0-fd09cde31839",

    "portfolioExpanded": [],

    "response": "",

    "sectors": [
        "Technology",
        "Energy",
        "Financial Services"
    ],

    "matrixIdentifier": "",

    # Matrices omitted from this test case
    "returnMatrix": pd.DataFrame(),
    "covarianceMatrix": pd.DataFrame(),
    "correlationMatrix": pd.DataFrame(),

    "success": True,

    "weights": np.array([
        0.3120555687229387,   # MU
        0.0720737971133315,   # NVDA
        0.24057682016609663,  # VOO
        0.15406009459769107,  # CASH
        0.029855134554203664, # VXUS
        0.06925343607931986,  # CVX
        0.12212514876641857   # JPM
    ]),

    "sectorWeights": {
        "Technology": 0.3841293658362702,
        "null": 0.4244920493179914,
        "Energy": 0.06925343607931986,
        "Financial Services": 0.12212514876641857
    },

    "hhi": 0.20478694877927225,

    "meanReturns": np.array([
        0.002676353885860711,
        0.0023400309622969044,
        0.0005394651539400293,
        0.0004084938098215429,
        0.0008651031450952485,
        0.0008691468879138101,
        0.0
    ]),

    "portfolioReturn": 0.32320528035424234,
    "portfolioBeta": 0.0,
    "portfolioVariance": 0.00025530473290483354,
    "portfolioVolatility": 0.2536469843937003,
    "sharpeRatio": 1.1165332047262304,

    "assetClasses": {},
    "sector_risk_score": 0.0,
    "sector_hhi": 0.0,
    "overall_stock_score": 0.0,

    "assetClassBreakdown": {
        "EQUITY": 0.5755079506820087,
        "ETF": 0.2704319547203003,
        "CRYPTO": 0.0,
        "CASH": 0.15406009459769107
    },

    "stockHHI": 0.369204195569449,

    "stockPositions": [],
    "etfPositions": [],
    "crypto_positions": [],

    "stockWeight": 0.5755079506820087,
    "etfWeight": 0.2704319547203003,
    "cryptoWeight": 0.0,
    "cashWeight": 0.15406009459769107,

    "stockInternalWeights": {
        "MU": 0.5422263382341385,
        "NVDA": 0.12523510236117516,
        "CVX": 0.12033445584418202,
        "JPM": 0.21220410356050431
    },

    "stockSectorWeights": {
        "Technology": 0.6674614405953136,
        "Energy": 0.12033445584418202,
        "Financial Services": 0.21220410356050431
    },

    "stockRisk": 0.261577557967713,
    "stockVolatility": 0.3706885972524933,

    "etfInternalWeights": {
        "VOO": 0.8896020457897369,
        "VXUS": 0.11039795421026313
    },

    # Not present in the supplied output
    "etfHHI": 0.0,

    "etfVolatility": 0.1657538907490256,
    "etfRisk": 0.09366115938173875,

    "etfSectorWeights": {
        "Technology": 0.6090036672572386,
        "Consumer Cyclical": 0.10719885692805767,
        "Communication Services": 0.2004685486024572,
        "Financial Services": 0.07908514754606406,
        "Healthcare": 0.0042437796661822964
    },

    "etfSectorHHI": 0.42883717086646117,
    "overall_score": 0.17586664883346265,
}

print(summarize_details(test_state))