from pydantic import BaseModel
from app.models.position import Position

class PortfolioRequest(BaseModel):
    portfolio: list[Position]
    username: str
    level: str