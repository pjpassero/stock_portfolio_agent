from app.state import State
from app.services.get_correlation_matrix_service import calculate_correlation_matrix
import pandas as pd

def build_correlation_matrix(state:State):
    df = state["returnMatrix"]
    df = df.drop(columns=["Date"])
    return {
        "correlationMatrix": df.corr()
    }