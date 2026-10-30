import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class TelemetrySpan(BaseModel):
    span_id: str
    trace_id: str
    agent_name: str
    action: str
    duration_ms: float
    tokens_prompt: int
    tokens_completion: int
    tokens_total: int
    cost_usd: float
    status: str
    metadata: Dict[str, Any] = {}
    timestamp: float

class LLMOpsTelemetry:
    """
    Enterprise Observability & Telemetry Engine (OpenTelemetry aligned).
    Tracks real-time agent execution latency, token economics, and guardrail metrics.
    """
    def __init__(self):
        self.spans: List[TelemetrySpan] = []
        # Pricing reference: $0.150 / 1M input tokens, $0.600 / 1M output tokens (standard GPT-4o-mini tier)
        self.input_cost_per_token = 0.00000015
        self.output_cost_per_token = 0.00000060

    def start_span(self, trace_id: str, agent_name: str, action: str):
        return {
            "span_id": str(uuid.uuid4())[:8],
            "trace_id": trace_id,
            "agent_name": agent_name,
            "action": action,
            "start_time": time.time(),
        }

    def end_span(
        self,
        span_ctx: Dict[str, Any],
        prompt_tokens: int,
        completion_tokens: int,
        status: str = "SUCCESS",
        metadata: Optional[Dict[str, Any]] = None
    ) -> TelemetrySpan:
        duration = round((time.time() - span_ctx["start_time"]) * 1000, 2)
        total_tokens = prompt_tokens + completion_tokens
        cost = round((prompt_tokens * self.input_cost_per_token) + (completion_tokens * self.output_cost_per_token), 6)
        
        span = TelemetrySpan(
            span_id=span_ctx["span_id"],
            trace_id=span_ctx["trace_id"],
            agent_name=span_ctx["agent_name"],
            action=span_ctx["action"],
            duration_ms=duration,
            tokens_prompt=prompt_tokens,
            tokens_completion=completion_tokens,
            tokens_total=total_tokens,
            cost_usd=cost,
            status=status,
            metadata=metadata or {},
            timestamp=time.time()
        )
        self.spans.append(span)
        return span

    def get_trace_summary(self, trace_id: str) -> Dict[str, Any]:
        trace_spans = [s for s in self.spans if s.trace_id == trace_id]
        total_duration = sum(s.duration_ms for s in trace_spans)
        total_tokens = sum(s.tokens_total for s in trace_spans)
        total_cost = sum(s.cost_usd for s in trace_spans)
        
        return {
            "trace_id": trace_id,
            "span_count": len(trace_spans),
            "total_latency_ms": round(total_duration, 2),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 6),
            "spans": [s.model_dump() for s in trace_spans]
        }

    def get_global_metrics(self) -> Dict[str, Any]:
        if not self.spans:
            return {
                "total_queries_processed": 0,
                "avg_latency_ms": 0.0,
                "total_tokens_consumed": 0,
                "total_cost_usd": 0.0,
                "guardrail_compliance_rate": "100.0%",
            }
        
        avg_latency = sum(s.duration_ms for s in self.spans) / len(self.spans)
        total_tokens = sum(s.tokens_total for s in self.spans)
        total_cost = sum(s.cost_usd for s in self.spans)
        success_count = sum(1 for s in self.spans if s.status in ("SUCCESS", "HUMAN_APPROVED"))
        compliance_rate = round((success_count / len(self.spans)) * 100, 1)

        return {
            "total_queries_processed": len(self.spans),
            "avg_latency_ms": round(avg_latency, 2),
            "total_tokens_consumed": total_tokens,
            "total_cost_usd": round(total_cost, 5),
            "guardrail_compliance_rate": f"{compliance_rate}%",
        }

telemetry_engine = LLMOpsTelemetry()
