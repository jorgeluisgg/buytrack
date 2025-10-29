from fastapi import FastAPI, Request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_verify_token")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    else:
        return {"status": "forbidden"}, 403

# @app.post("/webhook")
# async def handle_webhook(request: Request):
#     data = await request.json()
#     print(data)
#     return {"status": "received"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    print("Webhook received:")
    print(data)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]["value"]
        messages = changes.get("messages", [])

        if not messages:
            return {"status": "no messages"}

        msg = messages[0]
        msg_type = msg.get("type")
        sender = msg.get("from")

        if msg_type == "text":
            # CASE 1: Plain text message
            text = msg["text"]["body"]
            print(f"Text message received from {sender}: {text}")

        elif msg_type == "image":
            # CASE 2 & 3: Image message (with or without caption)
            media_id = msg["image"]["id"]
            caption = msg["image"].get("caption")
            print(f"Image received from {sender} with media_id: {media_id}")

            if caption:
                print(f"Caption: {caption}")

            image_url = get_image_url(media_id)
            print(f"Image URL: {image_url}")

            download_image(image_url, media_id)
            print("Image downloaded successfully.")

        else:
            print(f"Unsupported message type: {msg_type}")

    except Exception as e:
        print(f"Error handling webhook: {e}")

    return {"status": "received"}


def get_image_url(media_id: str):
    """Request WhatsApp Graph API to get the image URL"""
    url = f"https://graph.facebook.com/v17.0/{media_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("url")


def download_image(image_url: str, media_id: str):
    """Download the image from the returned URL"""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(image_url, headers=headers)
    response.raise_for_status()
    with open(f"{media_id}.jpg", "wb") as f:
        f.write(response.content)
