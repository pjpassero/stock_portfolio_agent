from langgraph.graph import StateGraph, START, END
from app.state import State

from app.nodes.get_portfolio_response import get_portfolio_response
from app.nodes.expand_portfolio import expand_position_details
from app.nodes.query_historical_data import query_historical_data
from app.nodes.build_returns_matrix import build_returns_matrix
from app.nodes.build_covariance_matrix import build_covariance_matrix
from app.nodes.build_correlation_matrix import build_correlation_matrix
from app.nodes.calculate_portfolio_statistics import build_statistics
from app.nodes.calculate_score_stocks import calculate_score
from app.nodes.sort_assets import classify_assets
from app.nodes.calculate_score_etf import calculate_etf_score
from app.nodes.overall_score import calculate_overall_score
from app.nodes.portfolio_summary import summarize_details
graph = StateGraph(State)




#graph.add_node("get_stock_data", get_stock_data)
graph.add_node("get_portfolio_response", get_portfolio_response)
graph.add_node("expand_details", expand_position_details)
graph.add_node("get_historical_data",query_historical_data)
graph.add_node("build_returns_matrix", build_returns_matrix)
graph.add_node("build_covariance_matrix", build_covariance_matrix)
graph.add_node("build_correlation_matrix", build_correlation_matrix)
graph.add_node("calculate_statistics", build_statistics)
graph.add_node("calculate_score",calculate_score)
graph.add_node("classify_assets", classify_assets)
graph.add_node("calculate_etf_score",calculate_etf_score)
graph.add_node("calculate_overall_score", calculate_overall_score)
graph.add_node("get_first_analysis", summarize_details)

#graph.add_edge(START, "get_stock_data")
#graph.add_edge(START, "get_portfolio_response")
#graph.add_edge("get_portfolio_response", END)

graph.add_edge(START, "expand_details")
graph.add_edge("expand_details", "classify_assets")
graph.add_edge("classify_assets", "get_historical_data")
graph.add_edge("get_historical_data", "build_returns_matrix")
graph.add_edge("build_returns_matrix", "build_covariance_matrix")
graph.add_edge("build_covariance_matrix", "build_correlation_matrix")
graph.add_edge("build_correlation_matrix", "calculate_statistics")
graph.add_edge("calculate_statistics", "calculate_score")
graph.add_edge("calculate_score", "calculate_etf_score")
graph.add_edge("calculate_etf_score", "calculate_overall_score")
graph.add_edge("calculate_overall_score", "get_first_analysis")
graph.add_edge("get_first_analysis", END)



app_graph = graph.compile()