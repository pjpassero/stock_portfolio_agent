from app.services.database_connector import get_connection
from langchain_core.tools import tool
from app.services.database_connector import get_connection


@tool
def change_position_size(ticker:str, amount:float):


    return "Hello World!"