import yfinance as yf

def get_company_data(ticker: str):

    stock = yf.Ticker(ticker)

    return stock.info