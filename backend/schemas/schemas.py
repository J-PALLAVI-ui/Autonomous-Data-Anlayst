from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ColumnProfile(BaseModel):
    name: str
    dtype: str
    general_type: str # 'numeric', 'categorical', 'datetime', 'boolean', 'id_or_unique'
    total_count: int
    null_count: int
    null_percentage: float
    unique_count: int
    sample_values: List[Any] = []
    stats: Optional[Dict[str, Any]] = None # min, max, mean, median, std, q25, q75 for numeric; top_values for categorical

class DatasetQualityMetric(BaseModel):
    missing_cells: int
    missing_cells_pct: float
    duplicate_rows: int
    duplicate_rows_pct: float
    outlier_count: int
    total_cells: int
    score: float # 0 - 100
    grade: str # A, B, C, D, F
    issues: List[Dict[str, Any]] = []
    recommendations: List[Dict[str, Any]] = []

class DatasetSummary(BaseModel):
    id: str
    filename: str
    file_size_bytes: int
    row_count: int
    column_count: int
    created_at: datetime
    columns: List[ColumnProfile]
    preview_rows: List[Dict[str, Any]]
    quality: DatasetQualityMetric

class DatasetListItem(BaseModel):
    id: str
    filename: str
    file_size_bytes: int
    row_count: int
    column_count: int
    quality_score: float
    created_at: datetime

class ExecutionLogEntry(BaseModel):
    task: str
    tool: str
    status: str # 'running', 'success', 'warning', 'error'
    execution_time_ms: float
    summary: str
    error: Optional[str] = None

class AnalysisPlanItem(BaseModel):
    step_number: int
    name: str
    description: str
    tool_to_use: str
    target_columns: List[str] = []
    rationale: str

class StartAnalysisRequest(BaseModel):
    dataset_id: str
    user_instructions: Optional[str] = None
    focus_columns: Optional[List[str]] = None

class AnalysisStatusResponse(BaseModel):
    session_id: str
    dataset_id: str
    status: str
    current_step: str
    progress_percent: int
    logs: List[ExecutionLogEntry]
    created_at: datetime
    completed_at: Optional[datetime] = None

class ChartDefinition(BaseModel):
    id: str
    title: str
    chart_type: str # 'bar', 'line', 'pie', 'histogram', 'scatter', 'box', 'heatmap'
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    description: str
    data: List[Dict[str, Any]]
    insights: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

class AnalysisInsight(BaseModel):
    category: str # 'executive_summary', 'key_driver', 'anomaly', 'trend', 'recommendation', 'risk'
    title: str
    finding: str # What happened?
    pattern: str # What patterns were identified?
    importance: str # Why is the finding important?
    recommendation: str # What action or recommendation can be considered?
    confidence: float # 0.0 - 1.0
    impact_level: str # 'high', 'medium', 'low'
    supporting_columns: List[str] = []

class AnalysisResultResponse(BaseModel):
    session_id: str
    dataset_id: str
    status: str
    plan: List[AnalysisPlanItem]
    execution_logs: List[ExecutionLogEntry]
    descriptive_stats: Dict[str, Any]
    correlations: Dict[str, Any]
    distributions: Dict[str, Any]
    trends: Optional[Dict[str, Any]] = None
    anomalies: Dict[str, Any]
    visualizations: List[ChartDefinition]
    insights: List[AnalysisInsight]
    quality_score: float

class ChatQueryRequest(BaseModel):
    dataset_id: str
    session_id: Optional[str] = None
    message: str

class ChatQueryResponse(BaseModel):
    id: str
    role: str
    content: str
    tools_used: List[str] = []
    chart: Optional[ChartDefinition] = None
    created_at: datetime

class CleaningOperationRequest(BaseModel):
    dataset_id: str
    operation: str # 'drop_duplicates', 'fill_missing', 'drop_columns', 'remove_outliers'
    params: Dict[str, Any] = {}

class CleaningPreviewResponse(BaseModel):
    operation: str
    rows_before: int
    rows_after: int
    columns_before: int
    columns_after: int
    sample_changes: List[Dict[str, Any]]
    quality_score_before: float
    quality_score_after: float
