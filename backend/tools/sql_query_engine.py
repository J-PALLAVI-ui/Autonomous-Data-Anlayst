import sqlite3
import pandas as pd
from typing import Dict, Any, List

def execute_analytical_sql(df: pd.DataFrame, query: str, table_name: str = "dataset") -> Dict[str, Any]:
    """Execute SQL query using DuckDB if available, or in-memory SQLite engine."""
    # Attempt DuckDB first
    try:
        import duckdb
        con = duckdb.connect(database=':memory:')
        con.register(table_name, df)
        result_df = con.execute(query).fetchdf()
        con.close()
        return {
            "engine": "duckdb",
            "columns": result_df.columns.tolist(),
            "data": result_df.to_dict(orient="records"),
            "row_count": len(result_df)
        }
    except Exception as e_duck:
        # Fallback to in-memory SQLite
        try:
            conn = sqlite3.connect(":memory:")
            # Clean dataframe for sqlite serialization
            clean_df = df.copy()
            for col in clean_df.select_dtypes(include=['datetime64', 'datetimetz']).columns:
                clean_df[col] = clean_df[col].astype(str)
            clean_df.to_sql(table_name, conn, index=False, if_exists="replace")
            result_df = pd.read_sql_query(query, conn)
            conn.close()
            return {
                "engine": "sqlite_memory",
                "columns": result_df.columns.tolist(),
                "data": result_df.to_dict(orient="records"),
                "row_count": len(result_df)
            }
        except Exception as e_sql:
            return {
                "engine": "error",
                "error": str(e_sql),
                "columns": [],
                "data": [],
                "row_count": 0
            }
