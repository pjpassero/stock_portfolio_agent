from typing import TypedDict
from app.models.fin_position import FinPosition
class FinState(TypedDict):
    portfolioId:str
    messages:list
    metrics: dict[str, any]
    portfolio:list[FinPosition]
    interpretation_level:str
    current_question:str
    newest_response:str