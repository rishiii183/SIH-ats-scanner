import type { Metadata } from 'next';
import './globals.css';
import { DisclaimerBanner } from './components/DisclaimerBanner';
import { Inter } from "next/font/google";
import { cn } from "@/lib/utils";
import { NextAuthProvider } from "./components/NextAuthProvider";

const inter = Inter({subsets:['latin'],variable:'--font-sans'});

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
    <html lang="en" className={cn("font-sans", inter.variable)}>
      <body className="min-h-screen flex flex-col bg-[#FDFBF7] text-slate-800 antialiased selection:bg-orange-500 selection:text-white">
        <NextAuthProvider>
          <DisclaimerBanner />
          <main className="flex-1">{children}</main>
          <footer className="w-full border-t border-slate-200 py-6 text-center text-xs text-slate-500">
            <p>© 2026 SIH-ATS Scanner • Built for Smart India Hackathon Participants</p>
          </footer>
        </NextAuthProvider>
      </body>
    </html>
  );
}
