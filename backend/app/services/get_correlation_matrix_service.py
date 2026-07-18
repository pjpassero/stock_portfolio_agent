import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "temp" / "returnsMatrices"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def calculate_correlation_matrix(filename:str):
    save_path = DATA_DIR / "returns.csv"
    df = pd.read_csv(save_path, index_col="Date")
    #print("Covariance:")
    #print(df.cov())
    return df.corr()