"use client";

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { signIn } from 'next-auth/react';
import { ArrowRight, Mail, Lock, Chrome, Home } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();

  const handleMockLogin = (e?: React.MouseEvent) => {
    e?.preventDefault();
    alert("Authenticating... This is a UI mockup. Redirecting to home!");
    router.push('/');
  };

  const handleGoogleLogin = (e?: React.MouseEvent) => {
    e?.preventDefault();
    signIn('google', { callbackUrl: '/' });
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden bg-slate-50">
      {/* Decorative background blobs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-orange-400/20 blur-[120px] mix-blend-multiply" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-400/20 blur-[120px] mix-blend-multiply" />

      <div className="w-full max-w-md p-8 relative z-10">
        {/* Back to Home Link */}
        <Link href="/" className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors mb-8">
          <Home className="w-4 h-4" />
          Back to Home
        </Link>

        {/* Glassmorphic Card */}
        <div className="w-full bg-white/40 backdrop-blur-2xl border border-white/60 shadow-[0_8px_32px_0_rgba(31,38,135,0.07)] rounded-3xl p-8 flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <h1 className="text-2xl font-extrabold tracking-tight text-slate-800">Welcome Back</h1>
            <p className="text-sm text-slate-500">Sign in to your account to continue</p>
          </div>

          {/* Google Sign In Button */}
          <button type="button" onClick={handleGoogleLogin} className="w-full relative group overflow-hidden flex items-center justify-center gap-3 px-5 py-3 rounded-xl text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300 shadow-sm transition-all">
            <Chrome className="w-5 h-5 text-slate-600 group-hover:text-orange-500 transition-colors" />
            <span>Continue with Google</span>
          </button>

          <div className="flex items-center gap-4 text-sm text-slate-400">
            <div className="flex-1 h-px bg-slate-200"></div>
            <span>or</span>
            <div className="flex-1 h-px bg-slate-200"></div>
          </div>

          {/* Email/Password Form */}
          <form className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-600 pl-1">Email</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="email"
                  placeholder="you@example.com"
                  className="w-full bg-white/60 border border-slate-200 text-slate-800 text-sm rounded-xl px-10 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-600 pl-1">Password</label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full bg-white/60 border border-slate-200 text-slate-800 text-sm rounded-xl px-10 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            <div className="flex justify-end">
              <a href="#" className="text-xs font-medium text-orange-600 hover:text-orange-700 transition-colors">Forgot password?</a>
            </div>

            <button type="button" onClick={handleMockLogin} className="w-full relative group overflow-hidden flex items-center justify-center gap-2 px-5 py-3 mt-2 rounded-xl text-sm font-semibold bg-slate-800 hover:bg-slate-900 text-white shadow-md transition-all">
              hywhwy