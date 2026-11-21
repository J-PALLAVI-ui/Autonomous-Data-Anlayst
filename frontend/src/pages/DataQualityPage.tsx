import React, { useState } from 'react';
import {
  ShieldCheck,
  AlertTriangle,
  CheckCircle2,
  Trash2,
  Sparkles,
  ArrowRight,
  Filter,
  RefreshCw,
  SlidersHorizontal,
  Info
} from 'lucide-react';
import { Dataset, CleaningPreview } from '../types';
import { api } from '../services/api';

interface DataQualityPageProps {
  selectedDataset: Dataset | null;
  onDatasetUpdated: (dataset: Dataset) => void;
}

export const DataQualityPage: React.FC<DataQualityPageProps> = ({
  selectedDataset,
  onDatasetUpdated,
}) => {
  const [cleaningPreview, setCleaningPreview] = useState<CleaningPreview | null>(null);
  const [activeOperation, setActiveOperation] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  if (!selectedDataset || !selectedDataset.quality) {
    return (
      <div className="p-8 max-w-7xl mx-auto">
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 text-xs">
          Please select or upload a dataset to view data quality analysis.
        </div>
      </div>
    );
  }

  const { quality } = selectedDataset;

  const handlePreview = async (operation: string, params: any = {}) => {
    try {
      setIsLoading(true);
      setActiveOperation(operation);
      setMessage(null);
      const preview = await api.previewCleaning(selectedDataset.id, operation, params);
      setCleaningPreview(preview);
    } catch (err: any) {
      setMessage(`Preview error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApply = async () => {
    if (!activeOperation) return;
    try {
      setIsLoading(true);
      const res = await api.applyCleaning(selectedDataset.id, activeOperation);
      setMessage(`Successfully created cleaned dataset: '${res.filename}' with Quality Score: ${res.quality_score}/100!`);
      setCleaningPreview(null);
      // Fetch new dataset details
      const newD = await api.getDataset(res.new_dataset_id);
      onDatasetUpdated(newD);
    } catch (err: any) {
      setMessage(`Application error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header & Quality Score Card */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <h2 className="text-xl font-bold text-white tracking-tight">Data Quality & Health Scorecard</h2>
          </div>
          <p className="text-xs text-slate-400">
            Comprehensive audit of completeness, duplicates, type validity, and distribution outliers for '{selectedDataset.filename}'
          </p>
        </div>

        {/* Big Score Dial */}
        <div className="flex items-center gap-4 bg-slate-900 border border-slate-800 rounded-2xl px-6 py-3">
          <div className="text-right">
            <div className="text-[10px] uppercase font-bold text-slate-400">Quality Index</div>
            <div className="text-2xl font-black text-emerald-400 tracking-tight">
              {quality.score} <span className="text-sm font-normal text-slate-500">/ 100</span>
            </div>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center font-black text-xl text-emerald-400">
            {quality.grade}
          </div>
        </div>
      </div>

      {message && (
        <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs flex items-center gap-2">
          <Info className="w-4 h-4 shrink-0" />
          <span>{message}</span>
        </div>
      )}

      {/* 4 Core Quality Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="text-xs font-semibold text-slate-400">Missing Values</div>
          <div className="text-2xl font-bold text-white">{quality.missing_cells_pct}%</div>
          <p className="text-[11px] text-slate-500">
            {quality.missing_cells.toLocaleString()} empty cells in matrix
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="text-xs font-semibold text-slate-400">Duplicate Records</div>
          <div className="text-2xl font-bold text-white">{quality.duplicate_rows_pct}%</div>
          <p className="text-[11px] text-slate-500">
            {quality.duplicate_rows} redundant row entries
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="text-xs font-semibold text-slate-400">Statistical Outliers</div>
          <div className="text-2xl font-bold text-white">{quality.outlier_count}</div>
          <p className="text-[11px] text-slate-500">
            Values outside 1.5x IQR boundaries
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
          <div className="text-xs font-semibold text-slate-400">Matrix Completeness</div>
          <div className="text-2xl font-bold text-emerald-400">
            {(100 - quality.missing_cells_pct).toFixed(1)}%
          </div>
          <p className="text-[11px] text-slate-500">
            {quality.total_cells.toLocaleString()} total data coordinates
          </p>
        </div>
      </div>

      {/* Interactive Remediation & Cleaning Studio */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-6">
        <div>
          <h3 className="text-base font-bold text-white tracking-tight">Interactive Cleaning Studio</h3>
          <p className="text-xs text-slate-400">
            Safe, non-destructive cleaning operations. Preview impacts before applying.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3 flex flex-col justify-between">
            <div>
              <div className="font-semibold text-sm text-slate-200">Deduplicate Dataset</div>
              <p className="text-xs text-slate-400 mt-1">
                Removes all {quality.duplicate_rows} duplicate rows, maintaining unique records only.
              </p>
            </div>
            <button
              onClick={() => handlePreview('drop_duplicates')}
              disabled={quality.duplicate_rows === 0 || isLoading}
              className={`w-full py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                quality.duplicate_rows === 0
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-500 text-white'
              }`}
            >
              Preview Deduplication
            </button>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3 flex flex-col justify-between">
            <div>
              <div className="font-semibold text-sm text-slate-200">Impute Missing Values</div>
              <p className="text-xs text-slate-400 mt-1">
                Fills missing numerical cells with median and categoricals with mode.
              </p>
            </div>
            <button
              onClick={() => handlePreview('fill_missing', { method: 'median' })}
              disabled={quality.missing_cells === 0 || isLoading}
              className={`w-full py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                quality.missing_cells === 0
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-500 text-white'
              }`}
            >
              Preview Imputation
            </button>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3 flex flex-col justify-between">
            <div>
              <div className="font-semibold text-sm text-slate-200">Filter Extreme Outliers</div>
              <p className="text-xs text-slate-400 mt-1">
                Filters statistical extreme values outside 1.5x IQR boundaries.
              </p>
            </div>
            <button
              onClick={() => {
                const numericCol = Object.keys(quality.outliers_by_column || {})[0];
                handlePreview('remove_outliers', { column: numericCol });
              }}
              disabled={quality.outlier_count === 0 || isLoading}
              className={`w-full py-2 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                quality.outlier_count === 0
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-500 text-white'
              }`}
            >
              Preview Outlier Trimming
            </button>
          </div>
        </div>

        {/* Cleaning Preview Modal / Box */}
        {cleaningPreview && (
          <div className="p-5 rounded-xl bg-slate-900 border border-blue-500/40 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-blue-400" />
                <h4 className="font-bold text-sm text-white">
                  Cleaning Preview: {cleaningPreview.operation.replace('_', ' ')}
                </h4>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCleaningPreview(null)}
                  className="px-3 py-1 rounded-lg text-xs text-slate-400 hover:text-slate-200 cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  onClick={handleApply}
                  disabled={isLoading}
                  className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white cursor-pointer shadow"
                >
                  {isLoading ? 'Applying...' : 'Approve & Save Cleaned Dataset'}
                </button>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
              <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                <div className="text-slate-500">Rows Impact</div>
                <div className="text-slate-200 font-bold mt-1">
                  {cleaningPreview.rows_before} → {cleaningPreview.rows_after}
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                <div className="text-slate-500">Columns Impact</div>
                <div className="text-slate-200 font-bold mt-1">
                  {cleaningPreview.columns_before} → {cleaningPreview.columns_after}
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                <div className="text-slate-500">Quality Score Before</div>
                <div className="text-amber-400 font-bold mt-1">
                  {cleaningPreview.quality_score_before} / 100
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800">
                <div className="text-slate-500">Quality Score After</div>
                <div className="text-emerald-400 font-bold mt-1">
                  {cleaningPreview.quality_score_after} / 100
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Column Completeness Progress List */}
      {quality.completeness_by_column && (
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
          <h3 className="text-base font-bold text-white tracking-tight">Column Completeness Breakdown</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(quality.completeness_by_column).map(([col, pct]) => {
              const numPct = typeof pct === 'number' ? pct : 100;
              return (
                <div key={col} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-slate-200">{col}</span>
                    <span className={numPct === 100 ? 'text-emerald-400 font-mono' : 'text-amber-400 font-mono'}>
                      {numPct}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${numPct === 100 ? 'bg-emerald-500' : 'bg-amber-500'}`}
                      style={{ width: `${numPct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
