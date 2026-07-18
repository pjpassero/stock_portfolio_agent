from langgraph.graph import StateGraph, START, END
from app.state import State

from app.nodes.get_portfolio_response import get_portfolio_response
from app.nodes.expand_portfolio import expand_position_details
from app.nodes.query_historical_data import query_historical_data
from app.nodes.build_returns_matrix import build_returns_matrix
from app.nodes.build_covariance_matrix import build_covariance_matrix
from app.nodes.build_correlation_matrix import build_correlation_matrix
graph = StateGraph(State)




#graph.add_node("get_stock_data", get_stock_data)
graph.add_node("get_portfolio_response", get_portfolio_response)
graph.add_node("expand_details", expand_position_details)
graph.add_node("get_historical_data",query_historical_data)
graph.add_node("build_returns_matrix", build_returns_matrix)
graph.add_node("build_covariance_matrix", build_covariance_matrix)
graph.add_node("build_correlation_matrix", build_correlation_matrix)

#graph.add_edge(START, "get_stock_data")
#graph.add_edge(START, "get_portfolio_response")
#graph.add_edge("get_portfolio_response", END)

graph.add_edge(START, "expand_details")
graph.add_edge("expand_details", "get_historical_data")
graph.add_edge("get_historical_data", "build_returns_matrix")
graph.add_edge("build_returns_matrix", "build_covariance_matrix")
graph.add_edge("build_covariance_matrix", "build_correlation_matrix")
graph.add_edge("build_correlation_matrix", END)

app_graph = graph.compile()