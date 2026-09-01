from app.models.positionExpanded import PositionExpanded
from pydantic import BaseModel

class ModelPortfolio(BaseModel):
    positions: list[PositionExpanded]
    portfolio_value: float
    expected_return: float | None = None
    volatility: float | None = None
    sharpe_ratio: float | None = None
    overall_score: float | None = None

    def change_position_allocation():
        return "Change Allocation"