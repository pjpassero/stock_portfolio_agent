from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv()

client = OpenAI()

prompt_path = Path("app/prompts/rec_changes.md")
recommendation_prompt = prompt_path.read_text(encoding="utf-8")

def find_changes(portfolio, analysis_response):
    response = client.responses.create(
        model="gpt-5.6-terra",
        instructions=recommendation_prompt,
        input=f"""
        Portfolio:
        {json.dumps(portfolio, indent=2)}

        Completed Portfolio Analysis:
        {analysis_response}
        """
    )
    return json.loads(response.output_text)


