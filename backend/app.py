# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import generate_summary
from pdf_utils import extract_text_from_pdf
from ocr_utils import extract_text_from_image
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ai-document-summarizer-khaki.vercel.app/"}})



@app.route("/summarize", methods=["POST"])
def summarize_route():
    try:
        file = request.files.get("file")
        length = request.form.get("length", "medium")

        if not file:
            return jsonify(error="No file uploaded"), 400

        filename = file.filename.lower()

        # Read file only once
        file_bytes = file.read()

        # Extract text
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        else:
            text = extract_text_from_image(file_bytes)

        if not text.strip():
            return jsonify(error="Could not extract any text from the document"), 400

        # Generate summary (Groq)
        summary = generate_summary(text, length)

        return jsonify(summary=summary)

    except Exception as e:
        return jsonify(error=f"Server error: {str(e)}"), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify(message="AI Document Summarizer Backend Running")


if __name__ == "__main__":
    app.run(debug=True)
