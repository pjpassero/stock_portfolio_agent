from fastapi import APIRouter

from app.graph import app_graph

router = APIRouter()


@router.get("/analyze/{ticker}")
def analyze_company(ticker: str):

    result = app_graph.invoke({
        "ticker": ticker.upper()
    })

    return result