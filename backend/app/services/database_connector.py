import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import Json

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE__HOST", "localhost"),
        database=os.getenv("DATABASE__NAME", "none"),
        user=os.getenv("DATABASE__USER"),
        password=os.getenv("DATABASE__PASSWORD"),
        port=os.getenv("DATABASE__PORT", 5432)
    )