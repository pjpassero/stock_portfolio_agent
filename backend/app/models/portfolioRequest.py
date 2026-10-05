from pydantic import BaseModel
from app.models.position import Position
from uuid import UUID

class PortfolioRequest(BaseModel):
    portfolio: list[Position]
    username: str
    level: str
    user_uuid: UUID