from pydantic import BaseModel
class Position(BaseModel):
    ticker: str
    shares: int
    costBasis: float
    currentBasis: float