import type { Metadata } from 'next';
import { JsonLd } from '../components/JsonLd';
import { organizationSchema, softwareAppSchema } from '../components/SeoSchemas';

export const metadata: Metadata = {
  title: 'SIH Pro Season Pass Pricing — SIH ATS Scanner',
  description: 'Upgrade to SIH ATS Scanner Pro Pass for ₹99. Get unlimited presentation re-evaluations, score delta diffing, and slide-by-slide AI jury rewrites.',
  openGraph: {
    title: 'SIH Pro Season Pass Pricing — SIH ATS Scanner',
    description: 'Upgrade to SIH ATS Scanner Pro Pass for ₹99. Get unlimited presentation re-evaluations, score delta diffing, and slide-by-slide AI jury rewrites.',
    type: 'website',
    url: 'https://sih-ats-scanner.vercel.app/upgrade',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SIH Pro Season Pass Pricing — SIH ATS Scanner',
    description: 'Upgrade to SIH ATS Scanner Pro Pass for ₹99. Get unlimited presentation re-evaluations, score delta diffing, and slide-by-slide AI jury rewrites.',
  },
};

export default function UpgradeLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <JsonLd data={[organizationSchema, softwareAppSchema]} />
      {children}
    </>
  );
}
