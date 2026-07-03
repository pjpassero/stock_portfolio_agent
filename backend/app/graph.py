from langgraph.graph import StateGraph, START, END
from app.state import State

from app.nodes.get_ticker import get_ticker
from app.nodes.get_stock_data import get_stock_data
from app.nodes.summarize import summarize_company

graph = StateGraph(State)

graph.add_node("get_ticker", get_ticker)
graph.add_node("get_stock_data", get_stock_data)
graph.add_node("get_response", summarize_company)

graph.add_edge(START, "get_ticker")
graph.add_edge("get_ticker", "get_stock_data")
graph.add_edge("get_stock_data", "get_response")
graph.add_edge("get_response", END)

app_graph = graph.compile()