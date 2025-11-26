import os
import json
from openai import OpenAI
from datetime import datetime
from sqlalchemy import create_engine

from app.utils import get_conversation

# Initialize OpenAI API
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths to prompt templates
BASE_DIR = "app/prompts"
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "system_prompt.txt")
CONTEXT_PROMPT_PATH = os.path.join(BASE_DIR, "context_template.txt")
DATABASE_URL = create_engine(os.getenv("DATABASE_URL"))
MODEL = os.getenv("LLM_MODEL")


def load_prompt(path: str) -> str:
    """Utility to safely load a text file as prompt."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt not found at: {path}")


def build_prompt(input_text: str, context_data: dict = None) -> dict:
    """
    Builds the structured prompt for the LLM combining:
    - system prompt (rules)
    - context prompt (user preferences, memory, etc.)
    - task prompt (specific instruction)
    """

    # Load all templates
    system_prompt = load_prompt(SYSTEM_PROMPT_PATH)
    # context_prompt_template = load_prompt(CONTEXT_PROMPT_PATH)
    # context_prompt = context_prompt_template.format(**context_data)

    return {
        "system_prompt": system_prompt,
    }


def handle_agent_output(agent_output, user_phone):
    try:
        parsed = json.loads(agent_output)
        if parsed.get("action") == "store_expense":
            expense = parsed.get("expense")
            from utils import insert_expense
            insert_expense(user_phone, expense)
            return "Expense stored successfully."
        else:
            return agent_output
    except:
        return agent_output


def call_llm(normalized_sender, model=MODEL, max_context_tokens=1500, response_tokens=404, engine=DATABASE_URL):
    """
    Main function to call the LLM and get structured data extraction.
    """

    # 1. Retrieve recent conversation
    history = get_conversation(normalized_sender,engine, limit=6) # set a higher limit to increase messages in memory
    system_prompt_data = build_prompt(input_text="")

    # 2. Build context for the LLM
    messages = [
        {"role": "system", "content": system_prompt_data["system_prompt"]},
    ]

    # 3. Append conversation history after the system prompt
    messages.extend(
        {"role": role, "content": message}
        for role, message in reversed(history)
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_completion_tokens=response_tokens # Adjust to limit model response
        )

        result_text = response.choices[0].message.content.strip()
        if not result_text:
            result_text= "I did not understand that. Can you rephrase?"
        return result_text

    except Exception as e:
        print("LLM failure:", str(e))
        return "I encountered an issue and could not understand. Please try again."
