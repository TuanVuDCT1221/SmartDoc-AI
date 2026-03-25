from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from smartdoc.config import settings
from smartdoc.document_loaders import load_document
from smartdoc.rag import RAGPipeline


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a SmartDoc end-to-end smoke test.")
    parser.add_argument("document", help="Path to a PDF or DOCX file")
    parser.add_argument("question", help="Question to ask the document")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Force Hugging Face libraries to use local cache only.",
    )
    args = parser.parse_args()

    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    sys.stdout.reconfigure(encoding="utf-8")
    document = load_document(Path(args.document))
    pipeline = RAGPipeline(settings)
    result = pipeline.answer_question(document, args.question)

    print(f"Document: {document.source_name} ({document.source_type})")
    print(f"Chunks: {result.chunk_count}")
    print(f"Retrieved contexts: {len(result.contexts)}")
    print("Answer:")
    print(result.answer)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
