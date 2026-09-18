"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { signIn } from 'next-auth/react';
import { ArrowRight, Mail, Lock, User, Home, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';
import { supabase } from '@/lib/supabase';

export default function LoginPage() {
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleGoogleLogin = async (e: React.MouseEvent) => {
    e.preventDefault();
    setError(null);
    setGoogleLoading(true);
    try {
      await signIn('google', { callbackUrl: '/' });
    } catch (err: any) {
      setError(err?.message || 'Failed to sign in with Google');
      setGoogleLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    const cleanEmail = email.trim().toLowerCase();

    if (!cleanEmail || !password.trim()) {
      setError('Please fill in all required fields.');
      return;
    }

    if (isSignUp && !name.trim()) {
      setError('Please enter your name.');
      return;
    }

    setLoading(true);

    try {
      // 1. Direct Supabase verification for clear, instant feedback
      const { data: existingUser, error: checkErr } = await supabase
        .from('users')
        .select('id, email, name')
        .eq('email', cleanEmail)
        .maybeSingle();

      if (isSignUp) {
        // Sign Up Logic: User must not already exist
        if (existingUser) {
          setError('An account with this email already exists. Please log in.');
          setLoading(false);
          return;
        }

        // Create new user in Supabase
        const { error: insertErr } = await supabase.from('users').insert({
          email: cleanEmail,
          name: name.trim(),
          auth_provider: 'email',
        });

        if (insertErr) {
          setError(insertErr.message || 'Failed to create account.');
          setLoading(false);
          return;
        }
      } else {
        // Log In Logic: User must already exist in database
        if (!existingUser) {
          setError('No account found with this email. Please sign up first.');
          setLoading(false);
          return;
        }
      }

      // 2. Establish NextAuth session
      const res = await signIn('credentials', {
        email: cleanEmail,
        password,
        name: isSignUp ? name.trim() : existingUser?.name || cleanEmail.split('@')[0],
        mode: isSignUp ? 'signup' : 'login',
        redirect: false,
      });

      if (res?.error) {
        setError('Authentication failed. Please check your credentials.');
        setLoading(false);
      } else {
        setSuccess(isSignUp ? 'Account created successfully! Redirecting...' : 'Logged in successfully! Redirecting...');
        setTimeout(() => {
          router.push('/');
          router.refresh();
        }, 700);
      }
    } catch (err: any) {
      setError(err?.message || 'An unexpected error occurred.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden bg-slate-50 selection:bg-orange-500 selection:text-white">
      {/* Decorative background blobs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-orange-400/20 blur-[120px] mix-blend-multiply" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-400/20 blur-[120px] mix-blend-multiply" />

      <div className="w-full max-w-md p-6 relative z-10">
        {/* Back to Home Link */}
        <Link 
          href="/" 
          className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors mb-6 group"
        >
          <Home className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform" />
          Back to Home
        </Link>

        {/* Glassmorphic Card */}
        <div className="w-full bg-white/70 backdrop-blur-2xl border border-white/80 shadow-[0_12px_40px_0_rgba(31,38,135,0.08)] rounded-3xl p-8 flex flex-col gap-6">
          
          {/* Header */}
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-1">
              <h1 className="text-2xl font-extrabold tracking-tight text-slate-900">
                {isSignUp ? 'Sign Up' : 'Log In'}
              </h1>
              <p className="text-sm text-slate-500">
                {isSignUp 
                  ? 'Create an account to evaluate your SIH presentations' 
                  : 'Welcome back! Sign in to continue'}
              </p>
            </div>

            {/* Standard Log In / Sign Up Tabs */}
            <div className="grid grid-cols-2 p-1 bg-slate-200/60 rounded-2xl text-xs font-semibold text-slate-600">
              <button
                type="button"
                onClick={() => { setIsSignUp(false); setError(null); setSuccess(null); }}
                className={`py-2 rounded-xl transition-all ${
                  !isSignUp 
                    ? 'bg-white text-slate-900 shadow-sm font-bold' 
                    : 'hover:text-slate-900 text-slate-500'
                }`}
              >
                Log In
              </button>
              <button
                type="button"
                onClick={() => { setIsSignUp(true); setError(null); setSuccess(null); }}
                className={`py-2 rounded-xl transition-all ${
                  isSignUp 
                    ? 'bg-white text-slate-900 shadow-sm font-bold' 
                    : 'hover:text-slate-900 text-slate-500'
                }`}
              >
                Sign Up
              </button>
            </div>
          </div>

          {/* Feedback Alerts */}
          {error && (
            <div className="flex items-center gap-2.5 p-3.5 rounded-xl bg-red-50/90 border border-red-200 text-red-700 text-xs font-medium animate-in fade-in slide-in-from-top-1">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-500" />
              <span>{error}</span>
            </div>
          )}

          {success && (
            <div className="flex items-center gap-2.5 p-3.5 rounded-xl bg-emerald-50/90 border border-emerald-200 text-emerald-700 text-xs font-medium animate-in fade-in slide-in-from-top-1">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0 text-emerald-500" />
              <span>{success}</span>
            </div>
          )}

          {/* Google Sign In Button */}
          <button 
            type="button" 
            onClick={handleGoogleLogin} 
            disabled={googleLoading || loading}
            className="w-full relative group overflow-hidden flex items-center justify-center gap-3 px-5 py-3 rounded-xl text-sm font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300 shadow-sm transition-all disabled:opacity-60"
          >
            {googleLoading ? (
              <Loader2 className="w-5 h-5 animate-spin text-orange-500" />
            ) : (
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                />
              </svg>
            )}
            <span>Continue with Google</span>
          </button>

          <div className="flex items-center gap-4 text-xs uppercase tracking-wider text-slate-400 font-bold">
            <div className="flex-1 h-px bg-slate-200"></div>
            <span>or</span>
            <div className="flex-1 h-px bg-slate-200"></div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {/* Name field (Only shown on Sign Up) */}
            {isSignUp && (
              <div className="flex flex-col gap-1.5 animate-in fade-in slide-in-from-top-2">
                <label className="text-xs font-semibold text-slate-700 pl-1">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    required={isSignUp}
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your name"
                    className="w-full bg-white border border-slate-200 text-slate-800 text-sm rounded-xl px-10 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all placeholder:text-slate-400"
                  />
                </div>
              </div>
            )}

            {/* Email field */}
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-semibold text-slate-700 pl-1">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full bg-white border border-slate-200 text-slate-800 text-sm rounded-xl px-10 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            {/* Password field */}
            <div className="flex flex-col gap-1.5">
              <div className="flex items-center justify-between pl-1">
                <label className="text-xs font-semibold text-slate-700">Password</label>
                {!isSignUp && (
                  <a href="#" className="text-xs font-medium text-orange-600 hover:text-orange-700 transition-colors">
                    Forgot password?
                  </a>
                )}
              </div>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-white border border-slate-200 text-slate-800 text-sm rounded-xl px-10 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            {/* Submit button */}
            <button 
              type="submit" 
              disabled={loading || googleLoading}
              className="w-full relative group overflow-hidden flex items-center justify-center gap-2 px-5 py-3.5 mt-2 rounded-xl text-sm font-semibold bg-slate-900 hover:bg-slate-800 text-white shadow-md transition-all disabled:opacity-60"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 animate-spin text-white" />
              ) : (
                <>
                  <span>{isSignUp ? 'Sign Up' : 'Log In'}</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>

          {/* Footer toggle link */}
          <div className="text-center text-xs text-slate-500">
            {isSignUp ? (
              <>
                Already have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setIsSignUp(false); setError(null); setSuccess(null); }}
                  className="font-bold text-orange-600 hover:text-orange-700 transition-colors underline-offset-2 hover:underline"
                >
                  Log in
                </button>
              </>
            ) : (
              <>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setIsSignUp(true); setError(null); setSuccess(null); }}
                  className="font-bold text-orange-600 hover:text-orange-700 transition-colors underline-offset-2 hover:underline"
                >
                  Sign up
                </button>
              </>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}