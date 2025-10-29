from fastapi import FastAPI, Request
import os
import requests
from PIL import Image
import pytesseract
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Tokens
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Helper function to download image
def download_image(url: str, media_id: str) -> str:
    file_path = f"{media_id}.jpg"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    except Exception as e:
        print(f"Error downloading image: {e}")
        return ""

# OCR function
def extract_text_from_image(file_path: str) -> str:
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

# Function to get media URL from WhatsApp Cloud API
def get_image_url(media_id: str) -> str:
    try:
        url = f"https://graph.facebook.com/v17.0/{media_id}"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("url")  # URL to download the image
    except Exception as e:
        print(f"Error fetching media URL: {e}")
        return ""

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
        print("Webhook received:")
        print(data)

        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])

                for msg in messages:
                    sender_id = msg.get("from")
                    msg_type = msg.get("type")
                    print(f"Message from {sender_id}, type: {msg_type}")

                    text_content = ""
                    caption = ""

                    # Handle text messages
                    if msg_type == "text":
                        text_content = msg.get("text", {}).get("body", "")
                        print(f"Text message: {text_content}")

                    # Handle images
                    elif msg_type == "image":
                        image_info = msg.get("image", {})
                        media_id = image_info.get("id")
                        caption = image_info.get("caption", "")
                        print(f"Image received with media_id: {media_id}")
                        if media_id:
                            image_url = get_image_url(media_id)
                            print(f"Image URL: {image_url}")
                            if image_url:
                                file_path = download_image(image_url, media_id)
                                if file_path:
                                    ocr_text = extract_text_from_image(file_path)
                                    # Combine caption + OCR
                                    text_content = f"{caption} {ocr_text}".strip()
                                    print(f"Extracted text from image: {text_content}")
                                    # Cleanup
                                    os.remove(file_path)

                    # Here you could save text_content to a database
                    print(f"Final extracted text to store: {text_content}")

        return {"status": "received"}
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return {"status": "error", "message": str(e)}
