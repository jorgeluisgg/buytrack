import requests
import os
import phonenumbers
import re
from sqlalchemy import text

# WEBHOOK UTILITIES
def download_image(url: str, media_id: str, access_token: str) -> str:
    """
    Downloads image from a URL and saves it locally in the downloads folder.
    Returns the file path or empty string if fails.
    """
    os.makedirs("./downloads", exist_ok=True)
    file_path = f"./downloads/{media_id}.jpg"
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    except Exception as e:
        print(f"Error downloading image: {e}")
        return ""

def get_image_url(media_id: str, access_token: str) -> str:
    """
    Fetches media URL from WhatsApp Cloud API using the provided media_id and access_token.
    """
    try:
        url = f"https://graph.facebook.com/v17.0/{media_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("url")  # URL to download the image
    except Exception as e:
        print(f"Error fetching media URL: {e}")
        return ""

import requests

# WHATSAPP UTILITIES
def send_whatsapp_message(recipient_id: str, message: str, access_token: str, phone_number_id: str):
    """
    Sends a WhatsApp text message using the Graph API.

    Args:
        recipient_id (str): WhatsApp ID of the recipient (user phone number in international format).
        message (str): The message body to send.
        access_token (str): WhatsApp Cloud API access token.
        phone_number_id (str): Phone number ID from your WhatsApp Cloud configuration.
    """
    try:
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {"body": message}
        }

        response = requests.post(url, headers=headers, json=payload)
        # response.raise_for_status()
        if response.status_code != 200:
            print(f"Error sending WhatsApp message: {response.text}")
        print(f"Message sent to {recipient_id}: {message[:80]}...")

    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

def canonical_e164(number: str, default_region: str = "MX") -> str:
    """
    Parse the number and return canonical E.164 digits without '+'.
    Example: '+52 1 55 3994 2359' -> '525539942359' (or '521...' normalized depending on parsing).
    default_region is used if no country code is present.
    """
    try:
        n = phonenumbers.parse(number, 'MX')
        if not phonenumbers.is_valid_number(n):
            n = phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)
            n = re.sub(r"^\+521", "+52", n)
            n = phonenumbers.parse(n, 'MX')
            n = phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)
        return n.strip('+')  # Graph API uses digits without plus
    except Exception:
        return re.sub(r'\D', '', number)

# DATABASE UTILITIES
def get_or_create_user(user_phone: str, engine):
    query_select = text("""
        SELECT id, phone, name
        FROM users
        WHERE phone = :p
    """)

    query_insert = text("""
        INSERT INTO users (phone)
        VALUES (:p)
        RETURNING id, phone, name
    """)

    with engine.begin() as conn:
        result = conn.execute(query_select, {"p": user_phone}).fetchone()
        if result:
            return result
        result = conn.execute(query_insert, {"p": user_phone}).fetchone()
        return result

def save_message(user_phone: str, role: str, message: str, engine):
    """
    Saves a message to the database for a given user.
    """
    query = text("""
        INSERT INTO messages (user_phone, role, message)
        VALUES (:u, :r, :m)
    """)
    with engine.begin() as conn:  # begin() handles commits automatically
        conn.execute(query, {"u": user_phone, "r": role, "m": message})

def get_conversation(user_phone: str, engine, limit: int = 10):
    query = text("""
        SELECT role, message
        FROM messages
        WHERE user_phone = :u
        ORDER BY created_at DESC
        LIMIT :limit
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"u": user_phone, "limit": limit})
        return result.fetchall()
