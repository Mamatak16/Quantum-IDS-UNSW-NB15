import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 py-8 px-4 sm:px-6 mt-16">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-sky-600" />
          <span className="font-bold text-slate-700">Quantum Intrusion Detection System</span>
          <span>— UNSW-NB15 Benchmark Edition</span>
        </div>
        <div className="font-mono">
          Powered by IBM Qiskit 2.5.1 &amp; Flask Backend
        </div>
      </div>
    </footer>
  );
}
