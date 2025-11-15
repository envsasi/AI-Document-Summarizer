# backend/ocr_utils.py
import io

import requests
import os

OCR_API_KEY = os.getenv("OCR_API_KEY")


def extract_text_from_image(file_stream):
    """
    Extract text from an image using OCR.Space API.
    Works with JPG, PNG, TIFF, scanned photos, etc.
    """

    if OCR_API_KEY is None:
        raise RuntimeError("OCR API key not configured")

    # Read bytes from uploaded file
    img_bytes = file_stream.read()

    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": OCR_API_KEY,
        "language": "eng",
        "OCREngine": 2
    }

    files = {
        "file": ("image.png", img_bytes)
    }

    try:
        response = requests.post(url, data=payload, files=files)
        data = response.json()

        if data.get("IsErroredOnProcessing"):
            raise RuntimeError(data.get("ErrorMessage", "OCR failed"))

        parsed = data.get("ParsedResults")
        if not parsed:
            return ""

        return parsed[0].get("ParsedText", "")
    except Exception as e:
        raise RuntimeError(f"OCR error: {e}")
