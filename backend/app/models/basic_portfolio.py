from pydantic import BaseModel
from app.models.position import Position


class BasicPortfolio(BaseModel):
    positions:list[Position]