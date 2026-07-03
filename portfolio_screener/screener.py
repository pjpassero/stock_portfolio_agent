import pandas as pd
import numpy as np
import yfinance as yf

portfolio_stock_sectors = {}

def match_sector(ticker):
    if not ticker:
        return False
    try:
        data = yf.Ticker(ticker)
        info = data.info or {}

        sector = info.get("sector", "")
        print("Sector:", sector)
        portfolio_stock_sectors[ticker] = sector
    except Exception as e:
        print("Sector lookup failed:", e)
        return False


def load_and_compute_returns(filename, ticker):

    match_sector(ticker)

    df = pd.read_csv(filename)

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    df["Close/Last"] = df["Close/Last"].replace('[\$,]', '', regex=True).astype(float)

    df[ticker] = df["Close/Last"].pct_change()

    return df[["Date", ticker]]


dnut = load_and_compute_returns("StockData/DNUT.csv", "DNUT")
nvda = load_and_compute_returns("StockData/NVDA.csv", "NVDA")
riot  = load_and_compute_returns("StockData/RIOT.csv",  "RIOT")
hnst  = load_and_compute_returns("StockData/HNST.csv",  "HNST")
ko  = load_and_compute_returns("StockData/KO.csv",  "KO")
mara  = load_and_compute_returns("StockData/MARA.csv",  "MARA") 
mu = load_and_compute_returns("StockData/MU.csv",  "MU")
rzlv = load_and_compute_returns("StockData/RZLV.csv",  "RZLV")
cvx = load_and_compute_returns("StockData/CVX.csv",  "CVX")
wm = load_and_compute_returns("StockData/WM.csv",  "WM")
xom = load_and_compute_returns("StockData/XOM.csv",  "XOM")
unh = load_and_compute_returns("StockData/UNH.csv",  "UNH")
voo = load_and_compute_returns("StockData/VOO.csv", "VOO")
vti = load_and_compute_returns("StockData/VTI.csv", "VTI")
vxus = load_and_compute_returns("StockData/VXUS.csv", "VXUS")

df = dnut.merge(nvda, on="Date")
df = df.merge(riot, on="Date")
df = df.merge(hnst, on="Date")
df = df.merge(ko, on="Date")
df = df.merge(mara, on="Date")
df = df.merge(mu, on="Date")
df = df.merge(rzlv, on="Date")
df = df.merge(voo, on="Date")
df = df.merge(vti, on="Date")
df = df.merge(cvx, on="Date")
df = df.merge(wm, on="Date")
df= df.merge(xom, on="Date")
df = df.merge(unh, on="Date")
df = df.merge(vxus, on="Date")

df = df.dropna()

rf_daily = 0.04 / 252
df["CASH"] = rf_daily

df.to_csv("returns_model_two.csv", index=False)

print(df.head())


df = pd.read_csv('returns.csv', index_col='Date')
cov_matrix = df.cov()
print(cov_matrix)


for sector in portfolio_stock_sectors:
    print(portfolio_stock_sectors[sector])
