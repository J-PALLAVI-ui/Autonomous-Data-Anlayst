import sys
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database.connection import SessionLocal
from models.models import AnalysisSessionModel, ReportModel

db = SessionLocal()
session = db.query(AnalysisSessionModel).filter(AnalysisSessionModel.status == 'completed').first()
if not session:
    print("No completed session found.")
    sys.exit(0)

results = json.loads(session.results_json)
insights = json.loads(session.insights_json)
logs = json.loads(session.execution_logs_json)
report = db.query(ReportModel).filter(ReportModel.session_id == session.id).first()

print(f"Execution logs ({len(logs)} steps):")
for l in logs:
    print(f" - [{l.get('status')}] {l.get('tool')}: {l.get('summary')}")

print(f"\nVisualizations ({len(results.get('visualizations', []))}):")
for v in results.get('visualizations', []):
    print(f" - Chart: {v.get('title')} ({v.get('chart_type')})")

print(f"\nBusiness Insights ({len(insights)}):")
for ins in insights:
    print(f" - [{ins.get('category')}] {ins.get('title')}")

if report:
    print(f"\nReport PDF path: {report.pdf_path}")
    print(f"PDF exists: {os.path.exists(report.pdf_path)} ({os.path.getsize(report.pdf_path)} bytes)")
else:
    print("\nNo report model found.")
