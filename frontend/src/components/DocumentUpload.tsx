import React from 'react';

interface DocumentUploadProps {
  documentId: string | null;
  filename: string;
  totalPages: number;
  isUploading: boolean;
  onFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onLoadSample: () => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  documentId,
  filename,
  totalPages,
  isUploading,
  onFileUpload,
  onLoadSample,
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-3 flex items-center">
        <span className="mr-2">📄</span> 1. Ingest RFP / Contract
      </h2>

      <div className="border-2 border-dashed border-slate-700 hover:border-indigo-500/60 transition-colors rounded-xl p-5 text-center cursor-pointer bg-slate-950/40">
        <input
          type="file"
          id="fileUpload"
          className="hidden"
          accept=".pdf,.txt,.doc,.docx"
          onChange={onFileUpload}
        />
        <label htmlFor="fileUpload" className="cursor-pointer flex flex-col items-center">
          <span className="text-3xl mb-2">📥</span>
          <span className="text-sm font-medium text-slate-200">Upload PDF or Agreement</span>
          <span className="text-xs text-slate-500 mt-1">Supports PDF, TXT, Markdown</span>
        </label>
      </div>

      <div className="relative my-4 text-center">
        <span className="bg-slate-900 px-3 text-xs text-slate-500 relative z-10 uppercase tracking-widest">
          or quick demo
        </span>
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-slate-800"></div>
        </div>
      </div>

      <button
        onClick={onLoadSample}
        disabled={isUploading}
        className="w-full bg-slate-800 hover:bg-slate-700/80 text-indigo-300 border border-indigo-500/30 rounded-xl py-2.5 px-4 text-xs font-semibold flex items-center justify-center space-x-2 transition shadow-sm"
      >
        <span>⚡</span>
        <span>{isUploading ? "Loading Benchmark..." : "Load Tier-1 Bank RFP Sample"}</span>
      </button>

      {documentId && (
        <div className="mt-4 p-3 bg-indigo-950/30 border border-indigo-500/20 rounded-xl text-xs space-y-1">
          <div className="flex justify-between font-mono">
            <span className="text-slate-400">File:</span>
            <span className="text-indigo-200 truncate max-w-[180px] font-medium">{filename}</span>
          </div>
          <div className="flex justify-between font-mono">
            <span className="text-slate-400">Pages Grounded:</span>
            <span className="text-emerald-400 font-bold">{totalPages} Pages</span>
          </div>
          <div className="flex justify-between font-mono">
            <span className="text-slate-400">Doc Ref ID:</span>
            <span className="text-slate-300">{documentId}</span>
          </div>
        </div>
      )}
    </div>
  );
};
