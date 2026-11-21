import React, { useEffect, useState } from 'react';
import {
  Database,
  BrainCircuit,
  Lightbulb,
  ShieldCheck,
  ArrowRight,
  UploadCloud,
  CheckCircle2,
  Clock,
  Sparkles,
  Play
} from 'lucide-react';
import { DashboardStats, Dataset } from '../types';
import { api } from '../services/api';
import { NavTab } from '../components/Sidebar';

interface DashboardPageProps {
  onNavigate: (tab: NavTab) => void;
  selectedDataset: Dataset | null;
  onSelectDataset: (d: Dataset) => void;
  onStartAnalysis: () => void;
  isAnalyzing: boolean;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  onNavigate,
  selectedDataset,
  onStartAnalysis,
  isAnalyzing,
}) => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      title: 'Datasets Ingested',
      value: stats?.total_datasets ?? 0,
      icon: Database,
      color: 'from-blue-600/20 to-blue-500/5',
      borderColor: 'border-blue-500/30',
      iconColor: 'text-blue-400',
      desc: 'Active files in repository',
    },
    {
      title: 'Autonomous Analyses',
      value: stats?.total_analyses ?? 0,
      icon: BrainCircuit,
      color: 'from-indigo-600/20 to-indigo-500/5',
      borderColor: 'border-indigo-500/30',
      iconColor: 'text-indigo-400',
      desc: 'End-to-end sessions executed',
    },
    {
      title: 'Actionable Insights',
      value: stats?.total_insights ?? 0,
      icon: Lightbulb,
      color: 'from-amber-600/20 to-amber-500/5',
      borderColor: 'border-amber-500/30',
      iconColor: 'text-amber-400',
      desc: 'AI-synthesized business drivers',
    },
    {
      title: 'Active Dataset Quality',
      value: selectedDataset ? `${selectedDataset.quality_score}%` : 'N/A',
      icon: ShieldCheck,
      color: 'from-emerald-600/20 to-emerald-500/5',
      borderColor: 'border-emerald-500/30',
      iconColor: 'text-emerald-400',
      desc: selectedDataset ? `Quality Grade: ${selectedDataset.quality_score >= 80 ? 'A/B' : 'Needs Review'}` : 'Select or upload dataset',
    },
  ];

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-blue-950/60 border border-slate-800 p-8 shadow-xl">
        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs font-semibold text-blue-400">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Autonomous Analytics 2.0</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight leading-tight">
            Independent AI-Powered Data Analysis & Strategic Insights
          </h1>
          <p className="text-sm text-slate-400 leading-relaxed">
            Upload any structured CSV or Excel dataset. The autonomous AI agent automatically profiles schemas, verifies data quality, computes descriptive and multivariate statistics, runs anomaly detection, synthesizes interactive charts, and produces executive PDF reports.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <button
              onClick={() => onNavigate('upload')}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/25 transition-all cursor-pointer"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Upload New Dataset</span>
            </button>

            {selectedDataset && (
              <button
                onClick={onStartAnalysis}
                disabled={isAnalyzing}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all cursor-pointer"
              >
                <Play className="w-3.5 h-3.5 text-blue-400 fill-current" />
                <span>Analyze '{selectedDataset.filename}'</span>
              </button>
            )}

            <button
              onClick={() => onNavigate('chat')}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition-all cursor-pointer"
            >
              <span>Ask AI Chat</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Ambient background blur */}
        <div className="absolute right-0 top-0 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          return (
            <div
              key={i}
              className={`p-6 rounded-2xl bg-gradient-to-br ${card.color} bg-slate-950/80 border ${card.borderColor} shadow-lg transition-all hover:scale-[1.01]`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-400 tracking-wide uppercase">
                  {card.title}
                </span>
                <div className={`p-2 rounded-xl bg-slate-900 border border-slate-800 ${card.iconColor}`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="text-3xl font-extrabold text-white tracking-tight">
                {card.value}
              </div>
              <div className="mt-2 text-xs text-slate-500 font-medium">
                {card.desc}
              </div>
            </div>
          );
        })}
      </div>

      {/* 2-Column Section: Recent Analyses & Ingested Datasets */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Analysis Sessions */}
        <div className="lg:col-span-2 bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">Recent Analysis Sessions</h2>
              <p className="text-xs text-slate-400">Autonomous analytical workflows executed on datasets</p>
            </div>
            <button
              onClick={() => onNavigate('history')}
              className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1 cursor-pointer"
            >
              <span>View All</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          {loading ? (
            <div className="py-12 text-center text-xs text-slate-500">Loading analysis history...</div>
          ) : !stats?.recent_analyses || stats.recent_analyses.length === 0 ? (
            <div className="py-12 text-center space-y-3">
              <Clock className="w-8 h-8 text-slate-600 mx-auto" />
              <p className="text-xs text-slate-400">No analytical sessions run yet.</p>
              <button
                onClick={onStartAnalysis}
                className="px-4 py-2 rounded-lg text-xs font-semibold bg-blue-600 text-white cursor-pointer"
              >
                Start First Analysis
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {stats.recent_analyses.map((a) => (
                <div
                  key={a.session_id}
                  className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 flex items-center justify-between hover:border-slate-700 transition-all"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-sm text-slate-200">
                        {a.dataset_name}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                        a.status === 'completed'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : a.status === 'running'
                          ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20 animate-pulse'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}>
                        {a.status}
                      </span>
                    </div>
                    <div className="text-xs text-slate-500 flex items-center gap-2">
                      <span>Step: {a.current_step}</span>
                      <span>•</span>
                      <span>{a.created_at ? new Date(a.created_at).toLocaleDateString() : 'Recent'}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => onNavigate('analyst')}
                    className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 cursor-pointer"
                  >
                    View Results
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Dataset Repository Card */}
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-white tracking-tight">Dataset Inventory</h2>
                <p className="text-xs text-slate-400">Ready for automated inspection</p>
              </div>
              <button
                onClick={() => onNavigate('upload')}
                className="text-xs font-semibold text-blue-400 hover:text-blue-300 cursor-pointer"
              >
                + Add
              </button>
            </div>

            <div className="space-y-2.5">
              {stats?.recent_datasets?.map((d) => (
                <div
                  key={d.id}
                  className={`p-3 rounded-xl border transition-all cursor-pointer ${
                    selectedDataset?.id === d.id
                      ? 'bg-blue-600/10 border-blue-500/40 text-blue-300'
                      : 'bg-slate-900/60 border-slate-800/80 hover:border-slate-700 text-slate-300'
                  }`}
                  onClick={() => onNavigate('upload')}
                >
                  <div className="flex items-center justify-between font-semibold text-xs">
                    <span className="truncate max-w-[140px]">{d.filename}</span>
                    <span className="text-[10px] text-emerald-400">Score: {d.quality_score}</span>
                  </div>
                  <div className="text-[11px] text-slate-500 mt-1 flex justify-between">
                    <span>{d.row_count} rows × {d.column_count} cols</span>
                    <span>CSV / Excel</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800">
            <button
              onClick={() => onNavigate('upload')}
              className="w-full py-2.5 rounded-xl text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 flex items-center justify-center gap-2 cursor-pointer"
            >
              <UploadCloud className="w-4 h-4 text-blue-400" />
              <span>Upload Dataset File</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
