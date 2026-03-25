# SmartDoc AI - Setup Checklist

## 1. Clone project

- Open terminal in the target workspace
- Clone or open the repository
- Move into the project folder:
  - `cd SmartDoc-AI`

## 2. Create Python virtual environment

- Create venv:
  - `python -m venv .venv`
- Activate on Windows:
  - `.\.venv\Scripts\activate`
- Activate on Linux or macOS:
  - `source .venv/bin/activate`

## 3. Install dependencies

- Install Python packages:
  - `pip install -r requirements.txt`

## 4. Prepare environment variables

- Copy `.env.example` to `.env`
- Verify these values:
  - `OLLAMA_BASE_URL`
  - `OLLAMA_MODEL=qwen2.5:7b`
  - `EMBEDDING_MODEL_NAME=sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
  - `CHUNK_SIZE`
  - `CHUNK_OVERLAP`
  - `RETRIEVAL_K`

## 5. Start Ollama

Choose one option:

### Option A - Local Ollama installation

- Install Ollama from `https://ollama.ai`
- Pull model:
  - `ollama pull qwen2.5:7b`
- Start Ollama if needed

### Option B - Docker

- Start Docker Desktop
- Run:
  - `docker compose up -d ollama`

## 6. Verify Ollama model

- Confirm `qwen2.5:7b` is available
- If using Docker, verify API at:
  - `http://localhost:11434/api/tags`

## 7. Start Streamlit app

- Run:
  - `streamlit run app.py`
- Open browser:
  - `http://localhost:8501`

## 8. Check base PDF flow

- Upload a sample PDF
- Ask a simple question from the document
- Confirm the app performs:
  - text extraction
  - chunking
  - embedding
  - retrieval
  - answer generation

## 9. Check DOCX support

- Upload a DOCX file with:
  - multiple headings
  - one or more tables
  - long paragraphs
- Ask a question about the DOCX content
- Confirm text is extracted cleanly and the answer is returned

## 10. Expected success criteria

- App opens successfully in Streamlit
- Sidebar shows Ollama status
- `qwen2.5:7b` is reachable
- PDF flow works end-to-end
- DOCX flow works end-to-end
- `data/`, `logs/`, and `vector_store/` are created automatically
