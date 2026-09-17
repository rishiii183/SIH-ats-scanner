import React from 'react';
import { Sparkles, FileSearch, ShieldCheck } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="w-full glass-panel sticky top-0 z-50 border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-emerald-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <FileSearch className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                SIH-ATS Scanner
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                SIH 2026 Ready
              </span>
            </div>
            <p className="text-xs text-slate-400">Official Rubric Presentation Score Evaluator</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden sm:flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20">
            <ShieldCheck className="w-4 h-4" />
            <span>Rubric Active: Max 6 Slides</span>
          </div>

          <button className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 text-white shadow-md transition-all">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Pro Features</span>
          </button>
        </div>
      </div>
    </header>
  );
};
