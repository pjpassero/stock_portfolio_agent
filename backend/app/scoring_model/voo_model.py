import numpy as np
import pandas as pd

import yfinance as yf

N = 500 #Rough companies in VOO

voo = yf.Ticker("VOO")

top_holdings = voo.funds_data.top_holdings

top_holdings_weight = top_holdings["Holding Percent"].sum()
remaining_weight = 1 - top_holdings_weight
top_holdings_weight = top_holdings["Holding Percent"].sum()

top_holdings_hhi = sum(
    weight ** 2
    for weight in top_holdings["Holding Percent"]
)


remaining_holdings = N - 10
remaining_holdings_hhi = (
    remaining_weight ** 2 / remaining_holdings
)
etf_hhi = top_holdings_hhi + remaining_holdings_hhi

effective_companies = 1 / etf_hhi

print("Top holdings weight:", top_holdings_weight)
print("Remaining weight:", 1 - top_holdings_weight)
print("Top 10 HHI:", top_holdings_hhi)
print("Remaining HHI:", remaining_holdings_hhi)
print("Estimated VOO HHI:", etf_hhi)
print("Effective companies:", effective_companies)