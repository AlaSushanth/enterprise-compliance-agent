import React from 'react';

interface StepTrace {
  agent: string;
  summary: string;
  latency_ms: number;
  status: string;
}

interface AgentGraphVisualizerProps {
  documentId: string | null;
  isRunning: boolean;
  currentAgent: string;
  stepHistory: StepTrace[];
  onRunPipeline: () => void;
}

export const AgentGraphVisualizer: React.FC<AgentGraphVisualizerProps> = ({
  documentId,
  isRunning,
  stepHistory,
  onRunPipeline,
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center">
        <span className="mr-2">⚙️</span> 2. Orchestration Pod
      </h2>

      <button
        onClick={onRunPipeline}
        disabled={!documentId || isRunning}
        className={`w-full py-3 px-4 rounded-xl font-bold text-sm flex items-center justify-center space-x-2 transition shadow-lg ${
          !documentId || isRunning
            ? "bg-slate-800 text-slate-500 cursor-not-allowed"
            : "bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30 active:scale-[0.98]"
        }`}
      >
        {isRunning ? (
          <>
            <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            <span>Agents Collaborating...</span>
          </>
        ) : (
          <>
            <span>🚀</span>
            <span>Run Multi-Agent Audit Pod</span>
          </>
        )}
      </button>

      <div className="mt-4 space-y-2">
        <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">
          Agent Execution Traces:
        </span>
        <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
          {stepHistory.length === 0 ? (
            <div className="text-xs text-slate-600 italic py-2">No agents dispatched yet.</div>
          ) : (
            stepHistory.map((step, idx) => (
              <div key={idx} className="bg-slate-950/60 border border-slate-800 rounded-lg p-2.5 text-xs">
                <div className="flex justify-between items-center mb-1">
                  <span className="font-semibold text-indigo-400 font-mono flex items-center">
                    <span className="h-1.5 w-1.5 rounded-full bg-indigo-400 mr-1.5"></span>
                    {step.agent}
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono">{step.latency_ms}ms</span>
                </div>
                <p className="text-slate-300 text-[11px] leading-relaxed">{step.summary}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
