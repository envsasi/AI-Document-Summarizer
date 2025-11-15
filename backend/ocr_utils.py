# from PIL import Image
# import pytesseract
# import io
#
# # If Tesseract is installed in Windows, uncomment this:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#
# def extract_text_from_image(file_bytes):
#     image = Image.open(io.BytesIO(file_bytes))
#     text = pytesseract.image_to_string(image)
#     return text



# backend/ocr_utils.py
from PIL import Image
import pytesseract
import io

def extract_text_from_image(file_stream):
    img_bytes = file_stream.read()
    image = Image.open(io.BytesIO(img_bytes))
    # If tesseract binary isn't available this will raise OSError — caller must handle
    text = pytesseract.image_to_string(image)
    return text

