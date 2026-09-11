from fastapi import FastAPI, UploadFile, File
from app.routers import analyze
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.services.yahoo import get_company_data
from app.models.position import Position
from app.routers import analyze
from app.agents.graph import app_graph
import os
import uuid
from dotenv import load_dotenv
from app.services.database_connector import get_connection
from pathlib import Path
from psycopg2.extras import Json
from fastapi.encoders import jsonable_encoder
from app.models.portfolioRequest import PortfolioRequest
from copy import deepcopy
from app.agents.reanalyze_graph import app_graph_analysis
from app.agents.extraction_agent import extract_graph
from psycopg2.extras import RealDictCursor
from app.tools.expand_position import expand_tickers
BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / ".env"

load_dotenv(BASE_DIR / ".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)




@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
        <body>
            <h1>StockAgent</h1>
        </body>
    </html>
    """

@app.get("/get_ticker_details/{ticker}")
def ticker_details(ticker: str):

    ticker = ticker.upper()
    if(ticker == "CASH"):
        return {
                "ticker": ticker.upper(),
                "price":"N/A"
            }

    else:
        info = get_company_data(ticker)
        price = (
                info.get("currentPrice")
                or info.get("regularMarketPrice")
                or info.get("previousClose")
            )
        return {
            "ticker": ticker.upper(),
            "price": price
         }


@app.get("/endpoint_test/new_data_stream/{portfolioId}")
def new_data_stream(portfolioId:str):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            portfolio_data_query = """
                SELECT portfolio_value, portfolio_beta, volatility, expected_return,sharpe_ratio,username, interpretation_level,hhi,
                portfolio_score, portfolio_return FROM portfolio WHERE id=%s
            """
            holdings_data_query = """
                SELECT * FROM portfolio_holding WHERE portfolio_id=%s
                """
            matrix_data_query = """ 
                SELECT * FROM matrix WHERE portfolio_id=%s
            """
            model_portfolio_query = """
                SELECT * FROM model_portfolio WHERE portfolio_id=%s
            """
            model_portfolio_positions_query = """
                SELECT * FROM model_portfolio_position WHERE portfolio_id=%s
            """
            get_fin_response = """SELECT * FROM fin_first_response WHERE portfolio_id=%s"""

            cur.execute(portfolio_data_query, (portfolioId,))
            result = cur.fetchone()

            cur.execute(get_fin_response,(portfolioId,))
            row = cur.fetchone()
            result["fin_first_response"] = row["fin_response"]

            cur.execute(holdings_data_query, (portfolioId,))
            holdings = cur.fetchall()

            positions = []

            for holding in holdings:
                position = {
                    "ticker": holding["ticker"],
                    "allocation": holding["allocation"],
                    "shares": holding["shares"],
                    "costBasis": holding["cost_basis"],
                    "currentBasis": holding["current_basis"]
                }

                positions.append(position)

            expanded_positions = expand_tickers(positions)    
            result["portfolioExpanded"] = expanded_positions
            cur.execute(model_portfolio_query, (portfolioId,))
            result["model_portfolio"] = cur.fetchone()

            cur.execute(model_portfolio_positions_query, (portfolioId,))
            result["model_portfolio"]["positions"] = cur.fetchall()

            cur.execute(matrix_data_query, (portfolioId,))
            matricies = cur.fetchall()
            correlation = {}
            covariance = {}

            for row in matricies:

                matrix = (
                    correlation
                    if row["type"] == "correlation"
                    else covariance
                )

                ticker_a = row["ticker_a"]
                ticker_b = row["ticker_b"]

                if ticker_a not in matrix:
                    matrix[ticker_a] = {}

                matrix[ticker_a][ticker_b] = row["value"]

            result["correlation"] = correlation
            result["covariance"] = covariance
        return dict(result)

@app.post("/portfolio/upload")
async def upload_file(file: UploadFile = File(...)): 
    print(file.filename)
    contents = await file.read()

    csv_text = contents.decode("utf-8-sig")

    print(csv_text)

    result = extract_graph.invoke({
        "rawCSV":csv_text
    })

    print(result["portfolio"])

    return result["portfolio"]
    
@app.get("/getportfolio/{portfolio_id}")
def get_portfolio(portfolio_id:str):
    print(portfolio_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT json_blob_temp FROM portfolio WHERE id=%s
                        
                        
                        """, (portfolio_id,))
            row = cur.fetchone()
            result = row[0]
    return result
@app.post("/portfolio/analyze")
def analyze_portfolio(portfoliorequest:PortfolioRequest):
    print(portfoliorequest)
    random_id = uuid.uuid4()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO portfolio (id)
                VALUES (%s)
                """,
                (random_id,),
            )
    conn.commit()
    print(portfoliorequest.portfolio)
    totalPortfolioValue = 0.0
    for stock in portfoliorequest.portfolio:
        print(stock.ticker)
        print(stock.shares)
        print(stock.costBasis)
        totalPortfolioValue += stock.currentBasis * stock.shares




    result = app_graph.invoke({
        "portfolio": portfoliorequest.portfolio,
        "portfolioValue":totalPortfolioValue,
        "portfolioId":random_id,
        "username":portfoliorequest.username,
        "interpretation_level":portfoliorequest.level
    })
    model_state = deepcopy(result)

    model_state["portfolioExpanded"] = deepcopy(
        result["model_portfolio"].positions
    )
    model_result = app_graph_analysis.invoke(model_state)


    result["model_portfolio"].expected_return = model_result["portfolioReturn"]
    result["model_portfolio"].volatility = model_result["portfolioVolatility"]
    result["model_portfolio"].sharpe_ratio = model_result["sharpeRatio"]
    result["model_portfolio"].portfolio_score = model_result["portfolio_score"]
    result["model_portfolio"].hhi = model_result["hhi"]

    print(model_result)
    #print(result)



    for key, value in result.items():
        try:
            jsonable_encoder(value)
            print(f"{key}: OK")
        except Exception as e:
            print(f"{key}: FAILED")
            print(type(value))
            raise

    json_result = jsonable_encoder(result)

    with get_connection() as conn:
         with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE portfolio
                SET json_blob_temp = %s, username=%s, interpretation_level=%s
                WHERE id = %s
                """,
                (
                    Json(json_result),
                    str(portfoliorequest.username),
                    str(portfoliorequest.level),
                    str(random_id),
                ),
            )
    conn.commit()

    return result