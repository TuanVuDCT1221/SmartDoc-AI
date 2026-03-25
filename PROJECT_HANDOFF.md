# SmartDoc AI - Technical Handoff

## 1. Muc dich tai lieu

Tai lieu nay duoc viet de nguoi trong nhom co the nhanh chong hieu:

- Du an hien dang duoc setup nhu the nao
- Luong xu ly hien tai cua ung dung
- Cac thanh phan chinh trong code dang lam gi
- Cach chay lai du an o may khac
- Pham vi da hoan thanh va cac gioi han hien tai

Noi dung ben duoi phan anh trang thai thuc te cua repo o giai doan hien tai.

## 2. Tong quan hien trang

SmartDoc AI hien dang la mot ung dung hoi dap tai lieu theo mo hinh RAG, giao dien bang Streamlit, su dung:

- Ollama de goi LLM `qwen2.5:7b`
- `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` de tao embedding
- FAISS de truy hoi cac doan van ban lien quan
- Ho tro 2 dinh dang tai lieu: `PDF` va `DOCX`

Luong dang hoat dong:

`Upload file -> Trich xuat text -> Chia chunk -> Tao embedding -> FAISS retrieval -> Tao prompt -> Ollama sinh cau tra loi`

Pham vi da hoan thanh:

- Base project setup
- Chay duoc ung dung Streamlit
- Tich hop Ollama + Qwen2.5:7b
- Pipeline RAG co ban
- Ho tro upload va hoi dap voi `PDF`
- Ho tro upload va hoi dap voi `DOCX`

Pham vi chua lam:

- Chat history
- Clear history
- Citation tracking
- Hybrid search
- Conversational RAG
- Bo test tu dong day du cho nhieu truong hop tai lieu

## 3. Nhung gi da duoc setup

### Moi truong va cau hinh

- Da co `requirements.txt` de cai dependency Python
- Da co `.env` va `.env.example` de quan ly cau hinh
- Da tach cau hinh tap trung trong `smartdoc/config.py`
- Khi app chay, he thong tu tao cac thu muc neu chua ton tai:
  - `data/`
  - `logs/`
  - `vector_store/`

### Ung dung va kien truc ma nguon

- `app.py`: diem vao chay Streamlit
- `smartdoc/ui.py`: giao dien, upload file, nhap cau hoi, goi pipeline, hien thi ket qua
- `smartdoc/document_loaders.py`: doc file `PDF` va `DOCX`, chuan hoa text
- `smartdoc/rag.py`: chia chunk, embed, FAISS retrieve, build prompt, sinh cau tra loi, luu vector index
- `smartdoc/ollama_client.py`: health check va goi API cua Ollama
- `smartdoc/config.py`: doc bien moi truong va tao doi tuong `settings`

### Docker va dong goi

- Da co `Dockerfile` de dong goi ung dung Streamlit
- Da co `docker-compose.yml` gom 2 service:
  - `smartdoc-app`
  - `ollama`

Neu chay bang Docker Compose, app se noi voi Ollama qua URL noi bo:

- `http://ollama:11434`

## 4. Luong xu ly chi tiet

### Buoc 1. Khoi dong app

- Nguoi dung chay `streamlit run app.py`
- `app.py` goi `main()` trong `smartdoc/ui.py`
- `settings.ensure_directories()` dam bao cac thu muc lam viec da ton tai

### Buoc 2. Kiem tra trang thai model

- UI tao `OllamaClient`
- App goi `health_check()` toi endpoint `/api/tags`
- Sidebar hien:
  - model dang dung
  - embedding model
  - chunk size
  - retrieval k
  - trang thai ket noi Ollama

### Buoc 3. Upload file va nhap cau hoi

- Nguoi dung upload `PDF` hoac `DOCX`
- File duoc ghi vao thu muc `data/`
- Cau hoi duoc nhap trong o text area

### Buoc 4. Doc noi dung tai lieu

Ham `load_document()` trong `smartdoc/document_loaders.py` phan nhanh theo dinh dang file:

- `PDF`: dung `pdfplumber` de trich text tung trang
- `DOCX`: dung `python-docx` de doc paragraph va table

Xu ly bo sung cho `DOCX`:

- Giu heading thanh dang `## ...`
- Gom noi dung bang theo tung dong `cell1 | cell2 | ...`

Sau khi doc xong:

- Text duoc chuan hoa khoang trang va xuong dong
- Neu file khong doc ra duoc noi dung, he thong bao loi

### Buoc 5. Tao pipeline RAG

`get_pipeline()` trong UI duoc cache bang `st.cache_resource`, nghia la:

- Khong phai tai lai embedding model moi lan bam nut
- Giam thoi gian khoi tao lai cac tai nguyen nang

Pipeline trong `smartdoc/rag.py` gom:

- `SentenceTransformer` de embed text
- `RecursiveCharacterTextSplitter` de chia chunk
- `OllamaClient` de sinh cau tra loi

### Buoc 6. Chia chunk va tao embedding

- Van ban duoc chia thanh cac chunk theo `chunk_size` va `chunk_overlap`
- Cac separator uu tien theo thu tu:
  - heading
  - doan trong
  - xuong dong
  - dau cham
  - khoang trang
- Moi chunk duoc embed voi `normalize_embeddings=True`

### Buoc 7. Retrieval bang FAISS

- Embedding cua cac chunk duoc dua vao `faiss.IndexFlatIP`
- Cau hoi cung duoc embed
- He thong lay `top-k` chunk lien quan nhat theo `RETRIEVAL_K`

### Buoc 8. Tao prompt va goi LLM

Prompt hien tai duoc thiet ke voi cac nguyen tac:

- Tra loi bang tieng Viet neu nguoi dung khong yeu cau ngon ngu khac
- Chi duoc dung context duoc trich ra
- Uu tien chunk xep truoc vi da duoc sap theo do lien quan
- Neu trong tai lieu khong co thong tin thi phai noi ro

### Buoc 9. Luu vector index

Sau moi lan xu ly:

- He thong ghi file `.faiss` vao `vector_store/`
- He thong ghi them file `.txt` chua noi dung chunk
- Ten file duoc dat theo MD5 cua `document.source_name`

Luu y:

- Hien tai index duoc tao lai cho moi lan hoi dap, sau do moi luu xuong o dia
- Chua co co che tai su dung index da luu de tranh embed lai o lan sau

## 5. Ho tro tai lieu

### PDF

Da ho tro:

- Trich text tung trang
- Gan nhan `[Page x]` vao noi dung de de theo doi

Han che:

- Neu PDF la scan image thuong se khong trich text tot vi chua co OCR

### DOCX

Da ho tro:

- Paragraph text
- Heading
- Table text

Han che:

- Chua xu ly sau cho image, textbox, footnote, header/footer, comment, track changes

## 6. Bien moi truong quan trong

Du an dang dung cac bien chinh sau trong `.env`:

- `APP_NAME`
- `DATA_DIR`
- `LOG_DIR`
- `VECTOR_STORE_DIR`
- `EMBEDDING_MODEL_NAME`
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `RETRIEVAL_K`
- `MAX_CONTEXT_CHARS`
- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`
- `OLLAMA_TIMEOUT_SECONDS`
- `OLLAMA_TEMPERATURE`

Gia tri mac dinh tham chieu trong repo hien tai:

- `OLLAMA_MODEL=qwen2.5:7b`
- `EMBEDDING_MODEL_NAME=sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
- `CHUNK_SIZE=1200`
- `CHUNK_OVERLAP=200`
- `RETRIEVAL_K=3`
- `MAX_CONTEXT_CHARS=10000`

## 7. Cach chay du an

### Cach 1. Chay local

1. Tao moi truong ao:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Cai dependency:

```powershell
pip install -r requirements.txt
```

3. Tao file `.env` tu `.env.example`

4. Dam bao Ollama dang chay va da pull model:

```powershell
ollama pull qwen2.5:7b
```

5. Chay app:

```powershell
streamlit run app.py
```

### Cach 2. Chay bang Docker Compose

```powershell
docker compose up -d --build
```

Sau do:

- Streamlit: `http://localhost:8501`
- Ollama API: `http://localhost:11434`

## 8. Kiem thu va xac minh da co

Da co script smoke test:

- `scripts/smoke_test.py`

Script nay cho phep test nhanh luong end-to-end:

```powershell
python scripts/smoke_test.py <duong_dan_file> "<cau_hoi>"
```

Theo trang thai hien tai da tung xac minh:

- App khoi dong duoc
- Ollama ket noi duoc
- PDF flow chay end-to-end
- DOCX flow chay end-to-end
- Source code compile duoc

## 9. Cau truc thu muc de team de theo doi

```text
SmartDoc-AI/
|- app.py
|- .env
|- .env.example
|- requirements.txt
|- Dockerfile
|- docker-compose.yml
|- SETUP_CHECKLIST.md
|- STATUS.md
|- PROJECT_HANDOFF.md
|- scripts/
|  |- smoke_test.py
|- smartdoc/
|  |- config.py
|  |- document_loaders.py
|  |- ollama_client.py
|  |- rag.py
|  |- ui.py
|- data/
|- logs/
|- vector_store/
`- documentation/
```

## 10. Cac diem can luu y khi phat trien tiep

- He thong hien tai moi tap trung vao 1 cau hoi / 1 lan upload, chua co hoi thoai nhieu luot
- Vector index duoc luu ra o dia nhung chua duoc nap lai de tai su dung
- Chua co test tu dong day du cho cac bo tai lieu phuc tap
- Chua co OCR cho file PDF scan
- Chua co co che trich dan nguon theo chunk trong cau tra loi
- `logs/` da duoc tao san nhung chua co logging chi tiet trong code

## 11. De xuat huong mo rong tiep theo

Neu tiep tuc phat trien, cac huong hop ly nhat la:

1. Them citation va hien thi nguon trich dan theo chunk
2. Tai su dung vector index da luu de giam thoi gian xu ly
3. Them chat history va conversational RAG
4. Bo sung test case tu dong cho nhieu file `DOCX` va `PDF`
5. Them OCR cho cac file PDF dang scan
6. Them logging va error reporting ro rang hon

## 12. Tai lieu nen doc cung

De co them context, co the doc them:

- `SETUP_CHECKLIST.md`: checklist setup nhanh cho may moi
- `STATUS.md`: trang thai cong viec va pham vi da hoan thanh

---

Neu can mo ta ngan gon trong 1 cau: hien tai SmartDoc AI da co mot bo khung RAG co the chay duoc end-to-end cho `PDF` va `DOCX`, su dung `FAISS + multilingual embeddings + Ollama Qwen2.5`, san sang de ca nhom tiep tuc mo rong them tinh nang.
