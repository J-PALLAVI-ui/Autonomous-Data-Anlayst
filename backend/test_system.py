import os
import sys
import time

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_full_pipeline():
    print("=== STARTING FULL PIPELINE TEST ===")
    
    # 1. Test datasets listing
    res = client.get("/api/datasets")
    assert res.status_code == 200, f"Datasets list failed: {res.text}"
    datasets = res.json()
    print(f"1. Datasets retrieved: {len(datasets)} found.")
    assert len(datasets) > 0, "No datasets found!"
    
    dataset_id = datasets[0]["id"]
    print(f"   Selected dataset: '{datasets[0]['filename']}' (ID: {dataset_id})")
    
    # 2. Test dataset detail
    res = client.get(f"/api/datasets/{dataset_id}")
    assert res.status_code == 200, f"Dataset detail failed: {res.text}"
    detail = res.json()
    print(f"2. Dataset profile verified: {detail['row_count']} rows, {detail['column_count']} cols, Quality: {detail['quality_score']}/100")
    
    # 3. Test start autonomous analysis
    res = client.post("/api/analysis/start", json={"dataset_id": dataset_id})
    assert res.status_code == 200, f"Start analysis failed: {res.text}"
    session_id = res.json()["session_id"]
    print(f"3. Autonomous analysis session initialized: {session_id}")
    
    # 4. Wait for analysis to complete (or run directly)
    print("4. Monitoring autonomous agent workflow execution...")
    max_wait = 30
    start_time = time.time()
    completed = False
    
    while time.time() - start_time < max_wait:
        res = client.get(f"/api/analysis/{session_id}/status")
        assert res.status_code == 200
        st = res.json()
        print(f"   Agent step: [{st['current_step']}] - {st['progress_percent']}%")
        if st["status"] == "completed":
            completed = True
            break
        elif st["status"] == "failed":
            raise RuntimeError("Analysis session failed!")
        time.sleep(1)
        
    assert completed, "Analysis did not complete within timeout!"
    print("   Analysis completed successfully!")
    
    # 5. Test results endpoint
    res = client.get(f"/api/analysis/{session_id}/results")
    assert res.status_code == 200
    results = res.json()
    print(f"5. Analysis results validated:")
    print(f"   - Plan items: {len(results['plan'])}")
    print(f"   - Tool execution logs: {len(results['execution_logs'])}")
    print(f"   - Numeric summaries: {len(results['descriptive_stats']['numeric_summary'])}")
    print(f"   - Correlated pairs: {len(results['correlations']['significant_pairs'])}")
    print(f"   - Synthesized visualizations: {len(results['visualizations'])}")
    print(f"   - Business insights: {len(results['insights'])}")
    
    assert len(results["visualizations"]) >= 3, "Expected at least 3 visualizations"
    assert len(results["insights"]) >= 3, "Expected at least 3 insights"
    
    # 6. Test AI Chat
    print("6. Testing AI Chat with dynamic SQL and tool execution...")
    chat_queries = [
        "Which category has the highest sales?",
        "Show me the monthly trend.",
        "Are there any unusual outliers?"
    ]
    for q in chat_queries:
        res = client.post("/api/chat", json={
            "dataset_id": dataset_id,
            "session_id": session_id,
            "message": q
        })
        assert res.status_code == 200
        chat_res = res.json()
        print(f"   User: '{q}'")
        print(f"   Agent (Tools: {chat_res['tools_used']}): {chat_res['content'][:90]}...")
        if chat_res.get("chart"):
            print(f"   -> Accompanying Chart: {chat_res['chart']['title']} ({chat_res['chart']['chart_type']})")
            
    # 7. Test Report generation and PDF download
    print("7. Testing Executive PDF Report...")
    res = client.get(f"/api/reports/{session_id}")
    assert res.status_code == 200
    report_meta = res.json()
    print(f"   Report metadata verified: '{report_meta['title']}' (PDF available: {report_meta['pdf_available']})")
    
    res_pdf = client.get(f"/api/reports/{session_id}/pdf")
    assert res_pdf.status_code == 200
    assert len(res_pdf.content) > 1000, "PDF content seems empty!"
    print(f"   PDF file downloaded successfully ({len(res_pdf.content):,} bytes).")
    
    # 8. Test Data Quality Cleaning Preview
    print("8. Testing Data Quality Cleaning Preview...")
    res_clean = client.post("/api/quality/preview-cleaning", json={
        "dataset_id": dataset_id,
        "operation": "drop_duplicates",
        "params": {}
    })
    assert res_clean.status_code == 200
    clean_info = res_clean.json()
    print(f"   Preview drop_duplicates: rows {clean_info['rows_before']} -> {clean_info['rows_after']}")
    
    print("\n=== ALL SYSTEM TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    test_full_pipeline()
