from langgraph.graph import StateGraph, START, END

from app.states.state import State

from app.nodes.calculate_portfolio_statistics import build_statistics
from app.nodes.sort_assets import classify_assets
from app.nodes.add_position import add_position
from app.nodes.route_model import route_model
from app.nodes.update_changes import update_database

from app.nodes.build_returns_matrix import build_returns_matrix
from app.nodes.build_covariance_matrix import build_covariance_matrix
from app.nodes.build_correlation_matrix import build_correlation_matrix
from app.nodes.scoring_model import start_scoring


graph = StateGraph(State)

graph.add_node("add_position", add_position)

graph.add_node("classify_assets", classify_assets)

graph.add_node("build_returns_matrix", build_returns_matrix)

graph.add_node("build_covariance_matrix", build_covariance_matrix)

graph.add_node("build_correlation_matrix", build_correlation_matrix)

graph.add_node("calculate_statistics", build_statistics)

graph.add_node("start_scoring", start_scoring)

graph.add_node("add_to_database", update_database)


graph.add_conditional_edges(
    START,
    route_model,
    {
        "add_position": "add_position",
        "calculate_statistics": "classify_assets"
    }
)

graph.add_edge("add_position", "classify_assets")

graph.add_edge("classify_assets", "build_returns_matrix")

graph.add_edge("build_returns_matrix", "build_covariance_matrix")

graph.add_edge("build_covariance_matrix", "build_correlation_matrix")

graph.add_edge("build_correlation_matrix", "calculate_statistics")

graph.add_edge("calculate_statistics", "start_scoring")

graph.add_edge("start_scoring", "add_to_database")

graph.add_edge("add_to_database", END)


app_graph_analysis = graph.compile()