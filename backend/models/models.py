import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey
from database.connection import Base

class DatasetModel(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    summary_json = Column(Text, nullable=True) # JSON of columns, types, null counts, stats, preview
    quality_score = Column(Float, default=100.0)
    quality_metrics_json = Column(Text, nullable=True) # JSON of quality checks


class AnalysisSessionModel(Base):
    __tablename__ = "analysis_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending") # pending, running, completed, failed
    current_step = Column(String(50), default="understanding") # understanding, planning, executing, validating, generating_insights, completed
    progress_percent = Column(Integer, default=0)
    plan_json = Column(Text, nullable=True) # Analysis plan
    execution_logs_json = Column(Text, nullable=True) # List of tool execution entries
    results_json = Column(Text, nullable=True) # Statistical, anomaly, correlation results
    insights_json = Column(Text, nullable=True) # Natural language findings & recommendations
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(36), nullable=True)
    role = Column(String(20), nullable=False) # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    tools_used_json = Column(Text, nullable=True)
    chart_data_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(36), nullable=False)
    title = Column(String(255), nullable=False)
    pdf_path = Column(String(500), nullable=True)
    report_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
