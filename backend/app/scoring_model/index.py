import pandas as pd
import numpy as np
import math
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data/returns"


aapl = pd.read_csv(DATA_DIR / "AAPL.csv", parse_dates=["Date"], index_col="Date")
mu = pd.read_csv(DATA_DIR/ "mu.csv", parse_dates=["Date"], index_col="Date")
xom = pd.read_csv(DATA_DIR/ "xom.csv", parse_dates=["Date"], index_col="Date")

weigths = np.array([0.50, 0.30, 0.20])

returns = pd.concat(
    [aapl["AAPL"], mu["MU"], xom["XOM"]],
    axis = 1,
    join = "inner"

)

portfolio_varaince = weigths.T @ returns.cov() @ weigths
marginal_contributions = returns.cov().values @ weigths
component_contribution = weigths * marginal_contributions
portfolio_daily_returns = returns @ weigths

portfolio_value = 10000 * (1+portfolio_daily_returns).cumprod()
running_peak = portfolio_value.cummax()
drawdown = (portfolio_value - running_peak) / running_peak
max_drawdown = drawdown.min()
bottom_date = drawdown.idxmin()
peak_date = portfolio_value.loc[:bottom_date].idxmax()
peak_value = portfolio_value.loc[peak_date]
after_bottom = portfolio_value.loc[bottom_date:]
recovered = after_bottom[after_bottom >= peak_value]


#Sortino Ratio
negative_returns = portfolio_daily_returns[portfolio_daily_returns < 0]

c_mu = component_contribution[1]
rc_mu = c_mu / portfolio_varaince

print(marginal_contributions)
print(component_contribution)

print(rc_mu)

print(portfolio_value.head())
print(running_peak.head())
print(drawdown.head())
print(max_drawdown)
print(bottom_date)
print(peak_date)


if not recovered.empty:
    recovery_date = recovered.index[0]
    print(recovery_date)
else:
    print("Still hasn't recovered")


#Sortino Test

downside_returns = np.minimum(portfolio_daily_returns, 0)
downside_deviation = np.sqrt(np.mean(downside_returns ** 2))
annualized_downside = downside_deviation * np.sqrt(252)
portfolio_return = portfolio_daily_returns.mean() * 252
sortino_ratio = (portfolio_return - 0.04) / annualized_downside


print("\nSortino\n")

print(downside_returns.head())
print(downside_deviation)
print(annualized_downside)
print(sortino_ratio)


