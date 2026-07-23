import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "temp" / "returnsMatrices"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def calculate_covariance_matrix(filename:str):
    save_path = DATA_DIR / "returns.csv"
    #print("Covariance:")
    #print(df.cov())
    return df.cov()