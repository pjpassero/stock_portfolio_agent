from app.state import State

def route_model(state:State):
    if(state["need_new_calculations"]):
        return "add_position"
    else:
        return "calculate_statistics"