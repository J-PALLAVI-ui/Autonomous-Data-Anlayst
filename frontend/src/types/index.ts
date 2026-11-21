export interface ColumnProfile {
  name: string;
  dtype: string;
  general_type: 'numeric' | 'categorical' | 'datetime' | 'boolean' | 'id_or_unique';
  total_count: number;
  null_count: number;
  null_percentage: number;
  unique_count: number;
  sample_values: any[];
  stats?: {
    min?: number;
    max?: number;
    mean?: number;
    median?: number;
    std?: number;
    q25?: number;
    q75?: number;
    top_values?: Record<string, number>;
    min_date?: string;
    max_date?: string;
    timespan_days?: number;
  };
}

export interface DatasetQuality {
  missing_cells: number;
  missing_cells_pct: number;
  duplicate_rows: number;
  duplicate_rows_pct: number;
  outlier_count: number;
  total_cells: number;
  score: number;
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  missing_by_column?: Record<string, { count: number; percentage: number }>;
  outliers_by_column?: Record<string, { count: number; percentage: number; lower_bound: number; upper_bound: number }>;
  completeness_by_column?: Record<string, number>;
  issues: Array<{
    type: string;
    severity: 'high' | 'medium' | 'low';
    message: string;
  }>;
  recommendations: Array<{
    action: string;
    target?: string | string[];
    title: string;
    description: string;
    impact: string;
  }>;
}

export interface Dataset {
  id: string;
  filename: string;
  file_size_bytes: number;
  row_count: number;
  column_count: number;
  quality_score: number;
  created_at: string;
  columns?: ColumnProfile[];
  preview_rows?: Record<string, any>[];
  quality?: DatasetQuality;
}

export interface ExecutionLogEntry {
  task: string;
  tool: string;
  status: 'running' | 'success' | 'warning' | 'error';
  execution_time_ms: number;
  summary: string;
  error?: string | null;
}

export interface AnalysisPlanItem {
  step_number: number;
  name: string;
  description: string;
  tool_to_use: string;
  target_columns: string[];
  rationale: string;
}

export interface ChartDefinition {
  id: string;
  title: string;
  chart_type: 'bar' | 'line' | 'pie' | 'histogram' | 'scatter' | 'box' | 'heatmap';
  x_axis?: string;
  y_axis?: string;
  description: string;
  data: any[];
  insights?: string;
  config?: any;
}

export interface AnalysisInsight {
  category: 'executive_summary' | 'key_driver' | 'anomaly' | 'trend' | 'recommendation' | 'risk';
  title: string;
  finding: string;
  pattern: string;
  importance: string;
  recommendation: string;
  confidence: number;
  impact_level: 'high' | 'medium' | 'low';
  supporting_columns: string[];
}

export interface AnalysisResults {
  session_id: string;
  dataset_id: string;
  dataset_name: string;
  status: string;
  plan: AnalysisPlanItem[];
  execution_logs: ExecutionLogEntry[];
  descriptive_stats: {
    numeric_summary: Record<string, any>;
    categorical_summary: Record<string, any>;
    grouped_breakdown: any[];
  };
  correlations: {
    columns: string[];
    matrix: Array<{ row: string; values: number[] }>;
    heatmap_cells: Array<{ x: string; y: string; correlation: number }>;
    significant_pairs: Array<{
      col1: string;
      col2: string;
      correlation: number;
      abs_correlation: number;
      strength: string;
      relationship: string;
    }>;
    summary: string;
  };
  trends?: {
    date_column: string;
    metric_column: string;
    frequency: string;
    direction: string;
    overall_growth_pct: number;
    peak_period: { period: string; sum: number };
    trough_period: { period: string; sum: number };
    trend_data: any[];
    summary: string;
  } | null;
  anomalies: {
    total_anomalies: number;
    anomaly_rate_pct: number;
    method: string;
    anomalous_records: Array<{
      row_index: number;
      severity_score: number;
      deviating_factors: string[];
      record: Record<string, any>;
    }>;
    column_outliers: Record<string, any>;
    summary: string;
  };
  visualizations: ChartDefinition[];
  insights: AnalysisInsight[];
  quality_score: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  tools_used?: string[];
  chart?: ChartDefinition | null;
  created_at: string;
}

export interface CleaningPreview {
  operation: string;
  rows_before: number;
  rows_after: number;
  columns_before: number;
  columns_after: number;
  sample_changes: any[];
  quality_score_before: number;
  quality_score_after: number;
}

export interface DashboardStats {
  total_datasets: number;
  total_analyses: number;
  total_insights: number;
  recent_analyses: Array<{
    session_id: string;
    dataset_id: string;
    dataset_name: string;
    status: string;
    current_step: string;
    progress_percent: number;
    created_at: string;
    completed_at?: string;
  }>;
  recent_datasets: Array<{
    id: string;
    filename: string;
    row_count: number;
    column_count: number;
    quality_score: number;
    created_at: string;
  }>;
}
