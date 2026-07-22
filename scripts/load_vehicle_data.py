"""
UrbanFlow — MySQL Vehicle Registrations Data Loader Script
Loads secondary dataset (OpenCity Pune Vehicle Registrations) into MySQL vehicle_registrations table.
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

from config import RAW_VEHICLE_CSV, VEHICLE_TABLE_NAME

def get_db_connection():
    """Establishes connection to MySQL database using credentials from .env"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "urbanflow_pune")
    )

def load_vehicle_data_to_mysql():
    """
    Reads vehicle registrations CSV from data/raw/pune_vehicle_registrations.csv
    and populates the MySQL vehicle_registrations table.
    """
    print("=" * 60)
    print("UrbanFlow MySQL Loader: Vehicle Registrations Data")
    print("=" * 60)

    if not RAW_VEHICLE_CSV.exists():
        print(f"NOTICE: Secondary vehicle registrations file not found at {RAW_VEHICLE_CSV}")
        print("To load vehicle data, download OpenCity Pune vehicle registrations dataset")
        print(f"and place CSV at: {RAW_VEHICLE_CSV}")
        sys.exit(0)

    try:
        df = pd.read_csv(RAW_VEHICLE_CSV)
        print(f"Loaded {len(df):,} records from vehicle CSV.")
    except Exception as e:
        print(f"ERROR: Failed to read CSV file: {e}")
        sys.exit(1)

    # Standardize column headers
    df.columns = [col.strip().lower() for col in df.columns]

    connection = None
    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            print("Database connection established successfully.")

            insert_query = f"""
            INSERT INTO {VEHICLE_TABLE_NAME} (year, vehicle_type, fuel_type, count)
            VALUES (%s, %s, %s, %s)
            """

            records = []
            for _, row in df.iterrows():
                records.append((
                    int(row.get('year', 0)),
                    str(row.get('vehicle_type', 'Unknown')),
                    str(row.get('fuel_type', 'Unknown')),
                    int(row.get('count', 0))
                ))

            cursor.executemany(insert_query, records)
            connection.commit()
            print("-" * 60)
            print(f"SUCCESS: Successfully inserted {len(records):,} vehicle registration rows into '{VEHICLE_TABLE_NAME}'.")
            print("-" * 60)

    except Error as e:
        print(f"\nDATABASE ERROR: Connection or insert query failed: {e}")
        if connection and connection.is_connected():
            connection.rollback()
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    load_vehicle_data_to_mysql()
