from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "file_upload.md"
)


def extract_csv_with_llm(csvText):
    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    prompt = prompt.replace(
            "{csv_data}",
            str(csvText)
    )
    response = client.responses.create(
            model="gpt-5.6-terra",
            input=prompt
    )
    
    return json.loads(response.output_text)