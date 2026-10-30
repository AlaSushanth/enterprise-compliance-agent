import os
from backend.app.rag.document_parser import DocumentParser

def test_text_chunking():
    sample_text = (
        "--- Page 1 ---\n"
        "All data must be encrypted with AES-256.\n"
        "--- Page 2 ---\n"
        "Liquidated damages of $1,000,000 shall apply in case of outage."
    )
    temp_path = "tests/temp_test_doc.txt"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(sample_text)

    try:
        chunks = DocumentParser.parse_file(temp_path)
        assert len(chunks) >= 2
        assert any(c["page"] == 1 for c in chunks)
        assert any(c["page"] == 2 for c in chunks)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
