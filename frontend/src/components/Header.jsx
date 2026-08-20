import React from 'react';
import { ShieldCheck, Activity, Cpu, Database } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, backendOnline }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'prediction', label: 'Live Prediction' },
    { id: 'batch', label: 'CSV Batch Scanner' },
    { id: 'comparison', label: 'Model Comparison' },
    { id: 'vqc-opt', label: 'VQC Optimization' },
    { id: 'dataset', label: 'Dataset Info' },
    { id: 'docs', label: 'Documentation' },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-sky-600 flex items-center justify-center text-white shadow-sm">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-slate-900 tracking-tight text-lg">QUANTUM IDS</span>
                <span className="tag tag-blue">UNSW-NB15</span>
              </div>
              <p className="text-xs text-slate-500 font-medium">Hybrid Quantum-Classical Cyber Telemetry</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === item.id
                    ? 'bg-sky-50 text-sky-700 font-bold border border-sky-200'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>

          {/* Backend Status Indicator */}
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${backendOnline ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`}></span>
            <span className="text-xs font-mono font-semibold text-slate-600">
              {backendOnline ? 'API 5001 Online' : 'Local Mode'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
