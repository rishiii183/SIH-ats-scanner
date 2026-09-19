'use client';

import React, { useState, useEffect } from 'react';
import { UploadCloud, FileText, CheckCircle2, Search, AlertCircle, PlusCircle, HelpCircle, ChevronDown, ChevronUp, Sparkles, ArrowRight, ShieldCheck, Zap } from 'lucide-react';
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
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);

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

  const selectedProblem = problemStatements.find(ps => ps.id === selectedPsId);

  return (
    <div className="w-full max-w-4xl mx-auto my-6 sm:my-10 p-6 sm:p-10 rounded-3xl bg-white/75 backdrop-blur-2xl border border-white/80 shadow-[0_24px_70px_rgba(15,23,42,0.06)] relative overflow-hidden">
      
      {/* Decorative inner glow */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-gradient-to-br from-orange-400/10 to-transparent rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />

      <div className="relative z-10">
        {/* Header Title Section */}
        <div className="text-center mb-10 space-y-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-orange-50 border border-orange-200/80 text-orange-600 text-xs font-bold tracking-wide shadow-sm">
            <Sparkles className="w-3.5 h-3.5 text-orange-500 animate-pulse" />
            <span>SIH 2026 OFFICIAL RUBRIC EVALUATOR</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-slate-900">
            Check Your SIH Deck{' '}
            <span className="bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 bg-clip-text text-transparent">
              Before Submitting
            </span>
          </h1>
          <p className="text-slate-500 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
            Get an instant ATS score, slide-by-slide jury feedback, and rewrite recommendations against the strict 6-slide Smart India Hackathon guidelines.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          
          {/* Step 1: Problem Statement Selector */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-orange-500 text-white text-[11px] font-extrabold flex items-center justify-center shadow-sm">
                  1
                </span>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Select Problem Statement ({problemStatements.length} Loaded)
                </label>
              </div>
              <span className="text-[11px] font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                Verified SIH 2026 Bank
              </span>
            </div>

            <div className="relative">
              <button
                type="button"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="w-full flex items-center justify-between px-4 py-3.5 bg-white/90 backdrop-blur-md border border-slate-200 rounded-2xl text-sm text-slate-800 shadow-sm hover:border-orange-300 hover:shadow-md transition-all focus:outline-none focus:ring-4 focus:ring-orange-500/10 focus:border-orange-400 text-left group"
              >
                <div className="truncate pr-4 flex items-center gap-2.5">
                  {isCustomPs ? (
                    <span className="font-bold text-orange-600 flex items-center gap-1.5">
                      <PlusCircle className="w-4 h-4" /> Custom Problem Statement
                    </span>
                  ) : selectedProblem ? (
                    <div className="flex items-center gap-2 truncate">
                      <span className="font-black text-orange-500 bg-orange-50 px-2 py-0.5 rounded-lg border border-orange-200 text-xs shrink-0">
                        {selectedProblem.ps_id}
                      </span>
                      <span className="font-semibold text-slate-800 truncate">
                        {selectedProblem.title}
                      </span>
                    </div>
                  ) : (
                    <span className="text-slate-400">Select a Problem Statement...</span>
                  )}
                </div>
                {isDropdownOpen ? (
                  <ChevronUp className="w-5 h-5 text-slate-400 shrink-0 group-hover:text-slate-600 transition-colors" />
                ) : (
                  <ChevronDown className="w-5 h-5 text-slate-400 shrink-0 group-hover:text-slate-600 transition-colors" />
                )}
              </button>

              {/* Dropdown Menu */}
              {isDropdownOpen && (
                <div className="absolute z-50 w-full mt-2 bg-white/95 backdrop-blur-3xl border border-slate-200/90 shadow-[0_20px_60px_rgba(15,23,42,0.12)] rounded-2xl overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
                  <div className="p-3 border-b border-slate-100 bg-slate-50/70">
                    <div className="relative">
                      <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                      <input
                        type="text"
                        placeholder="Search PS ID, Theme, or Title..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-500/20 transition-all shadow-sm"
                      />
                    </div>
                  </div>

                  <div className="w-full max-h-72 overflow-y-auto space-y-1 p-2">
                    <div
                      onClick={() => {
                        setIsCustomPs(true);
                        setSelectedPsId('CUSTOM');
                        setIsDropdownOpen(false);
                      }}
                      className={`p-3 rounded-xl cursor-pointer text-xs transition-all border ${
                        selectedPsId === 'CUSTOM'
                          ? 'bg-orange-50 border-orange-200 shadow-sm'
                          : 'border-transparent hover:bg-slate-50'
                      }`}
                    >
                      <div className="font-bold text-orange-600 flex items-center gap-2">
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
                          setIsDropdownOpen(false);
                        }}
                        className={`p-3 rounded-xl cursor-pointer transition-all border ${
                          selectedPsId === ps.id
                            ? 'bg-orange-50/90 border-orange-200 shadow-sm'
                            : 'border-transparent hover:bg-slate-50'
                        }`}
                      >
                        <div className="font-bold text-slate-800 text-xs">
                          <span className="text-orange-500 mr-2 font-black">[{ps.ps_id}]</span>
                          {ps.title}
                        </div>
                        <div className="text-[11px] text-slate-500 mt-1.5 flex flex-wrap items-center gap-2">
                          <span className="bg-white px-2 py-0.5 rounded-full border border-slate-200 font-medium">
                            {ps.theme}
                          </span>
                          <span className="bg-slate-100 px-2 py-0.5 rounded-full text-slate-600 uppercase font-bold text-[10px]">
                            {ps.category}
                          </span>
                        </div>
                      </div>
                    ))}

                    {filteredPs.length === 0 && (
                      <div className="p-4 text-center text-xs text-slate-400 font-medium">
                        No problem statements matching your search.
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Custom PS Textarea */}
            {isCustomPs && (
              <div className="p-4 rounded-2xl bg-orange-50/80 border border-orange-200/80 space-y-2 animate-in fade-in">
                <div className="flex items-center gap-1.5 text-xs text-orange-700 font-bold">
                  <PlusCircle className="w-4 h-4" />
                  <span>Enter Custom Problem Statement Title & Context</span>
                </div>
                <textarea
                  rows={3}
                  placeholder="Type or paste your problem statement description here..."
                  value={customPsText}
                  onChange={(e) => setCustomPsText(e.target.value)}
                  className="w-full p-3 bg-white border border-slate-200 shadow-sm rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20"
                />
              </div>
            )}
          </div>

          {/* Step 2: Drag and Drop Upload Area */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-orange-500 text-white text-[11px] font-extrabold flex items-center justify-center shadow-sm">
                  2
                </span>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Upload Presentation File (.pptx or .pdf)
                </label>
              </div>
              <span className="text-[11px] text-slate-400 font-medium">Max 25MB • Up to 6 Slides</span>
            </div>

            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-3xl p-8 sm:p-12 text-center transition-all cursor-pointer relative group ${
                dragActive
                  ? 'border-orange-500 bg-orange-50/80 scale-[1.01] shadow-lg shadow-orange-500/10'
                  : file
                  ? 'border-emerald-400 bg-emerald-50/70 shadow-sm'
                  : 'border-slate-300/80 hover:border-orange-400 bg-white/60 hover:bg-orange-50/20'
              }`}
            >
              <input
                type="file"
                accept=".pptx,.pdf"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-20"
              />

              {file ? (
                <div className="flex flex-col items-center justify-center gap-2.5 animate-in zoom-in-95 duration-200">
                  <div className="w-14 h-14 rounded-2xl bg-emerald-100/80 border border-emerald-200 flex items-center justify-center text-emerald-600 shadow-sm">
                    <CheckCircle2 className="w-7 h-7" />
                  </div>
                  <div className="space-y-0.5">
                    <p className="font-bold text-slate-800 text-sm sm:text-base">{file.name}</p>
                    <p className="text-xs font-medium text-emerald-600">
                      {(file.size / (1024 * 1024)).toFixed(2)} MB • File Ready for ATS Evaluation
                    </p>
                  </div>
                  <span className="text-[11px] text-slate-400 underline pt-1 group-hover:text-slate-600">
                    Click or drop another file to replace
                  </span>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center gap-3.5">
                  <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-orange-100 to-orange-50 flex items-center justify-center text-orange-500 border border-orange-200/80 shadow-sm group-hover:scale-110 group-hover:text-orange-600 transition-all">
                    <UploadCloud className="w-8 h-8" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm sm:text-base font-bold text-slate-800">
                      Drag & drop your presentation here, or{' '}
                      <span className="text-orange-600 underline underline-offset-2 hover:text-orange-700">browse</span>
                    </p>
                    <p className="text-xs text-slate-500">
                      Accepted formats: <strong className="text-slate-700 font-semibold">PPTX</strong> (PowerPoint) and <strong className="text-slate-700 font-semibold">PDF</strong>
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Error Message */}
          {errorMsg && (
            <div className="p-4 bg-red-50/90 border border-red-200 rounded-2xl text-xs font-semibold text-red-600 flex items-center gap-2.5 animate-in fade-in slide-in-from-top-1">
              <AlertCircle className="w-4 h-4 shrink-0 text-red-500" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Submit Action Button */}
          <button
            type="submit"
            disabled={!file}
            className={`w-full py-4 px-6 rounded-2xl font-bold text-sm sm:text-base shadow-xl transition-all flex items-center justify-center gap-3 relative overflow-hidden group ${
              file
                ? 'bg-gradient-to-r from-orange-500 via-orange-600 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-orange-500/25 cursor-pointer hover:shadow-2xl hover:scale-[1.01]'
                : 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200 shadow-none'
            }`}
          >
            {file && (
              <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
            )}
            <FileText className="w-5 h-5" />
            <span>Scan & Evaluate Deck Against SIH Rubric</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </form>

        {/* Guidelines / Accordion Section */}
        <div className="mt-14 border-t border-slate-200/80 pt-8">
          <h3 className="text-center text-xs font-bold text-slate-500 mb-6 uppercase tracking-widest flex items-center justify-center gap-2">
            <HelpCircle className="w-4 h-4 text-orange-500" />
            <span>SIH 2026 Presentation Rules & Guidelines</span>
          </h3>
          <AccordionApp items={[
            { 
              id: 1, 
              title: 'What is the official SIH 2026 Slide Cap?', 
              icon: <ShieldCheck className="w-5 h-5 text-orange-500" />, 
              content: 'The official SIH Idea Presentation format permits a maximum of 6 slides. Decks exceeding 6 slides receive automated penalty deductions in preliminary jury screening.' 
            },
            { 
              id: 2, 
              title: 'What mandatory slides must be included?', 
              icon: <CheckCircle2 className="w-5 h-5 text-emerald-500" />, 
              content: '1. Title & Team, 2. Problem Statement & Background, 3. Proposed Solution, 4. Technical Approach / Architecture, 5. Impact & Feasibility, 6. References & Team Details.' 
            },
            { 
              id: 3, 
              title: 'How does our AI evaluate technical feasibility?', 
              icon: <Zap className="w-5 h-5 text-amber-500" />, 
              content: 'Our ATS checks for explicit technology stacks (frameworks, databases, ML models, hardware controllers) and architecture flowcharts rather than vague buzzwords.' 
            }
          ]} />
        </div>

      </div>
    </div>
  );
};
