# 📄 DocSense

> Understand documents faster with AI.

DocSense is an AI-powered document understanding platform built using Python and Streamlit. It allows users to upload PDF documents, extract their text, generate structured summaries, and ask natural-language questions about the document using Google's Gemini model.

The goal of the project is to make long documents easier to understand without manually reading every page.

---

## ✨ Features

- 📄 Upload PDF documents
- ⚡ Fast text extraction using PyMuPDF
- 🤖 AI-generated document analysis
- 💬 Chat with your uploaded document
- 📊 Automatic document statistics
- 📥 Download extracted text
- 🌙 Clean dark-themed interface

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| UI | Streamlit |
| PDF Processing | PyMuPDF |
| AI Model | Google Gemini |
| Environment | python-dotenv |

---

## 📂 Project Structure

```
docsense/
│
├── app.py
├── requirements.txt
├── README.md
├── DOCUMENTATION.md
├── .env
└── assets/
```

---

## 🚀 Installation

Clone the repository

```bash
git clone <repo-url>
```

Move into the project

```bash
cd docsense
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run

```bash
streamlit run app.py
```

---

## Future Improvements

- Retrieval-Augmented Generation (RAG)
- Vector database integration
- OCR for scanned PDFs
- Multi-document support
- Source citations
- Semantic search

---

## Author

Built by Anush Ragu
