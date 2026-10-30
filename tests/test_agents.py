from backend.app.agents.graph import ComplianceAgentPodGraph

def test_multi_agent_pipeline_execution():
    chunks = [
        {"chunk_id": "c1", "page": 1, "text": "Customer data must be encrypted with AES-256 in transit and rest."},
        {"chunk_id": "c2", "page": 2, "text": "Vendor agrees to unlimited liability and liquidated damages of $1,000,000 USD."}
    ]
    
    state = ComplianceAgentPodGraph.initialize_state(
        document_id="doc_test_01",
        document_name="Test_Contract.txt",
        total_pages=2,
        raw_chunks=chunks
    )

    # Run pipeline up to human checkpoint
    state = ComplianceAgentPodGraph.run_pipeline(state)
    assert len(state["extracted_clauses"]) >= 2
    assert len(state["policy_matches"]) >= 2
    assert len(state["risk_evaluations"]) >= 2
    assert state["requires_human_review"] is True
    assert len(state["pending_decisions"]) >= 1

    # Apply human decision
    clause_id = state["pending_decisions"][0]["clause_id"]
    decisions = {clause_id: {"decision": "ACCEPT_RECOMMENDATION", "note": "Capped at $100k"}}
    final_state = ComplianceAgentPodGraph.resume_with_human_decisions(state, decisions)

    assert final_state["requires_human_review"] is False
    assert final_state["final_report"] is not None
    assert "metrics" in final_state["final_report"]
    assert final_state["final_report"]["metrics"]["total_requirements_analyzed"] >= 2
