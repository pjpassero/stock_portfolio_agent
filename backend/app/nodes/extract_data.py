from app.states.extraction_state import ExtractionState
from app.services.csv_extraction import extract_csv_with_llm
import json

def extract_csv(extraction_state:ExtractionState):
    data = extract_csv_with_llm(extraction_state["rawCSV"])


    return {
        "portfolio":data
    }