
from app.state import State
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

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
        #"portfolioBeta": state["portfolioBeta"],

        "stockWeight": state["stockWeight"],
        "stockRisk": state["stockRisk"],
        "stockVolatility": state["stockVolatility"],
        "stockHHI": state["stockHHI"],
        "stockInternalWeights": state["stockInternalWeights"],
        "stockSectorWeights": state["stockSectorWeights"],

        "etfWeight": state["etfWeight"],
        "etfRisk": state["etfRisk"],
        "etfVolatility": state["etfVolatility"],
        "etfInternalWeights": state["etfInternalWeights"],
        "etfSectorWeights": state["etfSectorWeights"],
        "etfSectorHHI": state["etfSectorHHI"],
        "cashWeight": state["cashWeight"],
        "cryptoWeight": state["cryptoWeight"],
        "portfolioRisk": state["portfolioRisk"],
        "portfolioScore":state["portfolio_score"]
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

    response = client.responses.create(
        model="gpt-5.5",
        instructions=prompt,
        input="Analyze this portfolio and provide the portfolio summary."
    )

    return {
        "fin_first_response": response.output_text
    }