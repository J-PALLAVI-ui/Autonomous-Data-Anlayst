import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

def calculate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """Perform comprehensive data quality analysis on dataframe."""
    total_rows = len(df)
    total_cols = len(df.columns)
    total_cells = total_rows * total_cols
    
    if total_cells == 0:
        return {
            "missing_cells": 0,
            "missing_cells_pct": 0.0,
            "duplicate_rows": 0,
            "duplicate_rows_pct": 0.0,
            "outlier_count": 0,
            "total_cells": 0,
            "score": 100.0,
            "grade": "A",
            "issues": [],
            "recommendations": []
        }
        
    # 1. Missing values
    missing_cells = int(df.isna().sum().sum())
    missing_pct = round((missing_cells / total_cells) * 100, 2)
    
    # Missing per column
    missing_by_col = {}
    for col in df.columns:
        cnt = int(df[col].isna().sum())
        if cnt > 0:
            missing_by_col[col] = {
                "count": cnt,
                "percentage": round((cnt / total_rows) * 100, 2)
            }
            
    # 2. Duplicate rows
    duplicate_rows = int(df.duplicated().sum())
    duplicate_pct = round((duplicate_rows / total_rows) * 100, 2) if total_rows > 0 else 0.0
    
    # 3. Outliers in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers_by_col = {}
    total_outliers = 0
    
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) >= 10:
            q25 = series.quantile(0.25)
            q75 = series.quantile(0.75)
            iqr = q75 - q25
            if iqr > 0:
                lower_bound = q25 - 1.5 * iqr
                upper_bound = q75 + 1.5 * iqr
                outlier_mask = (series < lower_bound) | (series > upper_bound)
                outlier_cnt = int(outlier_mask.sum())
                if outlier_cnt > 0:
                    total_outliers += outlier_cnt
                    outliers_by_col[col] = {
                        "count": outlier_cnt,
                        "percentage": round((outlier_cnt / len(series)) * 100, 2),
                        "lower_bound": round(float(lower_bound), 2),
                        "upper_bound": round(float(upper_bound), 2)
                    }
                    
    # 4. Column completeness
    completeness_by_col = {}
    empty_cols = []
    for col in df.columns:
        valid_cnt = int(df[col].notna().sum())
        comp_pct = round((valid_cnt / total_rows) * 100, 2) if total_rows > 0 else 0.0
        completeness_by_col[col] = comp_pct
        if valid_cnt == 0:
            empty_cols.append(col)
            
    # 5. Quality Score Calculation
    # Penalties
    missing_penalty = min(missing_pct * 0.8, 35.0)
    duplicate_penalty = min(duplicate_pct * 1.2, 25.0)
    outlier_pct = (total_outliers / total_cells) * 100 if total_cells > 0 else 0
    outlier_penalty = min(outlier_pct * 1.5, 15.0)
    empty_col_penalty = min(len(empty_cols) * 10.0, 25.0)
    
    total_penalty = missing_penalty + duplicate_penalty + outlier_penalty + empty_col_penalty
    score = max(0.0, min(100.0, round(100.0 - total_penalty, 1)))
    
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
        
    # 6. Structured Issues List
    issues = []
    recommendations = []
    
    if duplicate_rows > 0:
        issues.append({
            "type": "duplicates",
            "severity": "high" if duplicate_pct > 5 else "medium",
            "message": f"Found {duplicate_rows} duplicate rows ({duplicate_pct}% of total records)."
        })
        recommendations.append({
            "action": "drop_duplicates",
            "title": "Remove Duplicate Rows",
            "description": f"Deduplicate dataset to eliminate {duplicate_rows} redundant entries.",
            "impact": f"+{round(duplicate_penalty, 1)} pts quality score"
        })
        
    if missing_cells > 0:
        high_missing_cols = [c for c, v in missing_by_col.items() if v["percentage"] > 20]
        issues.append({
            "type": "missing_values",
            "severity": "high" if missing_pct > 10 else "medium",
            "message": f"Dataset contains {missing_cells} missing values ({missing_pct}% total missingness)."
        })
        if high_missing_cols:
            recommendations.append({
                "action": "drop_columns",
                "target": high_missing_cols,
                "title": f"Drop sparse columns ({', '.join(high_missing_cols[:3])})",
                "description": f"Columns with >20% missing values degrade analytical accuracy.",
                "impact": "Improves data density"
            })
        recommendations.append({
            "action": "fill_missing",
            "title": "Impute Missing Values",
            "description": "Fill missing numerical values with median and categoricals with mode.",
            "impact": f"+{round(missing_penalty, 1)} pts quality score"
        })
        
    if empty_cols:
        issues.append({
            "type": "empty_columns",
            "severity": "high",
            "message": f"{len(empty_cols)} completely empty columns detected: {', '.join(empty_cols)}."
        })
        
    if total_outliers > 0:
        issues.append({
            "type": "outliers",
            "severity": "medium",
            "message": f"Detected {total_outliers} statistical outliers across {len(outliers_by_col)} numerical columns."
        })
        recommendations.append({
            "action": "remove_outliers",
            "title": "Clip or Filter Extreme Outliers",
            "description": "Treat values outside 1.5x IQR boundaries to prevent skewing descriptive metrics.",
            "impact": "Normalizes distributions"
        })
        
    if not issues:
        issues.append({
            "type": "healthy",
            "severity": "low",
            "message": "Dataset is well-structured with no significant missing values or duplicate records."
        })
        
    return {
        "missing_cells": missing_cells,
        "missing_cells_pct": missing_pct,
        "duplicate_rows": duplicate_rows,
        "duplicate_rows_pct": duplicate_pct,
        "outlier_count": total_outliers,
        "total_cells": total_cells,
        "score": score,
        "grade": grade,
        "missing_by_column": missing_by_col,
        "outliers_by_column": outliers_by_col,
        "completeness_by_column": completeness_by_col,
        "issues": issues,
        "recommendations": recommendations
    }

def preview_cleaning_operation(df: pd.DataFrame, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate a cleaning operation without altering original dataframe."""
    clean_df = df.copy()
    rows_before = len(clean_df)
    cols_before = len(clean_df.columns)
    quality_before = calculate_data_quality(clean_df)["score"]
    
    sample_changes = []
    
    if operation == "drop_duplicates":
        dups = clean_df.duplicated()
        sample_changes = clean_df[dups].head(5).to_dict(orient="records")
        clean_df = clean_df.drop_duplicates()
        
    elif operation == "fill_missing":
        method = params.get("method", "median")
        cols = params.get("columns", clean_df.columns.tolist())
        for col in cols:
            if col in clean_df.columns and clean_df[col].isna().sum() > 0:
                if pd.api.types.is_numeric_dtype(clean_df[col]):
                    fill_val = clean_df[col].median() if method == "median" else clean_df[col].mean()
                else:
                    mode_val = clean_df[col].mode()
                    fill_val = mode_val[0] if not mode_val.empty else "Unknown"
                clean_df[col] = clean_df[col].fillna(fill_val)
                sample_changes.append({"column": col, "fill_value": str(fill_val), "filled_count": int(df[col].isna().sum())})
                
    elif operation == "drop_columns":
        cols_to_drop = [c for c in params.get("columns", []) if c in clean_df.columns]
        clean_df = clean_df.drop(columns=cols_to_drop)
        sample_changes = [{"dropped_columns": cols_to_drop}]
        
    elif operation == "remove_outliers":
        col = params.get("column")
        if col and col in clean_df.columns and pd.api.types.is_numeric_dtype(clean_df[col]):
            q25 = clean_df[col].quantile(0.25)
            q75 = clean_df[col].quantile(0.75)
            iqr = q75 - q25
            lb = q25 - 1.5 * iqr
            ub = q75 + 1.5 * iqr
            outlier_mask = (clean_df[col] < lb) | (clean_df[col] > ub)
            sample_changes = clean_df[outlier_mask].head(5).to_dict(orient="records")
            clean_df = clean_df[~outlier_mask]
            
    rows_after = len(clean_df)
    cols_after = len(clean_df.columns)
    quality_after = calculate_data_quality(clean_df)["score"]
    
    return {
        "operation": operation,
        "rows_before": rows_before,
        "rows_after": rows_after,
        "columns_before": cols_before,
        "columns_after": cols_after,
        "sample_changes": sample_changes,
        "quality_score_before": quality_before,
        "quality_score_after": quality_after
    }
