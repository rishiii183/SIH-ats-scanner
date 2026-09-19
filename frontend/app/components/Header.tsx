"use client";

import React from 'react';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';
import { Sparkles, FileSearch, LogOut, User } from 'lucide-react';

export const Header: React.FC = () => {
  const { data: session } = useSession();

  return (
    <div className="w-full flex justify-center sticky top-4 z-50 px-4 pt-2">
      <header className="w-full max-w-5xl bg-white/70 backdrop-blur-2xl border border-white/90 shadow-lg shadow-slate-200/40 rounded-full px-6 h-16 flex items-center justify-between transition-all">
        <Link href="/" className="flex items-center gap-4 group">
          <div className="relative w-11 h-11 rounded-2xl bg-orange-50 flex items-center justify-center border border-orange-100 shadow-sm group-hover:scale-105 transition-transform">
            <FileSearch className="w-5 h-5 text-orange-500" />
          </div>
          <div className="flex flex-col justify-center pt-0.5">
            <div className="flex items-center gap-2.5 mb-0.5">
              <span className="font-extrabold text-2xl tracking-tight leading-none bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                SIH ATS
              </span>
              <span className="text-[10px] uppercase font-bold tracking-widest px-2.5 py-1 rounded-full bg-orange-100 text-orange-600 border border-orange-200 leading-none">
                2026 Edition
              </span>
            </div>
            <p className="text-[12px] leading-none font-medium text-slate-500">Smart India Hackathon PPT Evaluator</p>
          </div>
        </Link>

        <div className="flex items-center gap-3.5">
          {session?.user ? (
            <div className="flex items-center gap-2.5">
              {/* Profile Chip Button */}
              <Link
                href="/profile"
                className="flex items-center gap-2 pl-2 pr-3.5 py-1.5 rounded-full bg-white/90 hover:bg-orange-50 border border-slate-200/90 hover:border-orange-200 shadow-xs hover:shadow-sm transition-all group"
                title="View Profile & History"
              >
                {session.user.image ? (
                  <img 
                    src={session.user.image} 
                    alt={session.user.name || "User"} 
                    className="w-7 h-7 rounded-full object-cover border border-white shadow-xs group-hover:scale-105 transition-transform" 
                  />
                ) : (
                  <div className="w-7 h-7 rounded-full bg-orange-500 text-white flex items-center justify-center text-xs font-bold shadow-xs">
                    {(session.user.name || session.user.email || "U")[0].toUpperCase()}
                  </div>
                )}
                <span className="text-xs font-bold text-slate-700 group-hover:text-orange-600 transition-colors max-w-[120px] truncate">
                  {session.user.name || session.user.email?.split('@')[0]}
                </span>
              </Link>

              <button
                type="button"
                onClick={() => signOut({ callbackUrl: '/' })}
                title="Sign Out"
                className="p-2 rounded-xl text-slate-400 hover:text-red-600 hover:bg-red-50 border border-transparent hover:border-red-100 transition-all"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link 
              href="/login" 
              className="text-sm font-bold text-slate-700 hover:text-orange-600 transition-colors px-3 py-1.5 rounded-xl hover:bg-orange-50/60"
            >
              Sign In
            </Link>
          )}

          <Link
            href="/profile"
            className="relative group overflow-hidden flex items-center gap-2 px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-sm hover:shadow-md transition-all"
          >
            <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]"></div>
            <Sparkles className="w-4 h-4 text-orange-100" />
            <span>Try Pro</span>
          </Link>
        </div>
      </header>
    </div>
  );
};
