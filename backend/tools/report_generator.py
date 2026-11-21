import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf_report(
    session_id: str,
    dataset_name: str,
    analysis_data: Dict[str, Any]
) -> str:
    """Generate a comprehensive, publication-quality executive PDF analysis report using ReportLab."""
    pdf_filename = f"report_{session_id}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette & Styles
    navy = colors.HexColor("#0f172a")
    blue = colors.HexColor("#2563eb")
    slate = colors.HexColor("#475569")
    light_bg = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#e2e8f0")
    
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=navy,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=slate,
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=navy,
        spaceBefore=14,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )
    
    bold_body = ParagraphStyle(
        "ReportBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    
    story = []
    
    # Document Header
    story.append(Paragraph("Autonomous Data Analyst Report", title_style))
    story.append(Paragraph(f"Dataset: <b>{dataset_name}</b> | Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=blue, spaceBefore=0, spaceAfter=15))
    
    # Section 1: Executive Overview & Data Quality Scorecard
    story.append(Paragraph("1. Executive Overview & Data Quality Scorecard", h2_style))
    
    overview = analysis_data.get("dataset_overview", {})
    quality_score = analysis_data.get("quality_score", 100.0)
    quality_grade = analysis_data.get("quality_grade", "A")
    
    overview_table_data = [
        [Paragraph("Metric", bold_body), Paragraph("Value", bold_body), Paragraph("Quality Parameter", bold_body), Paragraph("Status", bold_body)],
        [Paragraph("Total Rows", body_style), Paragraph(f"{overview.get('row_count', 0):,}", body_style), Paragraph("Quality Score", body_style), Paragraph(f"{quality_score} / 100", bold_body)],
        [Paragraph("Total Columns", body_style), Paragraph(f"{overview.get('column_count', 0)}", body_style), Paragraph("Quality Grade", body_style), Paragraph(f"Grade {quality_grade}", bold_body)],
        [Paragraph("Missing Rate", body_style), Paragraph(f"{analysis_data.get('missing_cells_pct', 0)}%", body_style), Paragraph("Duplicates Rate", body_style), Paragraph(f"{analysis_data.get('duplicate_rows_pct', 0)}%", body_style)]
    ]
    
    t_overview = Table(overview_table_data, colWidths=[120, 130, 140, 140])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), light_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), navy),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 10))
    
    # Section 2: Important Analytical Findings & Insights
    story.append(Paragraph("2. Autonomous AI Insights & Strategic Findings", h2_style))
    insights = analysis_data.get("insights", [])
    
    for idx, ins in enumerate(insights[:5], 1):
        ins_box = [
            [Paragraph(f"<b>Finding {idx}: {ins.get('title')}</b> [{ins.get('category', '').upper()}]", bold_body)],
            [Paragraph(f"<b>Observed:</b> {ins.get('finding')}", body_style)],
            [Paragraph(f"<b>Pattern & Importance:</b> {ins.get('pattern')} {ins.get('importance')}", body_style)],
            [Paragraph(f"<b>Recommendation:</b> {ins.get('recommendation')}", ParagraphStyle('Rec', parent=body_style, textColor=colors.HexColor('#047857')))]
        ]
        t_ins = Table(ins_box, colWidths=[530])
        t_ins.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), light_bg),
            ('BOX', (0, 0), (-1, -1), 1, border_color),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_ins)
        story.append(Spacer(1, 6))
        
    # Section 3: Statistical Summary Table
    story.append(Paragraph("3. Statistical Summary of Key Numeric Features", h2_style))
    stats_data = analysis_data.get("descriptive_stats", {}).get("numeric_summary", {})
    
    stats_table = [
        [
            Paragraph("Variable", bold_body),
            Paragraph("Mean", bold_body),
            Paragraph("Std Dev", bold_body),
            Paragraph("Min", bold_body),
            Paragraph("Median", bold_body),
            Paragraph("Max", bold_body)
        ]
    ]
    
    for col, s in list(stats_data.items())[:6]:
        stats_table.append([
            Paragraph(col, body_style),
            Paragraph(str(s.get("mean", 0)), body_style),
            Paragraph(str(s.get("std", 0)), body_style),
            Paragraph(str(s.get("min", 0)), body_style),
            Paragraph(str(s.get("median", 0)), body_style),
            Paragraph(str(s.get("max", 0)), body_style),
        ])
        
    if len(stats_table) > 1:
        t_stats = Table(stats_table, colWidths=[130, 80, 80, 80, 80, 80])
        t_stats.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t_stats)
    else:
        story.append(Paragraph("No numeric variables available for descriptive summary.", body_style))
        
    story.append(Spacer(1, 10))
    
    # Section 4: Key Correlations & Trend Trajectory
    story.append(Paragraph("4. Correlations & Trend Trajectory", h2_style))
    corr_summary = analysis_data.get("correlations", {}).get("summary", "No strong correlations observed.")
    story.append(Paragraph(f"<b>Correlation Summary:</b> {corr_summary}", body_style))
    story.append(Spacer(1, 4))
    
    trends = analysis_data.get("trends")
    if trends:
        story.append(Paragraph(f"<b>Temporal Dynamics:</b> {trends.get('summary', 'Trend detected.')}", body_style))
    else:
        story.append(Paragraph("<b>Temporal Dynamics:</b> No explicit date/time series detected in the dataset.", body_style))
        
    story.append(Spacer(1, 10))
    
    # Section 5: Detected Anomalies
    story.append(Paragraph("5. Anomaly & Outlier Detection Assessment", h2_style))
    anomaly_summary = analysis_data.get("anomalies", {}).get("summary", "No significant anomalies flagged.")
    story.append(Paragraph(anomaly_summary, body_style))
    story.append(Spacer(1, 10))
    
    # Section 6: Strategic Recommendations & Conclusion
    story.append(Paragraph("6. Recommendations & Final Conclusion", h2_style))
    conclusion_text = (
        "Based on autonomous multi-dimensional profiling, the dataset displays consistent structure. "
        "Business leaders and data teams should prioritize the identified high-impact drivers and resolve data quality "
        "concerns prior to operational deployment. Ongoing monitoring via the Autonomous Data Analyst pipeline is recommended."
    )
    story.append(Paragraph(conclusion_text, body_style))
    
    # Build Document
    doc.build(story)
    return pdf_path

def export_analysis_csv(df: pd.DataFrame, session_id: str) -> str:
    """Export dataset to a CSV file for download."""
    csv_filename = f"export_{session_id}.csv"
    csv_path = os.path.join(REPORTS_DIR, csv_filename)
    df.to_csv(csv_path, index=False)
    return csv_path
