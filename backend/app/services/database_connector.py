import psycopg2
import os
from dotenv import load_dotenv


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE__HOST", "localhost"),
        database=os.getenv("DATABASE__NAME", "edgar"),
        user=os.getenv("DATABASE__USER"),
        password=os.getenv("DATABASE__PASSWORD"),
        port=os.getenv("DATABASE__PORT", 5432)
    )