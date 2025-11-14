# 📘 AI Document Summarizer  
*A smart AI-powered web app that extracts text from PDFs and images, then generates clean, highlighted summaries — all inside a ChatGPT-style interface.*

---

## 📌 Overview  
This project is part of a **Technical Assessment** for the Software Engineer role.  
The goal is to build a **Document Summary Assistant** capable of:

- Extracting text from **PDFs and images**
- Generating **short, medium, or long summaries**
- Highlighting **important points**
- Handling **long documents** using a chunk-based LLM pipeline
- Providing a clean, modern **ChatGPT-like UI**

The system is optimized for accuracy, user experience, and scalability.

---

# ⭐ Key Features

### 🔹 1. AI Summaries (LLM-Based)
- Uses GROQ LLaMA model for fast, high-quality summarization  
- Clean paragraph output  
- Highlights **key phrases**  
- Supports Long → Medium → Short summary options  

---

### 🔹 2. Smart Text Extraction
#### PDF Extraction
- Uses **PyMuPDF** for fast and accurate text extraction  
- Supports multipage PDFs  

#### OCR for Images  
- Powered by **Tesseract OCR**  
- Works with:
  - Scanned documents  
  - Photos of pages  
  - Screenshots  
  - Low-quality images  

---

### 🔹 3. Chunk-Based Long Document Handling
LLMs have token limits, so long PDFs are automatically:

1. **Chunked into smaller text segments**  
2. Each chunk summarized individually  
3. Summaries merged  
4. Final summary generated  

This ensures the system handles 20+ page PDFs without failing.

---

### 🔹 4. Clean ChatGPT-Style Interface
Built with **React + TailwindCSS**, the UI supports:

✔ Drag & drop document upload  
✔ Smooth chat bubble layout  
✔ Auto-scrolling messages  
✔ File preview  
✔ Typing/loading indicators  
✔ Modern, responsive design  

---

### 🔹 5. Backend Architecture
- **Flask** backend  
- Route `/summarize` accepts file + summary length  
- Automatic text extraction based on file type  
- Cleans text before summarizing (removes markdown, bullets, symbols)  
- Returns clean, modest-length summary with highlighted key points  

---

# 🛠 Tech Stack

### 🖥 Frontend
- React (Vite)
- Tailwind CSS
- Lucide Icons

### 🧠 Backend
- Python (Flask)
- PyMuPDF (PDF text)
- pytesseract (OCR)
- groq (LLM API)
- dotenv

### 🤖 AI Model
- GROQ – `llama-3.1-8b-instant`

---

# 📦 Project Structure



AI-Document-Summarizer/
│
├── backend/
│ ├── app.py
│ ├── summarizer.py
│ ├── pdf_utils.py
│ ├── ocr_utils.py
│ ├── requirements.txt
│ └── flask_session/
│
└── frontend/
├── src/
│ ├── App.jsx
│ ├── components/
│ │ ├── ChatWindow.jsx
│ │ ├── ChatContainer.jsx
│ │ ├── UploadBar.jsx
│ │ └── MessageBubble.jsx
│ ├── index.css
│ └── main.jsx
├── package.json
└── tailwind.config.js





---

# 🚀 Getting Started

##backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


Add your GROQ key to .env:
GROQ_API_KEY=your_key_here


Run backend:
python app.py
---

##Frontend Setup

cd frontend
npm install
npm run dev


📄 How It Works

1.User uploads PDF/Image
2.Backend detects file type
3.Extracts text:
  PDFs → PyMuPDF
  Images → Tesseract OCR
4.Text is cleaned (no bold, bullets, markdown)
5.Long text → Chunked into sections
6.Each chunk summarized using GROQ
7.Final combined summary returned
8.UI displays summary in ChatGPT-style bubbles
---

<img width="1918" height="959" alt="image" src="https://github.com/user-attachments/assets/a74fff3f-737b-4e75-a0c8-855d05c9a109" />



---
🧪 Example Input vs Output

Input:
Scanned PDF containing job description paragraphs.

Output (formatted summary):
The system extracts text using OCR and generates a clean summary emphasizing key requirements, core responsibilities, and important competencies. The Assistant highlights relevant points while maintaining clarity and structure.

🔮 Future Enhancements
Dark mode
Export summary as PDF
Keyword extraction
Headline + sub-topic summaries
Page-wise summaries
Multi-file chat threads

✨ Author
Sasi Kiran
B.Tech CSE (AI)
AI/ML Developer | Full Stack Developer



⭐ Support
If you found this project useful, please ⭐ the repository!


