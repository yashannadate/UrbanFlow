"""
UrbanFlow — MySQL Traffic Data Loader Script
Loads cleaned traffic data into MySQL database with robust error handling and transactional commits.
"""

import os
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

# Import project paths & table config
from config import PROCESSED_TRAFFIC_CSV, TRAFFIC_TABLE_NAME

def get_db_connection():
    """
    Establishes connection to MySQL database using credentials from .env
    """
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", 3306))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "urbanflow_pune")

    print(f"Connecting to MySQL database '{database}' at {host}:{port} as user '{user}'...")
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

def load_traffic_to_mysql():
    """
    Reads processed traffic CSV and inserts records into the MySQL traffic_data table.
    """
    print("=" * 60)
    print("UrbanFlow MySQL Loader: Traffic Data")
    print("=" * 60)

    if not PROCESSED_TRAFFIC_CSV.exists():
        print(f"ERROR: Processed file not found at {PROCESSED_TRAFFIC_CSV}")
        print("Please run 'python scripts/clean_data.py' first.")
        sys.exit(1)

    try:
        df = pd.read_csv(PROCESSED_TRAFFIC_CSV)
        print(f"Loaded {len(df):,} records from processed CSV.")
    except Exception as e:
        print(f"ERROR: Failed to read CSV file: {e}")
        sys.exit(1)

    connection = None
    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            print("Database connection established successfully.")

            insert_query = f"""
            INSERT INTO {TRAFFIC_TABLE_NAME} (
                route_id, stop_name, latitude, longitude, time_slot,
                speed_congested, speed_freeflow, sri, congestion_level, is_peak_hour
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Prepare data tuples
            records = []
            for _, row in df.iterrows():
                records.append((
                    str(row.get('route_id', '')),
                    str(row.get('stop_name', '')),
                    float(row.get('latitude', 0.0)),
                    float(row.get('longitude', 0.0)),
                    str(row.get('time_slot', '')),
                    float(row.get('speed_congested', 0.0)),
                    float(row.get('speed_freeflow', 0.0)),
                    float(row.get('sri', 0.0)),
                    str(row.get('congestion_level', '')),
                    int(row.get('is_peak_hour', 0))
                ))

            # Batch execution
            batch_size = 1000
            total_records = len(records)
            print(f"Inserting {total_records:,} records into table '{TRAFFIC_TABLE_NAME}' in batches of {batch_size}...")

            for i in range(0, total_records, batch_size):
                batch = records[i:i + batch_size]
                cursor.executemany(insert_query, batch)
                connection.commit()
                print(f"  - Progress: {min(i + batch_size, total_records):,}/{total_records:,} rows inserted.")

            print("-" * 60)
            print(f"SUCCESS: Successfully inserted {total_records:,} rows into '{TRAFFIC_TABLE_NAME}'.")
            print("-" * 60)

    except Error as e:
        print(f"\nDATABASE ERROR: Connection or query failed: {e}")
        if connection and connection.is_connected():
            connection.rollback()
            print("Transaction rolled back due to error.")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    load_traffic_to_mysql()
