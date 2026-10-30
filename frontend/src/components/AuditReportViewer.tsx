import React from 'react';
import { FinalAuditReport } from '../types';

interface AuditReportViewerProps {
  documentId: string | null;
  report: FinalAuditReport | null;
}

export const AuditReportViewer: React.FC<AuditReportViewerProps> = ({
  documentId,
  report,
}) => {
  if (!report) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center shadow-xl flex flex-col items-center justify-center min-h-[400px]">
        <div className="h-16 w-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-3xl mb-4 text-indigo-400">
          📂
        </div>
        <h3 className="text-base font-bold text-white">Awaiting Document Audit</h3>
        <p className="text-xs text-slate-400 max-w-sm mt-2 leading-relaxed">
          Upload an enterprise vendor RFP or click <strong className="text-indigo-300">"Load Tier-1 Bank RFP Sample"</strong> to trigger the multi-agent pod and inspect live risk auditing.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-6">
      <div className="flex flex-wrap justify-between items-start gap-4 pb-4 border-b border-slate-800">
        <div>
          <span className="text-xs font-mono text-indigo-400 uppercase tracking-widest">
            Executive Audit Brief
          </span>
          <h2 className="text-xl font-bold text-white mt-1">{report.document_name}</h2>
          <div className="flex items-center space-x-2 mt-2">
            <span className="text-xs px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-500/30">
              Readiness: {report.overall_readiness_score}
            </span>
            <span className="text-xs px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 font-mono border border-slate-700">
              Verdict: {report.risk_verdict}
            </span>
          </div>
        </div>

        {documentId && (
          <a
            href={`/api/export-report/${documentId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold py-2 px-4 rounded-xl transition flex items-center space-x-2 shadow-md shadow-indigo-600/20"
          >
            <span>📥</span>
            <span>Export Audit Markdown</span>
          </a>
        )}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-center">
          <div className="text-2xl font-bold text-white">{report.metrics.total_requirements_analyzed}</div>
          <div className="text-[11px] text-slate-400 uppercase tracking-wider mt-1">Covenants Found</div>
        </div>
        <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-center">
          <div className="text-2xl font-bold text-emerald-400">{report.metrics.compliant}</div>
          <div className="text-[11px] text-slate-400 uppercase tracking-wider mt-1">Compliant</div>
        </div>
        <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-center">
          <div className="text-2xl font-bold text-rose-400">{report.metrics.critical_risks}</div>
          <div className="text-[11px] text-slate-400 uppercase tracking-wider mt-1">Critical Traps</div>
        </div>
        <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800 text-center">
          <div className="text-2xl font-bold text-amber-400">{report.metrics.high_risks}</div>
          <div className="text-[11px] text-slate-400 uppercase tracking-wider mt-1">High Risks</div>
        </div>
      </div>

      <div>
        <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3 flex items-center">
          <span className="mr-2">🔍</span> Itemized Compliance Findings & Grounded Citations
        </h3>
        <div className="overflow-x-auto rounded-xl border border-slate-800">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-950/80 border-b border-slate-800 text-slate-400 font-mono">
                <th className="p-3">Ref & Page</th>
                <th className="p-3">Category</th>
                <th className="p-3">Original Requirement</th>
                <th className="p-3">Risk Level</th>
                <th className="p-3">Policy Match</th>
                <th className="p-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 bg-slate-900/60">
              {report.itemized_clauses.map((clause, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition">
                  <td className="p-3 font-mono font-bold text-indigo-300 whitespace-nowrap">
                    <div>{clause.clause_id}</div>
                    <div className="text-[10px] text-slate-500 font-normal">Page {clause.page_number}</div>
                  </td>
                  <td className="p-3 text-slate-300 whitespace-nowrap font-medium">{clause.category}</td>
                  <td className="p-3 text-slate-300 text-[11px] max-w-xs">{clause.original_text}</td>
                  <td className="p-3 whitespace-nowrap">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        clause.risk_level === 'CRITICAL'
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                          : clause.risk_level === 'HIGH'
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : clause.risk_level === 'ACCEPTED_RISK'
                          ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                          : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      }`}
                    >
                      {clause.risk_level}
                    </span>
                  </td>
                  <td className="p-3 text-[11px] text-slate-400 font-mono">{clause.policy_reference}</td>
                  <td className="p-3 text-[11px] text-slate-300">{clause.recommended_action}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
