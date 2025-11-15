import os
import io
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from pdf_utils import extract_text_from_pdf
from ocr_utils import extract_text_from_image
from summarizer import generate_summary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("doc_summarizer")

app = Flask(__name__)

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")
CORS(app, origins=[FRONTEND_ORIGIN], supports_credentials=True)


def _ensure_stream(file_obj):
    if hasattr(file_obj, "stream"):
        return file_obj.stream
    if hasattr(file_obj, "read"):
        return file_obj
    if isinstance(file_obj, (bytes, bytearray)):
        return io.BytesIO(file_obj)
    raise TypeError("Invalid file object")


@app.route("/summarize", methods=["POST"])
def summarize_route():
    try:
        file = request.files.get("file")
        length = request.form.get("length", "medium")

        if not file:
            return jsonify(error="No file uploaded"), 400

        stream = _ensure_stream(file)
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(stream)
        else:
            text = extract_text_from_image(stream)

        if not text.strip():
            return jsonify(error="Could not extract text"), 400

        summary = generate_summary(text, length)
        return jsonify(summary=summary)

    except Exception:
        logger.exception("Backend crashed")
        return jsonify(error="Internal error"), 500


if __name__ == "__main__":
    # When running locally `python app.py` -> helpful debug info
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
