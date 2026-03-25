# SmartDoc AI - Current Status

## Scope being implemented

This status summary only covers:

- `Setup & Base`
- `Q1: Ho tro DOCX`

The project has not moved on to later items such as chat history, clear history, citation tracking, hybrid search, or conversational RAG.

## Architecture captured from the report

The current implementation follows the architecture described in the project report:

- `Presentation Layer`: Streamlit UI
- `Application Layer`: document loading, text splitting, retrieval, prompt building
- `Data Layer`: FAISS vector index, multilingual embeddings, local document storage
- `Model Layer`: Ollama with `qwen2.5:7b`

Implemented base flow:

`Upload -> Extract text -> Split -> Embed -> FAISS retrieve -> Ollama answer`

## What has been completed

### 1. Base project setup

Completed:

- Created runnable entrypoint in `app.py`
- Organized source code into modules under `smartdoc/`
- Added environment configuration with `.env` and `.env.example`
- Expanded `.gitignore`
- Added Docker support with `Dockerfile`, `docker-compose.yml`, and `.dockerignore`
- Added team setup checklist in `SETUP_CHECKLIST.md`
- Added working folders:
  - `data/`
  - `logs/`
  - `vector_store/`
- Created Python virtual environment `.venv`
- Installed project dependencies from `requirements.txt`

### 2. Base RAG application

Completed:

- Built Streamlit UI for document upload and question answering
- Added Ollama connectivity check in sidebar
- Added configurable chunking and retrieval settings
- Added FAISS indexing and retrieval pipeline
- Added multilingual embedding model support with `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
- Added Ollama integration for `qwen2.5:7b`
- Added caching for the pipeline in Streamlit to reduce repeated heavy reloads

Main files:

- `app.py`
- `smartdoc/ui.py`
- `smartdoc/config.py`
- `smartdoc/rag.py`
- `smartdoc/ollama_client.py`

### 3. Q1 - DOCX support

Completed:

- Added support for both `.pdf` and `.docx`
- Added file-type detection
- Added DOCX text extraction using `python-docx`
- Preserved heading structure in extracted DOCX text
- Extracted table content from DOCX files
- Added text normalization to reduce spacing and encoding noise
- Added basic unsupported-format and empty-content error handling

Main file:

- `smartdoc/document_loaders.py`

## Verification completed

### Verified locally

- Python environment was created successfully
- Dependencies were installed successfully
- Ollama was started through Docker
- Model `qwen2.5:7b` was pulled successfully
- Project source compiles successfully with `python -m compileall`
- Streamlit app was started successfully and responded with `HTTP 200`

### Smoke tests completed

#### DOCX

Result: `PASS`

- A sample DOCX file was generated in `data/sample_q1.docx`
- The system loaded the DOCX correctly
- Heading and table content were extracted correctly
- End-to-end question answering returned the expected answer:
  - `Vector store trong file DOCX mau la FAISS`

#### PDF

Result: `PASS` for base end-to-end flow

- The system loaded the sample PDF report
- Text extraction worked
- Chunking worked
- Embedding generation worked
- FAISS retrieval worked
- Ollama answer generation worked
- A direct smoke-test question returned the correct model answer:
  - `Qwen2.5:7b thong qua Ollama`

Note:

- An earlier phrasing about architecture returned a less clean answer even though retrieval was correct.
- After prompt tuning, the base PDF smoke test now returns a correct direct answer.

## Files added or updated

Created or updated during this phase:

- `app.py`
- `.env`
- `.env.example`
- `.gitignore`
- `.dockerignore`
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `smartdoc/__init__.py`
- `smartdoc/config.py`
- `smartdoc/document_loaders.py`
- `smartdoc/ollama_client.py`
- `smartdoc/rag.py`
- `smartdoc/ui.py`
- `scripts/smoke_test.py`
- `SETUP_CHECKLIST.md`
- `data/.gitkeep`
- `logs/.gitkeep`
- `vector_store/.gitkeep`

## What is not done yet

Still not completed:

- Keep Streamlit running as a persistent dev server for handoff
- More structured automated tests for multiple DOCX layouts

## Current conclusion

At the current stage:

- `Setup & Base` is implemented
- `Q1: Ho tro DOCX` is implemented
- The project can already run the base RAG workflow for both `PDF` and `DOCX`
- No work has been done beyond the requested scope
