import os
from dotenv import load_dotenv
from massive import RESTClient

load_dotenv()

client = RESTClient(os.getenv("MASSIVE_API_KEY"))

snapshot = client.get_snapshot_ticker(
    market_type="stocks",
    ticker="MU"
)

print(snapshot)