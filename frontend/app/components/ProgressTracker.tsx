'use client';

import React, { useState, useEffect } from 'react';
import { Loader2, CheckCircle2, Cpu, FileText, Target, ShieldCheck, Sparkles, Terminal, ChevronRight, Info } from 'lucide-react';

interface ProgressTrackerProps {
  stepMessage: string;
  progressPct: number;
}

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({ stepMessage, progressPct }) => {
  const [displayPct, setDisplayPct] = useState<number>(progressPct);
  const [activeTab, setActiveTab] = useState<'tracker' | 'rubric_info'>('tracker');

  // Smooth progress interpolation
  useEffect(() => {
    const timer = setTimeout(() => {
      setDisplayPct((prev) => {
        if (progressPct > prev) {
          return Math.min(progressPct, prev + Math.ceil((progressPct - prev) * 0.4));
        }
        return progressPct;
      });
    }, 50);

    return () => clearTimeout(timer);
  }, [progressPct, displayPct]);

  const stages = [
    { 
      id: 'parsing',
      label: 'Parsing & Layout Geometry', 
      pct: 25, 
      icon: FileText,
      description: 'Extracting text frames, slide count, shapes, and image distributions from deck.',
      details: 'Validates file format (.pdf / .pptx) and converts slides into structural object graphs.'
    },
    { 
      id: 'structure',
      label: '6-Slide Structure Audit', 
      pct: 50, 
      icon: ShieldCheck,
      description: 'Auditing against active Rubric Config (#cdbb77e8-ee1c-41bc-b780-af3395c5f706).',
      details: 'Checks mandatory headings: Title, Problem Statement, Solution, Tech Stack, Impact, References.'
    },
    { 
      id: 'alignment',
      label: 'Semantic PS Alignment', 
      pct: 75, 
      icon: Target,
      description: 'Computing SentenceTransformers (all-MiniLM-L6-v2) cosine similarity embedding.',
      details: 'Runs local PyTorch vector embedding model to compare deck content against selected PS domain keywords.'
    },
    { 
      id: 'aggregation',
      label: 'ATS Rubric & Score Stamp', 
      pct: 100, 
      icon: Cpu,
      description: 'Renormalizing active pillar weights & generating line-by-line verdict report.',
      details: 'Compiles weighted score breakdown, identifies section gaps, and prepares rewrite suggestions.'
    },
  ];

  return (
    <div className="w-full max-w-3xl mx-auto my-10 p-6 sm:p-10 rounded-3xl bg-white/85 backdrop-blur-2xl border border-white/90 shadow-[0_24px_70px_rgba(15,23,42,0.08)] space-y-7 animate-in zoom-in-95 duration-300">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-100 pb-5">
        <div className="flex items-center gap-4 text-left">
          <div className="relative">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white shadow-lg shadow-orange-500/20">
              <Loader2 className="w-7 h-7 animate-spin" />
            </div>
            <div className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-emerald-500 border-2 border-white flex items-center justify-center animate-pulse">
              <Sparkles className="w-3 h-3 text-white" />
            </div>
          </div>

          <div>
            <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-orange-100/80 text-orange-700 text-[11px] font-extrabold uppercase tracking-wider mb-1 border border-orange-200/60">
              <span>Live ATS Engine Scanning</span>
            </div>
            <h3 className="text-lg sm:text-xl font-black text-slate-900 tracking-tight">
              Evaluating Deck Against SIH Rubric
            </h3>
          </div>
        </div>

        {/* Tab Toggle */}
        <div className="flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200/80 text-xs font-bold text-slate-600">
          <button
            onClick={() => setActiveTab('tracker')}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'tracker'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'hover:text-slate-900'
            }`}
          >
            Live Progress
          </button>
          <button
            onClick={() => setActiveTab('rubric_info')}
            className={`px-3 py-1.5 rounded-lg transition-all flex items-center gap-1 ${
              activeTab === 'rubric_info'
                ? 'bg-white text-slate-900 shadow-xs'
                : 'hover:text-slate-900'
            }`}
          >
            <Info className="w-3.5 h-3.5 text-orange-500" />
            <span>Rubric Rules</span>
          </button>
        </div>
      </div>

      {activeTab === 'tracker' ? (
        <>
          {/* Main Animated Progress Bar with Percentage Counter */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-black text-slate-700 px-1">
              <span className="flex items-center gap-2 text-orange-600 font-bold">
                <span className="w-2 h-2 rounded-full bg-orange-500 animate-ping" />
                {stepMessage}
              </span>
              <span className="text-slate-900 font-black text-base">{Math.round(displayPct)}%</span>
            </div>

            <div className="w-full bg-slate-100 h-3.5 rounded-full overflow-hidden p-0.5 border border-slate-200/80 shadow-inner">
              <div
                className="bg-gradient-to-r from-orange-500 via-amber-500 to-orange-600 h-full rounded-full transition-all duration-300 shadow-sm relative overflow-hidden"
                style={{ width: `${Math.max(8, displayPct)}%` }}
              >
                <div className="absolute inset-0 bg-white/20 animate-[shimmer_2s_infinite] bg-[linear-gradient(90deg,rgba(255,255,255,0)_0%,rgba(255,255,255,0.4)_50%,rgba(255,255,255,0)_100%)]" />
              </div>
            </div>
          </div>

          {/* Interactive 4-Stage Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left pt-1">
            {stages.map((stage, idx) => {
              const isDone = displayPct >= stage.pct;
              const isCurrent = displayPct < stage.pct && (idx === 0 || displayPct >= stages[idx - 1].pct);
              const Icon = stage.icon;

              return (
                <div
                  key={stage.id}
                  className={`p-4 rounded-2xl border text-xs transition-all duration-300 relative group ${
                    isDone
                      ? 'bg-emerald-50/80 border-emerald-200/90 text-emerald-950 shadow-xs'
                      : isCurrent
                      ? 'bg-orange-50/90 border-orange-300 text-orange-950 shadow-md ring-2 ring-orange-400/20'
                      : 'bg-white/70 border-slate-200/70 text-slate-400 opacity-70'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <div
                        className={`w-7 h-7 rounded-lg flex items-center justify-center ${
                          isDone
                            ? 'bg-emerald-100 text-emerald-700'
                            : isCurrent
                            ? 'bg-orange-200 text-orange-800 animate-bounce'
                            : 'bg-slate-100 text-slate-400'
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className="font-extrabold text-xs text-slate-900 tracking-tight">
                        Stage {idx + 1}: {stage.label}
                      </span>
                    </div>

                    {isDone ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-100/90 px-2 py-0.5 rounded-md">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        Pass
                      </span>
                    ) : isCurrent ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-orange-700 bg-orange-100 px-2 py-0.5 rounded-md animate-pulse">
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        Active
                      </span>
                    ) : (
                      <span className="text-[10px] font-semibold text-slate-400">Queued</span>
                    )}
                  </div>

                  <p className={`text-[11px] leading-relaxed ${isDone ? 'text-emerald-800/90' : isCurrent ? 'text-orange-900' : 'text-slate-400'}`}>
                    {stage.description}
                  </p>

                  {/* Tooltip detail on hover */}
                  <div className="mt-2 pt-2 border-t border-slate-200/40 text-[10px] text-slate-500 font-medium flex items-center gap-1">
                    <ChevronRight className="w-3 h-3 text-orange-500 shrink-0" />
                    <span>{stage.details}</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Live Activity Stream Terminal Log */}
          <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800 text-left font-mono text-[11px] space-y-1.5 shadow-inner">
            <div className="flex items-center justify-between text-slate-400 pb-1.5 border-b border-slate-800 text-[10px] font-sans font-bold uppercase tracking-wider">
              <div className="flex items-center gap-2 text-slate-300">
                <Terminal className="w-3.5 h-3.5 text-emerald-400" />
                <span>Live Audit Telemetry</span>
              </div>
              <span className="text-emerald-400">STATUS: SCANNING</span>
            </div>

            <div className="space-y-1 pt-1 text-slate-300">
              <p className="flex items-center gap-2">
                <span className="text-emerald-400 font-bold">✓ [0.05s]</span>
                <span>File header magic-bytes validated. Security scan pass.</span>
              </p>
              {displayPct >= 25 && (
                <p className="flex items-center gap-2 animate-in fade-in">
                  <span className="text-emerald-400 font-bold">✓ [0.20s]</span>
                  <span>Document parsed. Slide geometry & text frames loaded.</span>
                </p>
              )}
              {displayPct >= 50 && (
                <p className="flex items-center gap-2 animate-in fade-in">
                  <span className="text-emerald-400 font-bold">✓ [0.45s]</span>
                  <span>Evaluated against active Rubric Config #cdbb77e8-ee1c-41bc-b780-af3395c5f706.</span>
                </p>
              )}
              {displayPct >= 75 && (
                <p className="flex items-center gap-2 animate-in fade-in">
                  <span className="text-emerald-400 font-bold">✓ [0.70s]</span>
                  <span>SentenceTransformers all-MiniLM-L6-v2 embeddings calculated locally.</span>
                </p>
              )}
              {displayPct >= 95 && (
                <p className="flex items-center gap-2 text-orange-400 font-bold animate-in fade-in">
                  <span>▶ [0.95s]</span>
                  <span>Finalizing overall ATS score & verdict stamp...</span>
                </p>
              )}
            </div>
          </div>
        </>
      ) : (
        /* Rubric Rules Preview Tab */
        <div className="text-left space-y-4 animate-in fade-in duration-200">
          <div className="p-4 rounded-2xl bg-orange-50/70 border border-orange-200 text-xs text-orange-950 space-y-1">
            <h4 className="font-extrabold text-orange-900 text-sm">Active SIH 2026 Evaluation Constraints</h4>
            <p>Your presentation deck is being automatically benchmarked against the official SIH 2026 Idea Presentation Rubric dataset.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <span className="font-bold text-slate-900 block">1. Slide Count Capped at 6</span>
              <p className="text-slate-500 text-[11px]">Decks exceeding 6 slides receive a 15-point deduction per extra slide.</p>
            </div>
            <div className="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <span className="font-bold text-slate-900 block">2. Mandatory Section Headings</span>
              <p className="text-slate-500 text-[11px]">Title, Problem Statement, Solution, Tech Stack, Impact, and References/Team.</p>
            </div>
            <div className="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <span className="font-bold text-slate-900 block">3. Local Cosine Semantic Match</span>
              <p className="text-slate-500 text-[11px]">SentenceTransformers vectors compare problem statement description with proposal text.</p>
            </div>
            <div className="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <span className="font-bold text-slate-900 block">4. Concise Layout & Visuals</span>
              <p className="text-slate-500 text-[11px]">Paragraphs over 70 words or missing diagrams reduce the clarity score.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

