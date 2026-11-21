import React from 'react';
import {
  LayoutDashboard,
  UploadCloud,
  BrainCircuit,
  BarChart3,
  ShieldCheck,
  MessageSquareCode,
  FileSpreadsheet,
  History,
  Settings,
  Database,
  Sparkles
} from 'lucide-react';
import { Dataset } from '../types';

export type NavTab =
  | 'dashboard'
  | 'upload'
  | 'analyst'
  | 'visualizations'
  | 'quality'
  | 'chat'
  | 'reports'
  | 'history'
  | 'settings';

interface SidebarProps {
  currentTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  datasets: Dataset[];
  selectedDataset: Dataset | null;
  onSelectDataset: (dataset: Dataset) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onSelectTab,
  datasets,
  selectedDataset,
  onSelectDataset,
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'upload', label: 'Upload Dataset', icon: UploadCloud },
    { id: 'analyst', label: 'AI Data Analyst', icon: BrainCircuit, badge: 'Agent' },
    { id: 'visualizations', label: 'Visualizations', icon: BarChart3 },
    { id: 'quality', label: 'Data Quality', icon: ShieldCheck },
    { id: 'chat', label: 'AI Chat', icon: MessageSquareCode, badge: 'Ask' },
    { id: 'reports', label: 'Reports', icon: FileSpreadsheet },
    { id: 'history', label: 'Analysis History', icon: History },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800 flex flex-col h-screen select-none shrink-0">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800/80 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/20">
          <BrainCircuit className="w-5 h-5" />
        </div>
        <div>
          <h1 className="font-bold text-sm tracking-tight text-white leading-tight">
            Autonomous
          </h1>
          <div className="flex items-center gap-1.5 text-xs text-blue-400 font-medium">
            <span>Data Analyst</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          </div>
        </div>
      </div>

      {/* Dataset Selector Quick Card */}
      <div className="p-3.5 mx-3 my-2 rounded-xl bg-slate-900/80 border border-slate-800/80">
        <div className="flex items-center justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
          <span className="flex items-center gap-1.5">
            <Database className="w-3.5 h-3.5 text-blue-400" />
            Active Dataset
          </span>
          <span className="text-[10px] text-slate-500">{datasets.length} total</span>
        </div>
        <select
          value={selectedDataset?.id || ''}
          onChange={(e) => {
            const d = datasets.find((item) => item.id === e.target.value);
            if (d) onSelectDataset(d);
          }}
          className="w-full bg-slate-950 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 truncate"
        >
          {datasets.length === 0 ? (
            <option value="">No datasets available</option>
          ) : (
            datasets.map((d) => (
              <option key={d.id} value={d.id}>
                {d.filename} ({d.row_count} rows)
              </option>
            ))
          )}
        </select>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 px-3 py-2 space-y-1 overflow-y-auto">
        <div className="text-[10px] uppercase font-bold text-slate-500 tracking-wider px-3 mb-2">
          Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id as NavTab)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold uppercase tracking-wider ${
                  isActive ? 'bg-blue-500/20 text-blue-300' : 'bg-slate-800 text-slate-400'
                }`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Agent Status Badge Footer */}
      <div className="p-3.5 m-3 rounded-xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 text-xs">
        <div className="flex items-center gap-2 text-slate-300 font-medium mb-1">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          <span>Autonomous AI Engine</span>
        </div>
        <p className="text-[11px] text-slate-500 leading-relaxed">
          Powered by tool-calling, Scikit-learn, DuckDB, and Gemini reasoning.
        </p>
      </div>
    </aside>
  );
};
