import React from 'react';
import Link from 'next/link';
import { Sparkles, FileSearch } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <div className="w-full flex justify-center sticky top-4 z-50 px-4 pt-4">
      <header className="w-full max-w-5xl bg-white/30 backdrop-blur-2xl border border-white/60 shadow-lg shadow-slate-200/40 rounded-full px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="relative w-12 h-12 rounded-2xl bg-orange-50 flex items-center justify-center border border-orange-100 shadow-sm">
            <FileSearch className="w-6 h-6 text-orange-500" />
          </div>
          <div className="flex flex-col justify-center pt-0.5">
            <div className="flex items-center gap-2.5 mb-1">
              <span className="font-extrabold text-2xl tracking-tight leading-none bg-gradient-to-r from-slate-800 to-slate-500 bg-clip-text text-transparent">
                SIH ATS
              </span>
              <span className="text-[10px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full bg-orange-100 text-orange-600 border border-orange-200 leading-none">
                2026 Edition
              </span>
            </div>
            <p className="text-[13px] leading-none font-medium text-slate-500">Smart India Hackathon PPT Evaluator</p>
          </div>
        </div>

        <div className="flex items-center gap-5">
          <Link href="/login" className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors px-1">
            Sign In
          </Link>
          <button className="relative group overflow-hidden flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold bg-orange-500 hover:bg-orange-600 text-white shadow-sm transition-all">
            <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
            <Sparkles className="w-4 h-4 text-orange-100" />
            <span>Try Pro</span>
          </button>
        </div>
      </header>
    </div>
  );
};
