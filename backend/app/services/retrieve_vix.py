import yfinance as yf


def get_vix():
    vix = yf.Ticker("^VIX")
    return vix.fast_info["lastPrice"]
