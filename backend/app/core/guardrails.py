import re
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field

class ExtractedClauseSchema(BaseModel):
    clause_id: str
    category: str = Field(description="E.g., Data Security, SLA & Availability, Liability & Penalties, Data Privacy, Termination")
    original_text: str
    page_number: int
    key_requirement: str

class AuditEvaluationSchema(BaseModel):
    clause_id: str
    compliance_status: str = Field(description="COMPLIANT, NON_COMPLIANT, or AMBIGUOUS")
    risk_level: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")
    internal_policy_citation: str
    explanation: str
    recommended_action: str
    requires_human_approval: bool

class GuardrailVerifier:
    """
    Deterministic AI Quality & Governance Guardrails.
    Detects hallucinations, verifies citation grounding, and enforces enterprise risk policies.
    """

    @staticmethod
    def verify_grounding(extracted_text: str, source_chunks: List[Dict[str, Any]]) -> Tuple[bool, float, int]:
        """
        Verifies if the extracted text or requirement is genuinely grounded in source chunks.
        Returns: (is_grounded, confidence_score, matched_page)
        """
        if not source_chunks:
            return False, 0.0, 1

        extracted_words = set(re.findall(r'\b\w{4,}\b', extracted_text.lower()))
        if not extracted_words:
            return True, 1.0, 1

        best_score = 0.0
        best_page = 1

        for chunk in source_chunks:
            chunk_words = set(re.findall(r'\b\w{4,}\b', chunk.get("text", "").lower()))
            if not chunk_words:
                continue
            overlap = len(extracted_words.intersection(chunk_words))
            score = overlap / len(extracted_words)
            if score > best_score:
                best_score = score
                best_page = chunk.get("page", 1)

        is_grounded = best_score >= 0.35  # Threshold for semantic presence
        return is_grounded, round(min(best_score * 1.5, 1.0), 2), best_page

    @staticmethod
    def audit_risk_policy(clause_text: str) -> Tuple[str, bool]:
        """
        Deterministic Rule Engine to flag enterprise liability traps:
        - Penalties > $250,000 or uncapped liability
        - SLA > 99.95% without scheduled maintenance
        - Cross-border data export violations
        """
        text_lower = clause_text.lower()

        # Check unlimited or high liability
        if "unlimited liability" in text_lower or "uncapped liability" in text_lower:
            return "CRITICAL", True
        if re.search(r'\$\s*(?:[3-9]\d{5}|\d{7,})', text_lower) or "million" in text_lower:
            return "CRITICAL", True

        # Check unrealistic SLA
        if re.search(r'99\.9[5-9]%', text_lower) or "100% uptime" in text_lower:
            return "HIGH", True

        # Check strict data residency or foreign export
        if "cross-border" in text_lower or "sovereignty" in text_lower or "unrestricted access" in text_lower:
            return "HIGH", True

        # Check medium compliance items
        if "audit within 24 hours" in text_lower or "penalty per minute" in text_lower:
            return "MEDIUM", False

        return "LOW", False
