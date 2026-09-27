from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)
from pathlib import Path
from dotenv import load_dotenv

from app.services.database_connector import get_connection
from app.tools.get_covariance import get_covariance
from app.tools.get_modeled_portfolio import get_model_portfolio
from app.tools.search_knowledge_base import search_knowledge

load_dotenv()


llm = ChatOpenAI(
    model="gpt-5.6",
    reasoning_effort="none"

)


tools = [
    get_covariance,
    get_model_portfolio,
    search_knowledge

]

tool_registry = {
    tool.name: tool
    for tool in tools
}

llm_with_tools = llm.bind_tools(tools)

PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "chat_prompt.md"
)


def execute_tool(tool_call, portfolioId):
    toolName = tool_call["name"]
    toolArgs = tool_call["args"].copy()

    toolToCall = tool_registry.get(toolName)

    if toolToCall is None:
        return {
            "errorr": f"Unknown tool: {toolName}"
        }

    if toolName == "get_covariance":
        toolArgs["portfolio_id"] = portfolioId
    elif toolName == "get_model_portfolio":
        toolArgs["portfolioId"] = portfolioId

    try:
        result = toolToCall.invoke(toolArgs)
        return result
    except Exception as e:
        return {
            "error": str(e),
            "tool": toolName
        }


def run_agent(messages, portfolioId, max_iterations=10):

    for _ in range(max_iterations):

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        if not response.tool_calls:
            return response

        for tool_call in response.tool_calls:

            tool_result = execute_tool(
                tool_call,
                portfolioId
            )

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

    raise RuntimeError(
        "Fin exceeded the maximum number of tool-calling iterations."
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


def ask_fin(
    portfolio,
    level,
    metrics,
    history,
    question,
    portfolioId
):

    instructions = build_prompt(
        portfolio,
        level,
        metrics,
        history
    )

    messages = [
        SystemMessage(content=instructions),
        HumanMessage(content=question)
    ]

    response = run_agent(
        messages,
        portfolioId
    )

    final_response = response.content



    with get_connection() as conn:
        with conn.cursor() as cur:

            new_chat_message = """
                INSERT INTO message (
                    portfolio_id,
                    role,
                    content
                )
                VALUES (%s, %s, %s)
            """

            cur.execute(
                new_chat_message,
                (
                    portfolioId,
                    "user",
                    question
                )
            )

            cur.execute(
                new_chat_message,
                (
                    portfolioId,
                    "assistant",
                    final_response
                )
            )

            conn.commit()

    return final_response