import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import LiveClassifier from './components/LiveClassifier';
import CsvBatchUploader from './components/CsvBatchUploader';
import ModelComparison from './components/ModelComparison';
import VqcOptimization from './components/VqcOptimization';
import DatasetInfo from './components/DatasetInfo';
import DocsPage from './components/DocsPage';
import Footer from './components/Footer';
import { api } from './utils/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [backendOnline, setBackendOnline] = useState(false);

  useEffect(() => {
    const checkBackend = async () => {
      const status = await api.getHealth();
      setBackendOnline(status?.status === 'ok' || status?.success === true);
    };
    checkBackend();
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} backendOnline={backendOnline} />

      {activeTab === 'dashboard' && <HeroSection setActiveTab={setActiveTab} />}

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-12">
            <LiveClassifier />
            <ModelComparison />
            <VqcOptimization />
          </div>
        )}

        {activeTab === 'prediction' && <LiveClassifier />}
        {activeTab === 'batch' && <CsvBatchUploader />}
        {activeTab === 'comparison' && <ModelComparison />}
        {activeTab === 'vqc-opt' && <VqcOptimization />}
        {activeTab === 'dataset' && <DatasetInfo />}
        {activeTab === 'docs' && <DocsPage />}
      </main>

      <Footer />
    </div>
  );
}
