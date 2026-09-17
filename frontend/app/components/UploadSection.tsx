'use client';

import React, { useState, useEffect } from 'react';
import { UploadCloud, FileText, CheckCircle2, Search, AlertCircle, PlusCircle, HelpCircle } from 'lucide-react';
import { AccordionApp } from '@/components/card-split-accordian';

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
  const [isCustomPs, setIsCustomPs] = useState<boolean>(false);
  const [customPsText, setCustomPsText] = useState<string>('');
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
    onStartUpload(file, isCustomPs ? 'CUSTOM' : selectedPsId);
  };

  const filteredPs = problemStatements.filter(
    (ps) =>
      ps.ps_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ps.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ps.theme.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="w-full max-w-4xl mx-auto my-8 p-6 sm:p-8 rounded-2xl bg-white border border-slate-200 shadow-xl relative overflow-hidden">
      <div className="relative z-10">
        <div className="text-center mb-8">
          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-slate-900 mb-2">
            Check Your SIH Deck <span className="bg-gradient-to-r from-orange-500 to-orange-400 bg-clip-text text-transparent">Before Submitting</span>
          </h1>
          <p className="text-slate-500 text-sm sm:text-base max-w-2xl mx-auto">
            Get an instant, line-by-line ATS score against the official SIH 2026 rubric (max 6 slides, technical depth, section structure).
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Step 1: Problem Statement Selector */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600">
                1. Select Official Problem Statement ({problemStatements.length} Available)
              </label>
              <span className="text-[11px] text-orange-500 font-medium">Updated for SIH 2026</span>
            </div>

            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search PS ID or Title (e.g. SIH26101, MedTech, Smart Cities)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-colors shadow-sm"
              />
            </div>

            <div className="w-full max-h-64 overflow-y-auto bg-slate-50 border border-slate-200 rounded-xl space-y-1 p-2">
              <div
                onClick={() => {
                  setIsCustomPs(true);
                  setSelectedPsId('CUSTOM');
                }}
                className={`p-3 rounded-lg cursor-pointer text-sm transition-colors border ${selectedPsId === 'CUSTOM'
                    ? 'bg-orange-50 border-orange-200'
                    : 'border-transparent hover:bg-slate-100'
                  }`}
              >
                <div className="font-semibold text-orange-600 flex items-center gap-2">
                  <PlusCircle className="w-4 h-4" />
                  + Paste Custom / College Problem Statement
                </div>
              </div>

              {filteredPs.map((ps) => (
                <div
                  key={ps.id}
                  onClick={() => {
                    setIsCustomPs(false);
                    setSelectedPsId(ps.id);
                  }}
                  className={`p-3 rounded-lg cursor-pointer transition-colors border ${selectedPsId === ps.id
                      ? 'bg-orange-50 border-orange-200'
                      : 'border-transparent hover:bg-slate-100'
                    }`}
                >
                  <div className="font-semibold text-slate-800 text-sm">
                    <span className="text-orange-500 mr-2">[{ps.ps_id}]</span>
                    {ps.title}
                  </div>
                  <div className="text-xs text-slate-500 mt-1.5 flex flex-wrap items-center gap-2">
                    <span className="bg-white px-2.5 py-0.5 rounded-full border border-slate-200">{ps.theme}</span>
                    <span className="bg-white px-2.5 py-0.5 rounded-full border border-slate-200 uppercase">{ps.category}</span>
                  </div>
                </div>
              ))}

              {filteredPs.length === 0 && (
                <div className="p-4 text-center text-sm text-slate-500">
                  No problem statements found matching your search.
                </div>
              )}
            </div>

            {/* Custom PS Input Box if Custom selected */}
            {isCustomPs && (
              <div className="p-4 rounded-xl bg-orange-50 border border-orange-100 space-y-2 animate-in fade-in">
                <div className="flex items-center gap-1.5 text-xs text-orange-600 font-semibold">
                  <PlusCircle className="w-4 h-4" />
                  <span>Custom / Local Problem Statement Details</span>
                </div>
                <textarea
                  rows={3}
                  placeholder="Paste your custom problem statement title & description here..."
                  value={customPsText}
                  onChange={(e) => setCustomPsText(e.target.value)}
                  className="w-full p-2.5 bg-white border border-slate-200 shadow-sm rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500"
                />
              </div>
            )}
          </div>

          {/* Step 2: File Upload Dropzone */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600">
              2. Upload Presentation (.pptx or .pdf)
            </label>
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer relative ${dragActive
                  ? 'border-orange-500 bg-orange-50 scale-[1.01]'
                  : file
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-slate-300 hover:border-slate-400 bg-slate-50'
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
                  <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 mb-1">
                    <CheckCircle2 className="w-6 h-6" />
                  </div>
                  <p className="font-semibold text-slate-800 text-sm">{file.name}</p>
                  <p className="text-xs text-slate-500">
                    {(file.size / (1024 * 1024)).toFixed(2)} MB • Ready to Scan
                  </p>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center gap-3">
                  <div className="w-14 h-14 rounded-2xl bg-orange-100 flex items-center justify-center text-orange-500 border border-orange-200">
                    <UploadCloud className="w-7 h-7" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-700">
                      Drag & drop your presentation here, or <span className="text-orange-600 underline">browse</span>
                    </p>
                    <p className="text-xs text-slate-500 mt-1">Supports PPTX and PDF files up to 25MB (Max 6 slides recommended)</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {errorMsg && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!file}
            className={`w-full py-3.5 px-6 rounded-xl font-bold text-sm shadow-xl transition-all flex items-center justify-center gap-2 ${file
                ? 'bg-orange-500 hover:bg-orange-600 text-white shadow-orange-500/20 cursor-pointer'
                : 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200 shadow-none'
              }`}
          >
            <FileText className="w-4 h-4" />
            <span>Scan & Evaluate Deck Against SIH Rubric</span>
          </button>
        </form>

        <div className="mt-12 border-t border-slate-200 pt-8">
          <h3 className="text-center text-sm font-semibold text-slate-500 mb-4 uppercase tracking-widest flex items-center justify-center gap-2">
            <HelpCircle className="w-4 h-4" /> FAQ & Guidelines
          </h3>
          <AccordionApp items={[
            { id: 1, title: 'What is SIH ATS Scanner?', icon: <Search className="w-5 h-5 text-orange-500" />, content: 'A Smart India Hackathon specialized tool to evaluate your presentation deck against the official judging criteria.' },
            { id: 2, title: 'How does scoring work?', icon: <CheckCircle2 className="w-5 h-5 text-emerald-500" />, content: 'Scores are generated by an AI analyzing Clarity, Innovation, Technical Feasibility, and Impact based on the SIH 2026 rubric.' },
            { id: 3, title: 'What format should I upload?', icon: <FileText className="w-5 h-5 text-blue-500" />, content: 'PDF and PPTX formats are supported. We recommend keeping it strictly under 6 slides to match SIH rules.' }
          ]} />
        </div>
      </div>
    </div>
  );
};
