import React from 'react';
import { PendingDecision } from '../types';

interface HumanReviewModalProps {
  pendingDecisions: PendingDecision[];
  humanChoices: Record<string, { decision: string; note: string }>;
  isRunning: boolean;
  onSelectChoice: (clauseId: string, choice: string) => void;
  onSubmit: () => void;
}

export const HumanReviewModal: React.FC<HumanReviewModalProps> = ({
  pendingDecisions,
  humanChoices,
  isRunning,
  onSelectChoice,
  onSubmit,
}) => {
  if (pendingDecisions.length === 0) return null;

  const allSelected = Object.keys(humanChoices).length >= pendingDecisions.length;

  return (
    <div className="bg-gradient-to-br from-amber-950/40 via-slate-900 to-slate-900 border-2 border-amber-500/50 rounded-2xl p-6 shadow-2xl">
      <div className="flex items-center space-x-3 mb-4">
        <div className="h-9 w-9 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 text-lg">
          ⚠️
        </div>
        <div>
          <h3 className="text-base font-bold text-amber-300">Human-in-the-Loop Approval Gate Triggered</h3>
          <p className="text-xs text-amber-200/70">
            The Risk Auditor Agent detected high-liability enterprise covenants requiring authorized review before signing.
          </p>
        </div>
      </div>

      <div className="space-y-4 my-4">
        {pendingDecisions.map((dec) => (
          <div key={dec.clause_id} className="bg-slate-950/80 border border-amber-500/30 rounded-xl p-4 text-xs space-y-2">
            <div className="flex justify-between items-center">
              <span className="font-mono font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                {dec.clause_id} • Page {dec.page_number}
              </span>
              <span className="font-mono text-rose-400 font-semibold px-2 py-0.5 rounded bg-rose-500/10 border border-rose-500/20">
                {dec.risk_level} RISK
              </span>
            </div>

            <p className="text-slate-200 font-mono text-[11px] bg-slate-900/90 p-2.5 rounded border border-slate-800">
              "{dec.original_text}"
            </p>

            <div className="text-slate-400 text-[11px]">
              <strong className="text-amber-300">Auditor Finding:</strong> {dec.explanation}
            </div>
            <div className="text-slate-400 text-[11px]">
              <strong className="text-emerald-400">Recommended Resolution:</strong> {dec.recommended_action}
            </div>

            <div className="pt-2 flex flex-wrap gap-2">
              <button
                onClick={() => onSelectChoice(dec.clause_id, "ACCEPT_RECOMMENDATION")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                  humanChoices[dec.clause_id]?.decision === "ACCEPT_RECOMMENDATION"
                    ? "bg-emerald-600 text-white ring-2 ring-emerald-400"
                    : "bg-slate-800 text-emerald-300 hover:bg-slate-700 border border-emerald-500/30"
                }`}
              >
                ✓ Counter-Offer with Liability Cap
              </button>
              <button
                onClick={() => onSelectChoice(dec.clause_id, "OVERRIDE_AND_ACCEPT_RISK")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                  humanChoices[dec.clause_id]?.decision === "OVERRIDE_AND_ACCEPT_RISK"
                    ? "bg-amber-600 text-white ring-2 ring-amber-400"
                    : "bg-slate-800 text-amber-300 hover:bg-slate-700 border border-amber-500/30"
                }`}
              >
                ⚠️ Accept Risk (Executive Override)
              </button>
              <button
                onClick={() => onSelectChoice(dec.clause_id, "REJECT_CLAUSE_ENTIRELY")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                  humanChoices[dec.clause_id]?.decision === "REJECT_CLAUSE_ENTIRELY"
                    ? "bg-rose-600 text-white ring-2 ring-rose-400"
                    : "bg-slate-800 text-rose-300 hover:bg-slate-700 border border-rose-500/30"
                }`}
              >
                ✕ Reject Clause Entirely
              </button>
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={onSubmit}
        disabled={!allSelected || isRunning}
        className={`w-full py-2.5 px-4 rounded-xl font-bold text-xs uppercase tracking-wider transition ${
          !allSelected || isRunning
            ? "bg-slate-800 text-slate-500 cursor-not-allowed"
            : "bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-600/30"
        }`}
      >
        Confirm Decisions & Synthesize Executive Report
      </button>
    </div>
  );
};
