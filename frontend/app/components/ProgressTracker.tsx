'use client';

import React from 'react';
import { Loader2, CheckCircle2, Cpu, FileText, Target, ShieldCheck, Sparkles } from 'lucide-react';

interface ProgressTrackerProps {
  stepMessage: string;
  progressPct: number;
}

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({ stepMessage, progressPct }) => {
  const stages = [
    { label: 'Parsing slides & text layout', pct: 25, icon: FileText },
    { label: 'Checking 6-slide constraints', pct: 50, icon: ShieldCheck },
    { label: 'Problem statement vector match', pct: 75, icon: Target },
    { label: 'Technical depth AI judgment', pct: 100, icon: Cpu },
  ];

  return (
    <div className="w-full max-w-2xl mx-auto my-12 p-8 sm:p-10 rounded-3xl bg-white/80 backdrop-blur-2xl border border-white/90 shadow-[0_24px_70px_rgba(15,23,42,0.07)] text-center space-y-6 animate-in zoom-in-95 duration-300">
      
      {/* Animated Icon */}
      <div className="relative inline-flex items-center justify-center">
        <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-orange-100 to-orange-50 border border-orange-200 flex items-center justify-center text-orange-500 shadow-sm">
          <Loader2 className="w-10 h-10 animate-spin text-orange-500" />
        </div>
        <div className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center shadow-md animate-bounce">
          <Sparkles className="w-3.5 h-3.5" />
        </div>
      </div>

      <div className="space-y-1.5">
        <h3 className="text-xl sm:text-2xl font-black tracking-tight text-slate-900">
          Evaluating Deck Against SIH 2026 Rubric
        </h3>
        <p className="text-xs sm:text-sm font-medium text-slate-500 max-w-md mx-auto">
          {stepMessage}
        </p>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-100/90 h-3 rounded-full overflow-hidden p-0.5 border border-slate-200/80 shadow-inner">
        <div
          className="bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 h-full rounded-full transition-all duration-500 shadow-sm"
          style={{ width: `${progressPct}%` }}
        />
      </div>

      {/* Stage Indicators */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-left pt-2">
        {stages.map((stage, idx) => {
          const isDone = progressPct >= stage.pct;
          const isCurrent = progressPct < stage.pct && (idx === 0 || progressPct >= stages[idx - 1].pct);
          const Icon = stage.icon;

          return (
            <div
              key={idx}
              className={`p-3.5 rounded-2xl border text-xs flex flex-col gap-2 transition-all shadow-xs ${
                isDone
                  ? 'bg-emerald-50/90 border-emerald-200 text-emerald-800'
                  : isCurrent
                  ? 'bg-orange-50/90 border-orange-300 text-orange-800 animate-pulse'
                  : 'bg-white/60 border-slate-200/80 text-slate-400'
              }`}
            >
              <div className="flex items-center justify-between">
                <Icon className={`w-4 h-4 ${isDone ? 'text-emerald-600' : isCurrent ? 'text-orange-600' : 'text-slate-400'}`} />
                {isDone && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />}
              </div>
              <span className="font-bold text-[11px] leading-tight">{stage.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
