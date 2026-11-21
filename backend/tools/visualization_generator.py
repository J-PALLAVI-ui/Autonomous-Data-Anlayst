import pandas as pd
import numpy as np
from typing import Dict, Any, List

def generate_visualizations(
    df: pd.DataFrame,
    correlations: Dict[str, Any],
    trends: Dict[str, Any] = None,
    descriptive_stats: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """Automatically select and configure meaningful, goal-oriented charts based on data characteristics."""
    charts = []
    
    numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if not ('id' in c.lower() or 'key' in c.lower())]
    cat_cols = [c for c in df.columns if c not in numeric_cols and df[c].nunique() > 1 and df[c].nunique() <= 20]
    
    # 1. Line Chart: Temporal Trend (if trend data exists)
    if trends and trends.get("trend_data"):
        trend_items = trends["trend_data"]
        charts.append({
            "id": "trend-line-chart",
            "title": f"Chronological Trend: {trends.get('metric_column', 'Metric')} over {trends.get('frequency', 'Period')}",
            "chart_type": "line",
            "x_axis": "period",
            "y_axis": "sum",
            "description": f"Displays temporal trajectory and growth patterns of {trends.get('metric_column')} across intervals.",
            "data": trend_items,
            "insights": trends.get("summary", ""),
            "config": {
                "color": "#3b82f6",
                "strokeWidth": 2,
                "secondaryY": "mean"
            }
        })
        
    # 2. Bar Chart: Categorical Aggregation (e.g. Top category vs primary numeric)
    if cat_cols and numeric_cols:
        cat_col = cat_cols[0]
        num_col = numeric_cols[0]
        try:
            agg_df = df.groupby(cat_col)[num_col].agg(['sum', 'mean']).reset_index()
            agg_df = agg_df.sort_values(by='sum', ascending=False).head(8)
            bar_data = [
                {
                    cat_col: str(row[cat_col]),
                    "Total": round(float(row['sum']), 2),
                    "Average": round(float(row['mean']), 2)
                }
                for _, row in agg_df.iterrows()
            ]
            if bar_data:
                charts.append({
                    "id": f"bar-{cat_col}-{num_col}",
                    "title": f"Aggregated {num_col} by {cat_col}",
                    "chart_type": "bar",
                    "x_axis": cat_col,
                    "y_axis": "Total",
                    "description": f"Compares cumulative performance and average values across {cat_col} segments.",
                    "data": bar_data,
                    "insights": f"Top category '{bar_data[0][cat_col]}' accounts for {bar_data[0]['Total']:,} total {num_col}.",
                    "config": {
                        "color": "#6366f1",
                        "secondaryColor": "#10b981"
                    }
                })
        except Exception:
            pass

    # 3. Pie Chart: Categorical Composition
    if cat_cols:
        pie_cat = cat_cols[0]
        vc = df[pie_cat].value_counts().head(6)
        total_non_null = len(df[pie_cat].dropna())
        pie_data = []
        for name, cnt in vc.items():
            pct = round((cnt / total_non_null) * 100, 1)
            pie_data.append({
                "name": str(name),
                "value": int(cnt),
                "percentage": pct
            })
        if len(pie_data) >= 2:
            charts.append({
                "id": f"pie-{pie_cat}",
                "title": f"Distribution Breakdown: {pie_cat}",
                "chart_type": "pie",
                "x_axis": "name",
                "y_axis": "value",
                "description": f"Proportional share of records across top categories in '{pie_cat}'.",
                "data": pie_data,
                "insights": f"'{pie_data[0]['name']}' is the dominant segment, representing {pie_data[0]['percentage']}% of total volume.",
                "config": {
                    "colors": ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#64748b"]
                }
            })

    # 4. Histogram: Frequency Distribution of primary continuous variable
    if numeric_cols:
        hist_col = numeric_cols[0]
        series = df[hist_col].dropna()
        if len(series) >= 10:
            try:
                counts, bin_edges = np.histogram(series, bins=10)
                hist_data = []
                for i in range(len(counts)):
                    bin_label = f"{round(float(bin_edges[i]), 1)} - {round(float(bin_edges[i+1]), 1)}"
                    hist_data.append({
                        "bin": bin_label,
                        "frequency": int(counts[i])
                    })
                charts.append({
                    "id": f"hist-{hist_col}",
                    "title": f"Frequency Distribution: {hist_col}",
                    "chart_type": "histogram",
                    "x_axis": "bin",
                    "y_axis": "frequency",
                    "description": f"Frequency distribution bins showing the spread and modality of {hist_col}.",
                    "data": hist_data,
                    "insights": f"Mean is {round(float(series.mean()), 2)} with standard deviation of {round(float(series.std()), 2)}.",
                    "config": {
                        "color": "#0ea5e9"
                    }
                })
            except Exception:
                pass

    # 5. Scatter Plot: Correlation between top 2 correlated numeric variables
    if correlations and correlations.get("significant_pairs"):
        top_pair = correlations["significant_pairs"][0]
        c1, c2 = top_pair["col1"], top_pair["col2"]
        valid_pairs = df[[c1, c2]].dropna()
        if len(valid_pairs) >= 5:
            # Sample up to 100 points for crisp interactive charting
            sample_df = valid_pairs.sample(min(100, len(valid_pairs)), random_state=42)
            scatter_data = [
                {
                    c1: round(float(row[c1]), 2),
                    c2: round(float(row[c2]), 2),
                    "tooltip": f"{c1}: {round(float(row[c1]), 2)}, {c2}: {round(float(row[c2]), 2)}"
                }
                for _, row in sample_df.iterrows()
            ]
            charts.append({
                "id": f"scatter-{c1}-{c2}",
                "title": f"Bivariate Relationship: {c1} vs {c2}",
                "chart_type": "scatter",
                "x_axis": c1,
                "y_axis": c2,
                "description": f"Explores the correlation and potential non-linearities between {c1} and {c2}.",
                "data": scatter_data,
                "insights": f"{top_pair['strength']} (Pearson r = {top_pair['correlation']}).",
                "config": {
                    "color": "#f97316"
                }
            })

    # 6. Box Plot: Distribution & Outliers for numeric columns
    if numeric_cols:
        box_data = []
        for col in numeric_cols[:5]:
            s = df[col].dropna()
            if len(s) >= 5:
                q25 = float(s.quantile(0.25))
                q75 = float(s.quantile(0.75))
                iqr = q75 - q25
                box_data.append({
                    "column": col,
                    "min": round(float(max(s.min(), q25 - 1.5 * iqr)), 2),
                    "q25": round(q25, 2),
                    "median": round(float(s.median()), 2),
                    "q75": round(q75, 2),
                    "max": round(float(min(s.max(), q75 + 1.5 * iqr)), 2),
                    "mean": round(float(s.mean()), 2)
                })
        if box_data:
            charts.append({
                "id": "box-plot-summary",
                "title": "Five-Number Statistical Summary (Box Plot)",
                "chart_type": "box",
                "x_axis": "column",
                "y_axis": "median",
                "description": "Displays minimum, 25th percentile, median, 75th percentile, and maximum across numeric features.",
                "data": box_data,
                "insights": "Useful for identifying variance ranges and detecting distribution skewness.",
                "config": {
                    "color": "#8b5cf6"
                }
            })

    # 7. Correlation Heatmap
    if correlations and correlations.get("heatmap_cells") and len(correlations.get("columns", [])) >= 2:
        charts.append({
            "id": "correlation-heatmap",
            "title": "Inter-Variable Correlation Heatmap",
            "chart_type": "heatmap",
            "x_axis": "x",
            "y_axis": "y",
            "description": "Pairwise Pearson correlation matrix showing linear dependencies among numerical columns.",
            "data": correlations["heatmap_cells"],
            "insights": correlations.get("summary", ""),
            "config": {
                "columns": correlations["columns"]
            }
        })
        
    return charts
