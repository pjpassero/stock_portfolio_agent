from langgraph.graph import StateGraph, START, END
from app.state import State

from app.nodes.get_stock_data import get_stock_data
from app.nodes.get_portfolio_response import get_portfolio_response

graph = StateGraph(State)




#graph.add_node("get_stock_data", get_stock_data)
graph.add_node("get_portfolio_response", get_portfolio_response)


#graph.add_edge(START, "get_stock_data")
graph.add_edge(START, "get_portfolio_response")
graph.add_edge("get_portfolio_response", END)

app_graph = graph.compile()