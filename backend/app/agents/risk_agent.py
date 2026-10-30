import re
from typing import Dict, Any, List
from backend.app.core.guardrails import GuardrailVerifier
from backend.app.core.telemetry import telemetry_engine

class RiskAuditorAgent:
    """
    Agent 3: Risk Auditing & Human-in-the-Loop Escalation Agent.
    Evaluates extracted clauses against retrieved policies, detects liabilities,
    assigns risk severity (LOW, MEDIUM, HIGH, CRITICAL), and triggers human review checkpoints.
    """

    @classmethod
    def execute(cls, state: Dict[str, Any]) -> Dict[str, Any]:
        trace_id = state.get("trace_id", "trace-default")
        span_ctx = telemetry_engine.start_span(trace_id, "RiskAuditorAgent", "audit_risks_and_guardrails")

        extracted = state.get("extracted_clauses", [])
        policy_matches_map = {p["clause_id"]: p for p in state.get("policy_matches", [])}
        
        risk_evaluations = []
        pending_decisions = []
        requires_human = False

        prompt_tokens = 0
        completion_tokens = 0

        for item in extracted:
            c_id = item["clause_id"]
            text = item["original_text"]
            policy = policy_matches_map.get(c_id, {})
            prompt_tokens += len(text.split())

            # Evaluate with Guardrail Policy Rules
            severity, auto_flag = GuardrailVerifier.audit_risk_policy(text)

            # Analyze compliance logic
            if severity == "CRITICAL":
                status = "NON_COMPLIANT"
                rec_action = "Reject clause or require mandatory liability cap (max 1x trailing 12mo contract value)."
                explanation = "Uncapped liability or severe financial penalty exceeds enterprise threshold ($250,000 USD)."
                requires_approval = True
            elif severity == "HIGH":
                status = "NON_COMPLIANT"
                rec_action = "Negotiate clause downwards to standard 99.9% uptime or regional data residency."
                explanation = "Requires SLA or residency parameters beyond standard certified guarantees."
                requires_approval = True
            elif severity == "MEDIUM":
                status = "AMBIGUOUS"
                rec_action = "Clarify notice window and audit scope in Appendix B."
                explanation = "Operational timeline is tighter than typical service cadence."
                requires_approval = False
            else:
                status = "COMPLIANT"
                rec_action = "Accept standard clause."
                explanation = f"Fully aligned with {policy.get('policy_title', 'Enterprise Standard')}."
                requires_approval = False

            eval_record = {
                "clause_id": c_id,
                "category": item["category"],
                "original_text": text,
                "page_number": item["page_number"],
                "compliance_status": status,
                "risk_level": severity,
                "policy_reference": policy.get("policy_reference", "General Standard"),
                "explanation": explanation,
                "recommended_action": rec_action,
                "requires_human_approval": requires_approval
            }
            risk_evaluations.append(eval_record)
            completion_tokens += 45

            if requires_approval:
                requires_human = True
                pending_decisions.append({
                    "clause_id": c_id,
                    "risk_level": severity,
                    "page_number": item["page_number"],
                    "original_text": text,
                    "explanation": explanation,
                    "recommended_action": rec_action,
                    "options": [
                        "ACCEPT_RECOMMENDATION (Counter-offer with Cap)",
                        "OVERRIDE_AND_ACCEPT_RISK (Executive Exception)",
                        "REJECT_CLAUSE_ENTIRELY"
                    ]
                })

        state["risk_evaluations"] = risk_evaluations
        state["requires_human_review"] = requires_human
        state["pending_decisions"] = pending_decisions

        span = telemetry_engine.end_span(
            span_ctx,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            status="HUMAN_REVIEW_REQUIRED" if requires_human else "SUCCESS",
            metadata={"risks_flagged": len(pending_decisions), "requires_human": requires_human}
        )

        state["current_agent"] = "RiskAuditorAgent"
        state["step_history"].append({
            "agent": "RiskAuditorAgent",
            "summary": f"Audit complete: {len(pending_decisions)} high-risk covenants flagged. Human-in-the-Loop check {'TRIGGERED' if requires_human else 'SKIPPED'}.",
            "latency_ms": span.duration_ms,
            "status": "PAUSED_FOR_REVIEW" if requires_human else "COMPLETED"
        })

        return state
