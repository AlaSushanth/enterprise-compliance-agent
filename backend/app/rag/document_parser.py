import re
import os
from typing import List, Dict, Any

class DocumentParser:
    """
    Enterprise Document Ingestion Parser.
    Extracts text, preserves page numbers/sections, and generates overlapping chunks.
    """

    @staticmethod
    def parse_file(file_path: str) -> List[Dict[str, Any]]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return DocumentParser._parse_pdf(file_path)
        else:
            return DocumentParser._parse_text(file_path)

    @staticmethod
    def _parse_pdf(file_path: str) -> List[Dict[str, Any]]:
        # Robust PDF parsing with pure Python fallback
        pages_content = []
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages_content.append({"page": idx + 1, "text": text})
        except Exception:
            # Fallback text extractor if pypdf is unavailable
            with open(file_path, "rb") as f:
                raw_data = f.read().decode("latin1", errors="ignore")
                # Extract text between parenthesis or text streams
                matches = re.findall(r'\(([^\)]{3,})\)', raw_data)
                cleaned_text = " ".join(matches) if matches else raw_data[:5000]
                pages_content.append({"page": 1, "text": cleaned_text})

        return DocumentParser._create_chunks(pages_content)

    @staticmethod
    def _parse_text(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Split by explicit page markers (e.g. --- Page X ---) or paragraph segments
        page_splits = re.split(r'---+\s*(?:Page\s*(\d+)|\n)\s*---+', content)
        pages_content = []

        if len(page_splits) > 1:
            current_page = 1
            for part in page_splits:
                if not part:
                    continue
                if part.isdigit():
                    current_page = int(part)
                else:
                    pages_content.append({"page": current_page, "text": part.strip()})
        else:
            # Approximate 500-word blocks as logical pages
            paragraphs = content.split("\n\n")
            page_num = 1
            current_buf = []
            for p in paragraphs:
                current_buf.append(p)
                if sum(len(x.split()) for x in current_buf) > 350:
                    pages_content.append({"page": page_num, "text": "\n\n".join(current_buf)})
                    current_buf = []
                    page_num += 1
            if current_buf:
                pages_content.append({"page": page_num, "text": "\n\n".join(current_buf)})

        return DocumentParser._create_chunks(pages_content)

    @staticmethod
    def _create_chunks(pages_content: List[Dict[str, Any]], chunk_size: int = 400, overlap: int = 80) -> List[Dict[str, Any]]:
        chunks = []
        chunk_id = 1
        for item in pages_content:
            page = item["page"]
            words = item["text"].split()
            if not words:
                continue

            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                chunk_text = " ".join(chunk_words)
                chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "page": page,
                    "text": chunk_text,
                    "word_count": len(chunk_words)
                })
                chunk_id += 1

        return chunks
