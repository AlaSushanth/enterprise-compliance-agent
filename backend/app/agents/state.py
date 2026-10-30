from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """
    LangGraph Workflow State Definition for Enterprise Compliance Pod.
    Tracks document ingestion, extracted clauses, RAG findings, risk alerts, and human decisions.
    """
    trace_id: str
    document_id: str
    document_name: str
    total_pages: int
    raw_chunks: List[Dict[str, Any]]
    
    # State accumulated across agents
    extracted_clauses: List[Dict[str, Any]]
    policy_matches: List[Dict[str, Any]]
    risk_evaluations: List[Dict[str, Any]]
    
    # Human-in-the-Loop checkpoint
    requires_human_review: bool
    pending_decisions: List[Dict[str, Any]]
    human_decisions: Dict[str, Any]  # Key: clause_id -> {decision: 'APPROVE'|'OVERRIDE'|'REJECT', note: ''}
    
    # Final Output & LLMOps
    final_report: Dict[str, Any]
    current_agent: str
    step_history: List[Dict[str, Any]]
