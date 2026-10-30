from typing import Dict, Any, List
from backend.app.rag.vector_store import vector_store
from backend.app.core.telemetry import telemetry_engine

class PolicyRAGAgent:
    """
    Agent 2: Policy Knowledge Retrieval & Mapping Agent (RAG).
    Conducts hybrid dense + BM25 vector retrieval over internal enterprise compliance baselines,
    mapping each extracted vendor clause to internal security, legal, and operational policies.
    """

    @classmethod
    def execute(cls, state: Dict[str, Any]) -> Dict[str, Any]:
        trace_id = state.get("trace_id", "trace-default")
        span_ctx = telemetry_engine.start_span(trace_id, "PolicyRAGAgent", "retrieve_internal_policies")

        extracted_clauses = state.get("extracted_clauses", [])
        policy_matches = []

        prompt_tokens = 0
        completion_tokens = 0

        for clause in extracted_clauses:
            query = f"{clause['category']}: {clause['original_text']}"
            prompt_tokens += len(query.split())

            # Hybrid RAG search against internal policy vector store
            matches = vector_store.hybrid_search(query=query, top_k=1, filter_type="POLICY")
            
            if matches:
                top_match = matches[0]
                meta = top_match["metadata"]
                match_record = {
                    "clause_id": clause["clause_id"],
                    "matched_policy_id": top_match["doc_id"],
                    "policy_title": meta.get("title", ""),
                    "policy_reference": meta.get("reference", ""),
                    "acceptable_threshold": meta.get("acceptable_threshold", ""),
                    "risk_guidance": meta.get("risk_guidance", ""),
                    "similarity_score": top_match["score"]
                }
            else:
                match_record = {
                    "clause_id": clause["clause_id"],
                    "matched_policy_id": "POL-GENERIC",
                    "policy_title": "Enterprise General Practice",
                    "policy_reference": "Corporate Standards Manual Sec 1",
                    "acceptable_threshold": "Standard business diligence applies.",
                    "risk_guidance": "Review manually.",
                    "similarity_score": 0.50
                }

            policy_matches.append(match_record)
            completion_tokens += 35

        span = telemetry_engine.end_span(
            span_ctx,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            status="SUCCESS",
            metadata={"policies_mapped": len(policy_matches)}
        )

        state["policy_matches"] = policy_matches
        state["current_agent"] = "PolicyRAGAgent"
        state["step_history"].append({
            "agent": "PolicyRAGAgent",
            "summary": f"Cross-referenced {len(policy_matches)} requirements against enterprise knowledge base (ISO-27001, SOC-2, SLA schedules).",
            "latency_ms": span.duration_ms,
            "status": "COMPLETED"
        })

        return state
