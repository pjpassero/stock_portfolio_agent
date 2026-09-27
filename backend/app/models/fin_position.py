from pydantic import BaseModel
class FinPosition(BaseModel):
    ticker: str
    shares: float
    costBasis: float
    currentBasis: float
    allocation:float
    assetClass:str
    MCR:float
    PCR:float
    CCR:float