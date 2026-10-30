from backend.app.core.guardrails import GuardrailVerifier

def test_guardrail_risk_policy_critical():
    critical_text = "Vendor shall agree to unlimited liability and $1,000,000 liquidated damages."
    severity, auto_flag = GuardrailVerifier.audit_risk_policy(critical_text)
    assert severity == "CRITICAL"
    assert auto_flag is True

def test_guardrail_risk_policy_high():
    high_text = "System must achieve 99.98% uptime availability."
    severity, auto_flag = GuardrailVerifier.audit_risk_policy(high_text)
    assert severity == "HIGH"
    assert auto_flag is True

def test_guardrail_grounding():
    chunks = [
        {"page": 1, "text": "All non-public client financial records must be protected using TLS 1.3 encryption protocols."},
        {"page": 2, "text": "Disaster recovery RTO must be under 1 hour."}
    ]
    query = "All financial records protected with TLS 1.3 protocols"
    is_grounded, conf, page = GuardrailVerifier.verify_grounding(query, chunks)
    assert is_grounded is True
    assert page == 1
    assert conf >= 0.5
