import yfinance as yf

def get_company_data(ticker: str):

    stock = yf.Ticker(ticker)

    history = stock.history(period="1d")

    if history.empty:
        return False
    else:  
        return stock.info
