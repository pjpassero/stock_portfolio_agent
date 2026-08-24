from app.state import State

#this is obviously wildy over simplified
def calculate_overall_score(state:State):
    return  {
        "overall_score":state["stockWeight"] * state["stockRisk"] + state["etfWeight"] * state["etfRisk"]
    }