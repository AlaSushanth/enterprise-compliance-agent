export interface TelemetrySpan {
  span_id: string;
  trace_id: string;
  agent_name: string;
  action: string;
  duration_ms: number;
  tokens_prompt: number;
  tokens_completion: number;
  tokens_total: number;
  cost_usd: number;
  status: string;
  timestamp: number;
}

export interface ExtractedClause {
  clause_id: string;
  category: string;
  original_text: string;
  page_number: number;
  confidence_score: number;
  is_grounded: boolean;
}

export interface RiskEvaluation {
  clause_id: string;
  category: string;
  original_text: string;
  page_number: number;
  compliance_status: "COMPLIANT" | "NON_COMPLIANT" | "AMBIGUOUS" | "REJECTED_BY_LEGAL";
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" | "ACCEPTED_RISK";
  policy_reference: string;
  explanation: string;
  recommended_action: string;
  requires_human_approval: boolean;
  human_decision?: string;
  human_note?: string;
}

export interface PendingDecision {
  clause_id: string;
  risk_level: string;
  page_number: number;
  original_text: string;
  explanation: string;
  recommended_action: string;
  options: string[];
}

export interface FinalAuditReport {
  document_name: string;
  audit_timestamp: string;
  overall_readiness_score: string;
  risk_verdict: string;
  metrics: {
    total_requirements_analyzed: number;
    compliant: number;
    non_compliant: number;
    ambiguous: number;
    critical_risks: number;
    high_risks: number;
  };
  key_takeaways: string[];
  itemized_clauses: RiskEvaluation[];
}

export interface TraceSummary {
  trace_id: string;
  span_count: number;
  total_latency_ms: number;
  total_tokens: number;
  total_cost_usd: number;
  spans: TelemetrySpan[];
}

export interface GlobalTelemetryMetrics {
  total_queries_processed: number;
  avg_latency_ms: number;
  total_tokens_consumed: number;
  total_cost_usd: number;
  guardrail_compliance_rate: string;
}
