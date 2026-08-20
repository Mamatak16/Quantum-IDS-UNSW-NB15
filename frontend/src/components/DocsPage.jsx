import React from 'react';
import { BookOpen, Code, Terminal, Layers } from 'lucide-react';

export default function DocsPage() {
  return (
    <div className="card p-6 sm:p-8 space-y-8">
      <div className="card-header border-none px-0 pt-0">
        <div>
          <h2 className="card-title">
            <BookOpen className="w-5 h-5 text-sky-600" />
            UNSW-NB15 Technical Documentation & System Manual
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Complete technical specs, quantum circuit formulations, data pre-processing rules, and REST API documentation.
          </p>
        </div>
        <span className="tag tag-blue">Documentation</span>
      </div>

      <div className="space-y-6 text-xs leading-relaxed text-slate-700">
        
        {/* Section 1 */}
        <section className="space-y-2">
          <h3 className="font-bold text-slate-900 text-sm font-mono border-b border-slate-200 pb-1">
            1. Why UNSW-NB15 Dataset was Selected
          </h3>
          <p>
            The <strong>UNSW-NB15 dataset</strong> was created by the Cyber Research Group at the Australian Centre for Cyber Security (ACCS) to address limitations in older legacy datasets. It reflects modern network traffic environments, containing synthetic contemporary attack activities alongside real normal network traffic behavior.
          </p>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-1 font-mono text-[11px]">
            <div>• Training Set Records: 175,341</div>
            <div>• Testing Set Records: 82,332</div>
            <div>• Total Feature Attributes: 49 Raw Columns</div>
            <div>• Categorical Columns: <code>proto</code>, <code>service</code>, <code>state</code></div>
          </div>
        </section>

        {/* Section 2 */}
        <section className="space-y-2">
          <h3 className="font-bold text-slate-900 text-sm font-mono border-b border-slate-200 pb-1">
            2. Quantum State Encoding & Hilbert Feature Space
          </h3>
          <p>
            The 4 PCA feature components <code>x = [f1, f2, f3, f4]</code> extracted from UNSW-NB15 telemetry are mapped into a 4-qubit quantum state vector via Pauli-Z rotation gates:
          </p>
          <div className="p-3 bg-slate-900 text-sky-300 font-mono rounded-lg text-[11px]">
            U_&Phi;(x) = exp( i &Sigma; x_j Z_j ) = &bigotimes; R_Z(2 x_j)
          </div>
          <p>
            The statevector inner product transition amplitude defines the Quantum Kernel Matrix:
          </p>
          <div className="p-3 bg-slate-900 text-sky-300 font-mono rounded-lg text-[11px]">
            K_ij = |&lt;&Phi;(x_i) | &Phi;(x_j)&gt;|^2
          </div>
        </section>

        {/* Section 3 */}
        <section className="space-y-2">
          <h3 className="font-bold text-slate-900 text-sm font-mono border-b border-slate-200 pb-1">
            3. Execution Commands
          </h3>
          <div className="p-4 bg-slate-900 text-sky-300 font-mono rounded-xl space-y-2 text-[11px]">
            <div># 1. Train all models & generate benchmark results</div>
            <div>python run_all.py</div>
            <div className="pt-1"># 2. Run VQC hyperparameter optimization</div>
            <div>python experiments/train_vqc.py</div>
            <div className="pt-1"># 3. Launch Flask Backend API (Port 5001)</div>
            <div>cd backend &amp;&amp; python app.py</div>
            <div className="pt-1"># 4. Launch React Frontend Dashboard (Port 5174)</div>
            <div>cd frontend &amp;&amp; npm run dev</div>
          </div>
        </section>

      </div>
    </div>
  );
}
