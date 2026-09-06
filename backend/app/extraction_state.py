from typing import TypedDict
from app.models.position import Position
from app.models.positionExpanded import PositionExpanded
import pandas as pd 
import numpy as np

class ExtractionState(TypedDict):
    rawCSV:str
    portfolio:dict

