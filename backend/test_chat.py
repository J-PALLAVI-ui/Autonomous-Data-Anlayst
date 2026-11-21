import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database.connection import SessionLocal
from models.models import DatasetModel, AnalysisSessionModel
from agents.autonomous_analyst import process_chat_query
from tools.dataset_profiler import load_dataset, profile_dataset

db = SessionLocal()
ds = db.query(DatasetModel).first()
df = load_dataset(ds.file_path)
profile = profile_dataset(df)

questions = [
    "Which category has the highest sales?",
    "Show me the monthly trend.",
    "Are there any unusual outliers in this data?",
    "What are the strongest correlations?",
    "What recommendations do you have?"
]

print("=== TESTING CONVERSATIONAL AI ANALYST ===")
for q in questions:
    res = process_chat_query(df, q, profile)
    print(f"\nUser: {q}")
    print(f"Tools Used: {res['tools_used']}")
    print(f"Agent Response:\n{res['content']}")
    if res.get('chart'):
        print(f"Generated Chart: {res['chart']['title']} ({res['chart']['chart_type']}) with {len(res['chart']['data'])} data points")
