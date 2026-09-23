from app.states.fin_state import FinState
from langgraph.graph import StateGraph, START, END
from app.nodes.collect_data_for_fin import collect_user_data
from app.nodes.fin_chat import chat_with_fin

fin_graph = StateGraph(FinState)

fin_graph.add_node("get_inital_data", collect_user_data)
fin_graph.add_node("chat_message", chat_with_fin)



#Edges

fin_graph.add_edge(START, "get_inital_data")
fin_graph.add_edge("get_inital_data", "chat_message")
fin_graph.add_edge("chat_message", END)


app_fin_graph = fin_graph.compile()