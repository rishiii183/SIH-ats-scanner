import React from 'react';
import Link from 'next/link';
import { CheckCircle2, ShieldCheck, FileText, Cpu, Clock, HelpCircle } from 'lucide-react';
import { JsonLd } from './JsonLd';
import { softwareAppSchema, faqPageSchema } from './SeoSchemas';

export const LandingContent: React.FC = () => {
  return (
    <section className="w-full max-w-5xl mx-auto my-12 space-y-12 px-4 sm:px-6">
      {/* JSON-LD Structured Data Injection */}
      <JsonLd data={[softwareAppSchema, faqPageSchema]} />

      {/* Freshness Badge */}
      <div className="flex items-center justify-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold shadow-2xs">
          <Clock className="w-3.5 h-3.5 text-emerald-600" />
          <span>Last updated: September 2026 — Scored against SIH 2026 official format rules</span>
        </div>
      </div>

      {/* GEO Answer-First Content Block */}
      <article className="bg-white/80 backdrop-blur-xl border border-slate-200/80 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          Smart India Hackathon (SIH 2026) Pitch Deck ATS Evaluator
        </h1>
        <p className="text-base text-slate-700 leading-relaxed font-normal">
          <strong>SIH ATS Scanner evaluates Smart India Hackathon (SIH 2026) pitch presentation decks against official format rules.</strong> It automatically audits slide count ceilings, mandatory section headings, presentation clarity, technical depth specificity, and problem statement alignment before submission.
        </p>
      </article>

      {/* Verifiable Specific Facts Grid */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-orange-500" />
          <span>5 Core Evaluation Pillars Scored by SIH ATS</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs space-y-2">
            <h3 className="font-extrabold text-sm text-slate-900 flex items-center gap-2">
              <FileText className="w-4 h-4 text-orange-500" />
              1. Structure & Format (Hard Check)
            </h3>
            <p className="text-xs text-slate-600 leading-normal">
              Audits maximum 6-slide ceiling limit, mandatory section titles (Title, Problem, Solution, Technical Approach, Impact, References), and file size under 25MB.
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs space-y-2">
            <h3 className="font-extrabold text-sm text-slate-900 flex items-center gap-2">
              <FileText className="w-4 h-4 text-emerald-500" />
              2. Presentation Clarity (Hard Check)
            </h3>
            <p className="text-xs text-slate-600 leading-normal">
              Ensures slide word density stays under 70 words per slide and verifies visual diagrams on technical slides.
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs space-y-2">
            <h3 className="font-extrabold text-sm text-slate-900 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-blue-500" />
              3. PS Alignment (Estimated)
            </h3>
            <p className="text-xs text-slate-600 leading-normal">
              Computes SentenceTransformers cosine similarity between presentation text and target problem statement descriptions.
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs space-y-2">
            <h3 className="font-extrabold text-sm text-slate-900 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-purple-500" />
              4. Technical Depth (Estimated)
            </h3>
            <p className="text-xs text-slate-600 leading-normal">
              Audits a 4-point technical checklist: named frameworks/languages, explicit database/storage, named ML models, and workflow architecture.
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs space-y-2">
            <h3 className="font-extrabold text-sm text-slate-900 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-amber-500" />
              5. Originality & Boilerplate (Estimated)
            </h3>
            <p className="text-xs text-slate-600 leading-normal">
              Scans for unreplaced template placeholder strings ("Lorem Ipsum", "Insert Text Here") and checks corpus uniqueness.
            </p>
          </div>
        </div>
      </div>

      {/* Crawlable Visible FAQ Section matching FAQPage Schema */}
      <div className="space-y-4 pt-4 border-t border-slate-200">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <HelpCircle className="w-5 h-5 text-orange-500" />
          <span>Frequently Asked Questions</span>
        </h2>
        <div className="space-y-3">
          <details className="group bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs [&_summary::-webkit-details-marker]:hidden" open>
            <summary className="flex items-center justify-between font-bold text-sm text-slate-900 cursor-pointer">
              <span>What does SIH ATS Scanner check in a Smart India Hackathon PPT?</span>
              <span className="ml-2 text-slate-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <p className="mt-3 text-xs text-slate-600 leading-relaxed">
              SIH ATS Scanner currently performs live automated screening for Structure & Format (6-slide ceiling limit, mandatory section headings), Presentation Clarity (word count density under 70 words per slide, visual diagram checks), and Problem Statement Alignment (semantic domain similarity). Technical Depth (AI checklist audit) and Originality (corpus comparison) require API key and dataset configuration, and are excluded with renormalized weights when unconfigured.
            </p>
          </details>

          <details className="group bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs [&_summary::-webkit-details-marker]:hidden">
            <summary className="flex items-center justify-between font-bold text-sm text-slate-900 cursor-pointer">
              <span>Is SIH ATS Scanner officially affiliated with Smart India Hackathon (SIH)?</span>
              <span className="ml-2 text-slate-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <p className="mt-3 text-xs text-slate-600 leading-relaxed">
              No. SIH ATS Scanner is an independent screening tool built for participants. It is not officially affiliated with, endorsed by, or sponsored by Smart India Hackathon (SIH), AICTE, or the Ministry of Education (MoE), Government of India.
            </p>
          </details>

          <details className="group bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs [&_summary::-webkit-details-marker]:hidden">
            <summary className="flex items-center justify-between font-bold text-sm text-slate-900 cursor-pointer">
              <span>What file formats are supported for evaluation?</span>
              <span className="ml-2 text-slate-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <p className="mt-3 text-xs text-slate-600 leading-relaxed">
              The scanner supports Microsoft PowerPoint (.pptx) and PDF (.pdf) documents up to 25MB in size.
            </p>
          </details>

          <details className="group bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs [&_summary::-webkit-details-marker]:hidden">
            <summary className="flex items-center justify-between font-bold text-sm text-slate-900 cursor-pointer">
              <span>How is technical depth evaluated?</span>
              <span className="ml-2 text-slate-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <p className="mt-3 text-xs text-slate-600 leading-relaxed">
              When an AI key is configured, Technical Depth is evaluated using a 4-point checklist checking for specific frameworks named, database technology specified, ML models, and workflow architecture. If unconfigured, Technical Depth is marked as unassessed and excluded from the total score without penalizing the deck.
            </p>
          </details>
        </div>
      </div>

      {/* Internal Linking & Resources Navigation Section */}
      <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 space-y-4">
        <h2 className="text-lg font-bold text-white tracking-tight">SIH Participant Resources & Guidelines</h2>
        <p className="text-xs text-slate-300">
          Explore essential guides and tools for optimizing your Smart India Hackathon presentation before final portal submission:
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Link href="/guidelines" className="px-4 py-2 rounded-xl bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold transition-all">
            SIH 2026 Format Guidelines & Checklist →
          </Link>
          <Link href="/faq" className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition-all border border-slate-700">
            Frequently Asked Questions →
          </Link>
          <Link href="/upgrade" className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold transition-all border border-slate-700">
            Pro Pricing & Batch Scanning →
          </Link>
        </div>
      </div>

      {/* Crawlable Non-Affiliation Disclaimer */}
      <div className="text-center text-xs text-slate-500 pt-4 border-t border-slate-200 space-y-1">
        <p><strong>Non-Affiliation Notice:</strong> SIH ATS Scanner is an independent educational tool developed for Smart India Hackathon participants.</p>
        <p>It is not affiliated with, authorized, maintained, sponsored, or endorsed by AICTE, Ministry of Education, or Government of India.</p>
      </div>
    </section>
  );
};
