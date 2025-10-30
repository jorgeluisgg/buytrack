from PIL import Image
import pytesseract

# Explicit tesseract path for Docker
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_image(file_path: str) -> str:
    """
    Given an image file path, extract text using OCR.
    """
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""
