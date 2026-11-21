import pandas as pd
import numpy as np
from typing import Dict, Any, List

def analyze_correlations(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute correlation matrix, identify key relationships, and format for heatmap visualization."""
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Filter out columns with 0 variance or ID-like columns
    valid_cols = []
    for col in numeric_df.columns:
        if numeric_df[col].std() > 0 and numeric_df[col].nunique() > 1 and not ('id' in col.lower() or 'key' in col.lower()):
            valid_cols.append(col)
            
    if len(valid_cols) < 2:
        return {
            "columns": valid_cols,
            "matrix": [],
            "heatmap_cells": [],
            "significant_pairs": [],
            "summary": "Insufficient numeric columns (minimum 2 needed) to calculate correlation matrix."
        }
        
    corr_matrix = numeric_df[valid_cols].corr(method='pearson').round(3)
    
    # Create 2D matrix array and flat cell list for Heatmap chart
    matrix_data = []
    heatmap_cells = []
    for r_idx, r_col in enumerate(valid_cols):
        row_values = []
        for c_idx, c_col in enumerate(valid_cols):
            val = float(corr_matrix.loc[r_col, c_col])
            if np.isnan(val):
                val = 0.0
            row_values.append(val)
            heatmap_cells.append({
                "x": c_col,
                "y": r_col,
                "correlation": round(val, 2)
            })
        matrix_data.append({"row": r_col, "values": row_values})
        
    # Find distinct pairs
    pairs = []
    for i in range(len(valid_cols)):
        for j in range(i + 1, len(valid_cols)):
            col1 = valid_cols[i]
            col2 = valid_cols[j]
            corr_val = float(corr_matrix.loc[col1, col2])
            if not np.isnan(corr_val):
                abs_val = abs(corr_val)
                if abs_val >= 0.7:
                    strength = "Strong Positive" if corr_val > 0 else "Strong Negative"
                elif abs_val >= 0.4:
                    strength = "Moderate Positive" if corr_val > 0 else "Moderate Negative"
                else:
                    strength = "Weak or No Correlation"
                    
                pairs.append({
                    "col1": col1,
                    "col2": col2,
                    "correlation": round(corr_val, 3),
                    "abs_correlation": round(abs_val, 3),
                    "strength": strength,
                    "relationship": f"{strength} relationship between '{col1}' and '{col2}' (r = {round(corr_val, 2)})"
                })
                
    pairs.sort(key=lambda x: x["abs_correlation"], reverse=True)
    
    top_pairs = pairs[:8]
    summary_text = ""
    if top_pairs:
        strongest = top_pairs[0]
        summary_text = f"Strongest relationship observed: {strongest['relationship']}."
    else:
        summary_text = "No strong linear correlations detected among numeric features."
        
    return {
        "columns": valid_cols,
        "matrix": matrix_data,
        "heatmap_cells": heatmap_cells,
        "significant_pairs": top_pairs,
        "summary": summary_text
    }
