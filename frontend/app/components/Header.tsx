"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';
import { Sparkles, FileSearch, LogOut, Menu, X, Home, BookOpen, HelpCircle, User } from 'lucide-react';

export const Header: React.FC = () => {
  const { data: session } = useSession();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="w-full flex flex-col items-center sticky top-2 sm:top-4 z-50 px-3 sm:px-4 pt-1 sm:pt-2">
      <header className="w-full max-w-5xl bg-white/80 backdrop-blur-2xl border border-white/90 shadow-lg shadow-slate-200/40 rounded-2xl sm:rounded-full px-4 sm:px-6 min-h-[56px] sm:h-16 flex items-center justify-between transition-all">
        
        {/* Brand Logo & Title */}
        <Link href="/" className="flex items-center gap-3 sm:gap-4 group min-h-[44px]">
          <div className="relative w-9 h-9 sm:w-11 sm:h-11 rounded-xl sm:rounded-2xl bg-orange-50 flex items-center justify-center border border-orange-100 shadow-xs group-hover:scale-105 transition-transform shrink-0">
            <FileSearch className="w-4 h-4 sm:w-5 sm:h-5 text-orange-500" />
          </div>
          <div className="flex flex-col justify-center">
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg sm:text-2xl tracking-tight leading-none bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                SIH ATS
              </span>
              <span className="text-[9px] sm:text-[10px] uppercase font-bold tracking-widest px-2 py-0.5 sm:py-1 rounded-full bg-orange-100 text-orange-600 border border-orange-200 leading-none">
                2026 Edition
              </span>
            </div>
            <p className="text-[10px] sm:text-[12px] leading-none font-medium text-slate-500 hidden sm:block mt-1">Smart India Hackathon PPT Evaluator</p>
          </div>
        </Link>

        {/* Desktop Navigation Items (md+) */}
        <div className="hidden md:flex items-center gap-3.5">
          {session?.user ? (
            <div className="flex items-center gap-2.5">
              <Link
                href="/profile"
                className="flex items-center gap-2 pl-2 pr-3.5 py-1.5 rounded-full bg-white/90 hover:bg-orange-50 border border-slate-200/90 hover:border-orange-200 shadow-xs transition-all group min-h-[44px]"
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
                className="min-h-[44px] min-w-[44px] flex items-center justify-center p-2 rounded-xl text-slate-400 hover:text-red-600 hover:bg-red-50 border border-transparent hover:border-red-100 transition-all cursor-pointer"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link 
              href="/login" 
              className="text-sm font-bold text-slate-700 hover:text-orange-600 transition-colors px-3 py-2 rounded-xl hover:bg-orange-50/60 min-h-[44px] flex items-center"
            >
              Sign In
            </Link>
          )}

          <Link
            href="/upgrade"
            className="relative group overflow-hidden flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-sm hover:shadow-md transition-all min-h-[44px]"
          >
            <Sparkles className="w-4 h-4 text-orange-100" />
            <span>Try Pro</span>
          </Link>
        </div>

        {/* Mobile Header Actions (Mobile Hamburger Toggle) */}
        <div className="flex md:hidden items-center gap-2">
          <Link
            href="/upgrade"
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-xs min-h-[44px]"
          >
            <Sparkles className="w-3.5 h-3.5 text-orange-100" />
            <span>Try Pro</span>
          </Link>

          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="min-h-[44px] min-w-[44px] flex items-center justify-center rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors border border-slate-200"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5 text-slate-800" /> : <Menu className="w-5 h-5 text-slate-800" />}
          </button>
        </div>
      </header>

      {/* Mobile Collapsible Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="w-full max-w-5xl mt-2 bg-white/95 backdrop-blur-3xl border border-slate-200 shadow-xl rounded-2xl p-4 md:hidden space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
          {session?.user ? (
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-3">
                {session.user.image ? (
                  <img src={session.user.image} alt="User" className="w-9 h-9 rounded-full object-cover border border-white shadow-xs" />
                ) : (
                  <div className="w-9 h-9 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-sm">
                    {(session.user.name || session.user.email || "U")[0].toUpperCase()}
                  </div>
                )}
                <div>
                  <p className="font-bold text-xs text-slate-800 truncate max-w-[160px]">{session.user.name || 'Participant'}</p>
                  <p className="text-[11px] text-slate-500 truncate max-w-[160px]">{session.user.email}</p>
                </div>
              </div>

              <Link
                href="/profile"
                onClick={() => setMobileMenuOpen(false)}
                className="px-3 py-1.5 rounded-lg bg-orange-500 text-white text-xs font-bold min-h-[44px] flex items-center"
              >
                Profile
              </Link>
            </div>
          ) : null}

          <nav className="flex flex-col gap-1 pt-1">
            <Link
              href="/"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-3 px-3.5 py-3 rounded-xl text-xs font-bold text-slate-700 hover:bg-orange-50 hover:text-orange-600 transition-colors min-h-[44px]"
            >
              <Home className="w-4 h-4 text-orange-500" />
              <span>ATS Scanner Home</span>
            </Link>

            <Link
              href="/guidelines"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-3 px-3.5 py-3 rounded-xl text-xs font-bold text-slate-700 hover:bg-orange-50 hover:text-orange-600 transition-colors min-h-[44px]"
            >
              <BookOpen className="w-4 h-4 text-orange-500" />
              <span>Format Guidelines & Checklist</span>
            </Link>

            <Link
              href="/faq"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-3 px-3.5 py-3 rounded-xl text-xs font-bold text-slate-700 hover:bg-orange-50 hover:text-orange-600 transition-colors min-h-[44px]"
            >
              <HelpCircle className="w-4 h-4 text-orange-500" />
              <span>FAQ & Rubric Rules</span>
            </Link>

            <Link
              href="/upgrade"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-3 px-3.5 py-3 rounded-xl text-xs font-bold text-orange-600 bg-orange-50/80 border border-orange-200/80 hover:bg-orange-100 transition-colors min-h-[44px]"
            >
              <Sparkles className="w-4 h-4 text-orange-500" />
              <span>Pro Season Pass (₹99)</span>
            </Link>
          </nav>

          {session?.user ? (
            <div className="pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => {
                  setMobileMenuOpen(false);
                  signOut({ callbackUrl: '/' });
                }}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-xs font-bold text-red-600 bg-red-50 border border-red-100 min-h-[44px]"
              >
                <LogOut className="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            </div>
          ) : (
            <div className="pt-2 border-t border-slate-100">
              <Link
                href="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-xs font-bold text-slate-800 bg-slate-100 border border-slate-200 min-h-[44px]"
              >
                <User className="w-4 h-4 text-slate-600" />
                <span>Sign In / Register</span>
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

