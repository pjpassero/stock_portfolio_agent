from typing import TypedDict
from app.models.position import Position
from app.models.positionExpanded import PositionExpanded
import pandas as pd 
import numpy as np

class State(TypedDict):
    portfolio:list[Position]
    username:str
    interpretation_level:str
    portfolioValue:int
    portfolioId:str
    portfolioExpanded:list[PositionExpanded]
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
    assetClassBreakdown:dict[str,float]
    stockHHI:float
    stockPositions:list
    etfPositions: list[PositionExpanded]
    crypto_positions:list
    stockWeight:float
    etfWeight:float
    cryptoWeight:float
    cashWeight:float
    stockInternalWeights: dict[str, float]
    stockSectorWeights:dict[str,float]
    stockRisk:float
    stockVolatility:float
    etfInternalWeights: dict[str, float]
    etfHHI: float
    etfVolatility: float
    etfRisk: float
    etfSectorWeights: dict[str, float]
    etfSectorHHI: float
    overall_score:float
    fin_first_response:str

