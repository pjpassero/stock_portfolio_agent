from app.services.database_connector import get_connection
from langchain_core.tools import tool


@tool
def get_covariance(ticker_a:str, ticker_b:str,portfolio_id:str = ""):
    """
    Get the covariance between two assets in the user's portfolio. 

    Use this when the user asks about covariance or how two assets may move together.
    """
    query = """
        SELECT value FROM matrix where portfolio_id=%s AND type=%s AND ticker_a=%s AND ticker_b=%s
        """

    values = (portfolio_id, "covariance", ticker_a.upper(), ticker_b.upper())

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            result = cur.fetchone()

    if result is None:
        return {
            "error":"Covariance Data not Found!"
        }
    return {
        "ticker_a": ticker_a.upper(),
        "ticker_b": ticker_b.upper(),
        "covariance": float(result[0])
    }