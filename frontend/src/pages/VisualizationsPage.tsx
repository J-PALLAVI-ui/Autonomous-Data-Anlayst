import React, { useState } from 'react';
import { BarChart3, Filter, Sparkles, Layers, Info } from 'lucide-react';
import { ChartDefinition, Dataset } from '../types';
import { ChartRenderer } from '../components/ChartRenderer';

interface VisualizationsPageProps {
  selectedDataset: Dataset | null;
  visualizations: ChartDefinition[];
  onStartAnalysis: () => void;
  isAnalyzing: boolean;
}

export const VisualizationsPage: React.FC<VisualizationsPageProps> = ({
  selectedDataset,
  visualizations,
  onStartAnalysis,
  isAnalyzing,
}) => {
  const [filterType, setFilterType] = useState<string>('all');

  const filteredCharts = visualizations.filter((chart) => {
    if (filterType === 'all') return true;
    return chart.chart_type === filterType;
  });

  const availableTypes = Array.from(new Set(visualizations.map((c) => c.chart_type)));

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <BarChart3 className="w-4 h-4" />
            </div>
            <h2 className="text-xl font-bold text-white tracking-tight">Interactive Visualizations</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            {selectedDataset
              ? `Displaying charts synthesized for '${selectedDataset.filename}'`
              : 'Select a dataset to view its visual charts.'}
          </p>
        </div>

        {/* Chart Filter Pills */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setFilterType('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              filterType === 'all'
                ? 'bg-blue-600 text-white shadow'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            All Charts ({visualizations.length})
          </button>
          {availableTypes.map((t) => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all cursor-pointer ${
                filterType === t
                  ? 'bg-blue-600 text-white shadow'
                  : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {visualizations.length === 0 ? (
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-12 text-center space-y-4">
          <Layers className="w-12 h-12 text-slate-600 mx-auto" />
          <h3 className="text-base font-bold text-slate-200">No Visualizations Synthesized Yet</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            The AI agent creates goal-oriented charts during the autonomous analysis lifecycle based on statistical relationships.
          </p>
          <button
            onClick={onStartAnalysis}
            disabled={isAnalyzing || !selectedDataset}
            className="px-5 py-2.5 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white cursor-pointer shadow-lg shadow-blue-600/20"
          >
            Run Autonomous Analysis Now
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredCharts.map((chart) => (
            <ChartRenderer key={chart.id} chart={chart} />
          ))}
        </div>
      )}
    </div>
  );
};
