import os
from io import BytesIO
from typing import Optional

import fitz  # PyMuPDF
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(page_title="DocSense", page_icon="📑", layout="wide")


def extract_pdf_text(file_bytes: bytes) -> tuple[str, int]:
    """Return readable text and number of pages from a PDF upload."""
    document = fitz.open(stream=BytesIO(file_bytes), filetype="pdf")
    try:
        return "\n\n".join(page.get_text("text") for page in document), len(document)
    finally:
        document.close()


def document_stats(text: str) -> dict[str, int]:
    words = text.split()
    return {"characters": len(text), "words": len(words), "reading_minutes": max(1, round(len(words) / 200))}


def analyse_with_gemini(text: str, question: Optional[str] = None) -> str:
    """Use Gemini when configured; never send more than the model needs."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Add GOOGLE_API_KEY or GEMINI_API_KEY to .env to use AI analysis.")

    import google.generativeai as genai

    genai.configure(api_key=api_key)
    # Gemini 1.5 Flash has been retired. Allow a project-specific override
    # without requiring a code edit when model availability changes.
    model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    excerpt = text[:100_000]
    if question:
        prompt = f"""Answer the question using only the document below. If the answer is not in the document, say so clearly. Cite the relevant wording or section where possible.

Question: {question}

Document:
{excerpt}"""
    else:
        prompt = f"""Analyse the following document. Use concise Markdown and provide:
1. A plain-language executive summary
2. Key topics or findings
3. Important dates, names, amounts, and decisions (only if present)
4. Risks, obligations, or action items
5. Three useful follow-up questions

Document:
{excerpt}"""
    return model.generate_content(prompt).text


def reset_document() -> None:
    for key in ("document_name", "document_text", "page_count", "analysis", "chat_history"):
        st.session_state.pop(key, None)


st.title("DocSense")
st.caption("Upload a PDF to understand it faster, surface key details, and ask grounded questions.")

with st.sidebar:
    st.header("Document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], on_change=reset_document)
    st.caption("Text-based PDFs work best. Scanned documents require OCR, which is not enabled yet.")

if uploaded_file and "document_text" not in st.session_state:
    try:
        with st.spinner("Reading your document…"):
            text, pages = extract_pdf_text(uploaded_file.getvalue())
        if not text.strip():
            st.error("No selectable text was found in this PDF. Try a text-based PDF or add OCR support.")
        else:
            st.session_state.document_name = uploaded_file.name
            st.session_state.document_text = text
            st.session_state.page_count = pages
            st.session_state.chat_history = []
    except Exception as error:
        st.error(f"We couldn't read that PDF: {error}")

if "document_text" not in st.session_state:
    st.info("Start by choosing a PDF from the Document panel.")
    st.stop()

text = st.session_state.document_text
stats = document_stats(text)
st.subheader(st.session_state.document_name)
metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Pages", st.session_state.page_count)
metric_2.metric("Words", f"{stats['words']:,}")
metric_3.metric("Characters", f"{stats['characters']:,}")
metric_4.metric("Read time", f"{stats['reading_minutes']} min")

analyse_tab, ask_tab, text_tab = st.tabs(["AI analysis", "Ask the document", "Extracted text"])

with analyse_tab:
    st.write("Create a structured brief from the uploaded document.")
    if st.button("Analyse document", type="primary"):
        try:
            with st.spinner("Finding the key points…"):
                st.session_state.analysis = analyse_with_gemini(text)
        except RuntimeError as error:
            st.warning(str(error))
        except Exception as error:
            st.error(f"Analysis failed: {error}")
    if st.session_state.get("analysis"):
        st.markdown(st.session_state.analysis)

with ask_tab:
    st.write("Ask a question and DocSense will answer from the uploaded document.")
    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])
    question = st.chat_input("For example: What actions are required?")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Reviewing the document…"):
                    answer = analyse_with_gemini(text, question)
            except RuntimeError as error:
                answer = str(error)
            except Exception as error:
                answer = f"I couldn't answer that question: {error}"
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

with text_tab:
    st.download_button("Download extracted text", text, file_name="document-text.txt", mime="text/plain")
    st.text_area("PDF text", text, height=520, disabled=True)
