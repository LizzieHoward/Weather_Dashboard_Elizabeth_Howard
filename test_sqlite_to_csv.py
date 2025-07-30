#!/usr/bin/env python3
"""
Test script to verify the SQLite to CSV conversion functionality.
"""

import unittest
import os
import csv
import sqlite3
from pathlib import Path
from sqlite_to_csv import convert_sqlite_to_csv


class TestSQLiteToCSV(unittest.TestCase):
    """Test cases for SQLite to CSV conversion functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_root = Path(__file__).parent
        self.db_path = self.project_root / "Data" / "weather_data.db"
        self.csv_path = self.project_root / "EHWeatherData.csv"
    
    def test_database_exists(self):
        """Test that the source database file exists."""
        self.assertTrue(self.db_path.exists(), f"Database file not found: {self.db_path}")
    
    def test_conversion_creates_csv(self):
        """Test that the conversion creates a CSV file."""
        # Remove CSV if it exists
        if self.csv_path.exists():
            os.remove(self.csv_path)
        
        # Run conversion
        result_path = convert_sqlite_to_csv()
        
        # Check that CSV file was created
        self.assertTrue(os.path.exists(result_path), "CSV file was not created")
        self.assertEqual(str(self.csv_path), result_path, "CSV file path mismatch")
    
    def test_csv_has_correct_structure(self):
        """Test that the CSV file has the correct structure and data."""
        # Ensure CSV exists
        if not self.csv_path.exists():
            convert_sqlite_to_csv()
        
        # Get expected data from database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute("PRAGMA table_info(weather)")
        expected_columns = [row[1] for row in cursor.fetchall()]
        
        # Get row count
        cursor.execute("SELECT COUNT(*) FROM weather")
        expected_row_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Check CSV structure
        with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Check headers
            headers = next(reader)
            self.assertEqual(headers, expected_columns, "CSV headers don't match database columns")
            
            # Count data rows
            data_rows = list(reader)
            self.assertEqual(len(data_rows), expected_row_count, "CSV row count doesn't match database")
    
    def test_data_integrity(self):
        """Test that the data in CSV matches the database."""
        # Ensure CSV exists
        if not self.csv_path.exists():
            convert_sqlite_to_csv()
        
        # Get data from database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather ORDER BY id")
        db_rows = cursor.fetchall()
        conn.close()
        
        # Get data from CSV
        with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip headers
            csv_rows = list(reader)
        
        # Compare row counts
        self.assertEqual(len(csv_rows), len(db_rows), "Row count mismatch between CSV and database")
        
        # Compare first and last rows to verify data integrity
        if db_rows:
            # Convert database row to strings for comparison (CSV data is all strings)
            first_db_row = [str(val) if val is not None else '' for val in db_rows[0]]
            last_db_row = [str(val) if val is not None else '' for val in db_rows[-1]]
            
            self.assertEqual(csv_rows[0], first_db_row, "First row data mismatch")
            self.assertEqual(csv_rows[-1], last_db_row, "Last row data mismatch")


if __name__ == '__main__':
    unittest.main()