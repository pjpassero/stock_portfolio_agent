from langgraph.graph import StateGraph, START, END

from app.state import State

from app.nodes.calculate_portfolio_statistics import build_statistics
from app.nodes.sort_assets import classify_assets
from app.nodes.calculate_score_stocks import calculate_score
from app.nodes.calculate_score_etf import calculate_etf_score
from app.nodes.overall_score import calculate_portfolio_risk
from app.nodes.add_position import add_position
from app.nodes.route_model import route_model



graph = StateGraph(State)
graph.add_node("add_position", add_position)
graph.add_node("calculate_statistics", build_statistics)
graph.add_node("classify_assets", classify_assets)
graph.add_node("calculate_score", calculate_score)
graph.add_node("calculate_etf_score", calculate_etf_score)
graph.add_node("calculate_overall_score", calculate_portfolio_risk)

graph.add_conditional_edges(START, route_model, {
    "add_position":"add_position",
    "calculate_statistics":"calculate_statistics"
})

graph.add_edge("add_position", "calculate_statistics")
graph.add_edge("calculate_statistics", "classify_assets")

graph.add_edge("classify_assets", "calculate_score")

graph.add_edge("calculate_score", "calculate_etf_score")

graph.add_edge("calculate_etf_score", "calculate_overall_score")

graph.add_edge("calculate_overall_score", END)


app_graph_analysis = graph.compile()