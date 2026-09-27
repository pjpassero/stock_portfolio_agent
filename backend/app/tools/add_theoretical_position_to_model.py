from app.services.database_connector import get_connection
from app.services.yahoo import get_company_data
from langchain_core.tools import tool


@tool
def add_user_ticker(ticker:str, shares:float):
    return "Hello World!"