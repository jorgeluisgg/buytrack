import os
import json
from openai import OpenAI
from datetime import datetime

# Initialize OpenAI API
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths to prompt templates
BASE_DIR = "app/prompts"
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "system_prompt.txt")
CONTEXT_PROMPT_PATH = os.path.join(BASE_DIR, "context_template.txt")
TASK_PROMPT_PATH = os.path.join(BASE_DIR, "task_prompt.txt")

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
    context_prompt_template = load_prompt(CONTEXT_PROMPT_PATH)
    task_prompt_template = load_prompt(TASK_PROMPT_PATH)

    # Fill context placeholders dynamically
    if context_data is None:
        context_data = {
            "user_name": "User",
            "language": "Spanish",
            "default_owner": "User",
            "default_category": "personal",
            "categories_and_subcategories": "- Housing\n- Services\n- Transport\n- Groceries\n- Savings\n- Education\n- Health\n- Eating Out\n- Going Out\n- Extras",
            "user_notes": "No additional notes provided.",
        }

    context_prompt = context_prompt_template.format(**context_data)
    task_prompt = task_prompt_template.replace("{{input_text}}", input_text.strip())

    return {
        "system_prompt": system_prompt,
        "context_prompt": context_prompt,
        "task_prompt": task_prompt
    }


def call_llm(input_text: str, context_data: dict = None) -> dict:
    """
    Main function to call the LLM and get structured data extraction.
    """
    message = input_text # delete after testing
    # prompts = build_prompt(input_text, context_data)

    # Combine all prompts into the chat message sequence
    # messages = [
    #     {"role": "system", "content": prompts["system_prompt"]},
    #     {"role": "user", "content": prompts["context_prompt"]},
    #     {"role": "user", "content": prompts["task_prompt"]},
    # ]

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": message}] # modify after testing
        )

        result_text = response.choices[0].message.content.strip()
        return result_text

        # Try to parse JSON output
        # try:
        #     return json.loads(result_text)
        # except json.JSONDecodeError:
        #     return {"error": "Failed to parse JSON", "raw_output": result_text}

    except Exception as e:
        return {"error": f"LLM call failed: {str(e)}"}
