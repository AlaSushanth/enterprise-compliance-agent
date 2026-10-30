from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_sample():
    res = client.get("/api/sample")
    assert res.status_code == 200
    assert "content" in res.json()

def test_full_pipeline_flow():
    # 1. Ingest sample
    sample_res = client.get("/api/sample")
    content = sample_res.json()["content"]

    up_res = client.post("/api/upload", data={"text_content": content, "filename": "API_Test.txt"})
    assert up_res.status_code == 200
    doc_id = up_res.json()["document_id"]

    # 2. Run Audit Pod
    audit_res = client.post(f"/api/run-audit/{doc_id}")
    assert audit_res.status_code == 200
    data = audit_res.json()
    assert data["requires_human_review"] is True
    assert len(data["pending_decisions"]) > 0

    # 3. Submit decision
    cid = data["pending_decisions"][0]["clause_id"]
    dec_res = client.post("/api/human-decision", json={
        "document_id": doc_id,
        "decisions": {cid: {"decision": "ACCEPT_RECOMMENDATION", "note": "Approved via test"}}
    })
    assert dec_res.status_code == 200
    assert dec_res.json()["final_report"]["risk_verdict"] is not None

    # 4. Check global telemetry
    telem_res = client.get("/api/telemetry")
    assert telem_res.status_code == 200
    assert telem_res.json()["total_queries_processed"] > 0
