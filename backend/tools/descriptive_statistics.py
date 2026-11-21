import pandas as pd
import numpy as np
from typing import Dict, Any, List

def calculate_descriptive_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive descriptive statistics for numerical and categorical variables."""
    numeric_stats = {}
    categorical_stats = {}
    grouped_stats = []
    
    # 1. Numeric statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) > 0:
            skew = float(series.skew()) if len(series) > 2 else 0.0
            kurt = float(series.kurtosis()) if len(series) > 3 else 0.0
            numeric_stats[col] = {
                "count": int(len(series)),
                "mean": round(float(series.mean()), 2),
                "std": round(float(series.std()), 2) if len(series) > 1 else 0.0,
                "variance": round(float(series.var()), 2) if len(series) > 1 else 0.0,
                "min": round(float(series.min()), 2),
                "q25": round(float(series.quantile(0.25)), 2),
                "median": round(float(series.median()), 2),
                "q75": round(float(series.quantile(0.75)), 2),
                "max": round(float(series.max()), 2),
                "skewness": round(skew, 2) if not np.isnan(skew) else 0.0,
                "kurtosis": round(kurt, 2) if not np.isnan(kurt) else 0.0
            }
            
    # 2. Categorical statistics
    cat_cols = [c for c in df.columns if c not in numeric_cols]
    for col in cat_cols:
        series = df[col].dropna()
        if len(series) > 0:
            vc = series.value_counts()
            top_vals = vc.head(6).to_dict()
            mode_val = series.mode().iloc[0] if not series.mode().empty else None
            categorical_stats[col] = {
                "count": int(len(series)),
                "unique_count": int(series.nunique()),
                "mode": str(mode_val) if mode_val is not None else "N/A",
                "top_value_frequency": int(vc.iloc[0]) if not vc.empty else 0,
                "distribution": {str(k): int(v) for k, v in top_vals.items()}
            }
            
    # 3. Grouped comparative statistics (pick top category and top numeric)
    candidate_cats = [c for c in cat_cols if 2 <= df[c].nunique() <= 15]
    candidate_nums = [c for c in numeric_cols if df[c].nunique() > 5 and not ('id' in c.lower() or 'key' in c.lower())]
    
    if candidate_cats and candidate_nums:
        cat_col = candidate_cats[0]
        num_col = candidate_nums[0]
        try:
            agg_df = df.groupby(cat_col)[num_col].agg(['count', 'mean', 'sum']).reset_index()
            agg_df = agg_df.sort_values(by='sum', ascending=False).head(10)
            grouped_stats = [
                {
                    "category_column": cat_col,
                    "numeric_column": num_col,
                    "category": str(row[cat_col]),
                    "count": int(row['count']),
                    "mean": round(float(row['mean']), 2),
                    "sum": round(float(row['sum']), 2)
                }
                for _, row in agg_df.iterrows()
            ]
        except Exception:
            grouped_stats = []
            
    return {
        "numeric_summary": numeric_stats,
        "categorical_summary": categorical_stats,
        "grouped_breakdown": grouped_stats
    }
