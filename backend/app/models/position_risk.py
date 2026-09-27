from typing import TypedDict

class PositionRiskContribution(TypedDict):
    ticker:str
    weight:float
    MCR:float
    PCR:float
    CCR:float