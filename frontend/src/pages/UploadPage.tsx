import React, { useState, useRef } from 'react';
import {
  UploadCloud,
  FileSpreadsheet,
  CheckCircle2,
  AlertTriangle,
  Database,
  Trash2,
  Play,
  Table as TableIcon,
  Sparkles,
  Info,
  Download
} from 'lucide-react';
import { Dataset, ColumnProfile } from '../types';
import { api } from '../services/api';

interface UploadPageProps {
  onDatasetUploaded: (dataset: Dataset) => void;
  selectedDataset: Dataset | null;
  onSelectDataset: (dataset: Dataset) => void;
  onStartAnalysis: () => void;
  isAnalyzing: boolean;
  onDeleteDataset: (id: string) => void;
}

export const UploadPage: React.FC<UploadPageProps> = ({
  onDatasetUploaded,
  selectedDataset,
  onStartAnalysis,
  isAnalyzing,
  onDeleteDataset,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    setError(null);
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (!['csv', 'xlsx', 'xls'].includes(ext || '')) {
      setError('Unsupported file type. Please upload a .csv, .xlsx, or .xls file.');
      return;
    }

    try {
      setIsUploading(true);
      const dataset = await api.uploadDataset(file);
      onDatasetUploaded(dataset);
    } catch (err: any) {
      setError(err.message || 'Failed to upload and parse dataset');
    } finally {
      setIsUploading(false);
    }
  };

  const handleLoadSample = async (filename: string) => {
    try {
      setIsUploading(true);
      setError(null);
      const res = await fetch(`/sample_datasets/${filename}`);
      if (!res.ok) throw new Error('Failed to fetch sample dataset file');
      const blob = await res.blob();
      const file = new File([blob], filename, { type: blob.type || 'text/csv' });
      const dataset = await api.uploadDataset(file);
      onDatasetUploaded(dataset);
    } catch (err: any) {
      setError(err.message || 'Failed to load sample dataset');
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const getTypeBadge = (type: string) => {
    switch (type) {
      case 'numeric':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
      case 'categorical':
        return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
      case 'datetime':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
      case 'boolean':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
      default:
        return 'bg-slate-700 text-slate-300 border-slate-600';
    }
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Upload Dropzone */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-10 text-center transition-all cursor-pointer ${
          isDragging
            ? 'border-blue-500 bg-blue-950/20 shadow-xl shadow-blue-500/10'
            : 'border-slate-800 bg-slate-950/60 hover:border-slate-700 hover:bg-slate-900/40'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          className="hidden"
          onChange={(e) => {
            if (e.target.files && e.target.files.length > 0) {
              handleFile(e.target.files[0]);
            }
          }}
        />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="w-14 h-14 rounded-2xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            {isUploading ? (
              <Sparkles className="w-6 h-6 animate-spin" />
            ) : (
              <UploadCloud className="w-6 h-6" />
            )}
          </div>

          <div>
            <h3 className="text-base font-bold text-slate-100">
              {isUploading ? 'Ingesting and Profiling Dataset...' : 'Click to Upload or Drag & Drop'}
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Supports CSV, Excel (.xlsx, .xls) up to 50MB
            </p>
          </div>

          <div className="flex items-center gap-3 text-[11px] text-slate-500">
            <span>• Automatic Schema Detection</span>
            <span>• Data Quality Scoring</span>
            <span>• Outlier Screening</span>
          </div>
        </div>
      </div>

      {/* Sample Datasets Ready to Test */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-400" />
              <h3 className="text-sm font-bold text-white tracking-tight">Ready-to-Use Benchmark Datasets</h3>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Click "One-Click Ingest" to immediately load and analyze any sample dataset, or download the files.
            </p>
          </div>
          <a
            href="/sample_datasets/sample_datasets.zip"
            download
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 transition-all cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-blue-400" />
            <span>Download All Datasets (.zip)</span>
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            {
              file: 'ecommerce_transactions_2025.csv',
              title: 'E-Commerce Retail',
              desc: '500 orders, 13 features (Sales, Profit, Discounts, Dates)',
              type: 'CSV',
              color: 'text-blue-400 border-blue-500/20 bg-blue-500/10'
            },
            {
              file: 'saas_churn_and_revenue.xlsx',
              title: 'SaaS Churn & Revenue',
              desc: '400 subscribers, 11 features (Tiers, Tenure, Spend, Churn)',
              type: 'Excel (.xlsx)',
              color: 'text-emerald-400 border-emerald-500/20 bg-emerald-500/10'
            },
            {
              file: 'financial_loan_portfolio.csv',
              title: 'Loan Portfolio & Risk',
              desc: '450 loans, 12 features (Credit Score, Income, Default Rate)',
              type: 'CSV',
              color: 'text-amber-400 border-amber-500/20 bg-amber-500/10'
            },
            {
              file: 'healthcare_patient_vitals.csv',
              title: 'Healthcare Patient Vitals',
              desc: '350 patients, 12 features (Blood Pressure, BMI, Glucose, Risk)',
              type: 'CSV',
              color: 'text-purple-400 border-purple-500/20 bg-purple-500/10'
            }
          ].map((item) => (
            <div
              key={item.file}
              className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 flex flex-col justify-between space-y-3 hover:border-slate-700 transition-all"
            >
              <div className="space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-slate-200">{item.title}</span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${item.color}`}>
                    {item.type}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">{item.desc}</p>
              </div>

              <div className="flex items-center gap-2 pt-2 border-t border-slate-800/60">
                <button
                  onClick={() => handleLoadSample(item.file)}
                  disabled={isUploading}
                  className="flex-1 py-1.5 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white cursor-pointer shadow transition-all text-center"
                >
                  One-Click Ingest
                </button>
                <a
                  href={`/sample_datasets/${item.file}`}
                  download
                  title="Download Raw File"
                  className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Dataset Profile & Details View */}
      {selectedDataset && (
        <div className="space-y-6">
          {/* Summary Strip */}
          <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <FileSpreadsheet className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-white tracking-tight">
                  {selectedDataset.filename}
                </h2>
                <div className="flex items-center gap-3 text-xs text-slate-400 mt-0.5">
                  <span>{(selectedDataset.file_size_bytes / 1024).toFixed(1)} KB</span>
                  <span>•</span>
                  <span>{selectedDataset.row_count.toLocaleString()} rows</span>
                  <span>•</span>
                  <span>{selectedDataset.column_count} columns</span>
                  <span>•</span>
                  <span>Uploaded {new Date(selectedDataset.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="text-right">
                <div className="text-[10px] uppercase font-bold text-slate-500">Data Quality Score</div>
                <div className="text-xl font-extrabold text-emerald-400">
                  {selectedDataset.quality_score}/100
                </div>
              </div>

              <button
                onClick={onStartAnalysis}
                disabled={isAnalyzing}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-blue-600/20 cursor-pointer"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Launch Autonomous Analysis</span>
              </button>

              <button
                onClick={() => onDeleteDataset(selectedDataset.id)}
                title="Delete Dataset"
                className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-rose-400 hover:border-rose-500/30 transition-all cursor-pointer"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Quality Metrics Highlights */}
          {selectedDataset.quality && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div className="text-xs text-slate-400">Missing Values</div>
                <div className="text-xl font-bold text-slate-100 mt-1">
                  {selectedDataset.quality.missing_cells_pct}%
                </div>
                <div className="text-[11px] text-slate-500">
                  {selectedDataset.quality.missing_cells} cells missing
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div className="text-xs text-slate-400">Duplicate Records</div>
                <div className="text-xl font-bold text-slate-100 mt-1">
                  {selectedDataset.quality.duplicate_rows_pct}%
                </div>
                <div className="text-[11px] text-slate-500">
                  {selectedDataset.quality.duplicate_rows} duplicate rows
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div className="text-xs text-slate-400">Detected Outliers</div>
                <div className="text-xl font-bold text-slate-100 mt-1">
                  {selectedDataset.quality.outlier_count}
                </div>
                <div className="text-[11px] text-slate-500">
                  Via 1.5x IQR boundaries
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div className="text-xs text-slate-400">Quality Assessment</div>
                <div className="text-xl font-bold text-emerald-400 mt-1">
                  Grade {selectedDataset.quality.grade}
                </div>
                <div className="text-[11px] text-slate-500">
                  {selectedDataset.quality.issues.length} flagged issue(s)
                </div>
              </div>
            </div>
          )}

          {/* Schema & Data Types Breakdown */}
          {selectedDataset.columns && selectedDataset.columns.length > 0 && (
            <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-white tracking-tight">Inferred Schema & Column Attributes</h3>
                  <p className="text-xs text-slate-400">Identified column classifications, completeness, and values</p>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="min-w-full text-xs">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400">
                      <th className="py-2.5 text-left font-semibold">Column Name</th>
                      <th className="py-2.5 text-left font-semibold">General Type</th>
                      <th className="py-2.5 text-left font-semibold">Native Dtype</th>
                      <th className="py-2.5 text-left font-semibold">Nulls</th>
                      <th className="py-2.5 text-left font-semibold">Distinct</th>
                      <th className="py-2.5 text-left font-semibold">Sample Values</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-900">
                    {selectedDataset.columns.map((col: ColumnProfile) => (
                      <tr key={col.name} className="hover:bg-slate-900/40">
                        <td className="py-2.5 font-semibold text-slate-200">{col.name}</td>
                        <td className="py-2.5">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider ${getTypeBadge(col.general_type)}`}>
                            {col.general_type}
                          </span>
                        </td>
                        <td className="py-2.5 font-mono text-[11px] text-slate-400">{col.dtype}</td>
                        <td className="py-2.5 text-slate-300">
                          {col.null_count > 0 ? (
                            <span className="text-amber-400 font-medium">
                              {col.null_count} ({col.null_percentage}%)
                            </span>
                          ) : (
                            <span className="text-slate-500">0%</span>
                          )}
                        </td>
                        <td className="py-2.5 text-slate-300">{col.unique_count.toLocaleString()}</td>
                        <td className="py-2.5 text-slate-400 font-mono text-[11px] truncate max-w-xs">
                          {col.sample_values?.slice(0, 3).map((v) => String(v)).join(', ')}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Dataset Interactive Preview Table */}
          {selectedDataset.preview_rows && selectedDataset.preview_rows.length > 0 && (
            <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <TableIcon className="w-4 h-4 text-blue-400" />
                  <h3 className="text-base font-bold text-white tracking-tight">Dataset Preview (First 15 Records)</h3>
                </div>
                <span className="text-xs text-slate-500 font-medium">
                  Showing {selectedDataset.preview_rows.length} rows of {selectedDataset.row_count.toLocaleString()}
                </span>
              </div>

              <div className="overflow-x-auto rounded-xl border border-slate-800 max-h-96">
                <table className="min-w-full text-xs">
                  <thead className="bg-slate-900 sticky top-0 z-10">
                    <tr className="border-b border-slate-800 text-slate-300">
                      <th className="p-2.5 text-left font-semibold text-slate-500 w-12">#</th>
                      {Object.keys(selectedDataset.preview_rows[0] || {}).map((col) => (
                        <th key={col} className="p-2.5 text-left font-semibold whitespace-nowrap">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 bg-slate-950/40">
                    {selectedDataset.preview_rows.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-900/40">
                        <td className="p-2.5 text-slate-500 font-mono text-[10px]">{idx + 1}</td>
                        {Object.keys(row).map((col) => (
                          <td key={col} className="p-2.5 text-slate-300 font-mono text-[11px] whitespace-nowrap">
                            {row[col] !== null && row[col] !== undefined ? String(row[col]) : <span className="text-slate-600 italic">null</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
