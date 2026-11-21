import React from 'react';
import {
  BrainCircuit,
  CheckCircle2,
  Clock,
  AlertCircle,
  Play,
  FileSpreadsheet,
  ArrowRight,
  TrendingUp,
  AlertTriangle,
  Lightbulb,
  ShieldCheck,
  Zap,
  BarChart2
} from 'lucide-react';
import { AnalysisResults, Dataset, ExecutionLogEntry } from '../types';
import { NavTab } from '../components/Sidebar';

interface AgentPageProps {
  selectedDataset: Dataset | null;
  onStartAnalysis: () => void;
  isAnalyzing: boolean;
  activeSessionId: string | null;
  sessionStatus: any;
  analysisResults: AnalysisResults | null;
  onNavigate: (tab: NavTab) => void;
}

const STAGES = [
  { id: 'understanding', label: '1. Understand Dataset', desc: 'Inspect schema & nulls' },
  { id: 'planning', label: '2. Plan Analysis', desc: 'Formulate hypotheses' },
  { id: 'executing', label: '3. Execute Tools', desc: 'Run parametric & ML models' },
  { id: 'validating', label: '4. Validate Results', desc: 'Verify data consistency' },
  { id: 'generating_insights', label: '5. Synthesize Insights', desc: 'Formulate business logic' },
  { id: 'completed', label: '6. Completed', desc: 'Dossier ready' },
];

export const AgentPage: React.FC<AgentPageProps> = ({
  selectedDataset,
  onStartAnalysis,
  isAnalyzing,
  sessionStatus,
  analysisResults,
  onNavigate,
}) => {
  const currentStep = sessionStatus?.current_step || (analysisResults ? 'completed' : 'understanding');
  const progressPercent = sessionStatus?.progress_percent || (analysisResults ? 100 : 0);
  const logs: ExecutionLogEntry[] = sessionStatus?.logs || analysisResults?.execution_logs || [];

  const getStepStatus = (index: number) => {
    const stageKeys = STAGES.map((s) => s.id);
    const currentIndex = stageKeys.indexOf(currentStep);

    if (currentIndex > index || currentStep === 'completed') return 'done';
    if (currentIndex === index && isAnalyzing) return 'active';
    return 'pending';
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header Card */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <BrainCircuit className="w-4 h-4" />
            </div>
            <h2 className="text-xl font-bold text-white tracking-tight">Autonomous AI Data Analyst</h2>
          </div>
          <p className="text-xs text-slate-400">
            {selectedDataset
              ? `Currently inspecting dataset: ${selectedDataset.filename} (${selectedDataset.row_count.toLocaleString()} rows)`
              : 'Please select or upload a dataset to begin autonomous analysis.'}
          </p>
        </div>

        {selectedDataset && (
          <div className="flex items-center gap-3">
            <button
              onClick={onStartAnalysis}
              disabled={isAnalyzing}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold shadow-lg transition-all ${
                isAnalyzing
                  ? 'bg-blue-600/40 text-blue-300 border border-blue-500/30 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-blue-600/20 cursor-pointer'
              }`}
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{isAnalyzing ? 'Analysis Running...' : 'Rerun Autonomous Analysis'}</span>
            </button>
          </div>
        )}
      </div>

      {/* 6-Stage Progress Stepper */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-white tracking-tight">Autonomous Workflow Lifecycle</h3>
            <p className="text-xs text-slate-400">Multi-stage pipeline managed independently by the AI agent</p>
          </div>
          <div className="text-right">
            <span className="text-xs font-bold text-blue-400">{progressPercent}% Completed</span>
          </div>
        </div>

        {/* Linear Progress Bar */}
        <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-600 to-indigo-500 transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Steps Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {STAGES.map((stage, idx) => {
            const status = getStepStatus(idx);
            return (
              <div
                key={stage.id}
                className={`p-3 rounded-xl border text-xs transition-all ${
                  status === 'done'
                    ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-300'
                    : status === 'active'
                    ? 'bg-blue-950/40 border-blue-500/50 text-blue-200 animate-pulse'
                    : 'bg-slate-900/40 border-slate-800/80 text-slate-500'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold">{stage.label}</span>
                  {status === 'done' ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  ) : status === 'active' ? (
                    <Clock className="w-3.5 h-3.5 text-blue-400 animate-spin shrink-0" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-slate-800 shrink-0" />
                  )}
                </div>
                <p className="text-[10px] text-slate-400 leading-tight">{stage.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Execution Logs Stream */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-blue-400" />
            <h3 className="text-base font-bold text-white tracking-tight">Agent Execution Log & Tool Call Trace</h3>
          </div>
          <span className="text-xs text-slate-500 font-medium">{logs.length} operations logged</span>
        </div>

        {logs.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-500">
            Click 'Launch Autonomous Analysis' to watch the agent execute analytical tools in real time.
          </div>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-slate-800/80">
            <table className="min-w-full text-xs">
              <thead className="bg-slate-900 text-slate-400">
                <tr className="border-b border-slate-800">
                  <th className="p-3 text-left font-semibold">Analytical Task</th>
                  <th className="p-3 text-left font-semibold">Tool Invoked</th>
                  <th className="p-3 text-left font-semibold">Status</th>
                  <th className="p-3 text-left font-semibold">Duration</th>
                  <th className="p-3 text-left font-semibold">Result Summary</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-900 bg-slate-950/40">
                {logs.map((log, i) => (
                  <tr key={i} className="hover:bg-slate-900/40 transition-colors">
                    <td className="p-3 font-semibold text-slate-200 whitespace-nowrap">{log.task}</td>
                    <td className="p-3 font-mono text-[11px] text-blue-400 whitespace-nowrap">{log.tool}</td>
                    <td className="p-3 whitespace-nowrap">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                        log.status === 'success'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : log.status === 'warning'
                          ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}>
                        {log.status}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-slate-400 whitespace-nowrap">{log.execution_time_ms} ms</td>
                    <td className="p-3 text-slate-300 max-w-md">{log.summary}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Formulated AI Plan Review */}
      {analysisResults?.plan && analysisResults.plan.length > 0 && (
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">Formulated Analytical Plan</h3>
              <p className="text-xs text-slate-400">Tailored statistical strategy devised autonomously by the agent</p>
            </div>
            <span className="text-xs text-slate-500">{analysisResults.plan.length} Plan Items</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {analysisResults.plan.map((item) => (
              <div
                key={item.step_number}
                className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 space-y-2 hover:border-slate-700 transition-all"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-blue-400">Step {item.step_number}</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                    {item.tool_to_use}
                  </span>
                </div>
                <h4 className="font-semibold text-sm text-slate-100">{item.name}</h4>
                <p className="text-xs text-slate-400">{item.description}</p>
                <div className="pt-2 text-[11px] text-slate-500 border-t border-slate-800/60">
                  <span className="font-semibold text-slate-400">Rationale: </span>
                  {item.rationale}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Generated Insights Presentation */}
      {analysisResults?.insights && analysisResults.insights.length > 0 && (
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-amber-400" />
              <div>
                <h3 className="text-base font-bold text-white tracking-tight">Autonomous Business Insights & Findings</h3>
                <p className="text-xs text-slate-400">Four-pillar structured findings: What Happened, Pattern, Importance, and Recommendation</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => onNavigate('visualizations')}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 cursor-pointer"
              >
                <BarChart2 className="w-3.5 h-3.5 text-blue-400" />
                <span>View {analysisResults.visualizations?.length || 0} Charts</span>
              </button>

              <button
                onClick={() => onNavigate('reports')}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white cursor-pointer"
              >
                <FileSpreadsheet className="w-3.5 h-3.5" />
                <span>Executive Report</span>
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {analysisResults.insights.map((ins, i) => (
              <div
                key={i}
                className="p-5 rounded-xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 shadow-md space-y-3 transition-all flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <span className="font-bold text-sm text-slate-100 leading-snug">{ins.title}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider shrink-0 ${
                      ins.impact_level === 'high'
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : ins.impact_level === 'medium'
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                    }`}>
                      {ins.category.replace('_', ' ')}
                    </span>
                  </div>

                  <div className="space-y-2 text-xs">
                    <div className="bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/60">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">What Happened?</div>
                      <div className="text-slate-300 mt-0.5">{ins.finding}</div>
                    </div>

                    <div className="bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/60">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Pattern & Underlying Cause</div>
                      <div className="text-slate-300 mt-0.5">{ins.pattern}</div>
                    </div>

                    <div className="bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/60">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Why It Matters</div>
                      <div className="text-slate-300 mt-0.5">{ins.importance}</div>
                    </div>
                  </div>
                </div>

                <div className="mt-2 pt-3 border-t border-slate-800 flex items-start gap-2 bg-emerald-950/20 p-2.5 rounded-lg border border-emerald-500/20">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <div className="text-xs">
                    <span className="font-bold text-emerald-300">Action: </span>
                    <span className="text-slate-200">{ins.recommendation}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
