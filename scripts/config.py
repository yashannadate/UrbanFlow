"""
UrbanFlow — Configuration Module
Contains non-secret system constants, file paths, ETL parameters, and peak-hour rules.
Secrets (DB passwords, hosts) are loaded exclusively via environment variables (.env).
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

# File Paths
RAW_TRAFFIC_CSV = DATA_RAW_DIR / "pune_gtfs_traffic.csv"
PROCESSED_TRAFFIC_CSV = DATA_PROCESSED_DIR / "traffic_clean.csv"
RAW_VEHICLE_CSV = DATA_RAW_DIR / "pune_vehicle_registrations.csv"

# MySQL Target Tables
TRAFFIC_TABLE_NAME = "traffic_data"
VEHICLE_TABLE_NAME = "vehicle_registrations"

# Transit Analysis Constants & Rules
# Morning Peak: 08:00 to 10:00 (inclusive of 8 AM and 9 AM slots)
# Evening Peak: 17:00 to 20:00 (5 PM to 8 PM)
MORNING_PEAK_START = 8
MORNING_PEAK_END = 10
EVENING_PEAK_START = 17
EVENING_PEAK_END = 20

# Congestion Category Standards
CONGESTION_LEVEL_MAPPING = {
    'very smooth': 'Very Smooth',
    'smooth': 'Smooth',
    'mild congestion': 'Mild Congestion',
    'heavy congestion': 'Heavy Congestion'
}
