from __future__ import annotations

from pathlib import Path

import streamlit as st

from smartdoc.config import settings
from smartdoc.document_loaders import load_document
from smartdoc.ollama_client import OllamaClient
from smartdoc.rag import RAGPipeline


SUPPORTED_TYPES = [".pdf", ".docx"]


@st.cache_resource(show_spinner=False)
def get_pipeline() -> RAGPipeline:
    return RAGPipeline(settings)


def main() -> None:
    settings.ensure_directories()
    st.set_page_config(page_title=settings.app_name, page_icon="📄", layout="wide")
    st.title("SmartDoc AI")
    st.caption("RAG document Q&A for PDF and DOCX with FAISS, multilingual embeddings, and Ollama Qwen2.5.")

    ollama_client = OllamaClient(
        settings.ollama_base_url,
        settings.ollama_model,
        timeout_seconds=settings.ollama_timeout_seconds,
    )
    healthy, status_message = ollama_client.health_check()

    with st.sidebar:
        st.subheader("System Status")
        st.write(f"Model: `{settings.ollama_model}`")
        if healthy:
            st.success(status_message)
        else:
            st.error(status_message)
        st.write(f"Embedding: `{settings.embedding_model_name}`")
        st.write(f"Chunk size: `{settings.chunk_size}`")
        st.write(f"Top-k retrieval: `{settings.retrieval_k}`")

    uploaded_file = st.file_uploader("Upload a PDF or DOCX document", type=["pdf", "docx"])
    question = st.text_area("Ask a question about the uploaded document", height=120)

    if st.button("Run SmartDoc", type="primary", disabled=uploaded_file is None or not question.strip()):
        if uploaded_file is None:
            st.warning("Please upload a document first.")
            return

        target_path = settings.data_dir / uploaded_file.name
        target_path.write_bytes(uploaded_file.getbuffer())

        try:
            document = load_document(target_path)
        except Exception as exc:  # noqa: BLE001
            st.exception(exc)
            return

        with st.spinner("Building embeddings, retrieving context, and asking the model..."):
            try:
                pipeline = get_pipeline()
                result = pipeline.answer_question(document, question.strip())
            except Exception as exc:  # noqa: BLE001
                st.exception(exc)
                return

        st.subheader("Answer")
        st.write(result.answer)

        st.subheader("Retrieval Summary")
        st.write(f"Source: `{document.source_name}`")
        st.write(f"Document type: `{document.source_type}`")
        st.write(f"Generated chunks: `{result.chunk_count}`")

        st.subheader("Retrieved Context")
        for idx, context in enumerate(result.contexts, start=1):
            with st.expander(f"Chunk {idx}"):
                st.text(context)

    st.divider()
    st.markdown(
        "Supported flow: `Upload -> Extract text -> Split -> Embed -> FAISS retrieve -> Ollama answer`"
    )
    st.markdown("Supported file types: `PDF`, `DOCX`")
