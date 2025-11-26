import json
from utils import insert_expense

def process_message(user_phone, user_text, llm_reply):
    """
    Receives:
    • phone number
    • user message
    • raw LLM reply (string)

    Returns:
    • final text to send back to the user
    """

    try:
        parsed = json.loads(llm_reply)

        action = parsed.get("action")

        if action == "store_expense":
            expense = parsed.get("expense", {})
            insert_expense(user_phone, expense)
            return "Your expense has been saved successfully."

        return llm_reply

    except Exception:
        return llm_reply
