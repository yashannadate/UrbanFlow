"""
UrbanFlow — Full System Demo & Verification Script
Runs end-to-end verification:
1. Data Cleaning ETL
2. Database Schema Creation (SQLite / MySQL compatibility)
3. Data Ingestion
4. Execution of all 5 SQL Analytical Queries with formatted table outputs
"""

import sqlite3
import pandas as pd
from pathlib import Path
import sys

# Add scripts directory to module search path
sys.path.append(str(Path(__file__).resolve().parent))
from clean_data import clean_traffic_data
from config import PROCESSED_TRAFFIC_CSV, BASE_DIR

DEMO_DB = BASE_DIR / "urbanflow_demo.db"

def run_sql_queries(conn):
    """Executes research analysis queries against the ingested database."""
    queries = {
        "Query 1: Average SRI & Speeds by Time Slot": """
            SELECT 
                time_slot,
                COUNT(*) AS total_records,
                ROUND(AVG(sri), 2) AS avg_sri,
                ROUND(AVG(speed_congested), 2) AS avg_congested_speed_kmh,
                ROUND(AVG(speed_freeflow), 2) AS avg_freeflow_speed_kmh
            FROM traffic_data
            GROUP BY time_slot
            ORDER BY avg_sri DESC;
        """,
        
        "Query 2: Top 10 Bottleneck Stops (by Avg SRI)": """
            SELECT 
                stop_name,
                COUNT(DISTINCT route_id) AS connecting_routes,
                COUNT(*) AS total_records,
                ROUND(AVG(sri), 2) AS avg_sri,
                ROUND(AVG(speed_congested), 2) AS avg_speed_kmh
            FROM traffic_data
            GROUP BY stop_name
            ORDER BY avg_sri DESC
            LIMIT 10;
        """,

        "Query 3: Congestion Level Severity Breakdown": """
            SELECT 
                congestion_level,
                COUNT(*) AS record_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM traffic_data), 2) AS percentage_share,
                ROUND(AVG(sri), 2) AS avg_sri
            FROM traffic_data
            GROUP BY congestion_level
            ORDER BY avg_sri DESC;
        """,

        "Query 4: Peak vs Non-Peak Operating Performance": """
            SELECT 
                CASE WHEN is_peak_hour = 1 THEN 'Peak Hours (8-10AM, 5-8PM)' ELSE 'Non-Peak Hours' END AS period_type,
                COUNT(*) AS record_count,
                ROUND(AVG(speed_congested), 2) AS avg_congested_speed_kmh,
                ROUND(AVG(speed_freeflow), 2) AS avg_freeflow_speed_kmh,
                ROUND(AVG(sri), 2) AS avg_sri
            FROM traffic_data
            GROUP BY is_peak_hour;
        """,

        "Query 5: Route Congestion Ranking": """
            SELECT 
                route_id,
                COUNT(DISTINCT stop_name) AS total_stops,
                ROUND(AVG(sri), 2) AS avg_route_sri,
                ROUND(MIN(speed_congested), 2) AS min_congested_speed,
                ROUND(AVG(speed_congested), 2) AS avg_congested_speed
            FROM traffic_data
            GROUP BY route_id
            ORDER BY avg_route_sri DESC;
        """
    }

    print("\n" + "=" * 70)
    print("  URBANFLOW DEMO: EXECUTING SQL ANALYTICAL QUERIES SUITE")
    print("=" * 70)

    for title, sql in queries.items():
        print(f"\n[+] {title}:")
        print("-" * 65)
        df_result = pd.read_sql_query(sql, conn)
        print(df_result.to_string(index=False))
        print("-" * 65)

def run_full_demo():
    print("\nSTARTING URBANFLOW END-TO-END DEMO VERIFICATION...\n")

    # Step 1: Run Data Cleaning ETL
    clean_traffic_data()

    if not PROCESSED_TRAFFIC_CSV.exists():
        print("ERROR: Processed dataset does not exist.")
        return

    # Step 2: Load into Local Demo Database
    print(f"Loading cleaned dataset into demo SQLite database at {DEMO_DB}...")
    df_clean = pd.read_csv(PROCESSED_TRAFFIC_CSV)

    conn = sqlite3.connect(DEMO_DB)
    df_clean.to_sql("traffic_data", conn, if_exists="replace", index=False)
    print("Data ingested successfully into database table 'traffic_data'.")

    # Step 3: Run Research Analysis Queries
    run_sql_queries(conn)
    conn.close()

    print("\n" + "=" * 70)
    print("DEMO VERIFICATION COMPLETE: ALL PIPELINES & QUERIES WORKING 100%!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_full_demo()
