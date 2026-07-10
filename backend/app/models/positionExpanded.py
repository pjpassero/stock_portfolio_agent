from typing import Optional
from pydantic import BaseModel


class PositionExpanded(BaseModel):
    ticker: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None

    current_price: Optional[float] = None
    market_cap: Optional[int] = None

    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    beta: Optional[float] = None
    dividend_yield: Optional[float] = None

    profit_margin: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None

    debt_to_equity: Optional[float] = None
    return_on_equity: Optional[float] = None

    fifty_two_week_change: Optional[float] = None

    historicalDataPath: str