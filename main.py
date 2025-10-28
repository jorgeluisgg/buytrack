from fastapi import FastAPI, Request
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_verify_token")

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    else:
        return {"status": "forbidden"}, 403

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    print(data)
    return {"status": "received"}
