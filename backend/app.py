from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import generate_summary
from pdf_utils import extract_text_from_pdf
from ocr_utils import extract_text_from_image

app = Flask(__name__)

# Allow only your Vercel domain
CORS(app,
     origins=["https://ai-document-summarizer-khaki.vercel.app"],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     supports_credentials=True)


@app.route("/summarize", methods=["POST", "OPTIONS"])
def summarize_route():

    # Handle browser preflight request
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    file = request.files.get("file")
    length = request.form.get("length", "medium")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.stream)
    else:
        text = extract_text_from_image(file.stream)

    if not text.strip():
        return jsonify({"error": "No readable text found"}), 400

    summary = generate_summary(text, length)
    return jsonify({"summary": summary})


@app.route("/", methods=["GET"])
def home():
    return jsonify(message="AI Document Summarizer Backend Running")


if __name__ == "__main__":
    app.run(debug=True)
