import React, { useState } from 'react';
import { UploadCloud, CheckCircle, AlertTriangle, FileSpreadsheet } from 'lucide-react';
import { api } from '../utils/api';

export default function CsvBatchUploader() {
  const [file, setFile] = useState(null);
  const [selectedModel, setSelectedModel] = useState('svm');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('model', selectedModel);

      const res = await api.uploadCsv(formData);
      if (res.success) {
        setResults(res.data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-6 sm:p-8 space-y-6">
      <div className="card-header border-none px-0 pt-0">
        <div>
          <h2 className="card-title">
            <FileSpreadsheet className="w-5 h-5 text-sky-600" />
            UNSW-NB15 CSV Batch Dataset Scanner
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Upload CSV network logs containing PCA features or UNSW-NB15 packet attributes for bulk classification.
          </p>
        </div>
        <span className="tag tag-blue">Batch Processing</span>
      </div>

      <div className="grid md:grid-cols-12 gap-6">
        
        <div className="md:col-span-5 space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
              Select Classification Model
            </label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="input-field"
            >
              <option value="svm">Classical SVM (RBF Kernel)</option>
              <option value="qsvm">Quantum SVM (ZFeatureMap 4-Qubit)</option>
              <option value="vqc">VQC Optimized (EfficientSU2 + SPSA)</option>
            </select>
          </div>

          <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center space-y-3 bg-slate-50 hover:bg-slate-100 transition-colors">
            <UploadCloud className="w-10 h-10 text-sky-600 mx-auto" />
            <div className="text-xs text-slate-600">
              <span className="font-bold">Click to upload</span> or drag and drop CSV file
            </div>
            <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" id="csv-input" />
            <label htmlFor="csv-input" className="btn-secondary text-xs inline-flex cursor-pointer">
              Choose CSV File
            </label>
            {file && <div className="text-xs font-mono text-sky-700 font-bold">{file.name}</div>}
          </div>

          <button onClick={handleUpload} disabled={!file || loading} className="btn-primary w-full">
            {loading ? 'Processing CSV Dataset...' : 'Scan CSV File'}
          </button>
        </div>

        <div className="md:col-span-7">
          {results ? (
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-3 font-mono text-center">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                  <div className="text-xs text-slate-500">Processed</div>
                  <div className="text-lg font-bold text-slate-900">{results.total_processed}</div>
                </div>
                <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200">
                  <div className="text-xs text-emerald-700">Normal</div>
                  <div className="text-lg font-bold text-emerald-800">{results.normal_count}</div>
                </div>
                <div className="p-3 rounded-xl bg-rose-50 border border-rose-200">
                  <div className="text-xs text-rose-700">Attacks</div>
                  <div className="text-lg font-bold text-rose-800">{results.attack_count}</div>
                </div>
              </div>

              <div className="max-h-64 overflow-y-auto border border-slate-200 rounded-xl">
                <table className="w-full text-xs">
                  <thead className="bg-slate-100 sticky top-0">
                    <tr>
                      <th className="p-2.5 text-left">Sample</th>
                      <th className="p-2.5 text-left">Prediction</th>
                      <th className="p-2.5 text-left">Risk</th>
                      <th className="p-2.5 text-left">Confidence</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 bg-white">
                    {results.predictions.map((p, idx) => (
                      <tr key={idx}>
                        <td className="p-2.5 font-mono">#{idx + 1}</td>
                        <td className="p-2.5 font-bold">{p.prediction}</td>
                        <td className="p-2.5">
                          <span className={`tag ${p.prediction.includes('Attack') ? 'tag-rose' : 'tag-green'} text-[10px]`}>
                            {p.threat}
                          </span>
                        </td>
                        <td className="p-2.5 font-mono">{p.confidence}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center p-8 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-500 font-mono text-center">
              Upload a UNSW-NB15 CSV file to view batch classification metrics.
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
