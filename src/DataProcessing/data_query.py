# src/DataProcessing/data_query.py

import sqlite3
import pandas as pd
from typing import Optional

def fetch_last_data_entry(city: str, db_path: str = "weather_data.db") -> Optional[pd.Series]:
    """
    Fetch the most recent weather entry for a given city from the SQLite database.
    
    Parameters:
        city (str): The name of the city to search for.
        db_path (str): Path to the SQLite database file.
        
    Returns:
        pd.Series: The most recent row as a pandas Series, or None if not found.
    """
    try:
        conn = sqlite3.connect(db_path)
        query = """
            SELECT * FROM weather
            WHERE name = ?
            ORDER BY dt DESC
            LIMIT 1
        """
        df = pd.read_sql_query(query, conn, params=(city,))
        conn.close()

        if not df.empty:
            return df.iloc[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return None
