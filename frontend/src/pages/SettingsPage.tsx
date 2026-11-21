import React, { useState, useEffect } from 'react';
import {
  Settings,
  Key,
  Cpu,
  Database,
  CheckCircle2,
  AlertCircle,
  Save,
  Eye,
  EyeOff,
  Sparkles,
  Info
} from 'lucide-react';
import { api } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [settings, setSettings] = useState<any | null>(null);
  const [statusMsg, setStatusMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await api.getSettings();
      setSettings(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setStatusMsg(null);
      await api.updateSettings({ gemini_api_key: apiKey });
      setStatusMsg({ type: 'success', text: 'Gemini API key updated successfully!' });
      setApiKey('');
      await loadSettings();
    } catch (err: any) {
      setStatusMsg({ type: 'error', text: err.message || 'Failed to update settings' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-8 space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <Settings className="w-4 h-4" />
            </div>
            <h2 className="text-xl font-bold text-white tracking-tight">Platform Settings</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Configure AI reasoning provider, inspect analytical engines, and adjust runtime parameters.
          </p>
        </div>
      </div>

      {statusMsg && (
        <div
          className={`p-4 rounded-xl text-xs flex items-center gap-2 border ${
            statusMsg.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
              : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
          }`}
        >
          {statusMsg.type === 'success' ? (
            <CheckCircle2 className="w-4 h-4 shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 shrink-0" />
          )}
          <span>{statusMsg.text}</span>
        </div>
      )}

      {/* Gemini API Key Configuration */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Key className="w-4 h-4 text-blue-400" />
            <h3 className="text-base font-bold text-white tracking-tight">Gemini API Key</h3>
          </div>
          <span
            className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
              settings?.gemini_api_configured
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
            }`}
          >
            {settings?.gemini_api_configured ? 'Active' : 'Offline / Standalone Mode'}
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed">
          The autonomous agent utilizes Gemini 2.0 Flash for high-level business hypothesis reasoning and conversational answers. If no key is set, the system uses its verified parametric statistical NLG engine with zero downtime.
        </p>

        <div className="space-y-2">
          <label className="text-[11px] font-semibold text-slate-300 block">
            Enter or Update Gemini API Key:
          </label>
          <div className="flex gap-2">
            <div className="relative flex-1">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={settings?.gemini_api_preview || 'AIzaSy...'}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-blue-500"
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300 cursor-pointer"
              >
                {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>

            <button
              onClick={handleSave}
              disabled={!apiKey.trim() || saving}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold shadow transition-all cursor-pointer ${
                apiKey.trim() && !saving
                  ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-blue-600/20'
                  : 'bg-slate-900 text-slate-600 border border-slate-800 cursor-not-allowed'
              }`}
            >
              <Save className="w-3.5 h-3.5" />
              <span>{saving ? 'Saving...' : 'Save Key'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Underlying Analytical Architecture Card */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-blue-400" />
          <h3 className="text-base font-bold text-white tracking-tight">Active Engine Infrastructure</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="text-slate-400 font-semibold">Analytical Query Engine</div>
            <div className="text-white font-bold">{settings?.analytical_engine || 'DuckDB 2.0 & SQLite'}</div>
            <p className="text-[10px] text-slate-500">In-memory analytical columnar queries</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="text-slate-400 font-semibold">Anomaly & ML Engine</div>
            <div className="text-white font-bold">{settings?.ml_engine || 'Scikit-Learn IsolationForest'}</div>
            <p className="text-[10px] text-slate-500">Multivariate outlier isolation</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <div className="text-slate-400 font-semibold">Report Generation</div>
            <div className="text-white font-bold">ReportLab PDF Engine</div>
            <p className="text-[10px] text-slate-500">Vector executive dossiers</p>
          </div>
        </div>
      </div>
    </div>
  );
};
