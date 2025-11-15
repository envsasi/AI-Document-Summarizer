# backend/pdf_utils.py
import fitz  # PyMuPDF

def extract_text_from_pdf(file_stream):
    # file_stream should support read(); if it's a bytes stream, read() returns bytes
    pdf_data = file_stream.read()
    if isinstance(pdf_data, bytes):
        doc = fitz.open(stream=pdf_data, filetype="pdf")
    else:
        # some cases file_stream is path-like -- but we expect bytes
        doc = fitz.open(stream=pdf_data, filetype="pdf")
    text = []
    for page in doc:
        text.append(page.get_text("text"))
    return "\n".join(text)
