from app.state import State
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
def summarize_company(state: State):

    prompt = f"""
    You are a senior equity research analyst.

    Analyze this company.

    Company: {state["company_name"]}
    Ticker: {state["ticker"]}
    Sector: {state["sector"]}
    Industry: {state["industry"]}

    Current Price: {state["current_price"]}
    Market Cap: {state["market_cap"]}
    Trailing PE: {state["trailing_pe"]}
    Forward PE: {state["forward_pe"]}
    Beta: {state["beta"]}

    Revenue Growth: {state["revenue_growth"]}
    Earnings Growth: {state["earnings_growth"]}
    Profit Margin: {state["profit_margin"]}
    ROE: {state["return_on_equity"]}
    Debt to Equity: {state["debt_to_equity"]}

    Write a professional financial summary. Please keep the summary in 200-300 words.
    """

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    state["summary"] = response.output_text

    return state

