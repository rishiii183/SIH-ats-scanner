'use client';

import React, { useState, useEffect } from 'react';
import { UploadCloud, FileText, CheckCircle2, Search, AlertCircle } from 'lucide-react';

interface ProblemStatement {
  id: string;
  ps_id: string;
  title: string;
  theme: string;
  category: string;
}

interface UploadSectionProps {
  onStartUpload: (file: File, psId: string) => void;
}

export const UploadSection: React.FC<UploadSectionProps> = ({ onStartUpload }) => {
  const [file, setFile] = useState<File | null>(null);
  const [problemStatements, setProblemStatements] = useState<ProblemStatement[]>([]);
  const [selectedPsId, setSelectedPsId] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [dragActive, setDragActive] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string>('');

  useEffect(() => {
    // Fetch problem statements from API
    fetch('/api/v1/problem-statements')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setProblemStatements(data);
          if (data.length > 0) setSelectedPsId(data[0].id);
        }
      })
      .catch(() => {
        // Fallback default list
        setProblemStatements([
          { id: 'ps-101', ps_id: 'SIH26101', title: 'AI-Based Smart Traffic Management System for Urban Cities', theme: 'Smart Cities', category: 'software' },
          { id: 'ps-102', ps_id: 'SIH26102', title: 'Automated Resume and Presentation ATS Evaluator', theme: 'EdTech', category: 'software' },
          { id: 'ps-103', ps_id: 'SIH26103', title: 'Blockchain-Based Supply Chain Transparency for Agriculture Products', theme: 'AgriTech', category: 'software' }
        ]);
      });
  }, []);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateAndSetFile = (selectedFile: File) => {
    setErrorMsg('');
    const ext = selectedFile.name.split('.').pop()?.toLowerCase();
    if (ext !== 'pptx' && ext !== 'pdf') {
      setErrorMsg('Invalid file format. Please upload a .pptx or .pdf presentation file.');
      return;
    }
    if (selectedFile.size > 25 * 1024 * 1024) {
      setErrorMsg('File size exceeds 25MB official limit.');
      return;
    }
    setFile(selectedFile);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setErrorMsg('Please select a presentation file to scan.');
      return;
    }
    onStartUpload(file, selectedPsId);
  };

  const filteredPs = problemStatements.filter(
    (ps) =>
      ps.ps_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ps.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ps.theme.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="w-full max-w-4xl mx-auto my-8 p-6 sm:p-8 rounded-2xl glass-panel border border-slate-800 shadow-2xl relative overflow-hidden">
      {/* Background ambient glow */}
      <div className="absolute -top-24 -left-24 w-72 h-72 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -right-24 w-72 h-72 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10">
        <div className="text-center mb-8">
          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white mb-2">
            Check Your SIH Deck <span className="bg-gradient-to-r from-indigo-400 to-emerald-400 bg-clip-text text-transparent">Before Submitting</span>
          </h1>
          <p className="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto">
            Get an instant, line-by-line ATS score against the official SIH 2026 rubric (max 6 slides, technical depth, section structure).
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Step 1: Problem Statement Selector */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
              1. Select Problem Statement
            </label>
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search PS ID or Title (e.g. SIH26101)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 bg-slate-900/80 border border-slate-700/80 rounded-xl text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
              />
            </div>
            
            <select
              value={selectedPsId}
              onChange={(e) => setSelectedPsId(e.target.value)}
              className="w-full py-2.5 px-3 bg-slate-900 border border-slate-700/80 rounded-xl text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
            >
              {filteredPs.length > 0 ? (
                filteredPs.map((ps) => (
                  <option key={ps.id} value={ps.id}>
                    [{ps.ps_id}] {ps.title} ({ps.theme})
                  </option>
                ))
              ) : (
                <option value="">General Track / Custom Problem Statement</option>
              )}
            </select>
          </div>

          {/* Step 2: File Upload Dropzone */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300">
              2. Upload Presentation (.pptx or .pdf)
            </label>
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer relative ${
                dragActive
                  ? 'border-indigo-500 bg-indigo-500/10 scale-[1.01]'
                  : file
                  ? 'border-emerald-500/50 bg-emerald-500/5'
                  : 'border-slate-700 hover:border-slate-500 bg-slate-900/50'
              }`}
            >
              <input
                type="file"
                accept=".pptx,.pdf"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />

              {file ? (
                <div className="flex flex-col items-center justify-center gap-2">
                  <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 mb-1">
                    <CheckCircle2 className="w-6 h-6" />
                  </div>
                  <p className="font-semibold text-slate-100 text-sm">{file.name}</p>
                  <p className="text-xs text-slate-400">
                    {(file.size / (1024 * 1024)).toFixed(2)} MB • Ready to Scan
                  </p>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center gap-3">
                  <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 border border-indigo-500/20">
                    <UploadCloud className="w-7 h-7" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-200">
                      Drag & drop your presentation here, or <span className="text-indigo-400 underline">browse</span>
                    </p>
                    <p className="text-xs text-slate-500 mt-1">Supports PPTX and PDF files up to 25MB (Max 6 slides recommended)</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {errorMsg && (
            <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-xs text-red-400 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!file}
            className={`w-full py-3.5 px-6 rounded-xl font-bold text-sm text-white shadow-xl transition-all flex items-center justify-center gap-2 ${
              file
                ? 'bg-gradient-to-r from-indigo-600 via-indigo-500 to-emerald-500 hover:opacity-95 shadow-indigo-500/25 cursor-pointer'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Scan & Evaluate Deck Against SIH Rubric</span>
          </button>
        </form>
      </div>
    </div>
  );
};
