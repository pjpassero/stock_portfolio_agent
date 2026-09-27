from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from dotenv import load_dotenv
from pathlib import Path
import json


load_dotenv()


llm = ChatOpenAI(
    model="gpt-5.6-terra",
    reasoning_effort="none"
)


# prompt_path = Path("app/prompts/rec_changes.md")
# recommendation_prompt = prompt_path.read_text(encoding="utf-8")

testing_prompt_path = Path("app/prompts/rec_changes_2.md")
testing_recommendation_prompt = testing_prompt_path.read_text(encoding="utf-8")


def find_changes(portfolio, analysis_response):

    messages = [
        SystemMessage(
            content=testing_recommendation_prompt
        ),
        HumanMessage(
            content=f"""
    Portfolio:
{json.dumps(portfolio, indent=2)}

Completed Portfolio Analysis:
{analysis_response}
"""
        )
    ]

    response = llm.invoke(
        messages,
        config={
            "run_name": "Fin Portfolio Recommendations"
        }
    )

    data = json.loads(response.content)
    print(data)
    return data