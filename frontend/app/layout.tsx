import type { Metadata } from 'next';
import './globals.css';
import { DisclaimerBanner } from './components/DisclaimerBanner';

export const metadata: Metadata = {
  title: 'SIH ATS Scanner — Smart India Hackathon Presentation Score Evaluator',
  description: 'Upload your SIH PPT/PDF idea deck and get an instant score against the official SIH 2026 rubric, slide-by-slide flags, and line-by-line rewrite suggestions.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-[#080b11] text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">
        <DisclaimerBanner />
        <main className="flex-1">{children}</main>
        <footer className="w-full border-t border-slate-800/80 py-6 text-center text-xs text-slate-500">
          <p>© 2026 SIH-ATS Scanner • Built for Smart India Hackathon Participants</p>
        </footer>
      </body>
    </html>
  );
}
