from fastapi import FastAPI, Request
import os
import requests
from sqlalchemy import create_engine

from app.utils import download_image, get_image_url, send_whatsapp_message, canonical_e164, save_message, get_or_create_user
from app.ocr import extract_text_from_image
from app.llm import call_llm
from app.agent_processor import process_message


# # Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

app = FastAPI()

# Root endpoint for basic health check
@app.get("/")
def root():
    return {"message": "FastAPI WhatsApp webhook running!"}

# Tokens
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
DATABASE_URL = create_engine(os.getenv("DATABASE_URL"))

# Verify webhook
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return {"status": "forbidden"}, 403

# Handle incoming messages
# @app.post("/webhook")
# async def handle_webhook(request: Request):
#     try:
#         data = await request.json()
#         for entry in data.get("entry", []):
#             for change in entry.get("changes", []):
#                 messages = change["value"].get("messages", [])
#                 for msg in messages:
#                     sender = msg["from"]
#                     msg_type = msg["type"]
#                     print(f"Message from {sender}, type: {msg_type}")

#                     if msg_type == "image":
#                         media_id = msg["image"]["id"]
#                         caption = msg["image"].get("caption", "")
#                         print(f"Image received with media_id: {media_id}")
#                         print(f"Caption: {caption}")

#                         # Step 1: Get image URL
#                         image_url = get_image_url(media_id, ACCESS_TOKEN)
#                         print(f"Image URL: {image_url}")

#                         # Step 2: Download image
#                         file_path = download_image(image_url, media_id, ACCESS_TOKEN)

#                         # Step 3: Extract OCR if downloaded
#                         extracted_text = extract_text_from_image(file_path) if file_path else ""
#                         final_text = f"{caption}, Text extracted from file: {extracted_text}".strip()
#                         print(f"Final extracted text to store: {final_text}")

#                     elif msg_type == "text":
#                         final_text = msg["text"]["body"]
#                         print(f"Text message: {final_text}")

#                     if final_text:
#                         llm_result = call_llm(final_text)
#                         print(f"Structured extraction: {llm_result}")

#                         # Step 5: Prepare response message
#                         if "error" in llm_result:
#                             reply_text = (
#                                 "There was an error processing your message:\n"
#                                 f"{llm_result['error']}\n\n"
#                                 "Please try again or rephrase your input."
#                             )
#                         else:
#                             formatted = "\n".join([f"**{k}:** {v}" for k, v in llm_result.items()])
#                             reply_text = f"✅ Here is the structured information I extracted:\n\n{formatted}"

#                         # Step 6: Send back to WhatsApp
#                         send_whatsapp_message(sender, reply_text, ACCESS_TOKEN, PHONE_NUMBER_ID)

#         return {"status": "received"}
#     except Exception as e:
#         print(f"Error handling webhook: {e}")
#         return {"status": "error"}, 500

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                messages = change["value"].get("messages", [])
                for msg in messages:
                    normalized_sender = canonical_e164(msg["from"], default_region="MX")
                    user = get_or_create_user(normalized_sender, DATABASE_URL)
                    msg_type = msg["type"]

                    if msg_type == "text":
                        user_message = msg["text"]["body"]
                        print(f"User: {user_message}")
                        # 1. Save the user message
                        save_message(normalized_sender, "user", user_message, DATABASE_URL)
                        # 4. Call LLM with context
                        raw_reply = call_llm(normalized_sender)
                        print(f"AI: {raw_reply}")
                        # 5. Prepare final reply using agent processor
                        final_reply = process_message(normalized_sender, user_message, raw_reply)
                        # 5. Save the reply
                        save_message(normalized_sender, "assistant", final_reply, DATABASE_URL)
                        # 6. Send reply back via WhatsApp
                        send_whatsapp_message(normalized_sender, final_reply, ACCESS_TOKEN, PHONE_NUMBER_ID)
    except Exception as e:
        print(f"Webhook error: {e}")
