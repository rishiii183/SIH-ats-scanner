'use client';

import React, { useState } from 'react';
import { 
  Award, ShieldAlert, CheckCircle2, ChevronDown, ChevronUp, 
  Sparkles, RefreshCw, FileText, Lock, ArrowUpRight, Cpu, Target, Layers, Layout
} from 'lucide-react';

interface Reason {
  deduction: number;
  message: string;
  cited_source?: string;
  slide_number?: number[];
}

interface CategoryDetail {
  score: number;
  weight: number;
  reasons: Reason[];
}

interface ReportData {
  overall_score: number;
  verdict_text: string;
  rubric_stamp: string;
  category_breakdown: {
    structure_format: CategoryDetail;
    ps_alignment: CategoryDetail;
    technical_depth: CategoryDetail;
    originality: CategoryDetail;
    clarity: CategoryDetail;
  };
  rewrite_suggestions?: Array<{ category: string; suggestion: string }>;
}

interface ReportDashboardProps {
  report: ReportData;
  onReset: () => void;
}

export const ReportDashboard: React.FC<ReportDashboardProps> = ({ report, onReset }) => {
  const [expandedCategory, setExpandedCategory] = useState<string | null>('structure_format');

  const { overall_score, verdict_text, rubric_stamp, category_breakdown, rewrite_suggestions } = report;

  const categories = [
    { key: 'structure_format', title: 'Structure & Format', icon: Layers, detail: category_breakdown.structure_format },
    { key: 'ps_alignment', title: 'Problem Statement Alignment', icon: Target, detail: category_breakdown.ps_alignment },
    { key: 'technical_depth', title: 'Technical Depth & Feasibility', icon: Cpu, detail: category_breakdown.technical_depth },
    { key: 'originality', title: 'Originality & Overlap', icon: Award, detail: category_breakdown.originality },
    { key: 'clarity', title: 'Presentation Clarity', icon: Layout, detail: category_breakdown.clarity },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
    if (score >= 70) return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
    return 'text-red-400 border-red-500/30 bg-red-500/10';
  };

  const toggleCategory = (key: string) => {
    setExpandedCategory(expandedCategory === key ? null : key);
  };

  return (
    <div className="w-full max-w-5xl mx-auto my-8 space-y-8 animate-in fade-in duration-500">
      {/* Top Banner Card */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-slate-800 shadow-2xl relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-3 text-center md:text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-xs text-indigo-300 font-medium">
            <Sparkles className="w-3.5 h-3.5" />
            <span>{rubric_stamp}</span>
          </div>

          <h2 className="text-2xl sm:text-3xl font-extrabold text-white">Presentation ATS Score Report</h2>
          <p className="text-sm text-slate-300 max-w-xl">{verdict_text}</p>

          <div className="flex flex-wrap items-center gap-3 pt-2 justify-center md:justify-start">
            <button 
              onClick={onReset}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center gap-1.5 transition-all"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Scan Another Deck</span>
            </button>
            <button className="px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg flex items-center gap-1.5 transition-all">
              <FileText className="w-3.5 h-3.5" />
              <span>Export PDF Report</span>
            </button>
          </div>
        </div>

        {/* Score Ring Gauge */}
        <div className="flex flex-col items-center shrink-0">
          <div className="relative w-36 h-36 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="42" stroke="currentColor" strokeWidth="8" className="text-slate-800" fill="transparent" />
              <circle
                cx="50"
                cy="50"
                r="42"
                stroke="currentColor"
                strokeWidth="8"
                strokeDasharray={264}
                strokeDashoffset={264 - (264 * overall_score) / 100}
                strokeLinecap="round"
                className={overall_score >= 85 ? 'text-emerald-400' : overall_score >= 70 ? 'text-amber-400' : 'text-red-400'}
                fill="transparent"
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center text-center">
              <span className="text-3xl font-black text-white">{overall_score}</span>
              <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Out of 100</span>
            </div>
          </div>
          <span className={`mt-3 px-3 py-1 rounded-full text-xs font-bold border ${getScoreColor(overall_score)}`}>
            {overall_score >= 85 ? 'Strong Fit' : overall_score >= 70 ? 'Moderate Fit' : 'Requires Fixes'}
          </span>
        </div>
      </div>

      {/* 5 Category Breakdown Grid */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <span>Category Breakdown & Official Rubric Audit</span>
          <span className="text-xs font-normal text-slate-400">(Click category to expand details)</span>
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {categories.map((cat) => {
            const isExpanded = expandedCategory === cat.key;
            const Icon = cat.icon;
            const catScore = cat.detail.score;

            return (
              <div
                key={cat.key}
                className="glass-panel rounded-xl border border-slate-800/80 overflow-hidden transition-all"
              >
                <div
                  onClick={() => toggleCategory(cat.key)}
                  className="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-slate-800/40 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 shrink-0">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-sm text-slate-100">{cat.title}</span>
                        <span className="text-[11px] text-slate-400 font-medium">({Math.round(cat.detail.weight * 100)}% Weight)</span>
                      </div>
                      <p className="text-xs text-slate-400">
                        {cat.detail.reasons.length} flag(s) identified
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <span className={`text-lg font-extrabold ${catScore >= 85 ? 'text-emerald-400' : catScore >= 70 ? 'text-amber-400' : 'text-red-400'}`}>
                        {catScore}/100
                      </span>
                    </div>
                    {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                  </div>
                </div>

                {/* Expanded Details */}
                {isExpanded && (
                  <div className="px-5 pb-5 pt-2 border-t border-slate-800/60 bg-slate-950/40 space-y-3 text-xs">
                    <div className="font-semibold text-slate-300">Detailed Deductions & Official Citations:</div>
                    {cat.detail.reasons.map((reason, rIdx) => (
                      <div
                        key={rIdx}
                        className={`p-3.5 rounded-xl border space-y-1.5 ${
                          reason.deduction > 0
                            ? 'bg-red-500/10 border-red-500/20 text-red-200'
                            : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-200'
                        }`}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex items-center gap-1.5 font-medium">
                            {reason.deduction > 0 ? (
                              <ShieldAlert className="w-4 h-4 text-red-400 shrink-0" />
                            ) : (
                              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                            )}
                            <span>{reason.message}</span>
                          </div>
                          {reason.deduction > 0 && (
                            <span className="px-2 py-0.5 rounded bg-red-500/20 text-red-300 text-[10px] font-bold shrink-0">
                              -{reason.deduction} pts
                            </span>
                          )}
                        </div>

                        {reason.cited_source && (
                          <div className="text-[11px] text-slate-400 italic pl-5 border-l-2 border-slate-700">
                            Source Citation: "{reason.cited_source}"
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Rewrite Suggestions Card */}
      {rewrite_suggestions && rewrite_suggestions.length > 0 && (
        <div className="glass-panel p-6 rounded-2xl border border-indigo-500/20 space-y-4">
          <div className="flex items-center gap-2 text-indigo-300 font-bold text-base">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <span>Line-by-Line Rewrite Suggestions</span>
          </div>

          <div className="grid grid-cols-1 gap-3">
            {rewrite_suggestions.map((sug, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-start gap-3">
                <span className="px-2 py-1 rounded bg-indigo-500/20 text-indigo-300 font-bold text-[10px] uppercase shrink-0 mt-0.5">
                  {sug.category}
                </span>
                <p className="text-xs text-slate-200 leading-relaxed">{sug.suggestion}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Paywall & Re-Check Diff Lock Preview */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 bg-gradient-to-r from-slate-900/90 to-indigo-950/40 relative overflow-hidden text-center space-y-4">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
          <Lock className="w-6 h-6" />
        </div>

        <div>
          <h4 className="text-lg font-bold text-white mb-1">Unlock Unlimited Re-Checks & Score Delta Diffing</h4>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Edit your deck based on recommendations, re-upload, and see exact score improvements (e.g. 64 → 81, +17 pts) with Razorpay cycle pass.
          </p>
        </div>

        <button className="px-6 py-3 rounded-xl font-bold text-xs bg-gradient-to-r from-indigo-500 to-emerald-500 text-white shadow-lg hover:opacity-95 transition-all inline-flex items-center gap-2">
          <span>Upgrade to SIH 2026 Season Pass (₹99)</span>
          <ArrowUpRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
