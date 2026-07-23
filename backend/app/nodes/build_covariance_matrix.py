from app.state import State
from app.services.get_covariance_matrix_service import calculate_covariance_matrix
import pandas as pd

def build_covariance_matrix(state:State):
    df = state["returnMatrix"]
    df = df.drop(columns=["Date"])
    return {
        "covarianceMatrix": df.cov()
    }