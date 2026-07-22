"""
UrbanFlow — Data Cleaning ETL Script
Cleans Pune GTFS Traffic Dataset and derives analytical features (e.g., peak-hour flags).
"""

import re
import sys
import pandas as pd
from config import RAW_TRAFFIC_CSV, PROCESSED_TRAFFIC_CSV, MORNING_PEAK_START, MORNING_PEAK_END, EVENING_PEAK_START, EVENING_PEAK_END

def parse_hour(time_slot_str):
    """
    Extracts the starting hour (0-23) from various time_slot string formats.
    Examples: '08:00:00', '08:00 - 09:00', '8:00 AM', '17:30', '8'
    """
    if pd.isna(time_slot_str):
        return None
    
    time_str = str(time_slot_str).strip()
    
    # Try finding first digit sequence (1-2 digits) representing the hour
    match = re.search(r'(\d{1,2})', time_str)
    if not match:
        return None
    
    hour = int(match.group(1))
    
    # Adjust for PM notation if present
    if 'PM' in time_str.upper() and hour < 12:
        hour += 12
    elif 'AM' in time_str.upper() and hour == 12:
        hour = 0
        
    return hour

def determine_peak_hour(time_slot_str):
    """
    Returns 1 if time_slot falls within peak hours (8-10 AM or 5-8 PM), else 0.
    Morning Peak: 08:00 to <10:00 (Hours 8, 9)
    Evening Peak: 17:00 to <20:00 (Hours 17, 18, 19)
    """
    hour = parse_hour(time_slot_str)
    if hour is None:
        return 0
    
    is_morning_peak = MORNING_PEAK_START <= hour < MORNING_PEAK_END
    is_evening_peak = EVENING_PEAK_START <= hour < EVENING_PEAK_END
    
    return 1 if (is_morning_peak or is_evening_peak) else 0

def clean_traffic_data():
    """
    Loads raw GTFS traffic data, cleans missing values, standardizes text fields,
    computes peak hour derivation, and exports to data/processed/traffic_clean.csv.
    """
    print("=" * 60)
    print("UrbanFlow ETL: Cleaning Traffic Data")
    print("=" * 60)

    if not RAW_TRAFFIC_CSV.exists():
        print(f"ERROR: Raw data file not found at: {RAW_TRAFFIC_CSV}")
        print("Please place 'pune_gtfs_traffic.csv' inside data/raw/ before running cleaning script.")
        sys.exit(1)

    print(f"Loading raw dataset from {RAW_TRAFFIC_CSV}...")
    df = pd.read_csv(RAW_TRAFFIC_CSV)
    
    initial_rows = len(df)
    print(f"Initial row count: {initial_rows:,}")

    # Standardize column headers (lowercase, strip whitespace)
    df.columns = [col.strip().lower() for col in df.columns]

    # Required columns check
    required_cols = {'stop_name', 'sri'}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        print(f"ERROR: Missing expected columns in raw CSV: {missing_cols}")
        sys.exit(1)

    # Drop rows with missing critical attributes (stop_name or sri)
    df_clean = df.dropna(subset=['stop_name', 'sri']).copy()
    dropped_missing = initial_rows - len(df_clean)
    print(f"Dropped {dropped_missing:,} rows due to missing 'stop_name' or 'sri'.")

    # Strip whitespace & title-case congestion_level
    if 'congestion_level' in df_clean.columns:
        df_clean['congestion_level'] = (
            df_clean['congestion_level']
            .astype(str)
            .str.strip()
            .str.title()
        )

    # Derive is_peak_hour feature
    if 'time_slot' in df_clean.columns:
        df_clean['is_peak_hour'] = df_clean['time_slot'].apply(determine_peak_hour)
    else:
        df_clean['is_peak_hour'] = 0

    # Clean data types for numeric metrics
    numeric_cols = ['latitude', 'longitude', 'speed_congested', 'speed_freeflow', 'sri']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # Re-drop any NaN introduced by numeric coercion in sri
    df_clean = df_clean.dropna(subset=['sri']).copy()

    final_rows = len(df_clean)
    print("-" * 60)
    print(f"Cleaning Complete.")
    print(f"Final Cleaned Row Count: {final_rows:,} (Removed {initial_rows - final_rows:,} rows in total)")
    print("-" * 60)

    # Ensure processed directory exists
    PROCESSED_TRAFFIC_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_TRAFFIC_CSV, index=False)
    print(f"Cleaned dataset saved successfully to: {PROCESSED_TRAFFIC_CSV}\n")

if __name__ == "__main__":
    clean_traffic_data()
