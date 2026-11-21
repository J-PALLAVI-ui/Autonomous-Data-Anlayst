import os
import json
import httpx
from typing import Dict, Any, List

def generate_insights_with_gemini(analysis_payload: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
    """Use Gemini 2.0 / 1.5 Flash to synthesize business insights from verified statistical results."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    prompt = f"""
You are a Principal Data Analyst and Business Strategist.
Analyze the following statistical analysis results computed directly on an uploaded dataset.

ANALYSIS DATA:
- Dataset Overview: {json.dumps(analysis_payload.get('dataset_overview', {}), indent=2)}
- Data Quality Score: {analysis_payload.get('quality_score')} ({analysis_payload.get('quality_grade')})
- Top Correlations: {json.dumps(analysis_payload.get('correlations', {}).get('significant_pairs', []), indent=2)}
- Temporal Trends: {json.dumps(analysis_payload.get('trends'), indent=2)}
- Detected Anomalies: {json.dumps(analysis_payload.get('anomalies', {}).get('summary'), indent=2)}
- Grouped Breakdown: {json.dumps(analysis_payload.get('descriptive_stats', {}).get('grouped_breakdown', []), indent=2)}

INSTRUCTIONS:
Generate 4 to 6 deeply meaningful, actionable business insights.
DO NOT fabricate numbers. Use only the actual computed statistics provided above.
Return a STRICT JSON list of objects, each adhering exactly to this schema:
[
  {{
    "category": "executive_summary" | "key_driver" | "anomaly" | "trend" | "recommendation" | "risk",
    "title": "Clear headline",
    "finding": "What happened? (Specific, concise description of the observed data)",
    "pattern": "What patterns were identified? (The underlying statistical or structural pattern)",
    "importance": "Why is the finding important? (Business impact or operational implication)",
    "recommendation": "What action or recommendation can be considered? (Actionable step)",
    "confidence": 0.95,
    "impact_level": "high" | "medium" | "low",
    "supporting_columns": ["col1", "col2"]
  }}
]
Respond ONLY with the JSON array. Do not add markdown backticks or commentary.
"""
    try:
        response = httpx.post(
            url,
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2, "response_mime_type": "application/json"}
            },
            timeout=25.0
        )
        if response.status_code == 200:
            result_json = response.json()
            text = result_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Clean possible markdown wrap
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            parsed = json.loads(text.strip())
            if isinstance(parsed, list) and len(parsed) > 0:
                return parsed
    except Exception as e:
        print(f"Gemini API generation error: {e}")
        
    return []

def generate_insights_deterministic(analysis_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Deterministic, high-fidelity business insight engine based strictly on computed results."""
    insights = []
    
    overview = analysis_payload.get("dataset_overview", {})
    quality_score = analysis_payload.get("quality_score", 100.0)
    quality_grade = analysis_payload.get("quality_grade", "A")
    descriptive = analysis_payload.get("descriptive_stats", {})
    correlations = analysis_payload.get("correlations", {})
    trends = analysis_payload.get("trends")
    anomalies = analysis_payload.get("anomalies", {})
    
    row_cnt = overview.get("row_count", 0)
    col_cnt = overview.get("column_count", 0)
    
    # 1. Executive Summary Insight
    insights.append({
        "category": "executive_summary",
        "title": "Dataset Dimensionality and Health Scorecard",
        "finding": f"Analyzed structured dataset containing {row_cnt:,} records across {col_cnt} columns.",
        "pattern": f"Overall data health achieved a Quality Score of {quality_score}/100 (Grade {quality_grade}).",
        "importance": "High data integrity ensures statistical tests and downstream predictive modeling remain robust.",
        "recommendation": "Review identified data quality items before deploying automated pipeline models.",
        "confidence": 0.98,
        "impact_level": "high",
        "supporting_columns": []
    })
    
    # 2. Key Driver / Grouped Insight
    grouped = descriptive.get("grouped_breakdown", [])
    if grouped:
        top_group = grouped[0]
        cat_col = top_group.get("category_column", "Category")
        num_col = top_group.get("numeric_column", "Metric")
        insights.append({
            "category": "key_driver",
            "title": f"Primary Performance Driver: {top_group.get('category')} leads {num_col}",
            "finding": f"The '{top_group.get('category')}' segment in '{cat_col}' generated {top_group.get('sum'):,} total {num_col} (average {top_group.get('mean')} per entry).",
            "pattern": f"Significant concentration of {num_col} concentrated within top tier categorical groups.",
            "importance": f"Resource allocation and optimization should capitalize on the top-performing {cat_col} segment.",
            "recommendation": f"Expand capacity in '{top_group.get('category')}' while investigating factors underperforming in secondary segments.",
            "confidence": 0.92,
            "impact_level": "high",
            "supporting_columns": [cat_col, num_col]
        })
        
    # 3. Correlation Insight
    pairs = correlations.get("significant_pairs", [])
    if pairs:
        top_pair = pairs[0]
        c1, c2 = top_pair["col1"], top_pair["col2"]
        r_val = top_pair["correlation"]
        insights.append({
            "category": "key_driver",
            "title": f"Bivariate Association: {c1} & {c2}",
            "finding": f"Detected a {top_pair['strength']} linear relationship between '{c1}' and '{c2}' with Pearson r = {r_val}.",
            "pattern": f"Changes in '{c1}' are strongly linked with proportional changes in '{c2}'.",
            "importance": f"Indicates that '{c1}' is a critical leading or co-dependent indicator for '{c2}'.",
            "recommendation": f"Incorporate '{c1}' into forecast models and monitoring alerts for '{c2}'.",
            "confidence": 0.90,
            "impact_level": "high" if abs(r_val) >= 0.7 else "medium",
            "supporting_columns": [c1, c2]
        })
        
    # 4. Temporal Trend Insight
    if trends and trends.get("direction"):
        direction = trends.get("direction")
        growth_pct = trends.get("overall_growth_pct", 0)
        metric = trends.get("metric_column", "Metric")
        peak = trends.get("peak_period", {})
        insights.append({
            "category": "trend",
            "title": f"Chronological Trajectory: {direction} ({growth_pct:+0.1f}%)",
            "finding": f"Over the analyzed timeframe, '{metric}' demonstrated a {direction} with an overall change of {growth_pct:+0.1f}%.",
            "pattern": f"Peak activity occurred during period '{peak.get('period', 'N/A')}' reaching {peak.get('sum', 0):,}.",
            "importance": "Helps distinguish seasonal cyclicality from structural secular growth.",
            "recommendation": "Align operational planning and inventory buffers with seasonal peak periods.",
            "confidence": 0.88,
            "impact_level": "high",
            "supporting_columns": [trends.get("date_column", "Date"), metric]
        })
        
    # 5. Anomaly Insight
    total_anomalies = anomalies.get("total_anomalies", 0)
    if total_anomalies > 0:
        rate = anomalies.get("anomaly_rate_pct", 0)
        outliers_cols = list(anomalies.get("column_outliers", {}).keys())
        insights.append({
            "category": "anomaly",
            "title": f"Anomaly Detection: {total_anomalies} Irregular Records ({rate}%)",
            "finding": f"IsolationForest algorithm isolated {total_anomalies} records showing abnormal multivariate distribution.",
            "pattern": f"Outliers predominantly deviate along: {', '.join(outliers_cols[:3]) if outliers_cols else 'numeric dimensions'}.",
            "importance": "Unchecked outliers can bias statistical estimators, averages, and predictive regressions.",
            "recommendation": "Review anomalous records individually; filter data entry glitches from genuine high-value events.",
            "confidence": 0.85,
            "impact_level": "medium",
            "supporting_columns": outliers_cols[:3]
        })
        
    # 6. Strategic Recommendation
    insights.append({
        "category": "recommendation",
        "title": "Data Governance and Continuous Monitoring",
        "finding": f"Current analysis identified key performance levers and distribution characteristics.",
        "pattern": "Systematic evaluation allows proactive business decision-making rather than reactive retrospectives.",
        "importance": "Actionable analytics improves operational responsiveness and profitability.",
        "recommendation": "Establish periodic automated runs with this autonomous analyst pipeline to track changes over time.",
        "confidence": 0.95,
        "impact_level": "high",
        "supporting_columns": []
    })
    
    return insights

def generate_insights(analysis_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Synthesize insights using Gemini API if key is available, falling back to deterministic engine."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key.strip():
        gemini_insights = generate_insights_with_gemini(analysis_payload, api_key.strip())
        if gemini_insights:
            return gemini_insights
            
    return generate_insights_deterministic(analysis_payload)
