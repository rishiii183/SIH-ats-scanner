import type { Metadata } from 'next';
import Link from 'next/link';
import { Header } from '../components/Header';
import { FileCheck, ArrowRight, AlertTriangle, ShieldCheck } from 'lucide-react';
import { JsonLd } from '../components/JsonLd';
import { organizationSchema } from '../components/SeoSchemas';

export const metadata: Metadata = {
  title: 'SIH 2026 PPT Format Guidelines & Slide Checklist — SIH ATS Scanner',
  description: 'Official Smart India Hackathon 2026 presentation format guidelines. Check mandatory slide titles, 6-slide ceiling limit, visual diagram rules, and tech stack details.',
  openGraph: {
    title: 'SIH 2026 PPT Format Guidelines & Slide Checklist',
    description: 'Official Smart India Hackathon 2026 presentation format guidelines. Check mandatory slide titles, 6-slide limit, visual diagram rules, and tech stack details.',
    type: 'website',
    url: 'https://sih-ats-scanner.vercel.app/guidelines',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SIH 2026 PPT Format Guidelines & Slide Checklist',
    description: 'Official Smart India Hackathon 2026 presentation format guidelines. Check mandatory slide titles, 6-slide limit, visual diagram rules, and tech stack details.',
  },
};

export default function GuidelinesPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#FDFBF7] text-slate-800 selection:bg-orange-500 selection:text-white">
      <JsonLd data={organizationSchema} />
      <Header />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-8 space-y-8">
        <div className="bg-white p-6 sm:p-10 rounded-3xl border border-slate-200 shadow-xs space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-50 text-orange-600 border border-orange-200 text-xs font-bold">
            <FileCheck className="w-3.5 h-3.5" />
            <span>SIH 2026 Format Standard</span>
          </div>

          <h1 className="text-3xl font-black text-slate-900 tracking-tight">
            Smart India Hackathon 2026 PPT Format Guidelines & Checklist
          </h1>

          <p className="text-sm text-slate-600 leading-relaxed">
            <strong>The Smart India Hackathon (SIH 2026) mandates a strict 6-slide presentation deck format.</strong> Submitting pitch decks that exceed the 6-slide ceiling or miss required section headings results in automatic disqualification during preliminary screening.
          </p>

          <div className="space-y-4 pt-4 border-t border-slate-100">
            <h2 className="text-xl font-extrabold text-slate-900">Mandatory 6-Slide Structure</h2>
            <ul className="space-y-3 text-xs text-slate-700">
              <li className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong>Slide 1: Title Slide</strong> — Team Name, Leader Contact, PS ID, Theme/Category.
              </li>
              <li className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong>Slide 2: Problem Statement</strong> — Background context, target beneficiaries, real-world pain points.
              </li>
              <li className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong>Slide 3: Proposed Solution</strong> — Innovation summary, unique value proposition, key features.
              </li>
              <li className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong>Slide 4: Technical Approach</strong> — Specific tech stack (frameworks, database, ML models, architecture flowchart).
              </li>
              <li className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong>Slide 5: Impact & Feasibility</strong> — Measurable outcomes, scalability plan, social/economic benefits.
              </li>
              <li className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <strong>Slide 6: References & Team</strong> — Team member roles, mentor details, citations.
              </li>
            </ul>
          </div>

          <div className="space-y-3 pt-4 border-t border-slate-100">
            <h2 className="text-xl font-extrabold text-slate-900 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              <span>Top 3 Common Rejection Flags</span>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="p-4 bg-red-50/60 rounded-2xl border border-red-200 space-y-1">
                <span className="text-xs font-bold text-red-900">Exceeding 6 Slides</span>
                <p className="text-[11px] text-red-700">Decks with 7+ slides violate the ceiling limit and lose format compliance points instantly.</p>
              </div>
              <div className="p-4 bg-amber-50/60 rounded-2xl border border-amber-200 space-y-1">
                <span className="text-xs font-bold text-amber-900">Paragraph Text Walls</span>
                <p className="text-[11px] text-amber-700">Slides containing &gt;70 words of dense paragraph text cause evaluator fatigue.</p>
              </div>
              <div className="p-4 bg-blue-50/60 rounded-2xl border border-blue-200 space-y-1">
                <span className="text-xs font-bold text-blue-900">Vague Tech Stack</span>
                <p className="text-[11px] text-blue-700">Listing generic terms like "AI and Database" instead of naming specific tools like "FastAPI & PostgreSQL".</p>
              </div>
            </div>
          </div>

          <div className="pt-6 flex justify-between items-center border-t border-slate-200">
            <Link href="/" className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition-all">
              <span>Scan Your Presentation Now</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
