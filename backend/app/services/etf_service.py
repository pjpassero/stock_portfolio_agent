import yfinance as yf


def get_etf_holdings(ticker:str) :
    etf = yf.Ticker(ticker)
    funds = etf.funds_data
    return funds.top_holdings

def get_holding_sector(ticker: str):
    info = yf.Ticker(ticker).info
    return info.get("sector")

def calculate_underlying_hhi(ticker: str):
    holdings = get_etf_holdings(ticker)

    weights = holdings["Holding Percent"]

    hhi = sum(
        weight ** 2
        for weight in weights
    )

    return float(hhi)

