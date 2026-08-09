from openai import OpenAI
from psycopg2.extras import Json
import pandas as pd
import numpy as np
from pathlib import Path
from database_connector import get_connection
#client = OpenAI()


sector_etfs = {
    "XLC": "Communication Services",
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLE": "Energy",
    "XLF": "Financials",
    "XLV": "Health Care",
    "XLI": "Industrials",
    "XLB": "Materials",
    "XLRE": "Real Estate",
    "XLK": "Technology",
    "XLU": "Utilities",
}

sector_volatilites = {

}

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sector_data" / "sector_returns.csv"


def get_updated_sector_returns():
    return "Hello World"


def build_new_sector_return_matrix():
    return "Returns"

def sector_covariance():
    df = pd.read_csv(DATA_DIR, index_col="Date")
    covariance = df.cov()

    with get_connection() as conn:
            with conn.cursor() as cur:
                insert_query = """
                        INSERT INTO sector_matrix (matrix_type, sector_a, sector_b, value)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (matrix_type, sector_a, sector_b)
                        DO UPDATE SET value = EXCLUDED.value, created_at = NOW()
                    """
    
                rows = [
                    ("covariance", a, b, float(covariance.loc[a, b]))
                    for a in covariance.index
                    for b in covariance.columns
                ]
    
                cur.executemany(insert_query, rows)
                conn.commit()
    return df.cov()

def sector_correlation():
    df = pd.read_csv(DATA_DIR, index_col="Date")
    correlation = df.corr()
    with get_connection() as conn:
                with conn.cursor() as cur:
                    insert_query = """
                        INSERT INTO sector_matrix (matrix_type, sector_a, sector_b, value)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (matrix_type, sector_a, sector_b)
                        DO UPDATE SET value = EXCLUDED.value, created_at = NOW()
                    """
                    rows = [
                        ("correlation", a, b, float(correlation.loc[a, b]))
                        for a in correlation.index
                        for b in correlation.columns
                    ]
        
                    cur.executemany(insert_query, rows)
                    conn.commit()
    return df.corr()

def sector_volatility():
    #come back to this later
    df = pd.read_csv(DATA_DIR, index_col="Date")
    daily_vol = df.std()
    annualized_vol = daily_vol * np.sqrt(252) 
    print(annualized_vol)

sector_volatility()