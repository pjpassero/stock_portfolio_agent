from app.state import State

def get_ticker(state:State):
    print(f"Ticker is {state['ticker']}")
    return state
