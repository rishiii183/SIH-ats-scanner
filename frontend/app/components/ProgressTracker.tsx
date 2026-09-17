'use client';

import React from 'react';
import { Loader2, CheckCircle2, Cpu, FileText, Target, ShieldCheck } from 'lucide-react';

interface ProgressTrackerProps {
  stepMessage: string;
  progressPct: number;
}

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({ stepMessage, progressPct }) => {
  const stages = [
    { label: 'Parsing slides & text layout', pct: 25, icon: FileText },
    { label: 'Checking 6-slide structure & constraints', pct: 50, icon: ShieldCheck },
    { label: 'Problem statement vector alignment', pct: 75, icon: Target },
    { label: 'Technical depth AI judgment (Gemini 1.5)', pct: 100, icon: Cpu },
  ];

  return (
    <div className="w-full max-w-2xl mx-auto my-12 p-8 rounded-2xl bg-white border border-slate-200 shadow-xl text-center space-y-6">
      <div className="w-16 h-16 rounded-full bg-orange-50 border border-orange-200 flex items-center justify-center mx-auto text-orange-500">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>

      <div>
        <h3 className="text-xl font-bold text-slate-800 mb-1">Scanning Deck Against Official Rubric</h3>
        <p className="text-xs text-slate-500">{stepMessage}</p>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden p-0.5 border border-slate-200 shadow-inner">
        <div
          className="bg-gradient-to-r from-orange-500 to-orange-400 h-full rounded-full transition-all duration-500 shadow-sm"
          style={{ width: `${progressPct}%` }}
        />
      </div>

      {/* Stage Indicators */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-left pt-4">
        {stages.map((stage, idx) => {
          const isDone = progressPct >= stage.pct;
          const isCurrent = progressPct < stage.pct && (idx === 0 || progressPct >= stages[idx - 1].pct);
          const Icon = stage.icon;

          return (
            <div
              key={idx}
              className={`p-3 rounded-xl border text-xs flex flex-col gap-2 transition-all shadow-sm ${
                isDone
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                  : isCurrent
                  ? 'bg-orange-50 border-orange-300 text-orange-700 animate-pulse'
                  : 'bg-white border-slate-200 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between">
                <Icon className="w-4 h-4" />
                {isDone ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> : null}
              </div>
              <span className="font-medium text-[11px] leading-tight">{stage.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
