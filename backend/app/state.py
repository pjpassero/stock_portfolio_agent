from typing import TypedDict

class State(TypedDict):
    ticker: str
    company_name: str
    sector: str
    industry: str
    current_price: float
    market_cap: int
    trailing_pe: float
    forward_pe: float
    beta: float
    dividend_yield: float
    profit_margin: float
    revenue_growth: float
    earnings_growth: float
    debt_to_equity: float
    return_on_equity: float
    fifty_two_week_change: float

    summary:str

