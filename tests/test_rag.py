from backend.app.rag.vector_store import vector_store

def test_vector_store_initialization():
    # Should have pre-seeded enterprise policies
    assert vector_store.total_docs >= 5

def test_hybrid_search_encryption():
    results = vector_store.hybrid_search("AES-256 TLS 1.3 encryption keys", top_k=1, filter_type="POLICY")
    assert len(results) > 0
    top = results[0]
    assert "Encryption" in top["metadata"]["title"]
    assert top["score"] > 0.1

def test_hybrid_search_sla():
    results = vector_store.hybrid_search("99.9% uptime SLA penalty", top_k=1, filter_type="POLICY")
    assert len(results) > 0
    top = results[0]
    assert "SLA" in top["metadata"]["title"] or "Service Level" in top["metadata"]["title"]
