from typing import TypedDict
from app.models.position import Position
from app.models.positionExpanded import PositionExpanded
import pandas as pd 
import numpy as np

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
    weights: np.ndarray
    sectorWeights: dict[str, float]
    hhi: float
    meanReturns: np.ndarray
    portfolioReturn: float
    portfolioBeta:float
    portfolioVariance: float
    portfolioVolatility: float
    sharpeRatio: float
    portfolioBeta: float
    assetClasses:dict[str,float]
    sector_risk_score:float
    sector_hhi:float
    overall_stock_score:float


