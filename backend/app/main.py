from fastapi import FastAPI
from app.routers import analyze
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analyze


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