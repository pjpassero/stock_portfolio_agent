from app.models.positionExpanded import PositionExpanded
from pydantic import BaseModel

class ModelPortfolio(BaseModel):
    positions: list[PositionExpanded]
    portfolio_value: float
    expected_return: float | None = None
    volatility: float | None = None
    variance:float | None = None
    sharpe_ratio: float | None = None
    sortino_ratio: float | None = None
    hhi:float | None = None
    beta:float | None = None
    portfolio_score: float | None = None

