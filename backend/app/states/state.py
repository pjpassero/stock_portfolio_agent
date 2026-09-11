from typing import TypedDict
from app.models.position import Position
from app.models.positionExpanded import PositionExpanded
from app.models.model_portfolio import ModelPortfolio
import pandas as pd 
import numpy as np

class State(TypedDict):
    portfolio:list[Position]
    model_portfolio:ModelPortfolio #need to account for in DB
    username:str #in database - fistname
    interpretation_level:str #in database
    portfolioValue:int #-in database
    portfolioId:str #in database
    portfolioExpanded:list[PositionExpanded] #IMPORTANT - UPDATE portfolio_holding to match data collected
    sectors:list[str] #IMPORTANT - need to account for
    returnMatrix:pd.DataFrame #Need to find a better way to store or dump after we are done
    covarianceMatrix:pd.DataFrame #in database in matrix table
    correlationMatrix:pd.DataFrame #in datab ase in matrix table
    success:bool #NOT USED - DEPRECATE
    weights: np.ndarray #represents each position allocation, can be reconstructed from allocations
    sectorWeights: dict[str, float] #IMPORTANT not ACCOUNT FOR - NULL ALSO 
    hhi: float #in database
    meanReturns: np.ndarray #NOT IN DATABASE
    portfolioReturn: float #NOT ACCOUNT FOR
    portfolioBeta:float #NOT CREATE YET IN CODE, NEED TO ACCOUT FOR
    portfolioVariance: float #NOT STORED
    portfolioVolatility: float #STORED, CHANGE OUT TO VARIANCE
    sharpeRatio: float #stored
    assetClasses:dict[str,float] #stored in portoflio_holding
    sector_risk_score:float #IN DB, NOT UPDATED
    sector_hhi:float #IN DB, NOT UPDATED
    assetClassBreakdown:dict[str,float] #LOOK INTO THIS, MAY NOT BE USED
    stockHHI:float #NOT IN DB DDL
    stockPositions:list #ONLY NEEDED FOR CALCULATIONS - DO NOT STORE THIS
    etfPositions: list[PositionExpanded] #ONLY NEEDED  FOR CALCULATIONS, DO NOT STORE  
    crypto_positions:list #ONLY NEEDED FOR CALCULATIONS, DO NOT STORE
    stockWeight:float #NOT STORED - add to DDL
    etfWeight:float #NOT STORED - add to DDL
    cryptoWeight:float #NOT STORED - add to DDL
    cashWeight:float #NOT STORED - add to DDL
    stockInternalWeights: dict[str, float] 
    stockSectorWeights:dict[str,float]
    stockRisk:float
    stockVolatility:float
    etfInternalWeights: dict[str, float]
    etfHHI: float #stored but not updated
    etfVolatility: float #change to varaince because volatility can be derieved
    etfRisk: float #stroed, not updated
    etfSectorWeights: dict[str, float]
    etfSectorHHI: float
    fin_first_response:str #stored in fin_first_response
    baseRisk: float #add
    averageCorrelation: float #add
    correlationRisk: float #add 
    portfolioRisk: float #add
    portfolio_score:float #add
    need_new_calculations:bool
    new_positions:list



