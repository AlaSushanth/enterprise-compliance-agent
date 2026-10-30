import React from 'react';
import { GlobalTelemetryMetrics } from '../types';

interface TelemetryStatsProps {
  metrics: GlobalTelemetryMetrics | null;
}

export const TelemetryStats: React.FC<TelemetryStatsProps> = ({ metrics }) => {
  if (!metrics) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl text-xs space-y-2 font-mono">
      <h3 className="font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center">
        <span className="mr-2">📈</span> LLMOps Governance
      </h3>
      <div className="flex justify-between text-slate-400">
        <span>Audit Compliance Rate:</span>
        <span className="text-emerald-400 font-bold">{metrics.guardrail_compliance_rate}</span>
      </div>
      <div className="flex justify-between text-slate-400">
        <span>Total Tokens Consumed:</span>
        <span className="text-slate-200">{metrics.total_tokens_consumed.toLocaleString()}</span>
      </div>
      <div className="flex justify-between text-slate-400">
        <span>Average Agent Latency:</span>
        <span className="text-slate-200">{metrics.avg_latency_ms} ms</span>
      </div>
    </div>
  );
};
