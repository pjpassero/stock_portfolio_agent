from app.state import State
from app.services.get_covariance_matrix_service import calculate_covariance_matrix

def build_covariance_matrix(state:State):
    return {
        "covarianceMatrix": calculate_covariance_matrix("returns")
    }