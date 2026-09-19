'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
  Award, ShieldAlert, CheckCircle2, ChevronDown, ChevronUp, 
  Sparkles, RefreshCw, FileText, Lock, ArrowUpRight, Cpu, Target, Layers, Layout, Lightbulb, Download
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
    { key: 'structure_format', title: 'Structure & Format Compliance', icon: Layers, detail: category_breakdown.structure_format },
    { key: 'ps_alignment', title: 'Problem Statement Alignment', icon: Target, detail: category_breakdown.ps_alignment },
    { key: 'technical_depth', title: 'Technical Depth & Feasibility', icon: Cpu, detail: category_breakdown.technical_depth },
    { key: 'originality', title: 'Originality & Competitive Advantage', icon: Award, detail: category_breakdown.originality },
    { key: 'clarity', title: 'Visual Clarity & Conciseness', icon: Layout, detail: category_breakdown.clarity },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-emerald-700 border-emerald-300 bg-emerald-50/90';
    if (score >= 70) return 'text-amber-700 border-amber-300 bg-amber-50/90';
    return 'text-red-700 border-red-300 bg-red-50/90';
  };

  const toggleCategory = (key: string) => {
    setExpandedCategory(expandedCategory === key ? null : key);
  };

  return (
    <div className="w-full max-w-5xl mx-auto my-6 sm:my-10 space-y-8 animate-in fade-in duration-500">
      
      {/* Top Banner Scorecard */}
      <div className="bg-white/80 backdrop-blur-2xl p-6 sm:p-10 rounded-3xl border border-white/90 shadow-[0_24px_70px_rgba(15,23,42,0.07)] relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-8">
        
        {/* Glow accent */}
        <div className="absolute top-0 right-0 w-72 h-72 bg-gradient-to-br from-orange-400/15 via-emerald-400/10 to-transparent rounded-full blur-3xl pointer-events-none" />

        <div className="space-y-4 text-center md:text-left relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-orange-50/90 border border-orange-200/90 text-xs text-orange-700 font-bold tracking-wide shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-orange-500" />
            <span>{rubric_stamp}</span>
          </div>

          <h2 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">
            Presentation ATS Scorecard
          </h2>
          <p className="text-sm text-slate-600 max-w-xl leading-relaxed font-medium">
            {verdict_text}
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-2 justify-center md:justify-start print:hidden">
            <button 
              onClick={onReset}
              className="px-4 py-2.5 rounded-xl text-xs font-bold bg-white/90 hover:bg-slate-100 text-slate-700 border border-slate-200 flex items-center gap-2 shadow-sm transition-all cursor-pointer"
            >
              <RefreshCw className="w-3.5 h-3.5 text-slate-500" />
              <span>Scan Another Deck</span>
            </button>
            <button 
              onClick={() => window.print()}
              className="px-5 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-md hover:shadow-lg flex items-center gap-2 transition-all cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export PDF Report</span>
            </button>
          </div>
        </div>

        {/* Score Ring Radial Gauge */}
        <div className="flex flex-col items-center shrink-0 relative z-10">
          <div className="relative w-32 h-32 sm:w-40 sm:h-40 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90 drop-shadow-sm" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="40" stroke="currentColor" strokeWidth="8" className="text-slate-100/90" fill="transparent" />
              <circle
                cx="50"
                cy="50"
                r="40"
                stroke="currentColor"
                strokeWidth="8"
                strokeDasharray={251.2}
                strokeDashoffset={251.2 - (251.2 * overall_score) / 100}
                strokeLinecap="round"
                className={`transition-all duration-1000 ${
                  overall_score >= 85 ? 'text-emerald-500' : overall_score >= 70 ? 'text-amber-500' : 'text-red-500'
                }`}
                fill="transparent"
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center text-center">
              <span className="text-3xl sm:text-4xl font-black tracking-tight text-slate-900">{overall_score}</span>
              <span className="text-[9px] sm:text-[10px] uppercase font-extrabold text-slate-400 tracking-wider">Out of 100</span>
            </div>
          </div>
          <span className={`mt-3 px-4 py-1 rounded-full text-xs font-black uppercase tracking-wider border shadow-sm ${getScoreColor(overall_score)}`}>
            {overall_score >= 85 ? 'Shortlist Ready' : overall_score >= 70 ? 'Competitive Deck' : 'Needs Refinement'}
          </span>
        </div>
      </div>

      {/* 5 Category Breakdown Cards */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
          <h3 className="text-base sm:text-lg font-black text-slate-900 flex items-center gap-2">
            <span>Category Breakdown & Jury Rubric Audit</span>
          </h3>
          <span className="text-xs font-semibold text-slate-400">Click card to expand slide citations</span>
        </div>

        <div className="grid grid-cols-1 gap-3.5">
          {categories.map((cat) => {
            const isExpanded = expandedCategory === cat.key;
            const Icon = cat.icon;
            const catScore = cat.detail.score;

            return (
              <div
                key={cat.key}
                className="bg-white/80 backdrop-blur-xl rounded-2xl border border-slate-200/80 overflow-hidden transition-all shadow-sm hover:shadow-md"
              >
                <div
                  onClick={() => toggleCategory(cat.key)}
                  className="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-slate-50/70 transition-colors min-h-[56px] select-none"
                  role="button"
                  aria-expanded={isExpanded}
                >
                  <div className="flex items-center gap-3 sm:gap-3.5 pr-2">
                    <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl bg-gradient-to-tr from-orange-100 to-orange-50 border border-orange-200/80 flex items-center justify-center text-orange-600 shrink-0 shadow-sm">
                      <Icon className="w-4 h-4 sm:w-5 sm:h-5" />
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
                        <span className="font-extrabold text-sm sm:text-base text-slate-900 leading-snug">{cat.title}</span>
                        <span className="text-[10px] text-orange-700 bg-orange-50 border border-orange-200 px-2 py-0.5 rounded-full font-bold shrink-0">
                          {Math.round(cat.detail.weight * 100)}% Weight
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">
                        {cat.detail.reasons.length} audit observation{cat.detail.reasons.length > 1 ? 's' : ''}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 sm:gap-4 shrink-0">
                    <div className="text-right">
                      <span className={`text-base sm:text-xl font-black ${
                        catScore >= 85 ? 'text-emerald-600' : catScore >= 70 ? 'text-amber-600' : 'text-red-500'
                      }`}>
                        {catScore}
                      </span>
                      <span className="text-xs text-slate-400 font-bold">/100</span>
                    </div>
                    <div className="w-9 h-9 sm:w-8 sm:h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 min-h-[36px] min-w-[36px]">
                      {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-600" /> : <ChevronDown className="w-4 h-4 text-slate-600" />}
                    </div>
                  </div>
                </div>

                {/* Expanded Details Drawer */}
                {isExpanded && (
                  <div className="px-4 sm:px-5 pb-5 pt-3 border-t border-slate-100 bg-slate-50/60 space-y-3 text-xs animate-in fade-in duration-200">
                    <div className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">
                      Jury Deductions & Official Rubric Citations:
                    </div>
                    {cat.detail.reasons.map((reason, rIdx) => (
                      <div
                        key={rIdx}
                        className={`p-3.5 sm:p-4 rounded-2xl border space-y-2 shadow-sm ${
                          reason.deduction > 0
                            ? 'bg-red-50/90 border-red-200 text-red-900'
                            : 'bg-emerald-50/90 border-emerald-200 text-emerald-900'
                        }`}
                      >
                        <div className="flex items-start justify-between gap-2.5">
                          <div className="flex items-start gap-2 font-semibold break-words min-w-0 flex-1">
                            {reason.deduction > 0 ? (
                              <ShieldAlert className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                            ) : (
                              <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                            )}
                            <span className="text-xs leading-relaxed break-words">{reason.message}</span>
                          </div>
                          {reason.deduction > 0 && (
                            <span className="px-2 py-0.5 rounded-full bg-red-100 border border-red-200 text-red-700 text-[10px] font-black shrink-0 shadow-xs">
                              -{reason.deduction} pts
                            </span>
                          )}
                        </div>

                        {reason.cited_source && (
                          <div className="text-[11px] text-slate-600 italic pl-3 border-l-2 border-slate-300 break-words overflow-hidden text-wrap">
                            <strong>Source Citation:</strong> "{reason.cited_source}"
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

      {/* Actionable Rewrite Suggestions */}
      {rewrite_suggestions && rewrite_suggestions.length > 0 && (
        <div className="bg-white/80 backdrop-blur-2xl p-6 sm:p-8 rounded-3xl border border-orange-200/90 space-y-4 shadow-sm">
          <div className="flex items-center gap-2.5 text-orange-600 font-extrabold text-base sm:text-lg">
            <Lightbulb className="w-5 h-5 text-orange-500" />
            <span>Actionable Slide-by-Slide Rewrite Suggestions</span>
          </div>

          <div className="grid grid-cols-1 gap-3.5">
            {rewrite_suggestions.map((sug, idx) => (
              <div key={idx} className="p-4 rounded-2xl bg-orange-50/60 border border-orange-200/70 flex items-start gap-3.5">
                <span className="px-2.5 py-1 rounded-full bg-orange-100 text-orange-800 font-black text-[10px] uppercase tracking-wide shrink-0 mt-0.5 border border-orange-200">
                  {sug.category}
                </span>
                <p className="text-xs sm:text-sm text-slate-700 leading-relaxed font-medium">
                  {sug.suggestion}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pro Pass Card */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 p-8 rounded-3xl text-white relative overflow-hidden text-center space-y-4 shadow-xl print:hidden">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-orange-500/20 text-orange-400 border border-orange-500/30">
          <Lock className="w-6 h-6" />
        </div>

        <div className="space-y-1">
          <h4 className="text-xl font-black tracking-tight text-white">
            Unlock Unlimited Re-Checks & Score Delta Diffing
          </h4>
          <p className="text-xs sm:text-sm text-slate-300 max-w-lg mx-auto">
            Apply the recommended fixes, re-upload your deck, and verify your score improvement (e.g. 64 ➔ 88, +24 pts) with the SIH 2026 Season Pass.
          </p>
        </div>

        <Link 
          href="/upgrade"
          className="px-6 py-3.5 rounded-2xl font-bold text-xs sm:text-sm bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg hover:shadow-orange-500/20 transition-all inline-flex items-center gap-2 hover:scale-[1.02]"
        >
          <span>Upgrade to SIH 2026 Pass (₹99)</span>
          <ArrowUpRight className="w-4 h-4" />
        </Link>

      </div>

    </div>
  );
};
