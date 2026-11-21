import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List

def load_dataset(file_path: str) -> pd.DataFrame:
    """Load dataset from CSV or Excel with robust encoding and format handling."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    
    # Try different encodings for CSV
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    for enc in encodings:
        try:
            return pd.read_csv(file_path, encoding=enc)
        except (UnicodeDecodeError, Exception):
            continue
    # Fallback default
    return pd.read_csv(file_path, errors='replace')

def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Inspect dataset rows, columns, data types, nulls, unique values, and stats."""
    total_rows = len(df)
    total_cols = len(df.columns)
    
    columns_profile = []
    
    for col in df.columns:
        series = df[col]
        null_count = int(series.isna().sum())
        null_pct = round((null_count / total_rows * 100) if total_rows > 0 else 0.0, 2)
        non_null_series = series.dropna()
        unique_count = int(non_null_series.nunique())
        
        dtype_str = str(series.dtype)
        general_type = "categorical"
        stats = {}
        
        # Check datetime using pandas api types
        is_date = False
        if pd.api.types.is_datetime64_any_dtype(series):
            is_date = True
        elif (pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)) and unique_count > 0:
            sample = non_null_series.head(20)
            try:
                converted = pd.to_datetime(sample, errors='coerce', format='mixed')
                if converted.notna().mean() > 0.8:
                    is_date = True
            except Exception:
                is_date = False
                
        if is_date:
            general_type = "datetime"
            try:
                dt_series = pd.to_datetime(series, errors='coerce', format='mixed')
                valid_dt = dt_series.dropna()
                if not valid_dt.empty:
                    stats = {
                        "min_date": str(valid_dt.min()),
                        "max_date": str(valid_dt.max()),
                        "timespan_days": int((valid_dt.max() - valid_dt.min()).days)
                    }
            except Exception:
                pass
        elif pd.api.types.is_bool_dtype(series):
            general_type = "boolean"
        elif pd.api.types.is_numeric_dtype(series):
            if unique_count == total_rows and total_rows > 20 and ('id' in col.lower() or 'key' in col.lower() or 'index' in col.lower()):
                general_type = "id_or_unique"
            elif unique_count <= 2 and set(non_null_series.unique()).issubset({0, 1, 0.0, 1.0}):
                general_type = "boolean"
            else:
                general_type = "numeric"
                if not non_null_series.empty:
                    stats = {
                        "min": round(float(non_null_series.min()), 2),
                        "max": round(float(non_null_series.max()), 2),
                        "mean": round(float(non_null_series.mean()), 2),
                        "median": round(float(non_null_series.median()), 2),
                        "std": round(float(non_null_series.std()), 2) if len(non_null_series) > 1 else 0.0,
                        "q25": round(float(non_null_series.quantile(0.25)), 2),
                        "q75": round(float(non_null_series.quantile(0.75)), 2)
                    }
        else:
            if unique_count == total_rows and total_rows > 20:
                general_type = "id_or_unique"
            else:
                general_type = "categorical"
                top_counts = non_null_series.value_counts().head(5).to_dict()
                stats = {
                    "top_values": {str(k): int(v) for k, v in top_counts.items()}
                }
        
        sample_vals = [
            (str(v) if not isinstance(v, (int, float, bool)) else (None if pd.isna(v) else v))
            for v in non_null_series.head(5).tolist()
        ]
        
        columns_profile.append({
            "name": col,
            "dtype": dtype_str,
            "general_type": general_type,
            "total_count": total_rows,
            "null_count": null_count,
            "null_percentage": null_pct,
            "unique_count": unique_count,
            "sample_values": sample_vals,
            "stats": stats
        })
        
    preview_df = df.head(15).replace({np.nan: None, np.inf: None, -np.inf: None})
    preview_rows = preview_df.to_dict(orient="records")
    clean_preview = []
    for row in preview_rows:
        clean_row = {}
        for k, v in row.items():
            if isinstance(v, (pd.Timestamp, np.datetime64)):
                clean_row[k] = str(v)
            elif isinstance(v, (np.integer, int)):
                clean_row[k] = int(v)
            elif isinstance(v, (np.floating, float)):
                clean_row[k] = None if (np.isnan(v) or np.isinf(v)) else round(float(v), 4)
            elif pd.isna(v):
                clean_row[k] = None
            else:
                clean_row[k] = v
        clean_preview.append(clean_row)
        
    return {
        "row_count": total_rows,
        "column_count": total_cols,
        "columns": columns_profile,
        "preview_rows": clean_preview
    }
