# curl -i -X POST `
#   https://graph.facebook.com/v22.0/857903394072476/messages `
#   -H 'Authorization: Bearer EAALhTecMIPQBPwqpQ0vWZBVdim3GMUeKZB82TpHUDM9FCMvjowgLhqZBdjthvZBoAMY2PBAy8KoOG2kae6LuAcBVc6ZCBfkP3LmM4bWteglRLrKZCd5OoTvZCEhPPLZAETqR5gyZA24tOBOY0BvkVDjnluuJxGsksHIk3DiSHdIfltZCzKHHA4rEpcAmbVpJ5Xrxps5EJFss5v8Eef3cehZBVxfD3S1XTkn2UNJdr67LrXCp4QR0gZDZD' `
#   -H 'Content-Type: application/json' `
#   -d '{ \"messaging_product\": \"whatsapp\", \"to\": \"525539942359\", \"type\": \"template\", \"template\": { \"name\": \"hello_world\", \"language\": { \"code\": \"en_US\" } } }'

import requests
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
TO_NUMBER = "525539942359"

url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "messaging_product": "whatsapp",
    "to": TO_NUMBER,
    "text": {"body": "Hello! This is a test message from Python."}
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.json())
