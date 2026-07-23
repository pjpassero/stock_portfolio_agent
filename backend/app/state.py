from typing import TypedDict
from app.models.position import Position
from app.models.positionExpanded import PositionExpanded
import pandas as pd 

class State(TypedDict):
    portfolio:list[Position]
    portfolioValue:int
    portfolioId:str
    portfolioExpanded:list[PositionExpanded]
    response:str
    sectors:list[str]
    matrixIdentifier:str
    returnMatrix:pd.DataFrame
    covarianceMatrix:pd.DataFrame
    correlationMatrix:pd.DataFrame
    success:bool

    


