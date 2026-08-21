from app.state import State

def classify_assets(state: State):
    stocks = []
    etfs = []
    crypto = []
    cash_weight = 0.0

    for position in state["portfolioExpanded"]:
        asset_class = position.assetClass

        if asset_class == "EQUITY":
            stocks.append(position)

        elif asset_class == "ETF":
            etfs.append(position)

        elif asset_class == "CRYPTOCURRENCY":
            crypto.append(position)

        elif asset_class == "CASH":
            cash_weight = position.allocation


    stock_weight = sum(position.allocation for position in stocks)
    etf_weight = sum(position.allocation for position in etfs)
    crypto_weight = sum(position.allocation for position in crypto)
    
    return {
        "stockPositions": stocks,
        "etfPositions": etfs,
        "cryptoPositions": crypto,
        "stockWeight": stock_weight,
        "etfWeight": etf_weight,
        "cryptoWeight": crypto_weight,
        "cashWeight":cash_weight
    }