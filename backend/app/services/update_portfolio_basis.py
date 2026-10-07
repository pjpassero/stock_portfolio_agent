from app.services.database_connector import get_connection
from pydantic import BaseModel
import yfinance as yf

class ModelPosition(BaseModel):
    ticker:str
    totalCostBasis:float
    shares:float


def update_basis(portfolioId: str):
    new_sum = 0

    get_positions = """
        SELECT ticker, current_basis, shares
        FROM portfolio_holding
        WHERE portfolio_id = %s
    """
    gotten_positions = []

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(get_positions, (portfolioId,))
            positions = cur.fetchall()

            for position in positions:
                new_pos = ModelPosition(
                    ticker=position[0],
                    totalCostBasis=position[1],
                    shares=position[2]
                )
                gotten_positions.append(new_pos)


            for gotten in gotten_positions:
                if gotten.ticker == "CASH":
                    new_sum += gotten.totalCostBasis
                    continue
                stock = yf.Ticker(gotten.ticker)
                current_price = stock.fast_info["last_price"]
                new_total_basis = gotten.shares * current_price
                gotten.totalCostBasis = new_total_basis
                new_sum += new_total_basis
                update = """UPDATE portfolio_holding SET current_basis=%s WHERE portfolio_id=%s AND ticker=%s"""
                update_portfolio = """UPDATE portfolio SET portfolio_value=%s WHERE id=%s"""
                cur.execute(update, (new_total_basis, portfolioId, gotten.ticker,))
                cur.execute(update_portfolio, (new_sum,portfolioId,))
            for gotten in gotten_positions:
                allocation = gotten.totalCostBasis / new_sum
                update_value = """UPDATE portfolio_holding SET allocation=%s WHERE portfolio_id=%s AND ticker=%s"""
                cur.execute(update_value, (allocation, portfolioId,gotten.ticker,))

        
                





