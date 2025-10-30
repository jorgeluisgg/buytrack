from fastapi import FastAPI, Request
import os
from app.utils import download_image, get_image_url
from app.ocr import extract_text_from_image

# # Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

app = FastAPI()

# Tokens
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

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
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                messages = change["value"].get("messages", [])
                for msg in messages:
                    sender = msg["from"]
                    msg_type = msg["type"]
                    print(f"Message from {sender}, type: {msg_type}")

                    if msg_type == "image":
                        media_id = msg["image"]["id"]
                        caption = msg["image"].get("caption", "")
                        print(f"Image received with media_id: {media_id}")
                        print(f"Caption: {caption}")

                        # Step 1: Get image URL
                        image_url = get_image_url(media_id, ACCESS_TOKEN)
                        print(f"Image URL: {image_url}")

                        # Step 2: Download image
                        file_path = download_image(image_url, media_id)

                        # Step 3: Extract OCR if downloaded
                        extracted_text = extract_text_from_image(file_path) if file_path else ""
                        final_text = f"{caption} {extracted_text}".strip()
                        print(f"Final extracted text to store: {final_text}")

                    elif msg_type == "text":
                        final_text = msg["text"]["body"]
                        print(f"Text message: {final_text}")

        return {"status": "received"}
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return {"status": "error"}, 500
