import uuid
from typing import Dict, Any, Optional
from backend.app.agents.state import AgentState
from backend.app.agents.extractor_agent import ExtractorAgent
from backend.app.agents.rag_agent import PolicyRAGAgent
from backend.app.agents.risk_agent import RiskAuditorAgent
from backend.app.agents.synthesizer_agent import SynthesizerAgent

class ComplianceAgentPodGraph:
    """
    LangGraph-Aligned Multi-Agent State Machine Workflow.
    Orchestrates Extractor -> RAG -> RiskAuditor -> Human Review Branch -> Synthesizer.
    """

    @classmethod
    def initialize_state(
        cls,
        document_id: str,
        document_name: str,
        total_pages: int,
        raw_chunks: list
    ) -> AgentState:
        return AgentState(
            trace_id=f"trace-{uuid.uuid4().hex[:10]}",
            document_id=document_id,
            document_name=document_name,
            total_pages=total_pages,
            raw_chunks=raw_chunks,
            extracted_clauses=[],
            policy_matches=[],
            risk_evaluations=[],
            requires_human_review=False,
            pending_decisions=[],
            human_decisions={},
            final_report={},
            current_agent="Supervisor",
            step_history=[]
        )

    @classmethod
    def run_pipeline(cls, state: AgentState) -> AgentState:
        """
        Executes the Multi-Agent graph synchronously until completion
        or until paused by a Human-in-the-Loop review requirement.
        """
        # Node 1: Extractor Agent
        state = ExtractorAgent.execute(state)

        # Node 2: Policy RAG Agent
        state = PolicyRAGAgent.execute(state)

        # Node 3: Risk Auditor Agent
        state = RiskAuditorAgent.execute(state)

        # Conditional Edge Check: Human-in-the-Loop
        if state["requires_human_review"] and not state["human_decisions"]:
            # Pause workflow for human intervention
            state["current_agent"] = "HumanApprovalGate"
            return state

        # Node 4: Synthesis & Final Executive Report
        state = SynthesizerAgent.execute(state)
        state["current_agent"] = "WorkflowCompleted"
        return state

    @classmethod
    def resume_with_human_decisions(cls, state: AgentState, decisions: Dict[str, Any]) -> AgentState:
        """
        Resumes the workflow graph after the human operator provides approvals/overrides.
        """
        state["human_decisions"] = decisions
        state["requires_human_review"] = False
        
        # Proceed directly to Synthesizer node
        state = SynthesizerAgent.execute(state)
        state["current_agent"] = "WorkflowCompleted"
        return state
