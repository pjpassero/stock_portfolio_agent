from typing import TypedDict
from app.models.position import Position
from app.models.positionExpanded import PositionExpanded


class State(TypedDict):
    portfolio:list[Position]
    portfolioExpanded:list[PositionExpanded]
    response:str
    sectors:list[str]
    matrixIdentifier:str
    returnsAddress:str


