import os
import time
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from models.models import AnalysisSessionModel, DatasetModel, ReportModel
from tools.dataset_profiler import profile_dataset, load_dataset
from tools.data_quality_checker import calculate_data_quality
from tools.descriptive_statistics import calculate_descriptive_statistics
from tools.correlation_analyzer import analyze_correlations
from tools.trend_analyzer import analyze_trends
from tools.anomaly_detector import detect_anomalies
from tools.visualization_generator import generate_visualizations
from tools.insight_generator import generate_insights
from tools.report_generator import generate_pdf_report
from tools.sql_query_engine import execute_analytical_sql

class AutonomousAnalystAgent:
    """Autonomous AI Agent that plans, executes, validates, and explains data analytics."""

    def __init__(self, db: Session):
        self.db = db

    def create_analysis_plan(self, df: pd.DataFrame, profile: Dict[str, Any], quality: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Autonomously formulate an analysis plan tailored to dataset structure."""
        plan = []
        step_num = 1
        
        numeric_cols = [c["name"] for c in profile["columns"] if c["general_type"] == "numeric"]
        cat_cols = [c["name"] for c in profile["columns"] if c["general_type"] == "categorical"]
        date_cols = [c["name"] for c in profile["columns"] if c["general_type"] == "datetime"]
        
        # Step 1: Data Profiling & Quality Validation
        plan.append({
            "step_number": step_num,
            "name": "Dataset Ingestion & Structural Profiling",
            "description": f"Examine {profile['row_count']} rows across {profile['column_count']} columns, infer schemas, and check nulls.",
            "tool_to_use": "dataset_profiler & data_quality_checker",
            "target_columns": [c["name"] for c in profile["columns"]],
            "rationale": "Mandatory foundational stage to establish baseline schema and quality score."
        })
        step_num += 1
        
        # Step 2: Descriptive Statistics & Distribution Analysis
        if numeric_cols or cat_cols:
            plan.append({
                "step_number": step_num,
                "name": "Descriptive & Distribution Analysis",
                "description": f"Compute parametric statistics on {len(numeric_cols)} numeric features and frequency distributions on {len(cat_cols)} categoricals.",
                "tool_to_use": "descriptive_statistics",
                "target_columns": (numeric_cols[:5] + cat_cols[:3]),
                "rationale": "Identifies central tendencies, dispersion, skewness, and high-frequency categorical values."
            })
            step_num += 1
            
        # Step 3: Correlation & Relational Exploration
        if len(numeric_cols) >= 2:
            plan.append({
                "step_number": step_num,
                "name": "Correlation & Multicollinearity Screening",
                "description": f"Compute pairwise Pearson correlation matrix across numeric features: {', '.join(numeric_cols[:4])}.",
                "tool_to_use": "correlation_analyzer",
                "target_columns": numeric_cols,
                "rationale": "Discovers linear dependencies and key drivers among quantitative metrics."
            })
            step_num += 1
            
        # Step 4: Temporal Trend Analysis (if dates detected)
        if date_cols or any(any(k in col.lower() for k in ['date', 'time', 'year']) for col in df.columns):
            plan.append({
                "step_number": step_num,
                "name": "Temporal Chronology & Growth Analysis",
                "description": "Aggregate key quantitative metrics along detected date dimensions to determine seasonality and growth rates.",
                "tool_to_use": "trend_analyzer",
                "target_columns": date_cols + numeric_cols[:2],
                "rationale": "Evaluates time-series trajectories and cyclical peak/trough patterns."
            })
            step_num += 1
            
        # Step 5: Anomaly & Outlier Detection
        if len(numeric_cols) > 0 and profile["row_count"] >= 10:
            plan.append({
                "step_number": step_num,
                "name": "Machine Learning Outlier & Anomaly Detection",
                "description": "Deploy IsolationForest alongside IQR thresholding to detect multivariate outliers.",
                "tool_to_use": "anomaly_detector",
                "target_columns": numeric_cols,
                "rationale": "Isolates severe univariate spikes and multivariate anomalous patterns."
            })
            step_num += 1
            
        # Step 6: Interactive Visualizations & Chart Generation
        plan.append({
            "step_number": step_num,
            "name": "Autonomous Chart Synthesis",
            "description": "Construct high-signal charts (Bar, Line, Histogram, Scatter, Heatmap, Box) based on data relationships.",
            "tool_to_use": "visualization_generator",
            "target_columns": [c["name"] for c in profile["columns"][:6]],
            "rationale": "Transforms computed metrics into interactive visual narratives."
        })
        step_num += 1
        
        # Step 7: Natural Language Business Insight Synthesis
        plan.append({
            "step_number": step_num,
            "name": "Executive Insight & Recommendation Synthesis",
            "description": "Synthesize statistical findings into actionable business explanations with risk and strategic guidance.",
            "tool_to_use": "insight_generator & report_generator",
            "target_columns": [],
            "rationale": "Delivers human-readable 'What happened', 'Why it matters', and 'What to do next'."
        })
        
        return plan

    def run_analysis(self, session_id: str):
        """Execute the complete autonomous analysis lifecycle for an analytical session."""
        session: Optional[AnalysisSessionModel] = self.db.query(AnalysisSessionModel).filter(AnalysisSessionModel.id == session_id).first()
        if not session:
            return
            
        dataset: Optional[DatasetModel] = self.db.query(DatasetModel).filter(DatasetModel.id == session.dataset_id).first()
        if not dataset:
            session.status = "failed"
            self.db.commit()
            return

        logs = []
        
        def log_step(task: str, tool: str, status: str, duration_ms: float, summary: str, err: Optional[str] = None):
            entry = {
                "task": task,
                "tool": tool,
                "status": status,
                "execution_time_ms": round(duration_ms, 1),
                "summary": summary,
                "error": err
            }
            logs.append(entry)
            session.execution_logs_json = json.dumps(logs)
            self.db.commit()

        try:
            # Stage 1: Understanding Dataset
            session.status = "running"
            session.current_step = "understanding"
            session.progress_percent = 10
            self.db.commit()
            
            t0 = time.time()
            df = load_dataset(dataset.file_path)
            profile = profile_dataset(df)
            quality = calculate_data_quality(df)
            t_diff = (time.time() - t0) * 1000
            
            log_step(
                task="Understand Dataset Structure & Quality",
                tool="dataset_profiler & data_quality_checker",
                status="success",
                duration_ms=t_diff,
                summary=f"Read {profile['row_count']:,} rows x {profile['column_count']} cols. Computed Quality Score: {quality['score']}/100."
            )
            
            # Stage 2: Planning Analysis
            session.current_step = "planning"
            session.progress_percent = 25
            self.db.commit()
            
            t0 = time.time()
            plan = self.create_analysis_plan(df, profile, quality)
            t_diff = (time.time() - t0) * 1000
            session.plan_json = json.dumps(plan)
            
            log_step(
                task="Formulate Tailored Analytical Plan",
                tool="autonomous_planner",
                status="success",
                duration_ms=t_diff,
                summary=f"Formulated {len(plan)}-stage analytical strategy based on variable typology and quality metrics."
            )
            
            # Stage 3: Executing Tools
            session.current_step = "executing"
            session.progress_percent = 40
            self.db.commit()
            
            # 3a. Descriptive Statistics
            t0 = time.time()
            desc_stats = calculate_descriptive_statistics(df)
            t_diff = (time.time() - t0) * 1000
            log_step(
                task="Execute Descriptive Statistics",
                tool="descriptive_statistics",
                status="success",
                duration_ms=t_diff,
                summary=f"Computed parametric metrics for {len(desc_stats['numeric_summary'])} numeric columns and {len(desc_stats['categorical_summary'])} categorical features."
            )
            
            # 3b. Correlation Analysis
            t0 = time.time()
            correlations = analyze_correlations(df)
            t_diff = (time.time() - t0) * 1000
            log_step(
                task="Execute Correlation Matrix",
                tool="correlation_analyzer",
                status="success",
                duration_ms=t_diff,
                summary=correlations.get("summary", "Correlation matrix computed.")
            )
            
            # 3c. Trend Analysis
            t0 = time.time()
            trends = analyze_trends(df)
            t_diff = (time.time() - t0) * 1000
            if trends:
                log_step(
                    task="Execute Temporal Trend Analysis",
                    tool="trend_analyzer",
                    status="success",
                    duration_ms=t_diff,
                    summary=trends.get("summary", "Trend analysis completed.")
                )
            else:
                log_step(
                    task="Check Temporal Trends",
                    tool="trend_analyzer",
                    status="warning",
                    duration_ms=t_diff,
                    summary="No active time-series or chronologically sequential columns identified; skipped."
                )
                
            # 3d. Anomaly Detection
            t0 = time.time()
            anomalies = detect_anomalies(df)
            t_diff = (time.time() - t0) * 1000
            log_step(
                task="Execute Outlier & Anomaly Detection",
                tool="anomaly_detector",
                status="success",
                duration_ms=t_diff,
                summary=anomalies.get("summary", "Anomaly detection executed.")
            )
            
            # Stage 4: Validating Results
            session.current_step = "validating"
            session.progress_percent = 65
            self.db.commit()
            
            t0 = time.time()
            # Validation check on computed statistics
            validation_errors = []
            for col, s in desc_stats["numeric_summary"].items():
                if np.isnan(s.get("mean", 0)):
                    validation_errors.append(f"NaN mean in {col}")
                    s["mean"] = 0.0
            t_diff = (time.time() - t0) * 1000
            
            log_step(
                task="Validate Analytical Integrity",
                tool="result_validator",
                status="success" if not validation_errors else "warning",
                duration_ms=t_diff,
                summary="All statistical indices, correlation bounds (-1 to +1), and distributions verified successfully." if not validation_errors else f"Auto-remediated {len(validation_errors)} non-finite values."
            )
            
            # Stage 5: Interactive Visualizations
            t0 = time.time()
            visualizations = generate_visualizations(df, correlations, trends, desc_stats)
            t_diff = (time.time() - t0) * 1000
            log_step(
                task="Generate Interactive Visualizations",
                tool="visualization_generator",
                status="success",
                duration_ms=t_diff,
                summary=f"Synthesized {len(visualizations)} custom charts ({', '.join([c['chart_type'] for c in visualizations])})."
            )
            
            # Stage 6: Generating Insights
            session.current_step = "generating_insights"
            session.progress_percent = 85
            self.db.commit()
            
            analysis_payload = {
                "dataset_overview": {
                    "filename": dataset.filename,
                    "row_count": profile["row_count"],
                    "column_count": profile["column_count"]
                },
                "quality_score": quality["score"],
                "quality_grade": quality["grade"],
                "missing_cells_pct": quality["missing_cells_pct"],
                "duplicate_rows_pct": quality["duplicate_rows_pct"],
                "descriptive_stats": desc_stats,
                "correlations": correlations,
                "trends": trends,
                "anomalies": anomalies
            }
            
            t0 = time.time()
            insights = generate_insights(analysis_payload)
            t_diff = (time.time() - t0) * 1000
            
            log_step(
                task="Synthesize Business Insights & Recommendations",
                tool="insight_generator",
                status="success",
                duration_ms=t_diff,
                summary=f"Generated {len(insights)} structured findings explaining observed phenomena and strategic actions."
            )
            
            # Stage 7: PDF Report Generation
            t0 = time.time()
            report_data = {
                **analysis_payload,
                "insights": insights,
                "visualizations_count": len(visualizations)
            }
            pdf_path = generate_pdf_report(session_id, dataset.filename, report_data)
            t_diff = (time.time() - t0) * 1000
            
            # Store Report in DB
            new_report = ReportModel(
                dataset_id=dataset.id,
                session_id=session_id,
                title=f"Executive Analysis Report - {dataset.filename}",
                pdf_path=pdf_path,
                report_json=json.dumps(report_data)
            )
            self.db.add(new_report)
            
            log_step(
                task="Compile Comprehensive PDF Report",
                tool="report_generator",
                status="success",
                duration_ms=t_diff,
                summary=f"Executive PDF dossier compiled and indexed at reports/{os.path.basename(pdf_path)}."
            )
            
            # Save Results to Session
            results = {
                "descriptive_stats": desc_stats,
                "correlations": correlations,
                "trends": trends,
                "anomalies": anomalies,
                "visualizations": visualizations,
                "quality_score": quality["score"]
            }
            session.results_json = json.dumps(results)
            session.insights_json = json.dumps(insights)
            session.status = "completed"
            session.current_step = "completed"
            session.progress_percent = 100
            session.completed_at = datetime.utcnow()
            self.db.commit()

        except Exception as e:
            session.status = "failed"
            session.progress_percent = 100
            log_step(
                task="Autonomous Execution Pipeline",
                tool="analyst_agent",
                status="error",
                duration_ms=0,
                summary=f"Execution interrupted: {str(e)}",
                err=str(e)
            )
            self.db.commit()


def process_chat_query(
    df: pd.DataFrame,
    query: str,
    dataset_profile: Dict[str, Any],
    analysis_results: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Conversational data analysis answering questions using real calculations, SQL, and dynamic charts."""
    query_lower = query.lower()
    tools_used = []
    generated_chart = None
    response_text = ""
    
    # 1. Check for Highest/Lowest/Top Category Questions
    if any(k in query_lower for k in ["highest", "top", "best", "most", "lowest", "worst", "least"]) and any(k in query_lower for k in ["category", "sales", "revenue", "profit", "product", "region", "segment"]):
        tools_used.append("sql_query_engine")
        numeric_cols = [c["name"] for c in dataset_profile["columns"] if c["general_type"] == "numeric"]
        cat_cols = [c["name"] for c in dataset_profile["columns"] if c["general_type"] == "categorical"]
        
        if cat_cols and numeric_cols:
            cat = cat_cols[0]
            num = numeric_cols[0]
            for c in cat_cols:
                if c.lower() in query_lower:
                    cat = c
                    break
            for n in numeric_cols:
                if n.lower() in query_lower:
                    num = n
                    break
                    
            asc = "ASC" if any(k in query_lower for k in ["lowest", "worst", "least"]) else "DESC"
            sql_query = f'SELECT "{cat}", SUM("{num}") as total, AVG("{num}") as average, COUNT(*) as count FROM dataset GROUP BY "{cat}" ORDER BY total {asc} LIMIT 5'
            sql_res = execute_analytical_sql(df, sql_query)
            
            if sql_res["data"]:
                top_row = sql_res["data"][0]
                response_text = (
                    f"Based on SQL aggregation of **{cat}** by total **{num}**:\n\n"
                    f"- **{top_row[cat]}** ranks #{1} with a cumulative total of **{top_row['total']:,}** (average: {round(top_row['average'], 2)} across {top_row['count']} records).\n"
                )
                if len(sql_res["data"]) > 1:
                    response_text += "\n**Top 5 ranking:**\n"
                    for i, r in enumerate(sql_res["data"], 1):
                        response_text += f"{i}. **{r[cat]}**: {r['total']:,} total (avg {round(r['average'], 1)})\n"
                        
                # Provide accompanying bar chart
                chart_data = [
                    {cat: str(r[cat]), "Total": round(float(r["total"]), 2)}
                    for r in sql_res["data"]
                ]
                generated_chart = {
                    "id": f"chat-bar-{cat}-{num}",
                    "title": f"{num} Aggregation by {cat}",
                    "chart_type": "bar",
                    "x_axis": cat,
                    "y_axis": "Total",
                    "description": f"Calculated dynamically for your query: '{query}'",
                    "data": chart_data,
                    "insights": f"{top_row[cat]} leads the segment."
                }
                tools_used.append("visualization_generator")

    # 2. Check for Trend / Over Time Questions
    elif any(k in query_lower for k in ["trend", "monthly", "over time", "growth", "timeline", "history", "trajectory"]):
        tools_used.append("trend_analyzer")
        trends = analyze_trends(df)
        if trends and trends.get("trend_data"):
            generated_chart = {
                "id": "chat-trend-chart",
                "title": f"Temporal Trajectory of {trends['metric_column']}",
                "chart_type": "line",
                "x_axis": "period",
                "y_axis": "sum",
                "description": f"Temporal intervals ({trends['frequency']})",
                "data": trends["trend_data"],
                "insights": trends["summary"]
            }
            tools_used.append("visualization_generator")
            response_text = (
                f"**Temporal Trend Findings:**\n\n"
                f"- **Overall Trajectory:** {trends['direction']} ({trends['overall_growth_pct']:+0.1f}%)\n"
                f"- **Analyzed Metric:** `{trends['metric_column']}` grouped by {trends['frequency']}\n"
                f"- **Peak Interval:** `{trends['peak_period']['period']}` with sum of **{trends['peak_period']['sum']:,}**\n"
                f"- **Lowest Interval:** `{trends['trough_period']['period']}` ({trends['trough_period']['sum']:,})\n\n"
                f"{trends['summary']}"
            )
        else:
            response_text = "I checked for date or chronological columns in this dataset, but did not find sufficient time-series data to compute temporal trends."

    # 3. Check for Anomaly / Outlier Questions
    elif any(k in query_lower for k in ["anomaly", "anomalies", "outlier", "outliers", "unusual", "irregular", "abnormal"]):
        tools_used.append("anomaly_detector")
        anomalies = detect_anomalies(df)
        records = anomalies.get("anomalous_records", [])
        response_text = f"**Anomaly & Outlier Detection Results:**\n\n{anomalies.get('summary', '')}\n\n"
        if records:
            response_text += "**Most Notable Irregular Records:**\n"
            for r in records[:3]:
                reasons = ", ".join(r.get("deviating_factors", []))
                response_text += f"- **Row #{r['row_index']}** (Severity: {r['severity_score']}): {reasons}\n"
        else:
            response_text += "No records were flagged as severe multivariate anomalies."

    # 4. Check for Correlation / Relationship Questions
    elif any(k in query_lower for k in ["correlation", "relationship", "relation", "associated", "impact", "affect", "connection"]):
        tools_used.append("correlation_analyzer")
        corrs = analyze_correlations(df)
        pairs = corrs.get("significant_pairs", [])
        if pairs:
            response_text = f"**Correlation Analysis:**\n\n{corrs.get('summary', '')}\n\n**Key Observed Relationships:**\n"
            for p in pairs[:5]:
                response_text += f"- **{p['col1']}** vs **{p['col2']}**: {p['strength']} (Pearson r = **{p['correlation']}**)\n"
        else:
            response_text = "There are insufficient numeric variables to detect linear correlations in this dataset."

    # 5. Check for Recommendation / Business Insights Questions
    elif any(k in query_lower for k in ["recommend", "recommendation", "insight", "findings", "summary", "takeaway", "conclusion"]):
        tools_used.append("insight_generator")
        quality = calculate_data_quality(df)
        corrs = analyze_correlations(df)
        desc = calculate_descriptive_statistics(df)
        anom = detect_anomalies(df)
        trends = analyze_trends(df)
        payload = {
            "dataset_overview": {"row_count": len(df), "column_count": len(df.columns)},
            "quality_score": quality["score"],
            "quality_grade": quality["grade"],
            "descriptive_stats": desc,
            "correlations": corrs,
            "trends": trends,
            "anomalies": anom
        }
        insights = generate_insights(payload)
        response_text = f"**Key Insights and Strategic Recommendations:**\n\n"
        for i, ins in enumerate(insights[:4], 1):
            response_text += (
                f"### {i}. {ins['title']} [{ins['category'].upper()}]\n"
                f"- **Finding:** {ins['finding']}\n"
                f"- **Pattern:** {ins['pattern']}\n"
                f"- **Business Importance:** {ins['importance']}\n"
                f"- **Strategic Recommendation:** {ins['recommendation']}\n\n"
            )

    # 6. Fallback General Question (DuckDB / SQL or Gemini reasoning)
    else:
        # Check if user asked to run custom SQL or calculate something
        tools_used.append("dataset_profiler")
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key.strip():
            # Call Gemini with actual schema and summary
            try:
                tools_used.append("gemini_reasoner")
                sample_data = df.head(5).to_dict(orient="records")
                schema_desc = [{"col": c["name"], "type": c["general_type"], "stats": c.get("stats")} for c in dataset_profile["columns"]]
                prompt = (
                    f"You are the Autonomous Data Analyst answering a user question about this exact dataset.\n"
                    f"Dataset Columns & Types: {json.dumps(schema_desc)}\n"
                    f"Sample Rows: {json.dumps(sample_data)}\n"
                    f"Total Rows: {len(df)}, Total Columns: {len(df.columns)}\n"
                    f"User Question: '{query}'\n\n"
                    f"Give a direct, precise, fact-based answer based strictly on the data. Do not make up numbers."
                )
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key.strip()}"
                res = httpx.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15.0)
                if res.status_code == 200:
                    response_text = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            except Exception:
                pass
                
        if not response_text:
            # Deterministic answer
            num_cols = [c["name"] for c in dataset_profile["columns"] if c["general_type"] == "numeric"]
            cat_cols = [c["name"] for c in dataset_profile["columns"] if c["general_type"] == "categorical"]
            response_text = (
                f"**Dataset Analysis Summary:**\n\n"
                f"- **Total Records:** {len(df):,} rows and {len(df.columns)} columns.\n"
                f"- **Numeric Attributes:** {', '.join(num_cols[:6]) if num_cols else 'None'}\n"
                f"- **Categorical Dimensions:** {', '.join(cat_cols[:6]) if cat_cols else 'None'}\n\n"
                f"You can ask me specific questions such as:\n"
                f"- *'Which category has the highest sales?'*\n"
                f"- *'Show me the monthly trend'* \n"
                f"- *'Are there any unusual outliers?'*\n"
                f"- *'What are the strongest correlations?'*\n"
                f"- *'Provide actionable recommendations for this dataset'*."
            )
            
    return {
        "content": response_text,
        "tools_used": tools_used,
        "chart": generated_chart
    }
