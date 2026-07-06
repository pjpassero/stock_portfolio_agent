from typing import TypedDict
from app.models.position import Position

class State(TypedDict):
    portfolio:list[Position]
    response:str

