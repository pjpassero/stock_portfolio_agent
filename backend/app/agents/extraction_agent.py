from app.states.extraction_state import ExtractionState
from langgraph.graph import StateGraph, START, END


from app.nodes.extract_data import extract_csv
from app.nodes.get_current_basis import update_current_basis

graph = StateGraph(ExtractionState)


graph.add_node("extract_csv", extract_csv)
graph.add_node("update_basis", update_current_basis)


graph.add_edge(START, "extract_csv")
graph.add_edge("extract_csv", "update_basis")
graph.add_edge("update_basis", END)


extract_graph = graph.compile()