from pydantic import BaseModel
class Position(BaseModel):
    ticker: str
    shares: float
    costBasis: float
    currentBasis: float