import os
import uuid
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from backend.app.config import settings
from backend.app.rag.document_parser import DocumentParser
from backend.app.rag.vector_store import vector_store
from backend.app.agents.graph import ComplianceAgentPodGraph
from backend.app.agents.state import AgentState
from backend.app.core.telemetry import telemetry_engine

router = APIRouter()

# Global session cache
SESSION_STATES: Dict[str, AgentState] = {}

class TextIngestPayload(BaseModel):
    filename: Optional[str] = "vendor_contract.txt"
    content: str

class HumanDecisionPayload(BaseModel):
    document_id: str
    decisions: Dict[str, Dict[str, Any]]  # clause_id -> {decision: str, note: str}

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "engine": "LangGraph + Hybrid RAG"
    }

@router.get("/sample")
def get_sample():
    sample_path = os.path.join(settings.SAMPLE_DIR, "sample_vendor_rfp.txt")
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail="Sample RFP document not found")
    
    with open(sample_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return {
        "filename": "sample_vendor_rfp.txt",
        "content": content,
        "total_characters": len(content)
    }

@router.post("/ingest-text")
def ingest_text_document(payload: TextIngestPayload):
    """
    Direct JSON ingestion endpoint - reliable and fast without multipart overhead.
    """
    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    saved_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_{payload.filename}")

    with open(saved_path, "w", encoding="utf-8") as f:
        f.write(payload.content)

    parsed_chunks = DocumentParser.parse_file(saved_path)
    if not parsed_chunks:
        raise HTTPException(status_code=400, detail="Could not parse text chunks.")

    # Index chunks into Hybrid Vector Store
    for chunk in parsed_chunks:
        vector_store.add_document(
            doc_id=f"{doc_id}_{chunk['chunk_id']}",
            text=chunk["text"],
            metadata={
                "type": "DOCUMENT",
                "doc_id": doc_id,
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"]
            }
        )

    total_pages = max(c["page"] for c in parsed_chunks)

    state = ComplianceAgentPodGraph.initialize_state(
        document_id=doc_id,
        document_name=payload.filename or "contract.txt",
        total_pages=total_pages,
        raw_chunks=parsed_chunks
    )
    SESSION_STATES[doc_id] = state

    return {
        "document_id": doc_id,
        "filename": payload.filename,
        "total_pages": total_pages,
        "chunks_indexed": len(parsed_chunks),
        "trace_id": state["trace_id"]
    }

@router.post("/upload")
async def upload_file(
    file: Optional[UploadFile] = File(None),
    text_content: Optional[str] = Form(None),
    filename: Optional[str] = Form("uploaded_rfp.txt")
):
    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    saved_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_{filename}")

    if file:
        file_bytes = await file.read()
        with open(saved_path, "wb") as f:
            f.write(file_bytes)
        parsed_chunks = DocumentParser.parse_file(saved_path)
    elif text_content:
        with open(saved_path, "w", encoding="utf-8") as f:
            f.write(text_content)
        parsed_chunks = DocumentParser.parse_file(saved_path)
    else:
        raise HTTPException(status_code=400, detail="Provide either a file or text content.")

    if not parsed_chunks:
        raise HTTPException(status_code=400, detail="Could not extract text chunks.")

    for chunk in parsed_chunks:
        vector_store.add_document(
            doc_id=f"{doc_id}_{chunk['chunk_id']}",
            text=chunk["text"],
            metadata={
                "type": "DOCUMENT",
                "doc_id": doc_id,
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"]
            }
        )

    total_pages = max(c["page"] for c in parsed_chunks)

    state = ComplianceAgentPodGraph.initialize_state(
        document_id=doc_id,
        document_name=filename or "document.txt",
        total_pages=total_pages,
        raw_chunks=parsed_chunks
    )
    SESSION_STATES[doc_id] = state

    return {
        "document_id": doc_id,
        "filename": filename,
        "total_pages": total_pages,
        "chunks_indexed": len(parsed_chunks),
        "trace_id": state["trace_id"]
    }

@router.post("/run-audit/{doc_id}")
def run_audit(doc_id: str):
    if doc_id not in SESSION_STATES:
        raise HTTPException(status_code=404, detail="Document not found.")

    state = SESSION_STATES[doc_id]
    updated_state = ComplianceAgentPodGraph.run_pipeline(state)
    SESSION_STATES[doc_id] = updated_state

    trace_info = telemetry_engine.get_trace_summary(updated_state["trace_id"])

    return {
        "document_id": doc_id,
        "trace_id": updated_state["trace_id"],
        "current_agent": updated_state["current_agent"],
        "requires_human_review": updated_state["requires_human_review"],
        "pending_decisions": updated_state.get("pending_decisions", []),
        "extracted_clauses_count": len(updated_state.get("extracted_clauses", [])),
        "step_history": updated_state.get("step_history", []),
        "final_report": updated_state.get("final_report", None),
        "telemetry": trace_info
    }

@router.post("/human-decision")
def record_human_decision(payload: HumanDecisionPayload):
    doc_id = payload.document_id
    if doc_id not in SESSION_STATES:
        raise HTTPException(status_code=404, detail="Document not found.")

    state = SESSION_STATES[doc_id]
    updated_state = ComplianceAgentPodGraph.resume_with_human_decisions(state, payload.decisions)
    SESSION_STATES[doc_id] = updated_state

    trace_info = telemetry_engine.get_trace_summary(updated_state["trace_id"])

    return {
        "document_id": doc_id,
        "current_agent": updated_state["current_agent"],
        "requires_human_review": False,
        "final_report": updated_state.get("final_report", {}),
        "step_history": updated_state.get("step_history", []),
        "telemetry": trace_info
    }

@router.get("/telemetry")
def get_telemetry():
    return telemetry_engine.get_global_metrics()

@router.get("/export-report/{doc_id}")
def export_report(doc_id: str):
    if doc_id not in SESSION_STATES or not SESSION_STATES[doc_id].get("final_report"):
        raise HTTPException(status_code=404, detail="Report not ready.")

    report = SESSION_STATES[doc_id]["final_report"]
    metrics = report.get("metrics", {})

    lines = [
        "# ENTERPRISE COMPLIANCE & RFP AUDIT REPORT",
        f"**Target Document:** {report.get('document_name')}",
        f"**Audit Generated:** {report.get('audit_timestamp')}",
        f"**Overall Compliance Readiness:** {report.get('overall_readiness_score')}",
        f"**Final Risk Verdict:** {report.get('risk_verdict')}",
        "",
        "## Summary Metrics",
        f"- Analyzed Requirements: {metrics.get('total_requirements_analyzed')}",
        f"- Fully Compliant: {metrics.get('compliant')}",
        f"- Non-Compliant / Flagged: {metrics.get('non_compliant')}",
        f"- Critical Liabilities: {metrics.get('critical_risks')}",
        f"- High Risks: {metrics.get('high_risks')}",
        "",
        "## Itemized Risk & Policy Evaluation",
        "| ID | Page | Category | Risk Level | Status | Policy Baseline | Recommended Action |",
        "|---|---|---|---|---|---|---|"
    ]

    for item in report.get("itemized_clauses", []):
        lines.append(
            f"| {item['clause_id']} | Page {item['page_number']} | {item['category']} | {item['risk_level']} | {item['compliance_status']} | {item['policy_reference']} | {item['recommended_action']} |"
        )

    return {"markdown_report": "\n".join(lines)}
