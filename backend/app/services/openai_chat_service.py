from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "chat_prompt.md"
)


def build_prompt(portfolio, level, metrics, history):
    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    prompt = prompt.replace(
        "{portfolio}",
        str(portfolio)
    )

    prompt = prompt.replace(
        "{understanding_level}",
        str(level)
    )

    prompt = prompt.replace(
        "{metrics}",
        str(metrics)
    )

    prompt = prompt.replace(
        "{history}",
        str(history)
    )

    return prompt


def ask_fin(portfolio, level, metrics, history, question):
    instructions = build_prompt(
        portfolio,
        level,
        metrics,
        history
    )

    response = client.responses.create(
        model="gpt-5.6",
        instructions=instructions,
        input=question
    )

    return response.output_text