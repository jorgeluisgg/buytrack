import requests
import os

def download_image(url: str, media_id: str) -> str:
    """
    Downloads image from a URL and saves it locally in the downloads folder.
    Returns the file path or empty string if fails.
    """
    os.makedirs("./downloads", exist_ok=True)
    file_path = f"./downloads/{media_id}.jpg"
    try:
        response = requests.get(url)
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
