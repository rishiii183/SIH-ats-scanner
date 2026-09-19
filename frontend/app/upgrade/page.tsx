"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { 
  Check, Sparkles, ShieldCheck, Zap, ArrowLeft, 
  CreditCard, QrCode, Lock, CheckCircle2, ArrowRight, 
  HelpCircle, Star, Award, Layers, Cpu, Flame, Loader2 
} from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { Header } from '../components/Header';

export default function UpgradePage() {
  const { data: session } = useSession();
  const router = useRouter();

  const [paymentMethod, setPaymentMethod] = useState<'upi' | 'card'>('upi');
  const [upiId, setUpiId] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePayment = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsProcessing(true);

    try {
      // Simulate real-time payment gateway handshake (Razorpay / UPI)
      await new Promise((resolve) => setTimeout(resolve, 1800));

      const userEmail = session?.user?.email;
      if (userEmail) {
        // Upgrade user plan in Supabase
        await supabase
          .from('users')
          .update({ plan: 'paid' })
          .eq('email', userEmail.toLowerCase().trim());
      }

      setIsSuccess(true);
      setTimeout(() => {
        router.push('/profile');
        router.refresh();
      }, 2000);
    } catch (err: any) {
      setError('Payment could not be completed. Please try again.');
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden bg-[#FDFBF7] selection:bg-orange-500 selection:text-white">
      {/* Ambient gradient lighting */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-orange-400/15 blur-[140px] pointer-events-none mix-blend-multiply" />
      <div className="absolute top-[30%] right-[-10%] w-[45%] h-[45%] rounded-full bg-emerald-400/15 blur-[140px] pointer-events-none mix-blend-multiply" />
      <div className="absolute bottom-[-10%] left-[20%] w-[45%] h-[45%] rounded-full bg-amber-300/15 blur-[140px] pointer-events-none mix-blend-multiply" />

      <Header />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 relative z-10 space-y-12 animate-in fade-in duration-300">
        
        {/* Navigation Breadcrumb */}
        <Link 
          href="/" 
          className="inline-flex items-center gap-2 text-sm font-bold text-slate-500 hover:text-slate-800 transition-colors group"
        >
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          <span>Back to Scanner</span>
        </Link>

        {/* Hero Banner */}
        <div className="text-center space-y-4 max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-gradient-to-r from-orange-100 to-amber-100 border border-orange-200/90 text-orange-800 text-xs font-black tracking-wide shadow-xs">
            <Flame className="w-4 h-4 text-orange-600 animate-bounce" />
            <span>SIH 2026 OFFICIAL SEASON PASS</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight leading-tight">
            Turn Your 65 Score Deck into a{' '}
            <span className="bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 bg-clip-text text-transparent">
              95+ Shortlist Winner
            </span>
          </h1>

          <p className="text-sm sm:text-base text-slate-600 leading-relaxed font-medium max-w-2xl mx-auto">
            Unlimited presentation re-evaluations, score delta diffing, and line-by-line jury rewrites for your entire team. One-time pass for the entire SIH 2026 season.
          </p>
        </div>

        {/* 2 Plans Comparison Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch">
          
          {/* Free Tier Card */}
          <div className="bg-white/70 backdrop-blur-2xl p-8 rounded-3xl border border-slate-200/80 shadow-sm flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-extrabold text-slate-800">Free Tier</h3>
                  <p className="text-xs text-slate-500">For casual initial testing</p>
                </div>
                <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600 text-xs font-bold border border-slate-200">
                  Current Tier
                </span>
              </div>

              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-black text-slate-900">₹0</span>
                <span className="text-xs text-slate-400 font-bold">/ forever</span>
              </div>

              <ul className="space-y-3 text-xs sm:text-sm text-slate-600 font-medium pt-2 border-t border-slate-100">
                <li className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-500 shrink-0" />
                  <span>3 Total Presentation Scans</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-500 shrink-0" />
                  <span>Basic 6-Slide Constraint Audit</span>
                </li>
                <li className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-emerald-500 shrink-0" />
                  <span>Problem Statement Semantic Alignment</span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-400">
                  <span className="w-4 h-4 rounded-full bg-slate-200 flex items-center justify-center text-[10px] text-slate-500 shrink-0">✕</span>
                  <span>No Unlimited Re-Scans</span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-400">
                  <span className="w-4 h-4 rounded-full bg-slate-200 flex items-center justify-center text-[10px] text-slate-500 shrink-0">✕</span>
                  <span>No Score Delta Diffing</span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-400">
                  <span className="w-4 h-4 rounded-full bg-slate-200 flex items-center justify-center text-[10px] text-slate-500 shrink-0">✕</span>
                  <span>No Slide-by-Slide AI Jury Rewrites</span>
                </li>
              </ul>
            </div>

            <Link
              href="/"
              className="w-full py-3.5 px-4 rounded-2xl text-xs sm:text-sm font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 text-center transition-all"
            >
              Continue on Free Tier
            </Link>
          </div>

          {/* Pro Pass Card (Highlighted) */}
          <div className="bg-gradient-to-b from-orange-500/10 via-white/80 to-white/95 backdrop-blur-2xl p-8 rounded-3xl border-2 border-orange-400 shadow-xl shadow-orange-500/10 flex flex-col justify-between space-y-6 relative overflow-hidden">
            
            {/* Top Recommended Tag */}
            <div className="absolute top-0 right-0 bg-gradient-to-r from-orange-500 to-amber-500 text-white text-[10px] font-black uppercase tracking-widest px-4 py-1.5 rounded-bl-2xl shadow-sm">
              MOST POPULAR FOR SIH TEAMS
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-xl font-black text-slate-900">SIH 2026 Pro Pass</h3>
                    <Sparkles className="w-4 h-4 text-orange-500" />
                  </div>
                  <p className="text-xs text-orange-700 font-semibold">Everything you need to qualify</p>
                </div>
              </div>

              <div className="flex items-baseline gap-2">
                <span className="text-5xl font-black text-slate-900">₹99</span>
                <span className="text-xs text-slate-400 line-through font-bold">₹499</span>
                <span className="text-xs text-emerald-600 font-extrabold bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                  80% OFF (Limited Season Price)
                </span>
              </div>

              <ul className="space-y-3 text-xs sm:text-sm text-slate-700 font-semibold pt-2 border-t border-orange-100">
                <li className="flex items-center gap-2.5 text-slate-900">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                    <Check className="w-3.5 h-3.5" />
                  </div>
                  <span><strong>Unlimited PPT Re-Scans</strong> (Iterate until 90+ score)</span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-900">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                    <Check className="w-3.5 h-3.5" />
                  </div>
                  <span><strong>Score Delta Diffing</strong> (See exact +18 pt gains per fix)</span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-900">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                    <Check className="w-3.5 h-3.5" />
                  </div>
                  <span><strong>Slide-by-Slide AI Jury Rewrites</strong> (Exact text & diagrams)</span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-900">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                    <Check className="w-3.5 h-3.5" />
                  </div>
                  <span><strong>Buzzword Penalty Shield</strong> (Concrete stack validator)</span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-900">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                    <Check className="w-3.5 h-3.5" />
                  </div>
                  <span><strong>Hardware & Software Track Custom Evaluator</strong></span>
                </li>
                <li className="flex items-center gap-2.5 text-slate-900">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
                    <Check className="w-3.5 h-3.5" />
                  </div>
                  <span><strong>2.5x Faster Priority AI Engine</strong></span>
                </li>
              </ul>
            </div>

            {/* Instant Checkout Trigger */}
            <a
              href="#checkout-box"
              className="w-full py-4 px-6 rounded-2xl font-black text-sm bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white text-center shadow-lg shadow-orange-500/25 hover:shadow-xl transition-all flex items-center justify-center gap-2"
            >
              <span>Get Pro Season Pass (₹99)</span>
              <ArrowRight className="w-4 h-4" />
            </a>
          </div>

        </div>

        {/* Payment Checkout Box */}
        <div id="checkout-box" className="bg-white/85 backdrop-blur-2xl p-6 sm:p-10 rounded-3xl border border-white/90 shadow-[0_24px_70px_rgba(15,23,42,0.08)] max-w-2xl mx-auto space-y-6">
          
          <div className="text-center space-y-1">
            <h2 className="text-2xl font-black text-slate-900">Complete Instant Upgrade</h2>
            <p className="text-xs text-slate-500">Instant activation for {session?.user?.email || 'your account'}</p>
          </div>

          {/* Payment Method Selector */}
          <div className="grid grid-cols-2 p-1 bg-slate-100 rounded-2xl text-xs font-bold text-slate-600">
            <button
              type="button"
              onClick={() => setPaymentMethod('upi')}
              className={`py-2.5 rounded-xl transition-all flex items-center justify-center gap-2 ${
                paymentMethod === 'upi' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'
              }`}
            >
              <QrCode className="w-4 h-4 text-orange-500" />
              <span>Instant UPI / QR</span>
            </button>
            <button
              type="button"
              onClick={() => setPaymentMethod('card')}
              className={`py-2.5 rounded-xl transition-all flex items-center justify-center gap-2 ${
                paymentMethod === 'card' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'
              }`}
            >
              <CreditCard className="w-4 h-4 text-orange-500" />
              <span>Cards / Net Banking</span>
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handlePayment} className="space-y-4">
            {paymentMethod === 'upi' ? (
              <div className="space-y-3">
                <div className="p-4 rounded-2xl bg-orange-50/70 border border-orange-200/80 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-orange-800">Scan & Pay via any UPI App</span>
                    <p className="text-xs font-bold text-slate-800">Google Pay, PhonePe, Paytm, CRED</p>
                  </div>
                  <div className="w-12 h-12 rounded-xl bg-white border border-orange-200 flex items-center justify-center text-slate-700 shadow-xs">
                    <QrCode className="w-7 h-7 text-orange-500" />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-700">Enter UPI ID / VPA</label>
                  <input
                    type="text"
                    required
                    placeholder="yourname@okhdfcbank or yourname@paytm"
                    value={upiId}
                    onChange={(e) => setUpiId(e.target.value)}
                    className="w-full p-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 shadow-sm font-medium"
                  />
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-700">Card Number</label>
                  <input
                    type="text"
                    placeholder="4532 •••• •••• 8921"
                    className="w-full p-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 shadow-sm"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-700">Expiry (MM/YY)</label>
                    <input
                      type="text"
                      placeholder="08/28"
                      className="w-full p-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 shadow-sm"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-700">CVV</label>
                    <input
                      type="password"
                      placeholder="•••"
                      maxLength={4}
                      className="w-full p-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 shadow-sm"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Price Breakdown */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2 text-xs">
              <div className="flex justify-between text-slate-500">
                <span>SIH 2026 Season Pro Access</span>
                <span>₹499</span>
              </div>
              <div className="flex justify-between text-emerald-600 font-semibold">
                <span>Participant Discount (80%)</span>
                <span>-₹400</span>
              </div>
              <div className="border-t border-slate-200 pt-2 flex justify-between font-black text-slate-900 text-sm">
                <span>Total Amount Due</span>
                <span>₹99 only</span>
              </div>
            </div>

            {error && (
              <div className="p-3.5 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {isSuccess && (
              <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-800 font-bold flex items-center gap-2 shadow-sm animate-in zoom-in-95">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
                <span>Payment Verified! Upgraded to SIH Pro Season Pass. Redirecting...</span>
              </div>
            )}

            {/* Pay Button */}
            <button
              type="submit"
              disabled={isProcessing || isSuccess}
              className="w-full py-4 px-6 rounded-2xl font-black text-sm bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg shadow-orange-500/25 transition-all flex items-center justify-center gap-2 disabled:opacity-60 cursor-pointer"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-white" />
                  <span>Verifying Transaction with Gateway...</span>
                </>
              ) : isSuccess ? (
                <span>Activated!</span>
              ) : (
                <>
                  <Lock className="w-4 h-4" />
                  <span>Pay ₹99 & Unlock Pro Pass Instantly</span>
                </>
              )}
            </button>
          </form>

          <div className="flex items-center justify-center gap-4 text-[11px] text-slate-400 font-semibold pt-1">
            <span className="flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
              256-Bit Encrypted Payment
            </span>
            <span>•</span>
            <span>Instant Activation</span>
          </div>

        </div>

      </main>
    </div>
  );
}
