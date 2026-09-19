import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';
import { DisclaimerBanner } from './components/DisclaimerBanner';
import { Inter } from "next/font/google";
import { cn } from "@/lib/utils";
import { NextAuthProvider } from "./components/NextAuthProvider";
import { JsonLd } from './components/JsonLd';
import { organizationSchema } from './components/SeoSchemas';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://sih-ats-scanner.vercel.app';

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: 'SIH ATS Scanner — Smart India Hackathon Presentation Score Evaluator',
    template: '%s | SIH ATS Scanner',
  },
  description: 'SIH ATS Scanner evaluates Smart India Hackathon (SIH 2026) pitch presentation decks against official format rules, slide count limits, clarity, technical depth, and problem statement alignment.',
  keywords: [
    'Smart India Hackathon 2026',
    'SIH PPT format guidelines',
    'SIH presentation scanner',
    'SIH ATS score evaluator',
    'SIH pitch deck checklist',
    'SIH technical approach slide',
  ],
  authors: [{ name: 'SIH ATS Scanner' }],
  creator: 'SIH ATS Scanner',
  publisher: 'SIH ATS Scanner',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    title: 'SIH ATS Scanner — Smart India Hackathon Presentation Score Evaluator',
    description: 'Upload your SIH PPT/PDF idea deck and get an instant score against official SIH 2026 rubric, slide-by-slide flags, and line-by-line rewrite suggestions.',
    url: baseUrl,
    siteName: 'SIH ATS Scanner',
    locale: 'en_US',
    type: 'website',
    images: [
      {
        url: `${baseUrl}/og-image.png`,
        width: 1200,
        height: 630,
        alt: 'SIH ATS Scanner — Smart India Hackathon Presentation Evaluator',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SIH ATS Scanner — Smart India Hackathon Presentation Score Evaluator',
    description: 'Upload your SIH PPT/PDF idea deck and get an instant score against official SIH 2026 rubric, slide-by-slide flags, and line-by-line rewrite suggestions.',
    images: [`${baseUrl}/og-image.png`],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={cn("font-sans", inter.variable)}>
      <head>
        <JsonLd data={organizationSchema} />
      </head>
      <body className="min-h-screen flex flex-col bg-[#FDFBF7] text-slate-800 antialiased selection:bg-orange-500 selection:text-white">
        <NextAuthProvider>
          <DisclaimerBanner />
          <main className="flex-1">{children}</main>
          <footer className="w-full border-t border-slate-200 bg-white/60 py-8 px-4 text-center text-xs text-slate-500 space-y-4">
            <div className="flex flex-wrap justify-center items-center gap-6 font-semibold text-slate-600">
              <Link href="/" className="hover:text-orange-600 transition-colors">Home Scanner</Link>
              <Link href="/guidelines" className="hover:text-orange-600 transition-colors">Format Guidelines & Checklist</Link>
              <Link href="/faq" className="hover:text-orange-600 transition-colors">FAQ & Scoring Rules</Link>
              <Link href="/upgrade" className="hover:text-orange-600 transition-colors">Pro Season Pass</Link>
            </div>
            <p>© 2026 SIH-ATS Scanner • Built for Smart India Hackathon Participants</p>
            <p className="text-[11px] text-slate-400 max-w-xl mx-auto">
              SIH ATS Scanner is an independent educational tool. Not affiliated with, authorized, maintained, sponsored, or endorsed by AICTE or Ministry of Education, Government of India.
            </p>
          </footer>
        </NextAuthProvider>
      </body>
    </html>
  );
}
