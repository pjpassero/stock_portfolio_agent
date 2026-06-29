from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import yfinance as yf 

class State(TypedDict):
    company:str


def get_company(state:State):
    print(f"Node 1: Received company: {state['company']}")
    return state

def greet_company(state:State):
    print(f"Node 2: Hello, {state['company']}!")
    return state


graph = StateGraph(State)

graph.add_node("get_company", get_company)
graph.add_node("greet_company", greet_company)


graph.add_edge(START, "get_company")
graph.add_edge("get_company", "greet_company")
graph.add_edge("greet_company",END)

app = graph.compile()

result = app.invoke({"company":"Apple"})

print("\n Final State:")
print(result)