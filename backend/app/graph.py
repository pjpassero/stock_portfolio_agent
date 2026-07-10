from langgraph.graph import StateGraph, START, END
from app.state import State

from app.nodes.get_portfolio_response import get_portfolio_response
from app.nodes.expand_portfolio import expand_position_details
from app.nodes.query_historical_data import query_historical_data
graph = StateGraph(State)




#graph.add_node("get_stock_data", get_stock_data)
graph.add_node("get_portfolio_response", get_portfolio_response)
graph.add_node("expand_details", expand_position_details)
graph.add_node("get_historical_data",query_historical_data)

#graph.add_edge(START, "get_stock_data")
#graph.add_edge(START, "get_portfolio_response")
#graph.add_edge("get_portfolio_response", END)

graph.add_edge(START, "expand_details")
graph.add_edge("expand_details", "get_historical_data")
graph.add_edge("get_historical_data", END)

app_graph = graph.compile()