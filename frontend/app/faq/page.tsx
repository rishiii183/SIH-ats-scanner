import type { Metadata } from 'next';
import Link from 'next/link';
import { Header } from '../components/Header';
import { HelpCircle, ArrowRight } from 'lucide-react';
import { JsonLd } from '../components/JsonLd';
import { faqPageSchema, organizationSchema } from '../components/SeoSchemas';

export const metadata: Metadata = {
  title: 'SIH ATS Scanner FAQ — Pitch Deck Scoring & Evaluation Rules',
  description: 'Frequently asked questions about Smart India Hackathon (SIH 2026) presentation scoring, slide limits, technical checklists, and problem statement alignment.',
  openGraph: {
    title: 'SIH ATS Scanner FAQ — Pitch Deck Scoring Rules',
    description: 'Frequently asked questions about Smart India Hackathon (SIH 2026) presentation scoring, slide limits, technical checklists, and problem statement alignment.',
    type: 'website',
    url: 'https://sih-ats-scanner.vercel.app/faq',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SIH ATS Scanner FAQ — Pitch Deck Scoring Rules',
    description: 'Frequently asked questions about Smart India Hackathon (SIH 2026) presentation scoring, slide limits, technical checklists, and problem statement alignment.',
  },
};

export default function FaqPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#FDFBF7] text-slate-800 selection:bg-orange-500 selection:text-white">
      <JsonLd data={[organizationSchema, faqPageSchema]} />
      <Header />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-8 space-y-8">
        <div className="bg-white p-6 sm:p-10 rounded-3xl border border-slate-200 shadow-xs space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-50 text-orange-600 border border-orange-200 text-xs font-bold">
            <HelpCircle className="w-3.5 h-3.5" />
            <span>SIH ATS Knowledge Base</span>
          </div>

          <h1 className="text-3xl font-black text-slate-900 tracking-tight">
            Frequently Asked Questions (SIH ATS Scanner)
          </h1>

          <div className="space-y-4 pt-2">
            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <h2 className="font-extrabold text-sm text-slate-900">
                What does SIH ATS Scanner check in a Smart India Hackathon PPT?
              </h2>
              <p className="text-xs text-slate-600 leading-relaxed">
                SIH ATS Scanner currently performs live automated screening for Structure & Format (6-slide ceiling limit, mandatory section headings), Presentation Clarity (word count density under 70 words per slide, visual diagram checks), and Problem Statement Alignment (semantic domain similarity). Technical Depth (AI checklist audit) and Originality (corpus comparison) require API key and dataset configuration, and are excluded with renormalized weights when unconfigured.
              </p>
            </div>

            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <h2 className="font-extrabold text-sm text-slate-900">
                Is SIH ATS Scanner officially affiliated with Smart India Hackathon (SIH)?
              </h2>
              <p className="text-xs text-slate-600 leading-relaxed">
                No. SIH ATS Scanner is an independent screening tool built for participants. It is not officially affiliated with, endorsed by, or sponsored by Smart India Hackathon (SIH), AICTE, or the Ministry of Education (MoE), Government of India.
              </p>
            </div>

            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <h2 className="font-extrabold text-sm text-slate-900">
                What file formats are supported for evaluation?
              </h2>
              <p className="text-xs text-slate-600 leading-relaxed">
                The scanner supports Microsoft PowerPoint (.pptx) and PDF (.pdf) documents up to 25MB in size.
              </p>
            </div>

            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <h2 className="font-extrabold text-sm text-slate-900">
                How is technical depth evaluated?
              </h2>
              <p className="text-xs text-slate-600 leading-relaxed">
                When an AI key is configured, Technical Depth is evaluated using a 4-point checklist checking for specific frameworks named, database technology specified, ML models, and workflow architecture. If unconfigured, Technical Depth is marked as unassessed and excluded from the total score without penalizing the deck.
              </p>
            </div>
          </div>

          <div className="pt-6 flex justify-between items-center border-t border-slate-200">
            <Link href="/" className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition-all">
              <span>Back to Presentation Scanner</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
