import React, { useState, useEffect } from 'react';
import {
  History,
  Clock,
  CheckCircle2,
  AlertCircle,
  Trash2,
  ArrowRight,
  GitCompare,
  FileSpreadsheet,
  Database,
  BarChart2
} from 'lucide-react';
import { Dataset, DashboardStats } from '../types';
import { api } from '../services/api';
import { NavTab } from '../components/Sidebar';

interface HistoryPageProps {
  datasets: Dataset[];
  selectedDataset: Dataset | null;
  onSelectDataset: (d: Dataset) => void;
  onNavigate: (tab: NavTab) => void;
  onLoadSession: (sessionId: string) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({
  datasets,
  selectedDataset,
  onSelectDataset,
  onNavigate,
  onLoadSession,
}) => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  // Comparison state
  const [compareD1, setCompareD1] = useState<string>(datasets[0]?.id || '');
  const [compareD2, setCompareD2] = useState<string>(datasets[1]?.id || datasets[0]?.id || '');

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
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

  const d1 = datasets.find((d) => d.id === compareD1);
  const d2 = datasets.find((d) => d.id === compareD2);

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <History className="w-4 h-4" />
            </div>
            <h2 className="text-xl font-bold text-white tracking-tight">Analysis History & Model Runs</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Persisted analytical sessions, previous tool execution logs, and dataset comparison tools.
          </p>
        </div>
      </div>

      {/* Historical Sessions Table */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
        <h3 className="text-base font-bold text-white tracking-tight">Previous Analytical Sessions</h3>

        {loading ? (
          <div className="py-8 text-center text-xs text-slate-500">Loading sessions from SQLite...</div>
        ) : !stats?.recent_analyses || stats.recent_analyses.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-500">
            No analysis sessions have been saved yet.
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-slate-800">
            <table className="min-w-full text-xs">
              <thead className="bg-slate-900 text-slate-400">
                <tr className="border-b border-slate-800">
                  <th className="p-3 text-left font-semibold">Dataset</th>
                  <th className="p-3 text-left font-semibold">Session ID</th>
                  <th className="p-3 text-left font-semibold">Status</th>
                  <th className="p-3 text-left font-semibold">Progress</th>
                  <th className="p-3 text-left font-semibold">Created</th>
                  <th className="p-3 text-right font-semibold">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-900 bg-slate-950/40">
                {stats.recent_analyses.map((s) => (
                  <tr key={s.session_id} className="hover:bg-slate-900/40">
                    <td className="p-3 font-semibold text-slate-200">{s.dataset_name}</td>
                    <td className="p-3 font-mono text-[11px] text-slate-400 truncate max-w-[120px]">
                      {s.session_id}
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                        s.status === 'completed'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                      }`}>
                        {s.status}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-slate-300">{s.progress_percent}%</td>
                    <td className="p-3 text-slate-400">
                      {s.created_at ? new Date(s.created_at).toLocaleString() : 'N/A'}
                    </td>
                    <td className="p-3 text-right">
                      <button
                        onClick={() => {
                          onLoadSession(s.session_id);
                          onNavigate('analyst');
                        }}
                        className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white cursor-pointer shadow"
                      >
                        Reopen Analysis
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Dataset Comparison Feature */}
      {datasets.length >= 2 && (
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-6">
          <div className="flex items-center gap-2">
            <GitCompare className="w-5 h-5 text-blue-400" />
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">Dataset Comparison Studio</h3>
              <p className="text-xs text-slate-400">Compare dimensionality, data health, and metrics across versions</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-[11px] font-semibold text-slate-400 block mb-1">Dataset 1</label>
              <select
                value={compareD1}
                onChange={(e) => setCompareD1(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200"
              >
                {datasets.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.filename} ({d.row_count} rows)
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-[11px] font-semibold text-slate-400 block mb-1">Dataset 2</label>
              <select
                value={compareD2}
                onChange={(e) => setCompareD2(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200"
              >
                {datasets.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.filename} ({d.row_count} rows)
                  </option>
                ))}
              </select>
            </div>
          </div>

          {d1 && d2 && (
            <div className="overflow-x-auto rounded-xl border border-slate-800">
              <table className="min-w-full text-xs">
                <thead className="bg-slate-900 text-slate-400">
                  <tr className="border-b border-slate-800">
                    <th className="p-3 text-left font-semibold">Parameter</th>
                    <th className="p-3 text-left font-semibold">{d1.filename}</th>
                    <th className="p-3 text-left font-semibold">{d2.filename}</th>
                    <th className="p-3 text-left font-semibold">Delta</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900 bg-slate-950/40">
                  <tr>
                    <td className="p-3 font-semibold text-slate-300">Total Rows</td>
                    <td className="p-3 font-mono">{d1.row_count.toLocaleString()}</td>
                    <td className="p-3 font-mono">{d2.row_count.toLocaleString()}</td>
                    <td className="p-3 font-mono text-blue-400">
                      {(d2.row_count - d1.row_count >= 0 ? '+' : '') + (d2.row_count - d1.row_count).toLocaleString()}
                    </td>
                  </tr>
                  <tr>
                    <td className="p-3 font-semibold text-slate-300">Total Columns</td>
                    <td className="p-3 font-mono">{d1.column_count}</td>
                    <td className="p-3 font-mono">{d2.column_count}</td>
                    <td className="p-3 font-mono text-blue-400">
                      {(d2.column_count - d1.column_count >= 0 ? '+' : '') + (d2.column_count - d1.column_count)}
                    </td>
                  </tr>
                  <tr>
                    <td className="p-3 font-semibold text-slate-300">Quality Score</td>
                    <td className="p-3 font-mono text-emerald-400">{d1.quality_score}/100</td>
                    <td className="p-3 font-mono text-emerald-400">{d2.quality_score}/100</td>
                    <td className="p-3 font-mono text-emerald-400">
                      {(d2.quality_score - d1.quality_score >= 0 ? '+' : '') + (d2.quality_score - d1.quality_score).toFixed(1)} pts
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
