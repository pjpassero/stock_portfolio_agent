from fastapi import FastAPI
from app.routers import analyze
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.services.yahoo import get_company_data
from app.models.position import Position
from app.routers import analyze
from app.graph import app_graph

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
def ticker_details(ticker:str):
    info = get_company_data(ticker)
    return {
        "ticker": ticker.upper(),
        "price": info["currentPrice"]
    }

@app.post("/portfolio/analyze")
def analyze_portfolio(portfolio: list[Position]):

    for stock in portfolio:
        print(stock.ticker)
        print(stock.shares)
        print(stock.costBasis)

    result = app_graph.invoke({
        "portfolio": portfolio
    })
    print(result)
    return result