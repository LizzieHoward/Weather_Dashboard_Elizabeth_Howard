#!/usr/bin/env python3
"""
Script to convert SQLite weather database to CSV format.
Converts Data/weather_data.db to EHWeatherData.csv in the root directory.
"""

import sqlite3
import csv
import os
from pathlib import Path


def convert_sqlite_to_csv():
    """
    Convert the weather data from SQLite database to CSV format.
    
    The CSV file will be named 'EHWeatherData.csv' and placed in the root directory.
    """
    # Define paths
    script_dir = Path(__file__).parent
    db_path = script_dir / "Data" / "weather_data.db"
    csv_path = script_dir / "EHWeatherData.csv"
    
    # Check if database file exists
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all data from weather table
        cursor.execute("SELECT * FROM weather ORDER BY id")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute("PRAGMA table_info(weather)")
        columns = [row[1] for row in cursor.fetchall()]
        
        conn.close()
        
        # Write to CSV file
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(columns)
            
            # Write data rows
            writer.writerows(rows)
        
        print(f"Successfully converted {len(rows)} records from SQLite to CSV")
        print(f"Output file: {csv_path}")
        print(f"Columns: {', '.join(columns)}")
        
        return str(csv_path)
        
    except Exception as e:
        print(f"Error converting database to CSV: {e}")
        raise


if __name__ == "__main__":
    convert_sqlite_to_csv()