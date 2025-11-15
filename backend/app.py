# backend/app.py
import os
import io
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# your helper modules (unchanged)
from pdf_utils import extract_text_from_pdf
from summarizer import generate_summary
from ocr_utils import extract_text_from_image, OCR_API_KEY

# load OCR API key from environment
OCR_API_KEY = os.getenv("OCR_API_KEY", None)

# Setup logging so Render shows traces
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("document_summarizer")

app = Flask(__name__)
# Configure allowed origin via environment variable for safety
frontend_origin = os.getenv("FRONTEND_ORIGIN", None)  # e.g. https://your-frontend.vercel.app
if frontend_origin:
    CORS(app, origins=[frontend_origin], supports_credentials=True)
else:
    # fallback: do NOT allow all origins in production; only for local dev if needed
    CORS(app, supports_credentials=True)

@app.route("/healthz", methods=["GET"])
def health():
    return jsonify(status="ok", time=datetime.utcnow().isoformat())

def _ensure_stream(obj):
    """
    Accept either a Werkzeug FileStorage (request.files[...]),
    or raw bytes (just in case). Return a file-like object with .read()
    """
    # FileStorage from Flask has .stream
    try:
        # if it's FileStorage
        stream = obj.stream
        return stream
    except Exception:
        # If user passed raw bytes (or something else), wrap in BytesIO
        if isinstance(obj, (bytes, bytearray)):
            return io.BytesIO(obj)
        # if it's already a file-like, just return
        if hasattr(obj, "read"):
            return obj
        raise TypeError("Unsupported file object")

@app.route("/summarize", methods=["POST"])
def summarize_route():
    try:
        # get file and length param
        file = request.files.get("file")
        length = request.form.get("length", "medium")
        if not file:
            return jsonify(error="No file uploaded"), 400

        # Make a safe stream (handles both FileStorage or bytes)
        try:
            stream = _ensure_stream(file)
        except Exception as e:
            logger.exception("Invalid upload object")
            return jsonify(error="Invalid upload object"), 400

        # Determine whether pdf or image by filename
        filename = getattr(file, "filename", "") or ""
        lower = filename.lower()
        if lower.endswith(".pdf"):
            text = extract_text_from_pdf(stream)
        else:
            # for images and other formats, use OCR
            # note: Pillow expects a byte stream
            text = extract_text_from_image(stream)

        if not text or not text.strip():
            return jsonify(error="No readable text found in the uploaded file"), 400

        # generate summary (wrap in try so LLM / API errors are captured)
        try:
            summary = generate_summary(text, length)
        except Exception as e:
            # Log the full exception for debugging (Render logs will show it)
            logger.exception("LLM summarization failed")
            # If the external model returned an HTTP error, we may inspect e to return useful info
            return jsonify(error=f"Summarization failed: {str(e)}"), 500

        # Return response
        return jsonify(summary=summary)
    except Exception as e:
        # Catch-all so we always return JSON, and we can see the traceback in logs
        logger.exception("Unexpected server error")
        return jsonify(error="Internal server error"), 500

if __name__ == "__main__":
    # When running locally `python app.py` -> helpful debug info
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
