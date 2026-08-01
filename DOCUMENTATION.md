# 📘 DocSense Documentation

## Project Overview

DocSense is an AI-powered document understanding application designed to simplify reading long PDF documents.

Instead of scrolling through dozens of pages, users can upload a PDF and receive:

- a structured summary
- important information
- answers to questions about the document

The application focuses on improving accessibility and reducing the time required to understand lengthy documents.

---

# Objectives

The primary objective was to build an end-to-end application capable of

- accepting PDF uploads
- extracting document contents
- performing AI-based analysis
- answering user questions
- presenting the results through a simple user interface

---

# System Architecture

```
User

↓

Upload PDF

↓

PyMuPDF extracts text

↓

Text Processing

↓

Gemini API

↓

Generated Summary / Answers

↓

Displayed in Streamlit
```

---

# Workflow

## 1. Upload

The user uploads a PDF through the Streamlit interface.

Supported format:

- PDF

---

## 2. Text Extraction

PyMuPDF reads every page and extracts selectable text.

The extracted content is combined into one document string.

---

## 3. Document Statistics

The application calculates

- page count
- word count
- character count
- estimated reading time

These metrics help users quickly understand the size of the uploaded document.

---

## 4. AI Analysis

When the user clicks **Analyse Document**, the extracted text is sent to the Gemini API.

Gemini generates:

- Executive Summary
- Key Topics
- Important Information
- Risks or Action Items
- Follow-up Questions

---

## 5. Question Answering

Users can ask natural-language questions.

The application sends both

- the extracted document
- the user's question

to Gemini.

Gemini generates an answer based on the uploaded document.

---

# Design Decisions

## Why Streamlit?

- Rapid development
- Clean interface
- Python-only stack
- Easy deployment

---

## Why PyMuPDF?

PyMuPDF provides fast and reliable extraction of text from digital PDF files while preserving page ordering.

---

## Why Gemini?

Gemini provides strong document understanding and natural-language reasoning while requiring minimal backend infrastructure.

---

# Assumptions

- Uploaded PDFs contain selectable text.
- Internet access is available for AI analysis.
- The Gemini API key is configured correctly.
- Documents remain within the supported context length of the selected model.

---

# Limitations

Current version:

- No OCR support for scanned PDFs
- No semantic search
- No vector database
- No multi-document reasoning
- No persistent document storage

---

# Future Scope

Potential improvements include

- Retrieval-Augmented Generation (RAG)
- ChromaDB integration
- Embeddings
- Semantic search
- OCR support
- Multi-document chat
- Source citations
- Document history

---

# Challenges Faced

During development the primary challenges were

- extracting readable text from different PDF layouts
- designing prompts that generated structured responses
- keeping the user interface responsive while waiting for AI responses
- balancing simplicity with useful functionality

---

# Reflection

One thing I enjoyed while building DocSense was seeing how a relatively small Python application could combine PDF processing and large language models into a practical productivity tool.

Lowkey one of those projects where you upload a huge PDF thinking "nah this is gonna take forever" and then the AI gives you the important bits in seconds 😭

Still plenty of room to improve, but it's a solid foundation for adding retrieval, semantic search, and more advanced document understanding features in future iterations.