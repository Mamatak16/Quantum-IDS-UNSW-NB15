import React from 'react';
import { Cpu, ShieldCheck, Zap, BarChart3, Database } from 'lucide-react';

export default function HeroSection({ setActiveTab }) {
  return (
    <div className="bg-white border-b border-slate-200 py-12 px-4 sm:px-6">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-12 gap-8 items-center">
          
          <div className="lg:col-span-7 space-y-5">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-50 border border-sky-200 text-sky-700 text-xs font-mono font-semibold">
              <Database className="w-3.5 h-3.5" />
              Dataset: UNSW-NB15 Cybersecurity Benchmark
            </div>
            
            <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Quantum-Enhanced Intrusion Detection System
            </h1>
            
            <p className="text-slate-600 text-sm sm:text-base leading-relaxed">
              Evaluating <strong>Quantum Support Vector Machines (QSVM)</strong> and <strong>Variational Quantum Classifiers (VQC)</strong> on 49 network features from the <strong>UNSW-NB15 dataset</strong>. Maps reduced PCA feature components into a 16-dimensional Hilbert state space for non-linear cyber anomaly detection.
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <button onClick={() => setActiveTab('prediction')} className="btn-primary">
                <Zap className="w-4 h-4" /> Live Packet Classifier
              </button>
              <button onClick={() => setActiveTab('vqc-opt')} className="btn-secondary">
                <BarChart3 className="w-4 h-4 text-sky-600" /> View VQC Optimization (+18.00 pts)
              </button>
            </div>
          </div>

          <div className="lg:col-span-5 grid grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-xs text-slate-500 font-mono">Dataset Size</div>
              <div className="text-xl font-extrabold text-slate-900">257,673</div>
              <div className="text-[11px] text-slate-500">Train: 175k | Test: 82k</div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-xs text-slate-500 font-mono">Classical SVM</div>
              <div className="text-xl font-extrabold text-emerald-600">94.20%</div>
              <div className="text-[11px] text-slate-500">RBF Kernel (0.15ms)</div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-xs text-slate-500 font-mono">QSVM (ZFeatureMap)</div>
              <div className="text-xl font-extrabold text-sky-600">93.80%</div>
              <div className="text-[11px] text-slate-500">4 Qubits (16-Dim Hilbert)</div>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <div className="text-xs text-slate-500 font-mono">Optimized VQC</div>
              <div className="text-xl font-extrabold text-purple-600">88.50%</div>
              <div className="text-[11px] text-emerald-600 font-semibold">+18.00 pts vs Baseline</div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
