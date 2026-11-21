import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

def analyze_trends(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Detect date columns and analyze temporal trends, growth rates, and seasonality."""
    date_col = None
    
    # 1. Identify datetime column
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_col = col
            break
            
    if not date_col:
        for col in df.columns:
            if df[col].dtype == 'object':
                sample = df[col].dropna().head(20)
                try:
                    converted = pd.to_datetime(sample, errors='coerce', format='mixed')
                    if converted.notna().mean() > 0.8:
                        date_col = col
                        break
                except Exception:
                    continue
                    
    # Also check for 'year', 'date', 'month', 'timestamp' in column names
    if not date_col:
        for col in df.columns:
            if any(k in col.lower() for k in ['date', 'time', 'year', 'month', 'period']):
                try:
                    pd.to_datetime(df[col].dropna().head(10), errors='coerce', format='mixed')
                    date_col = col
                    break
                except Exception:
                    continue
                    
    if not date_col:
        return None
        
    try:
        temp_df = df.copy()
        temp_df['__parsed_date__'] = pd.to_datetime(temp_df[date_col], errors='coerce', format='mixed')
        valid_df = temp_df.dropna(subset=['__parsed_date__'])
        
        if len(valid_df) < 5:
            return None
            
        valid_df = valid_df.sort_values(by='__parsed_date__')
        min_date = valid_df['__parsed_date__'].min()
        max_date = valid_df['__parsed_date__'].max()
        days_span = (max_date - min_date).days
        
        # Determine appropriate frequency aggregation
        if days_span > 730:
            freq = 'YE' # Annual
            freq_label = 'Year'
        elif days_span > 90:
            freq = 'ME' # Monthly
            freq_label = 'Month'
        elif days_span > 14:
            freq = 'W' # Weekly
            freq_label = 'Week'
        else:
            freq = 'D' # Daily
            freq_label = 'Day'
            
        # Select key numeric column to analyze over time
        numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if not ('id' in c.lower() or 'key' in c.lower())]
        if not numeric_cols:
            return None
            
        target_num_col = numeric_cols[0]
        
        valid_df.set_index('__parsed_date__', inplace=True)
        resampled = valid_df[target_num_col].resample(freq).agg(['sum', 'mean', 'count']).reset_index()
        resampled = resampled[resampled['count'] > 0]
        
        if len(resampled) < 2:
            return None
            
        trend_points = []
        for _, row in resampled.iterrows():
            d_str = row['__parsed_date__'].strftime('%Y-%m-%d' if freq in ['W', 'D'] else ('%Y-%m' if freq == 'ME' else '%Y'))
            trend_points.append({
                "period": d_str,
                "sum": round(float(row['sum']), 2),
                "mean": round(float(row['mean']), 2),
                "count": int(row['count'])
            })
            
        # Growth calculation
        first_sum = trend_points[0]["sum"]
        last_sum = trend_points[-1]["sum"]
        growth_pct = round(((last_sum - first_sum) / abs(first_sum) * 100) if first_sum != 0 else 0.0, 2)
        
        if growth_pct > 5:
            direction = "Upward Growth"
        elif growth_pct < -5:
            direction = "Downward Decline"
        else:
            direction = "Stable / Steady"
            
        # Peak & trough
        peak_period = max(trend_points, key=lambda x: x["sum"])
        trough_period = min(trend_points, key=lambda x: x["sum"])
        
        return {
            "date_column": date_col,
            "metric_column": target_num_col,
            "frequency": freq_label,
            "direction": direction,
            "overall_growth_pct": growth_pct,
            "first_period_val": first_sum,
            "last_period_val": last_sum,
            "peak_period": peak_period,
            "trough_period": trough_period,
            "trend_data": trend_points,
            "summary": f"{direction} of {growth_pct}% detected in '{target_num_col}' across {len(trend_points)} {freq_label.lower()}s. Peak reached in {peak_period['period']} ({peak_period['sum']:,})."
        }
    except Exception as e:
        return None
