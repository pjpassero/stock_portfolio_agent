from langgraph.graph import StateGraph, START, END
from app.states.extraction_state import ExtractionState

def extract_viable_content(extraction_state:ExtractionState):
    raw_csv = extraction_state["rawCSV"]


