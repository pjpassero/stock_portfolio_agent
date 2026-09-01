from langchain_core.tools import tool
from app.models.model_portfolio import ModelPortfolio
from app.state import State

@tool
def create_model_portfolio() -> str:
    """
    Creates a new model portfolio that can be used
    to test hypothetical portfolio changes.
    """

    print("Create Model Called!")

    return "Model portfolio created successfully."

print(create_model_portfolio.invoke({}))