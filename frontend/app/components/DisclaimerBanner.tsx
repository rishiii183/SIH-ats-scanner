import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  return (
    <div className="w-full bg-amber-50 border-b border-amber-200 py-2.5 px-4 text-xs text-amber-700 flex items-center justify-center gap-2">
      <ShieldAlert className="w-4 h-4 text-amber-500 shrink-0" />
      <span>
        <strong>Legal Disclaimer:</strong> This is an independent tool and is not affiliated with, endorsed by, or officially connected to Smart India Hackathon (SIH), AICTE, or the Ministry of Education. Scores are estimates based on publicly available format guidelines.
      </span>
    </div>
  );
};
