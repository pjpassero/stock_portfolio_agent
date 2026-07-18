from app.state import State
from app.services.get_correlation_matrix_service import calculate_correlation_matrix

def build_correlation_matrix(state:State):
    return {
        "correlationMatrix": calculate_correlation_matrix("returns")
    }