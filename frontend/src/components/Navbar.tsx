import React from 'react';
import { NavTab } from './Sidebar';
import { Dataset } from '../types';
import { Database, Play, Sparkles } from 'lucide-react';

interface NavbarProps {
  currentTab: NavTab;
  selectedDataset: Dataset | null;
  onStartAnalysis: () => void;
  isAnalyzing: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  selectedDataset,
  onStartAnalysis,
  isAnalyzing,
}) => {
  const getTabTitle = (tab: NavTab) => {
    switch (tab) {
      case 'dashboard': return 'Dashboard Overview';
      case 'upload': return 'Dataset Ingestion & Quality Profiler';
      case 'analyst': return 'Autonomous AI Data Analyst Agent';
      case 'visualizations': return 'Interactive Visualizations & Exploratory Charts';
      case 'quality': return 'Data Quality & Remediation Studio';
      case 'chat': return 'Conversational AI Analyst';
      case 'reports': return 'Executive PDF Dossiers & Reports';
      case 'history': return 'Analysis History & Model Runs';
      case 'settings': return 'Platform Settings & AI Configuration';
    }
  };

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      <div>
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span>Platform</span>
          <span>/</span>
          <span className="text-blue-400 capitalize">{currentTab}</span>
        </div>
        <h2 className="text-base font-bold text-slate-100 tracking-tight">
          {getTabTitle(currentTab)}
        </h2>
      </div>

      <div className="flex items-center gap-4">
        {selectedDataset && (
          <div className="hidden md:flex items-center gap-3 px-3.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
            <Database className="w-3.5 h-3.5 text-blue-400" />
            <span className="font-semibold text-slate-200 truncate max-w-[150px]">
              {selectedDataset.filename}
            </span>
            <span className="text-slate-500">•</span>
            <span className="text-slate-400">{selectedDataset.row_count.toLocaleString()} rows</span>
            <span className="text-slate-500">•</span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
              selectedDataset.quality_score >= 80
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
            }`}>
              QS: {selectedDataset.quality_score}
            </span>
          </div>
        )}

        {selectedDataset && (
          <button
            onClick={onStartAnalysis}
            disabled={isAnalyzing}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold shadow-md transition-all ${
              isAnalyzing
                ? 'bg-blue-600/40 text-blue-300 cursor-not-allowed border border-blue-500/30'
                : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-blue-600/20 hover:shadow-blue-600/40 cursor-pointer'
            }`}
          >
            {isAnalyzing ? (
              <>
                <Sparkles className="w-3.5 h-3.5 animate-spin" />
                <span>Agent Running...</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Run Autonomous Analysis</span>
              </>
            )}
          </button>
        )}
      </div>
    </header>
  );
};
