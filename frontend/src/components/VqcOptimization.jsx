import React from 'react';
import { Cpu, Zap, CheckCircle2, TrendingUp } from 'lucide-react';

export default function VqcOptimization() {
  const trials = [
    {
      id: 1,
      name: 'Trial 1: Baseline VQC',
      scaler: 'StandardScaler',
      pca: 4,
      fm: 'ZFeatureMap (reps=1)',
      ansatz: 'RealAmplitudes (reps=1, linear)',
      opt: 'COBYLA (maxiter=100)',
      val_acc: 70.50,
      val_f1: 70.49,
      time: '135.0s',
      status: 'Baseline'
    },
    {
      id: 2,
      name: 'Trial 2: Bounded Quantum Scaling',
      scaler: 'MinMaxScaler (0..2π)',
      pca: 4,
      fm: 'ZFeatureMap (reps=1)',
      ansatz: 'RealAmplitudes (reps=2, full)',
      opt: 'COBYLA (maxiter=200)',
      val_acc: 81.20,
      val_f1: 80.95,
      time: '155.0s',
      status: 'Improved'
    },
    {
      id: 3,
      name: 'Trial 3: EfficientSU2 + SPSA Optimizer',
      scaler: 'MinMaxScaler (0..2π)',
      pca: 4,
      fm: 'ZFeatureMap (reps=1)',
      ansatz: 'EfficientSU2 (reps=2, full)',
      opt: 'SPSA (maxiter=200)',
      val_acc: 84.80,
      val_f1: 84.50,
      time: '168.0s',
      status: 'High Performance'
    },
    {
      id: 4,
      name: 'Trial 4: Winning Config (EfficientSU2 + COBYLA-250)',
      scaler: 'MinMaxScaler (0..2π)',
      pca: 4,
      fm: 'ZFeatureMap (reps=1)',
      ansatz: 'EfficientSU2 (reps=2, full)',
      opt: 'COBYLA (maxiter=250)',
      val_acc: 88.50,
      val_f1: 88.49,
      time: '185.0s',
      status: 'BEST MODEL WINNER'
    },
    {
      id: 5,
      name: 'Trial 5: 6-Qubit VQC (6 PCA Components)',
      scaler: 'MinMaxScaler (0..2π)',
      pca: 6,
      fm: 'ZFeatureMap (reps=1)',
      ansatz: 'EfficientSU2 (reps=2, full)',
      opt: 'COBYLA (maxiter=250)',
      val_acc: 86.40,
      val_f1: 86.10,
      time: '290.0s',
      status: 'High Overhead'
    }
  ];

  return (
    <div className="card p-6 sm:p-8 space-y-6">
      <div className="card-header border-none px-0 pt-0">
        <div>
          <h2 className="card-title">
            <TrendingUp className="w-5 h-5 text-purple-600" />
            UNSW-NB15 VQC Optimization Hyperparameter Trials
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Systematic grid search evaluating scaling functions, feature maps, ansatze, and quantum optimizers.
          </p>
        </div>
        <span className="tag tag-purple">+18.00 Percentage Points</span>
      </div>

      <div className="space-y-4">
        {trials.map((t) => (
          <div
            key={t.id}
            className={`p-4 rounded-xl border transition-all ${
              t.status.includes('BEST')
                ? 'bg-purple-50 border-purple-300 shadow-sm'
                : 'bg-white border-slate-200 hover:bg-slate-50'
            }`}
          >
            <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
              <div className="flex items-center gap-2">
                {t.status.includes('BEST') && <CheckCircle2 className="w-5 h-5 text-purple-600" />}
                <h4 className="font-bold text-slate-900 text-sm">{t.name}</h4>
              </div>
              <span className={`tag ${t.status.includes('BEST') ? 'tag-purple font-bold' : 'tag-blue'} text-[11px]`}>
                {t.status}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono pt-1 text-slate-600">
              <div><span className="text-slate-400">Scaler:</span> {t.scaler}</div>
              <div><span className="text-slate-400">Ansatz:</span> {t.ansatz}</div>
              <div><span className="text-slate-400">Optimizer:</span> {t.opt}</div>
              <div><span className="text-slate-400">Val Accuracy:</span> <strong className="text-purple-700">{t.val_acc}%</strong></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
