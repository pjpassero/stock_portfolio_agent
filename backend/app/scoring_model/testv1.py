import numpy as np
import pandas as pd

import yfinance as yf

TIME_PERIOD = 5
V_MAX = 0.40 #TBD
HHI_MAX = 1.0
HHI_MIN = 1 / 11

tickers = ['MU', 'NVDA', 'VOO', 'CVX', 'AAPL']
#below will need to be not hardcoded as we go further
sector_map = {
    "MU": "technology",
    "NVDA": "technology",
    "CVX": "energy",
    "AAPL": "technology"
}
sector_exposure = {}
weights = np.array([0.08, 0.32, 0.22, 0.18, 0.20])
portfolio_inital_value = 10000

portfolio = {}

prices = yf.download(tickers, period="5y", progress=False)['Close']
returns = prices.pct_change().dropna()
portfolio = {"returns":returns}

#Step 1
covariance_matrix = portfolio["returns"].cov()
daily_portfolio_varaince = weights.T @ covariance_matrix @ weights
v_raw = np.sqrt(252 * daily_portfolio_varaince)
v = min(v_raw / V_MAX, 1)


#Step 2
for i, ticker in enumerate(tickers):
    if ticker in sector_map:
        sector = sector_map[ticker]
        if sector in sector_exposure:
            sector_exposure[sector] += weights[i]
        else:
            sector_exposure[sector] = weights[i]

voo = yf.Ticker("VOO")
voo_sector_weights = voo.funds_data.sector_weightings
voo_weight = weights[2]

for sector, sector_weight in voo_sector_weights.items():
    exposure = voo_weight * sector_weight
    if sector in sector_exposure:
        sector_exposure[sector] += exposure
    else:
        sector_exposure[sector] = exposure

sector_hhi = 0
for sector, exposure in sector_exposure.items():
    sector_hhi += exposure ** 2

C_sector = (sector_hhi - HHI_MIN) / (1 - HHI_MIN)

#print(portfolio["returns"])
print(covariance_matrix)
print(v_raw)

print(sector_exposure)
print(sum(sector_exposure.values()))
print(sector_hhi)
print(C_sector)