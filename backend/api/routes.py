import os
import json
import uuid
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.connection import get_db
from models.models import DatasetModel, AnalysisSessionModel, ChatMessageModel, ReportModel
from schemas.schemas import (
    DatasetSummary, DatasetListItem, StartAnalysisRequest,
    AnalysisStatusResponse, AnalysisResultResponse, ChatQueryRequest,
    ChatQueryResponse, CleaningOperationRequest, CleaningPreviewResponse
)
from tools.dataset_profiler import profile_dataset, load_dataset
from tools.data_quality_checker import calculate_data_quality, preview_cleaning_operation
from tools.report_generator import generate_pdf_report, export_analysis_csv, REPORTS_DIR
from agents.autonomous_analyst import AutonomousAnalystAgent, process_chat_query

router = APIRouter(prefix="/api")

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# --- DASHBOARD STATS ---
@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_datasets = db.query(DatasetModel).count()
    total_analyses = db.query(AnalysisSessionModel).filter(AnalysisSessionModel.status == "completed").count()
    
    # Count insights generated
    sessions = db.query(AnalysisSessionModel).filter(AnalysisSessionModel.status == "completed").all()
    total_insights = 0
    for s in sessions:
        if s.insights_json:
            try:
                insights_list = json.loads(s.insights_json)
                total_insights += len(insights_list)
            except Exception:
                pass
                
    recent_analyses = []
    recent_sessions = db.query(AnalysisSessionModel).order_by(desc(AnalysisSessionModel.created_at)).limit(5).all()
    for s in recent_sessions:
        dataset = db.query(DatasetModel).filter(DatasetModel.id == s.dataset_id).first()
        recent_analyses.append({
            "session_id": s.id,
            "dataset_id": s.dataset_id,
            "dataset_name": dataset.filename if dataset else "Unknown Dataset",
            "status": s.status,
            "current_step": s.current_step,
            "progress_percent": s.progress_percent,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "completed_at": s.completed_at.isoformat() if s.completed_at else None
        })
        
    recent_datasets = db.query(DatasetModel).order_by(desc(DatasetModel.created_at)).limit(5).all()
    datasets_activity = [
        {
            "id": d.id,
            "filename": d.filename,
            "row_count": d.row_count,
            "column_count": d.column_count,
            "quality_score": d.quality_score,
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in recent_datasets
    ]
    
    return {
        "total_datasets": total_datasets,
        "total_analyses": total_analyses,
        "total_insights": total_insights,
        "recent_analyses": recent_analyses,
        "recent_datasets": datasets_activity
    }


# --- DATASET MANAGEMENT ---
@router.post("/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validation
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".csv", ".xlsx", ".xls"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a CSV or Excel (.xlsx, .xls) file.")
        
    dataset_id = str(uuid.uuid4())
    saved_filename = f"{dataset_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_size = os.path.getsize(file_path)
    
    # Process dataset
    try:
        df = load_dataset(file_path)
        profile = profile_dataset(df)
        quality = calculate_data_quality(df)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Failed to parse dataset file: {str(e)}")
        
    dataset = DatasetModel(
        id=dataset_id,
        filename=file.filename,
        file_path=file_path,
        file_size_bytes=file_size,
        row_count=profile["row_count"],
        column_count=profile["column_count"],
        summary_json=json.dumps(profile),
        quality_score=quality["score"],
        quality_metrics_json=json.dumps(quality)
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    return {
        "id": dataset.id,
        "filename": dataset.filename,
        "file_size_bytes": dataset.file_size_bytes,
        "row_count": dataset.row_count,
        "column_count": dataset.column_count,
        "quality_score": dataset.quality_score,
        "created_at": dataset.created_at.isoformat(),
        "columns": profile["columns"],
        "preview_rows": profile["preview_rows"],
        "quality": quality
    }


@router.get("/datasets", response_model=List[DatasetListItem])
def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(DatasetModel).order_by(desc(DatasetModel.created_at)).all()
    return [
        DatasetListItem(
            id=d.id,
            filename=d.filename,
            file_size_bytes=d.file_size_bytes,
            row_count=d.row_count,
            column_count=d.column_count,
            quality_score=d.quality_score,
            created_at=d.created_at
        )
        for d in datasets
    ]


@router.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    dataset = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    profile = json.loads(dataset.summary_json) if dataset.summary_json else {}
    quality = json.loads(dataset.quality_metrics_json) if dataset.quality_metrics_json else {}
    
    return {
        "id": dataset.id,
        "filename": dataset.filename,
        "file_size_bytes": dataset.file_size_bytes,
        "row_count": dataset.row_count,
        "column_count": dataset.column_count,
        "quality_score": dataset.quality_score,
        "created_at": dataset.created_at.isoformat(),
        "columns": profile.get("columns", []),
        "preview_rows": profile.get("preview_rows", []),
        "quality": quality
    }


@router.get("/datasets/{dataset_id}/preview")
def get_dataset_preview(dataset_id: str, db: Session = Depends(get_db)):
    dataset = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    profile = json.loads(dataset.summary_json) if dataset.summary_json else {}
    return {
        "id": dataset.id,
        "filename": dataset.filename,
        "columns": profile.get("columns", []),
        "preview_rows": profile.get("preview_rows", [])
    }


@router.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: str, db: Session = Depends(get_db)):
    dataset = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    # Remove file on disk if exists
    if dataset.file_path and os.path.exists(dataset.file_path):
        try:
            os.remove(dataset.file_path)
        except Exception:
            pass
            
    # Cascade delete in DB
    db.query(AnalysisSessionModel).filter(AnalysisSessionModel.dataset_id == dataset_id).delete()
    db.query(ChatMessageModel).filter(ChatMessageModel.dataset_id == dataset_id).delete()
    db.query(ReportModel).filter(ReportModel.dataset_id == dataset_id).delete()
    db.delete(dataset)
    db.commit()
    
    return {"status": "success", "message": f"Dataset '{dataset.filename}' and all associated analyses deleted."}


# --- AUTONOMOUS ANALYSIS PIPELINE ---
def run_analysis_task(session_id: str):
    from database.connection import SessionLocal
    db = SessionLocal()
    try:
        agent = AutonomousAnalystAgent(db)
        agent.run_analysis(session_id)
    finally:
        db.close()

@router.post("/analysis/start")
def start_analysis(
    req: StartAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    dataset = db.query(DatasetModel).filter(DatasetModel.id == req.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    session_id = str(uuid.uuid4())
    session = AnalysisSessionModel(
        id=session_id,
        dataset_id=dataset.id,
        status="running",
        current_step="understanding",
        progress_percent=10,
        execution_logs_json=json.dumps([{
            "task": "Initialize Autonomous Agent",
            "tool": "orchestrator",
            "status": "success",
            "execution_time_ms": 1.0,
            "summary": f"Initialized analysis session for '{dataset.filename}'."
        }])
    )
    db.add(session)
    db.commit()
    
    # Run the agent in background task
    background_tasks.add_task(run_analysis_task, session_id)
    
    return {
        "session_id": session_id,
        "dataset_id": dataset.id,
        "status": "running",
        "current_step": "understanding",
        "progress_percent": 10
    }


@router.get("/analysis/{session_id}/status")
def get_analysis_status(session_id: str, db: Session = Depends(get_db)):
    session = db.query(AnalysisSessionModel).filter(AnalysisSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Analysis session not found")
        
    logs = json.loads(session.execution_logs_json) if session.execution_logs_json else []
    
    return {
        "session_id": session.id,
        "dataset_id": session.dataset_id,
        "status": session.status,
        "current_step": session.current_step,
        "progress_percent": session.progress_percent,
        "logs": logs,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None
    }


@router.get("/analysis/{session_id}/results")
def get_analysis_results(session_id: str, db: Session = Depends(get_db)):
    session = db.query(AnalysisSessionModel).filter(AnalysisSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Analysis session not found")
        
    dataset = db.query(DatasetModel).filter(DatasetModel.id == session.dataset_id).first()
    
    plan = json.loads(session.plan_json) if session.plan_json else []
    logs = json.loads(session.execution_logs_json) if session.execution_logs_json else []
    results = json.loads(session.results_json) if session.results_json else {}
    insights = json.loads(session.insights_json) if session.insights_json else []
    
    return {
        "session_id": session.id,
        "dataset_id": session.dataset_id,
        "dataset_name": dataset.filename if dataset else "Unknown Dataset",
        "status": session.status,
        "plan": plan,
        "execution_logs": logs,
        "descriptive_stats": results.get("descriptive_stats", {}),
        "correlations": results.get("correlations", {}),
        "trends": results.get("trends"),
        "anomalies": results.get("anomalies", {}),
        "visualizations": results.get("visualizations", []),
        "insights": insights,
        "quality_score": results.get("quality_score", dataset.quality_score if dataset else 100.0)
    }


# --- VISUALIZATIONS ---
@router.get("/visualizations/{session_or_dataset_id}")
def get_visualizations(session_or_dataset_id: str, db: Session = Depends(get_db)):
    # Try as session_id first
    session = db.query(AnalysisSessionModel).filter(AnalysisSessionModel.id == session_or_dataset_id).first()
    if not session:
        # Try latest completed session for dataset_id
        session = db.query(AnalysisSessionModel).filter(
            AnalysisSessionModel.dataset_id == session_or_dataset_id,
            AnalysisSessionModel.status == "completed"
        ).order_by(desc(AnalysisSessionModel.completed_at)).first()
        
    if not session or not session.results_json:
        raise HTTPException(status_code=404, detail="No visualizations found for this identifier.")
        
    results = json.loads(session.results_json)
    return {
        "session_id": session.id,
        "dataset_id": session.dataset_id,
        "visualizations": results.get("visualizations", [])
    }


# --- AI CHAT WITH YOUR DATA ---
@router.post("/chat")
def chat_with_dataset(req: ChatQueryRequest, db: Session = Depends(get_db)):
    dataset = db.query(DatasetModel).filter(DatasetModel.id == req.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    df = load_dataset(dataset.file_path)
    profile = json.loads(dataset.summary_json) if dataset.summary_json else profile_dataset(df)
    
    # Save user message
    user_msg = ChatMessageModel(
        dataset_id=dataset.id,
        session_id=req.session_id,
        role="user",
        content=req.message
    )
    db.add(user_msg)
    db.commit()
    
    # Process via agent
    analysis_results = None
    if req.session_id:
        sess = db.query(AnalysisSessionModel).filter(AnalysisSessionModel.id == req.session_id).first()
        if sess and sess.results_json:
            analysis_results = json.loads(sess.results_json)
            
    res = process_chat_query(df, req.message, profile, analysis_results)
    
    # Save assistant message
    asst_msg = ChatMessageModel(
        dataset_id=dataset.id,
        session_id=req.session_id,
        role="assistant",
        content=res["content"],
        tools_used_json=json.dumps(res.get("tools_used", [])),
        chart_data_json=json.dumps(res.get("chart")) if res.get("chart") else None
    )
    db.add(asst_msg)
    db.commit()
    db.refresh(asst_msg)
    
    return {
        "id": asst_msg.id,
        "role": "assistant",
        "content": asst_msg.content,
        "tools_used": res.get("tools_used", []),
        "chart": res.get("chart"),
        "created_at": asst_msg.created_at.isoformat()
    }


@router.get("/chat/{dataset_id}/history")
def get_chat_history(dataset_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatMessageModel).filter(ChatMessageModel.dataset_id == dataset_id).order_by(ChatMessageModel.created_at).all()
    out = []
    for m in messages:
        out.append({
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "tools_used": json.loads(m.tools_used_json) if m.tools_used_json else [],
            "chart": json.loads(m.chart_data_json) if m.chart_data_json else None,
            "created_at": m.created_at.isoformat()
        })
    return out


# --- DATA QUALITY CLEANING ---
@router.post("/quality/preview-cleaning")
def preview_cleaning(req: CleaningOperationRequest, db: Session = Depends(get_db)):
    dataset = db.query(DatasetModel).filter(DatasetModel.id == req.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    df = load_dataset(dataset.file_path)
    res = preview_cleaning_operation(df, req.operation, req.params)
    return res


@router.post("/quality/apply-cleaning")
def apply_cleaning(req: CleaningOperationRequest, db: Session = Depends(get_db)):
    dataset = db.query(DatasetModel).filter(DatasetModel.id == req.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    df = load_dataset(dataset.file_path)
    preview = preview_cleaning_operation(df, req.operation, req.params)
    
    # Save as new cleaned dataset version
    clean_df = df.copy()
    if req.operation == "drop_duplicates":
        clean_df = clean_df.drop_duplicates()
    elif req.operation == "fill_missing":
        method = req.params.get("method", "median")
        cols = req.params.get("columns", clean_df.columns.tolist())
        for c in cols:
            if c in clean_df.columns:
                if pd.api.types.is_numeric_dtype(clean_df[c]):
                    clean_df[c] = clean_df[c].fillna(clean_df[c].median() if method == "median" else clean_df[c].mean())
                else:
                    m = clean_df[c].mode()
                    clean_df[c] = clean_df[c].fillna(m[0] if not m.empty else "Unknown")
    elif req.operation == "drop_columns":
        cols_to_drop = [c for c in req.params.get("columns", []) if c in clean_df.columns]
        clean_df = clean_df.drop(columns=cols_to_drop)
    elif req.operation == "remove_outliers":
        col = req.params.get("column")
        if col and col in clean_df.columns and pd.api.types.is_numeric_dtype(clean_df[col]):
            q25 = clean_df[col].quantile(0.25)
            q75 = clean_df[col].quantile(0.75)
            iqr = q75 - q25
            lb = q25 - 1.5 * iqr
            ub = q75 + 1.5 * iqr
            clean_df = clean_df[(clean_df[col] >= lb) & (clean_df[col] <= ub)]
            
    # Save cleaned file
    clean_id = str(uuid.uuid4())
    base_name, ext = os.path.splitext(dataset.filename)
    clean_filename = f"{base_name}_cleaned_{req.operation}{ext}"
    clean_file_path = os.path.join(UPLOAD_DIR, f"{clean_id}_{clean_filename}")
    
    if ext.lower() in [".xlsx", ".xls"]:
        clean_df.to_excel(clean_file_path, index=False)
    else:
        clean_df.to_csv(clean_file_path, index=False)
        
    profile = profile_dataset(clean_df)
    quality = calculate_data_quality(clean_df)
    
    new_dataset = DatasetModel(
        id=clean_id,
        filename=clean_filename,
        file_path=clean_file_path,
        file_size_bytes=os.path.getsize(clean_file_path),
        row_count=profile["row_count"],
        column_count=profile["column_count"],
        summary_json=json.dumps(profile),
        quality_score=quality["score"],
        quality_metrics_json=json.dumps(quality)
    )
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    
    return {
        "status": "success",
        "new_dataset_id": new_dataset.id,
        "filename": new_dataset.filename,
        "rows": new_dataset.row_count,
        "columns": new_dataset.column_count,
        "quality_score": new_dataset.quality_score,
        "changes": preview
    }


# --- REPORTS ---
@router.get("/reports/{session_or_dataset_id}")
def get_report_meta(session_or_dataset_id: str, db: Session = Depends(get_db)):
    report = db.query(ReportModel).filter(
        (ReportModel.session_id == session_or_dataset_id) | (ReportModel.dataset_id == session_or_dataset_id)
    ).order_by(desc(ReportModel.created_at)).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found for this session.")
        
    return {
        "id": report.id,
        "dataset_id": report.dataset_id,
        "session_id": report.session_id,
        "title": report.title,
        "pdf_available": os.path.exists(report.pdf_path) if report.pdf_path else False,
        "report_data": json.loads(report.report_json),
        "created_at": report.created_at.isoformat()
    }


@router.get("/reports/{session_or_dataset_id}/pdf")
def download_report_pdf(session_or_dataset_id: str, db: Session = Depends(get_db)):
    report = db.query(ReportModel).filter(
        (ReportModel.session_id == session_or_dataset_id) | (ReportModel.dataset_id == session_or_dataset_id)
    ).order_by(desc(ReportModel.created_at)).first()
    
    if not report or not report.pdf_path or not os.path.exists(report.pdf_path):
        raise HTTPException(status_code=404, detail="PDF report file not found on disk.")
        
    return FileResponse(
        report.pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(report.pdf_path)
    )


@router.get("/reports/{session_or_dataset_id}/csv")
def download_analysis_csv(session_or_dataset_id: str, db: Session = Depends(get_db)):
    session = db.query(AnalysisSessionModel).filter(
        (AnalysisSessionModel.id == session_or_dataset_id) | (AnalysisSessionModel.dataset_id == session_or_dataset_id)
    ).order_by(desc(AnalysisSessionModel.created_at)).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
        
    dataset = db.query(DatasetModel).filter(DatasetModel.id == session.dataset_id).first()
    if not dataset or not os.path.exists(dataset.file_path):
        raise HTTPException(status_code=404, detail="Dataset file not found.")
        
    df = load_dataset(dataset.file_path)
    csv_path = export_analysis_csv(df, session.id)
    
    return FileResponse(
        csv_path,
        media_type="text/csv",
        filename=f"analysis_export_{dataset.filename}"
    )


# --- SETTINGS ---
@router.get("/settings")
def get_settings():
    api_key = os.getenv("GEMINI_API_KEY", "")
    return {
        "gemini_api_configured": bool(api_key and api_key.strip()),
        "gemini_api_preview": f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else ("Configured" if api_key else "Not Configured"),
        "active_model": "gemini-2.0-flash",
        "analytical_engine": "DuckDB & SQLite Memory",
        "ml_engine": "Scikit-Learn IsolationForest"
    }


@router.post("/settings")
def update_settings(payload: Dict[str, str]):
    api_key = payload.get("gemini_api_key")
    if api_key is not None:
        os.environ["GEMINI_API_KEY"] = api_key.strip()
    return {"status": "success", "message": "Settings updated successfully."}
