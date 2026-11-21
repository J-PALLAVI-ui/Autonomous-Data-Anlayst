import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect statistical and multivariate anomalies using IQR and Scikit-Learn IsolationForest."""
    numeric_df = df.select_dtypes(include=[np.number])
    valid_cols = [c for c in numeric_df.columns if numeric_df[c].nunique() > 2 and not ('id' in c.lower() or 'key' in c.lower())]
    
    total_rows = len(df)
    if total_rows < 10 or not valid_cols:
        return {
            "total_anomalies": 0,
            "anomaly_rate_pct": 0.0,
            "method": "insufficient_data",
            "anomalous_records": [],
            "column_outliers": {},
            "summary": "Dataset has too few records or numeric features to perform anomaly detection."
        }
        
    # 1. Statistical Outliers per column via IQR
    column_outliers = {}
    for col in valid_cols:
        series = df[col].dropna()
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        iqr = q75 - q25
        if iqr > 0:
            lb = q25 - 1.5 * iqr
            ub = q75 + 1.5 * iqr
            outlier_rows = df[(df[col] < lb) | (df[col] > ub)]
            if len(outlier_rows) > 0:
                column_outliers[col] = {
                    "count": len(outlier_rows),
                    "lower_bound": round(float(lb), 2),
                    "upper_bound": round(float(ub), 2),
                    "extremes": [round(float(x), 2) for x in pd.concat([outlier_rows[col].head(3), outlier_rows[col].tail(3)]).unique()]
                }
                
    # 2. Multivariate Isolation Forest
    clean_numeric = numeric_df[valid_cols].copy()
    for col in valid_cols:
        clean_numeric[col] = clean_numeric[col].fillna(clean_numeric[col].median())
        
    contamination = min(0.05, max(0.01, 5.0 / total_rows))
    iso = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
    preds = iso.fit_predict(clean_numeric)
    scores = iso.decision_function(clean_numeric)
    
    anomaly_indices = np.where(preds == -1)[0]
    total_anomalies = len(anomaly_indices)
    anomaly_rate = round((total_anomalies / total_rows) * 100, 2)
    
    # Extract top anomalous records
    anomalous_records = []
    if total_anomalies > 0:
        # Sort by anomaly severity (lowest decision function score)
        sorted_anomaly_idx = sorted(anomaly_indices, key=lambda idx: scores[idx])
        for idx in sorted_anomaly_idx[:8]:
            row_dict = df.iloc[idx].to_dict()
            # Clean values for JSON
            cleaned_row = {}
            reasons = []
            for k, v in row_dict.items():
                if isinstance(v, (np.floating, float)):
                    cleaned_row[k] = None if (np.isnan(v) or np.isinf(v)) else round(float(v), 2)
                elif isinstance(v, (np.integer, int)):
                    cleaned_row[k] = int(v)
                else:
                    cleaned_row[k] = str(v)
                    
                # Reason check
                if k in column_outliers:
                    co = column_outliers[k]
                    val = row_dict[k]
                    if pd.notna(val) and (val < co["lower_bound"] or val > co["upper_bound"]):
                        reasons.append(f"{k}={cleaned_row[k]} (beyond normal range [{co['lower_bound']}, {co['upper_bound']}])")
                        
            anomalous_records.append({
                "row_index": int(idx),
                "severity_score": round(float(-scores[idx]), 3),
                "deviating_factors": reasons if reasons else ["Multivariate deviation across combined features"],
                "record": cleaned_row
            })
            
    summary_text = (
        f"Detected {total_anomalies} anomalous records ({anomaly_rate}% of dataset) using Scikit-Learn IsolationForest. "
        f"{len(column_outliers)} numeric features contain severe univariate outliers outside 1.5x IQR."
        if total_anomalies > 0 else "No significant statistical or multivariate anomalies detected."
    )
    
    return {
        "total_anomalies": total_anomalies,
        "anomaly_rate_pct": anomaly_rate,
        "method": "IsolationForest & IQR",
        "anomalous_records": anomalous_records,
        "column_outliers": column_outliers,
        "summary": summary_text
    }
