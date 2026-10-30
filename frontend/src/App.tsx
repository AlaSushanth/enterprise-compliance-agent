import React, { useState, useEffect } from "react";

export interface AgentSpan {
  span_id: string;
  agent_name: string;
  action: string;
  duration_ms: number;
  tokens_total: number;
  cost_usd: number;
  status: string;
}

export interface ClauseFinding {
  clause_id: string;
  category: string;
  original_text: string;
  page_number: number;
  compliance_status: string;
  risk_level: string;
  policy_reference: string;
  explanation: string;
  recommended_action: string;
}

export const App: React.FC = () => {
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [currentAgent, setCurrentAgent] = useState<string>("Supervisor Ready");
  const [findings, setFindings] = useState<ClauseFinding[]>([]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <header className="border-b border-slate-800 bg-slate-900 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">🛡️</span>
          <div>
            <h1 className="text-lg font-bold text-white">AEGIS-OPERATOR</h1>
            <p className="text-xs text-slate-400">Enterprise Multi-Agent Compliance & RFP Auditor</p>
          </div>
        </div>
      </header>
      <main className="p-6 max-w-7xl mx-auto w-full">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold uppercase text-indigo-400">LangGraph Agent Pod Workspace</h2>
          <p className="text-xs text-slate-400 mt-1">Autonomous orchestration with RAG, guardrails, and telemetry.</p>
        </div>
      </main>
    </div>
  );
};

export default App;
