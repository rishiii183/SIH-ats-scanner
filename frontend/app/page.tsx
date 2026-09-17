'use client';

import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { UploadSection } from './components/UploadSection';
import { ProgressTracker } from './components/ProgressTracker';
import { ReportDashboard } from './components/ReportDashboard';

export default function Home() {
  const [submissionId, setSubmissionId] = useState<string | null>(null);
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
      }
    } catch (err) {
      setErrorMsg('Failed to fetch evaluation report.');
    }
  };

  const handleStartUpload = async (file: File, psId: string) => {
    setStatus('processing');
    setErrorMsg(null);
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
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 px-4 sm:px-6 lg:px-8 py-6">
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
          <div className="w-full max-w-lg mx-auto my-12 p-8 rounded-2xl glass-panel border border-red-500/30 text-center space-y-4">
            <div className="w-12 h-12 rounded-full bg-red-500/10 text-red-400 flex items-center justify-center mx-auto font-bold text-xl">
              !
            </div>
            <h3 className="text-lg font-bold text-white">Scan Failed</h3>
            <p className="text-xs text-slate-400">{errorMsg}</p>
            <button
              onClick={handleReset}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 text-slate-200 border border-slate-700 hover:bg-slate-700"
            >
              Try Again
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
