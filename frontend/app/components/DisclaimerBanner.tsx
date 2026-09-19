import React from 'react';
import { Info } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  return (
    <div className="w-full bg-amber-50/80 backdrop-blur-md border-b border-amber-200/70 py-2 px-4 text-[11px] text-amber-800 flex items-center justify-center gap-2 font-medium">
      <Info className="w-3.5 h-3.5 text-amber-600 shrink-0" />
      <span>
        <strong className="font-bold text-amber-900">Disclaimer:</strong> Independent evaluator built for participants. Not officially affiliated with AICTE or Ministry of Education. Scores simulate publicly available SIH guidelines.
      </span>
    </div>
  );
};
