import React from 'react';
import { Database, ShieldAlert, Layers, CheckCircle2 } from 'lucide-react';

export default function DatasetInfo() {
  const attackCategories = [
    { name: 'Normal', desc: 'Legitimate normal operational network traffic.', color: 'emerald' },
    { name: 'Fuzzers', desc: 'Attempting to discover security vulnerabilities by feeding random data.', color: 'purple' },
    { name: 'Analysis', desc: 'Port scans, spam, and HTML page intrusion attempts.', color: 'sky' },
    { name: 'Backdoors', desc: 'Bypassing stealthily standard authentication controls.', color: 'rose' },
    { name: 'DoS', desc: 'Denial of Service overloading system memory & bandwidth.', color: 'rose' },
    { name: 'Exploits', desc: 'Exploiting known security flaws in operating systems & services.', color: 'amber' },
    { name: 'Generic', desc: 'Technique that collides against block cipher cryptographic functions.', color: 'amber' },
    { name: 'Reconnaissance', desc: 'Gathering network topology and system configuration data.', color: 'blue' },
    { name: 'Shellcode', desc: 'Malicious payload code injected to gain root shell execution.', color: 'purple' },
    { name: 'Worms', desc: 'Self-replicating malware propagating across host nodes.', color: 'rose' }
  ];

  return (
    <div className="space-y-8">
      <div className="card p-6 sm:p-8 space-y-6">
        <div className="card-header border-none px-0 pt-0">
          <div>
            <h2 className="card-title">
              <Database className="w-5 h-5 text-sky-600" />
              UNSW-NB15 Benchmark Dataset Specification
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Comprehensive overview of the modern UNSW-NB15 network intrusion dataset created by ACCS.
            </p>
          </div>
          <span className="tag tag-blue">UNSW-NB15 Dataset</span>
        </div>

        <div className="grid sm:grid-cols-3 gap-4 text-xs font-mono">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
            <div className="text-slate-500">Training Records</div>
            <div className="text-xl font-bold text-slate-900">175,341</div>
            <div className="text-[10px] text-slate-500">UNSW_NB15_training-set.csv</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
            <div className="text-slate-500">Testing Records</div>
            <div className="text-xl font-bold text-slate-900">82,332</div>
            <div className="text-[10px] text-slate-500">UNSW_NB15_testing-set.csv</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
            <div className="text-slate-500">Feature Count</div>
            <div className="text-xl font-bold text-slate-900">49 Features</div>
            <div className="text-[10px] text-slate-500">Reduced to 4D PCA Space</div>
          </div>
        </div>

        {/* Attack Categories Table */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-900 text-sm font-mono uppercase">UNSW-NB15 10 Attack & Traffic Taxonomy</h3>
          <div className="grid sm:grid-cols-2 gap-3">
            {attackCategories.map((c) => (
              <div key={c.name} className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-1 text-xs">
                <div className="flex items-center justify-between font-bold">
                  <span className="text-slate-900 font-mono">{c.name}</span>
                  <span className="tag tag-blue text-[10px]">{c.name === 'Normal' ? 'Benign' : 'Malicious Attack'}</span>
                </div>
                <p className="text-slate-600 text-[11px]">{c.desc}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
