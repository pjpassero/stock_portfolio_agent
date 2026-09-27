from app.states.state import State

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from pathlib import Path
from dotenv import load_dotenv
import json


load_dotenv()


llm = ChatOpenAI(
    model="gpt-5.5",
    reasoning_effort="none"
)


PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "analysis_prompt.md"
)


def summarize_details(state: State):

    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    portfolio = [
        {
            "ticker": position.ticker,
            "companyName": position.company_name,
            "shares": position.shares,
            "sector": position.sector,
            "industry": position.industry,
            "allocation": position.allocation,
            "currentPrice": position.current_price,
            "currentValue": (
                position.shares * position.current_price
                if position.current_price is not None
                else None
            ),
            "costBasis": position.costBasis,
            "assetClass": position.assetClass,
        }
        for position in state["portfolioExpanded"]
    ]

    metrics = {
        "portfolioValue": state["portfolioValue"],
        "portfolioReturn": state["portfolioReturn"],
        "portfolioVolatility": state["portfolioVolatility"],
        "sharpeRatio": state["sharpeRatio"],
        # "portfolioBeta": state["portfolioBeta"],

        "stockWeight": state["stockWeight"],
        "etfWeight": state["etfWeight"],
        "cashWeight": state["cashWeight"],
        "cryptoWeight": state["cryptoWeight"],
        "portfolioScore": state["portfolio_score"]
    }

    prompt = prompt.replace(
        "{portfolio}",
        json.dumps(portfolio, indent=2, default=str)
    )

    prompt = prompt.replace(
        "{understanding_level}",
        state["interpretation_level"]
    )

    prompt = prompt.replace(
        "{metrics}",
        json.dumps(metrics, indent=2, default=str)
    )

    messages = [
        SystemMessage(content=prompt),
        HumanMessage(
            content="Analyze this portfolio and provide the portfolio summary."
        )
    ]

    response = llm.invoke(
        messages,
        config={
            "run_name": "Fin Portfolio Summary"
        }
    )

    return {
        "fin_first_response": response.content
    }