import yfinance as yf

symbol = yf.Ticker("TEST")

print(symbol.info)