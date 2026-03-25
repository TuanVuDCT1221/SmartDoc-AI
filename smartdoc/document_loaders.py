from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pdfplumber
from docx import Document as DocxDocument


@dataclass(slots=True)
class LoadedDocument:
    text: str
    source_name: str
    source_type: str


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_document(file_path: str | Path) -> LoadedDocument:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = extract_pdf_text(path)
    elif suffix == ".docx":
        text = extract_docx_text(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    if not text.strip():
        raise ValueError("The uploaded file did not produce readable text.")

    return LoadedDocument(
        text=normalize_text(text),
        source_name=path.name,
        source_type=suffix.lstrip("."),
    )


def extract_pdf_text(path: Path) -> str:
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            page_text = page_text.strip()
            if page_text:
                pages.append(f"[Page {page_number}]\n{page_text}")
    return "\n\n".join(pages)


def extract_docx_text(path: Path) -> str:
    doc = DocxDocument(path)
    parts: list[str] = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue
        style_name = getattr(paragraph.style, "name", "") or ""
        if style_name.lower().startswith("heading"):
            parts.append(f"\n## {text}\n")
        else:
            parts.append(text)

    for table_index, table in enumerate(doc.tables, start=1):
        rows: list[str] = []
        for row in table.rows:
            cells = [normalize_text(cell.text) for cell in row.cells]
            cleaned_cells = [cell for cell in cells if cell]
            if cleaned_cells:
                rows.append(" | ".join(cleaned_cells))
        if rows:
            parts.append(f"\n[Table {table_index}]\n" + "\n".join(rows))

    return "\n\n".join(parts)
