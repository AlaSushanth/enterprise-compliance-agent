from typing import List, Dict, Any

ENTERPRISE_COMPLIANCE_POLICIES: List[Dict[str, Any]] = [
    {
        "policy_id": "POL-SEC-01",
        "category": "Data Security & Encryption",
        "title": "Encryption At Rest and In Transit",
        "clause_reference": "ISO-27001 Control A.10.1 / NIST SP 800-52",
        "standard_text": (
            "All customer data must be encrypted in transit using TLS 1.3 (minimum TLS 1.2) "
            "and at rest using FIPS 140-3 validated AES-256 bit encryption keys managed via enterprise KMS. "
            "Deprecate all DES, 3DES, and RC4 ciphers."
        ),
        "acceptable_threshold": "AES-256 and TLS 1.3 mandatory; customer-managed keys (CMK) supported.",
        "risk_guidance": "Flag non-compliance if client requests unencrypted channels or proprietary weak algorithms."
    },
    {
        "policy_id": "POL-SLA-02",
        "category": "SLA & Availability",
        "title": "Service Level Agreement and Uptime Guarantee",
        "clause_reference": "Standard Master Service Agreement (MSA) Schedule 4",
        "standard_text": (
            "Standard production cloud availability commitment is 99.9% uptime per calendar month, "
            "excluding scheduled preventative maintenance windows (Sunday 02:00-06:00 UTC). "
            "Service credit penalties are strictly capped at 15% of the monthly recurring subscription fee."
        ),
        "acceptable_threshold": "Maximum commitment 99.95%. Penalties capped at 20% monthly fee. NEVER accept uncapped fines.",
        "risk_guidance": "CRITICAL RISK if client demands 99.99%+ uptime or liquidated damages exceeding monthly billing."
    },
    {
        "policy_id": "POL-LIA-03",
        "category": "Liability & Penalties",
        "title": "Limitation of Liability and Indemnification Caps",
        "clause_reference": "Enterprise Legal Risk Framework Section 12",
        "standard_text": (
            "Neither party shall be liable for indirect, incidental, punitive, or consequential damages. "
            "Total aggregate liability arising out of or related to this agreement shall not exceed "
            "the fees actually paid by customer in the preceding twelve (12) months, or $250,000 USD, whichever is lower."
        ),
        "acceptable_threshold": "Liability must be capped at 1x to 2x 12-month trailing contract value. Never agree to unlimited liability.",
        "risk_guidance": "CRITICAL RISK if client stipulates unlimited liability or individual employee liability."
    },
    {
        "policy_id": "POL-PRV-04",
        "category": "Data Privacy & Residency",
        "title": "Data Sovereignty and GDPR/DPDP Cross-Border Transfer",
        "clause_reference": "GDPR Chapter V / India DPDP Act 2023 / EU Standard Contractual Clauses (SCC)",
        "standard_text": (
            "Customer personal data must reside in geographic regions designated by the customer (EU-Frankfurt, US-East, or India-Mumbai). "
            "Cross-border transfer requires explicit data processing agreements (DPA) and Standard Contractual Clauses. "
            "Data subjects have full right to erasure (Right to be Forgotten) within 30 days."
        ),
        "acceptable_threshold": "Regional data isolation supported on AWS, Azure, and GCP multi-region instances.",
        "risk_guidance": "HIGH RISK if client requires unrestricted ad-hoc foreign data export without signed DPA."
    },
    {
        "policy_id": "POL-BCP-05",
        "category": "Business Continuity & Disaster Recovery",
        "title": "Disaster Recovery RTO and RPO Guarantees",
        "clause_reference": "SOC-2 Trust Services Criteria Availability (A1.2)",
        "standard_text": (
            "Recovery Point Objective (RPO) is guaranteed at <= 15 minutes. "
            "Recovery Time Objective (RTO) is guaranteed at <= 4 hours for Tier-1 mission critical services. "
            "Automated geo-replicated snapshots taken hourly."
        ),
        "acceptable_threshold": "RTO <= 4 hours, RPO <= 1 hour.",
        "risk_guidance": "HIGH RISK if client mandates zero RPO (0 seconds) without dedicated multi-region active-active cluster."
    }
]
