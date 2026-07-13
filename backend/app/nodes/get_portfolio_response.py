from app.state import State
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI()
def get_portfolio_response(state: State):

    prompt = f"""
    You are a wealth manager. Rate my portfolio based on the portfolio I give you:

    portfolio: {state['portfolio']}

    Write a professional analysis summary. Please keep the summary in 200-300 words.
    """

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    state["response"] = response.output_text

    return state

