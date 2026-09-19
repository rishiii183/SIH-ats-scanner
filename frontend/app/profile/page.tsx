"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useSession, signOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { 
  User, Mail, School, Sparkles, LogOut, ArrowLeft, 
  Clock, CheckCircle2, ShieldCheck, FileText, ArrowUpRight, 
  Edit3, Save, Loader2, AlertCircle 
} from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { Header } from '../components/Header';

interface UserProfileData {
  id?: string;
  email: string;
  name: string;
  college?: string;
  auth_provider: string;
  plan: string;
  created_at?: string;
}

interface UserScan {
  id: string;
  file_name: string;
  status: string;
  created_at: string;
  report?: {
    overall_score: number;
    verdict_text: string;
  };
}

export default function ProfilePage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  const [userData, setUserData] = useState<UserProfileData | null>(null);
  const [college, setCollege] = useState('');
  const [name, setName] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [scans, setScans] = useState<UserScan[]>([]);

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login');
      return;
    }

    if (session?.user?.email) {
      loadUserProfile(session.user.email);
    }
  }, [session, status]);

  const loadUserProfile = async (email: string) => {
    setLoading(true);
    try {
      // 1. Fetch user profile from Supabase
      const { data: user, error } = await supabase
        .from('users')
        .select('*')
        .eq('email', email.toLowerCase().trim())
        .maybeSingle();

      if (user) {
        setUserData(user);
        setName(user.name || session?.user?.name || '');
        setCollege(user.college || '');

        // 2. Fetch user's scan history
        const { data: userSubmissions } = await supabase
          .from('submissions')
          .select('id, file_name, status, created_at, reports(overall_score, verdict_text)')
          .eq('user_id', user.id)
          .order('created_at', { ascending: false });

        if (userSubmissions) {
          const formattedScans = userSubmissions.map((sub: any) => ({
            id: sub.id,
            file_name: sub.file_name,
            status: sub.status,
            created_at: sub.created_at,
            report: Array.isArray(sub.reports) && sub.reports.length > 0 ? sub.reports[0] : sub.reports,
          }));
          setScans(formattedScans);
        }
      } else {
        // Fallback with session data
        setUserData({
          email,
          name: session?.user?.name || '',
          auth_provider: 'google',
          plan: 'free',
        });
        setName(session?.user?.name || '');
      }
    } catch (err) {
      console.error('Error loading profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session?.user?.email) return;

    setSaving(true);
    setSaveError(null);
    setSaveSuccess(false);

    try {
      const { error } = await supabase
        .from('users')
        .update({
          name: name.trim(),
          college: college.trim(),
        })
        .eq('email', session.user.email.toLowerCase().trim());

      if (error) throw error;

      setSaveSuccess(true);
      setIsEditing(false);
      if (userData) {
        setUserData({ ...userData, name: name.trim(), college: college.trim() });
      }
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err: any) {
      setSaveError(err?.message || 'Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#FDFBF7]">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
          <p className="text-sm font-semibold text-slate-500">Loading your profile...</p>
        </div>
      </div>
    );
  }

  const joinDate = userData?.created_at 
    ? new Date(userData.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    : 'Recent Member';

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden bg-[#FDFBF7] selection:bg-orange-500 selection:text-white">
      {/* Decorative ambient background blobs */}
      <div className="absolute top-[-5%] left-[-10%] w-[45%] h-[45%] rounded-full bg-orange-400/10 blur-[130px] pointer-events-none mix-blend-multiply" />
      <div className="absolute top-[25%] right-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-400/10 blur-[130px] pointer-events-none mix-blend-multiply" />

      <Header />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10 space-y-8 animate-in fade-in duration-300">
        
        {/* Back Link */}
        <Link 
          href="/" 
          className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-slate-800 transition-colors group"
        >
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          Back to ATS Scanner
        </Link>

        {/* Profile Card Header */}
        <div className="bg-white/80 backdrop-blur-2xl p-6 sm:p-10 rounded-3xl border border-white/90 shadow-[0_24px_70px_rgba(15,23,42,0.06)] relative overflow-hidden flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          
          <div className="flex items-center gap-5">
            {/* User Avatar */}
            <div className="relative">
              {session?.user?.image ? (
                <img 
                  src={session.user.image} 
                  alt={userData?.name || "User Avatar"} 
                  className="w-20 h-20 sm:w-24 sm:h-24 rounded-3xl object-cover border-2 border-white shadow-md"
                />
              ) : (
                <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-3xl bg-gradient-to-tr from-orange-500 to-amber-500 text-white flex items-center justify-center text-3xl font-black shadow-md">
                  {(userData?.name || userData?.email || "U")[0].toUpperCase()}
                </div>
              )}
              <div className="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-emerald-500 border-2 border-white flex items-center justify-center text-white shadow-sm" title="Active Account">
                <CheckCircle2 className="w-4 h-4" />
              </div>
            </div>

            {/* User Info */}
            <div className="space-y-1">
              <div className="flex items-center gap-2.5">
                <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
                  {userData?.name || session?.user?.name || "Participant"}
                </h1>
                <span className="text-[11px] uppercase tracking-wider font-extrabold px-3 py-1 rounded-full bg-orange-50 text-orange-700 border border-orange-200">
                  {userData?.plan === 'paid' ? 'SIH Pro Pass' : 'Free Tier'}
                </span>
              </div>
              <p className="text-sm font-medium text-slate-500 flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                {userData?.email}
              </p>
              <div className="flex flex-wrap items-center gap-4 text-xs font-semibold text-slate-400 pt-1">
                <span className="flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  Joined {joinDate}
                </span>
                <span>•</span>
                <span className="capitalize text-slate-600">
                  Auth via {userData?.auth_provider || 'Google'}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center gap-3 w-full md:w-auto">
            <button
              type="button"
              onClick={() => setIsEditing(!isEditing)}
              className="flex-1 md:flex-none px-4 py-2.5 rounded-xl text-xs font-bold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-sm transition-all flex items-center justify-center gap-2"
            >
              <Edit3 className="w-4 h-4 text-slate-500" />
              <span>{isEditing ? 'Cancel Editing' : 'Edit Profile'}</span>
            </button>
            <button
              type="button"
              onClick={() => signOut({ callbackUrl: '/login' })}
              className="px-4 py-2.5 rounded-xl text-xs font-bold bg-red-50 hover:bg-red-100 text-red-600 border border-red-200/80 shadow-sm transition-all flex items-center justify-center gap-2"
            >
              <LogOut className="w-4 h-4" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>

        {/* Edit Profile Form (Collapsible) */}
        {isEditing && (
          <div className="bg-white/80 backdrop-blur-2xl p-6 sm:p-8 rounded-3xl border border-orange-200/80 shadow-sm animate-in fade-in slide-in-from-top-2">
            <h3 className="text-base font-extrabold text-slate-900 mb-4 flex items-center gap-2">
              <Edit3 className="w-4 h-4 text-orange-500" />
              <span>Update Profile Information</span>
            </h3>

            <form onSubmit={handleSaveProfile} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-700">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Your full name"
                      className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs sm:text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 shadow-sm"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-700">College / Institute</label>
                  <div className="relative">
                    <School className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={college}
                      onChange={(e) => setCollege(e.target.value)}
                      placeholder="e.g. IIT Kharagpur / MAKAUT"
                      className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-xs sm:text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 shadow-sm"
                    />
                  </div>
                </div>
              </div>

              {saveError && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{saveError}</span>
                </div>
              )}

              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-5 py-2.5 rounded-xl text-xs font-bold bg-orange-500 hover:bg-orange-600 text-white shadow flex items-center gap-2 disabled:opacity-60"
                >
                  {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                  <span>Save Changes</span>
                </button>
              </div>
            </form>
          </div>
        )}

        {saveSuccess && (
          <div className="p-4 rounded-2xl bg-emerald-50/90 border border-emerald-200 text-emerald-800 text-xs font-bold flex items-center gap-2 shadow-sm animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Profile successfully updated!</span>
          </div>
        )}

        {/* 2-Column Grid: Plan Status + Scan History */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Plan & Usage Card */}
          <div className="bg-white/80 backdrop-blur-2xl p-6 rounded-3xl border border-white/90 shadow-sm space-y-5 lg:col-span-1">
            <div className="flex items-center justify-between">
              <h3 className="font-extrabold text-base text-slate-900">Your Plan</h3>
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-orange-100 text-orange-700">
                {userData?.plan === 'paid' ? 'Pro' : 'Free'}
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-orange-50/80 border border-orange-200/80 space-y-2">
              <div className="flex items-center gap-2 text-xs font-extrabold text-orange-900">
                <Sparkles className="w-4 h-4 text-orange-600" />
                <span>SIH 2026 Season Pass</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Upgrade for unlimited presentation re-checks, full diff improvements, and line-by-line AI jury rewrite suggestions.
              </p>
            </div>

            <ul className="space-y-2.5 text-xs text-slate-600 font-medium">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Instant 6-Slide Constraint Check</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Problem Statement Alignment Score</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Export PDF Evaluator Reports</span>
              </li>
              <li className="flex items-center gap-2 text-slate-400">
                <ShieldCheck className="w-4 h-4 text-slate-300 shrink-0" />
                <span>Unlimited Deck Re-Scans (Pro Only)</span>
              </li>
            </ul>

            <button className="w-full py-3 px-4 rounded-xl text-xs font-bold bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-md flex items-center justify-center gap-2 transition-all">
              <span>Upgrade Pass (₹99)</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>

          {/* Scan History Card */}
          <div className="bg-white/80 backdrop-blur-2xl p-6 sm:p-8 rounded-3xl border border-white/90 shadow-sm space-y-5 lg:col-span-2">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-extrabold text-base sm:text-lg text-slate-900">Recent ATS Evaluations</h3>
                <p className="text-xs text-slate-500">Your past presentation uploads and score reports</p>
              </div>
              <Link 
                href="/"
                className="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-orange-500 hover:bg-orange-600 text-white shadow-sm transition-all"
              >
                + New Scan
              </Link>
            </div>

            {scans.length > 0 ? (
              <div className="space-y-3">
                {scans.map((scan) => (
                  <div 
                    key={scan.id} 
                    className="p-4 rounded-2xl bg-white border border-slate-200/80 flex items-center justify-between gap-4 shadow-xs hover:shadow-sm transition-all"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-orange-50 border border-orange-100 flex items-center justify-center text-orange-500 shrink-0">
                        <FileText className="w-5 h-5" />
                      </div>
                      <div className="space-y-0.5">
                        <p className="font-bold text-xs sm:text-sm text-slate-800 max-w-[200px] sm:max-w-xs truncate">
                          {scan.file_name}
                        </p>
                        <p className="text-[11px] text-slate-400">
                          {new Date(scan.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                        </p>
                      </div>
                    </div>

                    <div className="text-right flex items-center gap-3">
                      {scan.report?.overall_score !== undefined ? (
                        <div className="text-right">
                          <span className={`text-base font-black ${
                            scan.report.overall_score >= 85 ? 'text-emerald-600' : scan.report.overall_score >= 70 ? 'text-amber-600' : 'text-red-500'
                          }`}>
                            {scan.report.overall_score}
                          </span>
                          <span className="text-[10px] text-slate-400 font-bold">/100</span>
                        </div>
                      ) : (
                        <span className="text-[10px] uppercase font-bold text-slate-400">
                          {scan.status}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-8 text-center rounded-2xl bg-slate-50/70 border border-slate-200/70 space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-orange-50 text-orange-500 border border-orange-100 flex items-center justify-center mx-auto">
                  <FileText className="w-6 h-6" />
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-bold text-slate-800">No evaluations yet</p>
                  <p className="text-xs text-slate-500 max-w-xs mx-auto">
                    Upload your first SIH presentation deck to receive instant scorecards and jury feedback.
                  </p>
                </div>
                <Link
                  href="/"
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white shadow-sm transition-all"
                >
                  Scan Deck Now
                </Link>
              </div>
            )}
          </div>

        </div>

      </main>
    </div>
  );
}
