'use client';

import React, { useState, useEffect } from 'react';
import { getSession } from 'next-auth/react';
import { Header } from './components/Header';
import { UploadSection } from './components/UploadSection';
import { ProgressTracker } from './components/ProgressTracker';
import { ReportDashboard } from './components/ReportDashboard';
import { AlertCircle, RotateCcw } from 'lucide-react';
import { supabase } from '@/lib/supabase';

export default function Home() {
  const [submissionId, setSubmissionId] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string>('');
  const [status, setStatus] = useState<'idle' | 'processing' | 'completed' | 'failed'>('idle');
  const [progressMsg, setProgressMsg] = useState<string>('Initiating scan...');
  const [progressPct, setProgressPct] = useState<number>(10);
  const [report, setReport] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Poll status when scanning
  useEffect(() => {
    if (!submissionId || status !== 'processing') return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/v1/submissions/${submissionId}/status`);
        if (res.ok) {
          const data = await res.json();
          setProgressMsg(data.progress_step || 'Processing deck...');
          setProgressPct(data.progress_pct || 50);

          if (data.status === 'completed') {
            setStatus('completed');
            fetchReport(submissionId);
          } else if (data.status === 'failed') {
            setStatus('failed');
            setErrorMsg(data.error_message || 'Evaluation failed. Please try again.');
          }
        }
      } catch (err) {
        console.error('Status poll error', err);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [submissionId, status]);

  const fetchReport = async (subId: string) => {
    try {
      const res = await fetch(`/api/v1/submissions/${subId}/report`);
      if (res.ok) {
        const data = await res.json();
        setReport(data);

        // Record scan history for the user
        const session = await getSession();
        const userEmail = session?.user?.email;
        const newScanItem = {

          id: subId,
          file_name: uploadedFileName || 'SIH_Presentation.pptx',
          created_at: new Date().toISOString(),
          status: 'completed',
          report: {
            overall_score: data.overall_score,
            verdict_text: data.verdict_text,
          }
        };

        if (userEmail) {
          // 1. Save to local storage for instant sync
          const storageKey = `sih_user_scans_${userEmail.toLowerCase()}`;
          const existing = JSON.parse(localStorage.getItem(storageKey) || '[]');
          const updated = [newScanItem, ...existing.filter((s: any) => s.id !== subId)];
          localStorage.setItem(storageKey, JSON.stringify(updated));

          // 2. Persist to Supabase if user exists
          try {
            const { data: userRec } = await supabase
              .from('users')
              .select('id')
              .eq('email', userEmail.toLowerCase())
              .maybeSingle();

            if (userRec?.id) {
              const { data: subData } = await supabase.from('submissions').insert({
                user_id: userRec.id,
                file_name: uploadedFileName || 'SIH_Presentation.pptx',
                file_url: 'local',
                file_type: uploadedFileName?.endsWith('.pdf') ? 'pdf' : 'pptx',
                status: 'completed',
              }).select().single();

              if (subData?.id) {
                await supabase.from('reports').insert({
                  submission_id: subData.id,
                  overall_score: data.overall_score,
                  verdict_text: data.verdict_text,
                  category_breakdown: data.category_breakdown || {},
                  rewrite_suggestions: data.rewrite_suggestions || [],
                });
              }
            }
          } catch (dbErr) {
            console.error('Supabase scan persist error:', dbErr);
          }
        }
      }
    } catch (err) {
      setErrorMsg('Failed to fetch evaluation report.');
    }
  };

  const handleStartUpload = async (file: File, psId: string) => {
    setStatus('processing');
    setErrorMsg(null);
    setUploadedFileName(file.name);
    setProgressMsg('Uploading presentation file...');
    setProgressPct(15);

    const formData = new FormData();
    formData.append('file', file);
    if (psId) formData.append('ps_id', psId);


    try {
      const res = await fetch('/api/v1/submissions/upload', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Upload failed. Please check file format.');
      }

      const data = await res.json();
      setSubmissionId(data.submission_id);
    } catch (err: any) {
      setStatus('failed');
      setErrorMsg(err.message || 'Error uploading file.');
    }
  };

  const handleReset = () => {
    setSubmissionId(null);
    setStatus('idle');
    setReport(null);
    setErrorMsg(null);
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden bg-[#FDFBF7] selection:bg-orange-500 selection:text-white">
      {/* Subtle Ambient Decorative Gradient Blobs */}
      <div className="absolute top-[-5%] left-[-10%] w-[45%] h-[45%] rounded-full bg-orange-400/10 blur-[130px] pointer-events-none mix-blend-multiply" />
      <div className="absolute top-[20%] right-[-10%] w-[40%] h-[40%] rounded-full bg-emerald-400/10 blur-[130px] pointer-events-none mix-blend-multiply" />
      <div className="absolute bottom-[-10%] left-[20%] w-[50%] h-[50%] rounded-full bg-slate-300/20 blur-[140px] pointer-events-none mix-blend-multiply" />

      <Header />

      <main className="flex-1 px-4 sm:px-6 lg:px-8 py-6 relative z-10">
        {status === 'idle' && (
          <UploadSection onStartUpload={handleStartUpload} />
        )}

        {status === 'processing' && (
          <ProgressTracker stepMessage={progressMsg} progressPct={progressPct} />
        )}

        {status === 'completed' && report && (
          <ReportDashboard report={report} onReset={handleReset} />
        )}

        {status === 'failed' && (
          <div className="w-full max-w-lg mx-auto my-16 p-8 rounded-3xl bg-white/80 backdrop-blur-2xl shadow-[0_20px_60px_rgba(0,0,0,0.06)] border border-red-200/80 text-center space-y-5 animate-in fade-in zoom-in-95 duration-300">
            <div className="w-14 h-14 rounded-2xl bg-red-50 text-red-500 flex items-center justify-center mx-auto border border-red-100 shadow-sm">
              <AlertCircle className="w-7 h-7" />
            </div>
            <div className="space-y-1">
              <h3 className="text-xl font-extrabold text-slate-900 tracking-tight">Scan Failed</h3>
              <p className="text-sm text-slate-500">{errorMsg}</p>
            </div>
            <button
              onClick={handleReset}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold bg-slate-900 hover:bg-slate-800 text-white shadow-md hover:shadow-lg transition-all"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Try Again</span>
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
