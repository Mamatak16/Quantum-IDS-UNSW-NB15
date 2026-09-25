import React, { useState } from 'react';
import { 
  BarChart3, CheckCircle2, Trophy, Clock, 
  Activity, Radar as RadarIcon, Zap, TrendingUp, Layers
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  LineChart, Line
} from 'recharts';

export default function ModelComparison() {
  const [activeTab, setActiveTab] = useState('bar'); // 'bar' | 'radar' | 'latency' | 'progression'

  const models = [
    {
      name: 'Classical SVM',
      shortName: 'Classical SVM',
      kernel: 'Radial Basis Function (RBF)',
      accuracy: 94.20,
      precision: 93.80,
      recall: 94.50,
      f1_score: 94.15,
      macro_f1: 92.80,
      latency: 0.15,
      latencyStr: '0.15 ms',
      time: '6.8s',
      color: '#0284c7' // sky-600
    },
    {
      name: 'Quantum SVM (QSVM)',
      shortName: 'QSVM',
      kernel: 'ZFeatureMap (4-Qubit Kernel)',
      accuracy: 93.80,
      precision: 93.10,
      recall: 93.90,
      f1_score: 93.50,
      macro_f1: 92.10,
      latency: 16.20,
      latencyStr: '16.20 ms',
      time: '52.4s',
      color: '#2563eb' // blue-600
    },
    {
      name: 'VQC Baseline',
      shortName: 'VQC Baseline',
      kernel: 'ZFeatureMap + RealAmplitudes (COBYLA-100)',
      accuracy: 70.50,
      precision: 69.80,
      recall: 71.20,
      f1_score: 70.49,
      macro_f1: 69.10,
      latency: 48.00,
      latencyStr: '48.00 ms',
      time: '135.0s',
      color: '#d97706' // amber-600
    },
    {
      name: 'VQC Optimized',
      shortName: 'VQC Optimized',
      kernel: 'EfficientSU2 + MinMaxScaler + SPSA-250',
      accuracy: 88.50,
      precision: 87.90,
      recall: 89.10,
      f1_score: 88.49,
      macro_f1: 87.20,
      latency: 42.00,
      latencyStr: '42.00 ms',
      time: '185.0s',
      color: '#9333ea' // purple-600
    }
  ];

  // Data for grouped metric comparison bar chart
  const metricComparisonData = [
    {
      metric: 'Accuracy',
      'Classical SVM': 94.20,
      'Quantum SVM (QSVM)': 93.80,
      'VQC Baseline': 70.50,
      'VQC Optimized': 88.50,
    },
    {
      metric: 'Precision',
      'Classical SVM': 93.80,
      'Quantum SVM (QSVM)': 93.10,
      'VQC Baseline': 69.80,
      'VQC Optimized': 87.90,
    },
    {
      metric: 'Recall',
      'Classical SVM': 94.50,
      'Quantum SVM (QSVM)': 93.90,
      'VQC Baseline': 71.20,
      'VQC Optimized': 89.10,
    },
    {
      metric: 'F1 Score',
      'Classical SVM': 94.15,
      'Quantum SVM (QSVM)': 93.50,
      'VQC Baseline': 70.49,
      'VQC Optimized': 88.49,
    },
    {
      metric: 'Macro F1',
      'Classical SVM': 92.80,
      'Quantum SVM (QSVM)': 92.10,
      'VQC Baseline': 69.10,
      'VQC Optimized': 87.20,
    }
  ];

  // Radar chart normalized metrics
  const radarData = [
    { subject: 'Accuracy', 'Classical SVM': 94.20, 'QSVM': 93.80, 'VQC Baseline': 70.50, 'VQC Optimized': 88.50 },
    { subject: 'Precision', 'Classical SVM': 93.80, 'QSVM': 93.10, 'VQC Baseline': 69.80, 'VQC Optimized': 87.90 },
    { subject: 'Recall', 'Classical SVM': 94.50, 'QSVM': 93.90, 'VQC Baseline': 71.20, 'VQC Optimized': 89.10 },
    { subject: 'F1 Score', 'Classical SVM': 94.15, 'QSVM': 93.50, 'VQC Baseline': 70.49, 'VQC Optimized': 88.49 },
    { subject: 'Macro F1', 'Classical SVM': 92.80, 'QSVM': 92.10, 'VQC Baseline': 69.10, 'VQC Optimized': 87.20 }
  ];

  // Latency comparison data
  const latencyData = [
    { name: 'Classical SVM', latency: 0.15, color: '#0284c7', category: 'Classical' },
    { name: 'QSVM Kernel', latency: 16.20, color: '#2563eb', category: 'Quantum Kernel' },
    { name: 'VQC Baseline', latency: 48.00, color: '#d97706', category: 'Variational Quantum' },
    { name: 'VQC Optimized', latency: 42.00, color: '#9333ea', category: 'Variational Quantum' }
  ];

  // VQC Progression data across trials
  const vqcProgressionData = [
    { trial: 'Trial 1 (Baseline)', accuracy: 70.50, f1: 70.49, label: '70.50%' },
    { trial: 'Trial 2 (Scaling)', accuracy: 81.20, f1: 80.95, label: '81.20%' },
    { trial: 'Trial 3 (EfficientSU2)', accuracy: 84.80, f1: 84.50, label: '84.80%' },
    { trial: 'Trial 4 (Winner)', accuracy: 88.50, f1: 88.49, label: '88.50%' },
    { trial: 'Trial 5 (6-Qubit)', accuracy: 86.40, f1: 86.10, label: '86.40%' }
  ];

  // Custom Glassmorphism Tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900/95 backdrop-blur text-white p-3 rounded-xl shadow-xl border border-slate-700 text-xs font-mono z-50">
          <p className="font-bold text-slate-200 border-b border-slate-700 pb-1 mb-2">{label}</p>
          <div className="space-y-1">
            {payload.map((entry, index) => (
              <div key={`item-${index}`} className="flex items-center justify-between gap-4">
                <span className="flex items-center gap-1.5" style={{ color: entry.color || entry.fill }}>
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color || entry.fill }}></span>
                  {entry.name}:
                </span>
                <span className="font-bold text-white">
                  {typeof entry.value === 'number' ? `${entry.value.toFixed(2)}${entry.unit || '%'}` : entry.value}
                </span>
              </div>
            ))}
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-8">
      {/* Top Benchmark Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-sky-50 border border-sky-200 flex items-center gap-3">
          <div className="p-3 bg-sky-600 text-white rounded-lg">
            <Trophy className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-mono uppercase text-sky-800 font-bold">Top Overall Classifier</div>
            <div className="text-lg font-extrabold text-sky-950">Classical SVM (94.20%)</div>
            <div className="text-xs text-sky-700">Highest accuracy & lowest latency (0.15ms)</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-blue-50 border border-blue-200 flex items-center gap-3">
          <div className="p-3 bg-blue-600 text-white rounded-lg">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-mono uppercase text-blue-800 font-bold">Quantum Kernel Standard</div>
            <div className="text-lg font-extrabold text-blue-950">QSVM (93.80%)</div>
            <div className="text-xs text-blue-700">ZFeatureMap 4-qubit Hilbert space representation</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-purple-50 border border-purple-200 flex items-center gap-3">
          <div className="p-3 bg-purple-600 text-white rounded-lg">
            <TrendingUp className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-mono uppercase text-purple-800 font-bold">VQC Gain</div>
            <div className="text-lg font-extrabold text-purple-950">88.50% Accuracy</div>
            <div className="text-xs text-purple-700">+18.00% boost over baseline via EfficientSU2</div>
          </div>
        </div>
      </div>

      {/* Main Graph & Table Container */}
      <div className="card p-6 sm:p-8 space-y-6">
        <div className="card-header border-none px-0 pt-0 flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="card-title">
              <BarChart3 className="w-5 h-5 text-sky-600" />
              Fair Model Comparative Evaluation (UNSW-NB15)
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Rigorous benchmarking on UNSW-NB15 test set comparing Classical SVM, QSVM Kernel, VQC Baseline, and VQC Optimized.
            </p>
          </div>
          <span className="tag tag-green">Tested on UNSW-NB15</span>
        </div>

        {/* Interactive Graph View Selector Tabs */}
        <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-3">
          <button
            onClick={() => setActiveTab('bar')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 ${
              activeTab === 'bar'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5" />
            Grouped Metrics Bar Chart
          </button>

          <button
            onClick={() => setActiveTab('radar')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 ${
              activeTab === 'radar'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            <RadarIcon className="w-3.5 h-3.5" />
            Performance Radar Web
          </button>

          <button
            onClick={() => setActiveTab('latency')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 ${
              activeTab === 'latency'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            Inference Latency (ms)
          </button>

          <button
            onClick={() => setActiveTab('progression')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 ${
              activeTab === 'progression'
                ? 'bg-sky-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            <TrendingUp className="w-3.5 h-3.5" />
            VQC Optimization Curve
          </button>
        </div>

        {/* Graph Display Area */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 sm:p-6 min-h-[360px] flex flex-col justify-center">
          {activeTab === 'bar' && (
            <div>
              <div className="text-xs font-mono font-bold text-slate-700 mb-4 flex items-center justify-between">
                <span>Model Metrics Benchmarking (%)</span>
                <span className="text-slate-400 font-normal">Higher is better</span>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={metricComparisonData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="metric" tick={{ fontSize: 11, fill: '#475569' }} />
                    <YAxis domain={[60, 100]} tick={{ fontSize: 11, fill: '#475569' }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                    <Bar dataKey="Classical SVM" fill="#0284c7" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="Quantum SVM (QSVM)" fill="#2563eb" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="VQC Baseline" fill="#d97706" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="VQC Optimized" fill="#9333ea" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'radar' && (
            <div>
              <div className="text-xs font-mono font-bold text-slate-700 mb-2 flex items-center justify-between">
                <span>Multi-dimensional Performance Profile (Radar Web)</span>
                <span className="text-slate-400 font-normal">Coverage comparison</span>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart outerRadius="75%" data={radarData}>
                    <PolarGrid stroke="#cbd5e1" />
                    <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: '#334155' }} />
                    <PolarRadiusAxis angle={30} domain={[60, 100]} tick={{ fontSize: 10 }} />
                    <Radar name="Classical SVM" dataKey="Classical SVM" stroke="#0284c7" fill="#0284c7" fillOpacity={0.2} />
                    <Radar name="QSVM" dataKey="QSVM" stroke="#2563eb" fill="#2563eb" fillOpacity={0.2} />
                    <Radar name="VQC Baseline" dataKey="VQC Baseline" stroke="#d97706" fill="#d97706" fillOpacity={0.15} />
                    <Radar name="VQC Optimized" dataKey="VQC Optimized" stroke="#9333ea" fill="#9333ea" fillOpacity={0.25} />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '5px' }} />
                    <Tooltip content={<CustomTooltip />} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'latency' && (
            <div>
              <div className="text-xs font-mono font-bold text-slate-700 mb-4 flex items-center justify-between">
                <span>Inference Latency per Sample (milliseconds)</span>
                <span className="text-slate-400 font-normal">Lower is better</span>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={latencyData} layout="vertical" margin={{ top: 10, right: 30, left: 40, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis type="number" unit=" ms" tick={{ fontSize: 11, fill: '#475569' }} />
                    <YAxis dataKey="name" type="category" tick={{ fontSize: 11, fill: '#334155', fontWeight: 600 }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="latency" name="Latency (ms)" radius={[0, 6, 6, 0]}>
                      {latencyData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'progression' && (
            <div>
              <div className="text-xs font-mono font-bold text-slate-700 mb-4 flex items-center justify-between">
                <span>VQC Accuracy Progression Across Optimization Trials</span>
                <span className="text-purple-700 font-bold">+18.00% Jump from Trial 1 to Trial 4</span>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={vqcProgressionData} margin={{ top: 15, right: 30, left: -10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="trial" tick={{ fontSize: 11, fill: '#475569' }} />
                    <YAxis domain={[65, 92]} unit="%" tick={{ fontSize: 11, fill: '#475569' }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Line 
                      type="monotone" 
                      dataKey="accuracy" 
                      name="Validation Accuracy" 
                      stroke="#9333ea" 
                      strokeWidth={3}
                      dot={{ r: 6, fill: '#9333ea', stroke: '#ffffff', strokeWidth: 2 }} 
                      activeDot={{ r: 8 }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="f1" 
                      name="F1 Score" 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      strokeDasharray="4 4"
                      dot={{ r: 4, fill: '#3b82f6' }} 
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>

        {/* Detailed Comparative Metrics Table */}
        <div className="space-y-2">
          <div className="text-xs font-mono font-bold text-slate-700 uppercase">
            Full Benchmarking Metrics Table
          </div>
          <div className="overflow-x-auto border border-slate-200 rounded-xl">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-100 font-mono text-slate-700 uppercase">
                <tr>
                  <th className="p-3">Model Taxonomy</th>
                  <th className="p-3">Feature Map / Kernel</th>
                  <th className="p-3">Accuracy</th>
                  <th className="p-3">Precision</th>
                  <th className="p-3">Recall</th>
                  <th className="p-3">F1 Score</th>
                  <th className="p-3">Macro F1</th>
                  <th className="p-3">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {models.map((m) => (
                  <tr key={m.name} className="hover:bg-slate-50">
                    <td className="p-3 font-bold text-slate-900 flex items-center gap-2">
                      {m.name === 'Classical SVM' && <Trophy className="w-4 h-4 text-amber-500" />}
                      <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ backgroundColor: m.color }}></span>
                      {m.name}
                    </td>
                    <td className="p-3 font-mono text-slate-600">{m.kernel}</td>
                    <td className="p-3 font-bold text-slate-900">{m.accuracy.toFixed(2)}%</td>
                    <td className="p-3 font-mono">{m.precision.toFixed(2)}%</td>
                    <td className="p-3 font-mono">{m.recall.toFixed(2)}%</td>
                    <td className="p-3 font-mono font-bold text-sky-700">{m.f1_score.toFixed(2)}%</td>
                    <td className="p-3 font-mono">{m.macro_f1.toFixed(2)}%</td>
                    <td className="p-3 font-mono text-slate-500">{m.latencyStr}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Highlight Banner for VQC Improvement */}
        <div className="p-5 rounded-xl bg-purple-50 border border-purple-200 flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="text-xs font-mono font-bold text-purple-900 uppercase">Genuine VQC Optimization Process</div>
            <div className="text-sm font-extrabold text-purple-950">
              VQC Performance Improved from 70.50% to 88.50% Accuracy (+18.00 percentage points)
            </div>
            <div className="text-xs text-purple-700">
              Achieved via MinMaxScaler (0 to 2π) quantum angle scaling, EfficientSU2 ansatz with full entanglement, and SPSA/COBYLA-250 optimizer.
            </div>
          </div>
          <span className="tag tag-purple text-xs font-bold px-3 py-1">
            +18.00 pts Improvement
          </span>
        </div>

      </div>
    </div>
  );
}

