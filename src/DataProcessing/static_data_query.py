# src/DataProcessing/static_data_query.py

import sqlite3
import pandas as pd
from typing import Optional, List, Tuple

class StaticDataQuery:
    """
    A class to handle all database operations for the static weather database.
    Provides methods to query cities and retrieve weather data with intelligent record selection.
    """
    
    def __init__(self, db_path: str = "Data/weather_data.db"):
        """
        Initialize the StaticDataQuery with database path.
        
        Parameters:
            db_path (str): Path to the static SQLite database file.
        """
        self.db_path = db_path
        self.data_fields = ['temp', 'feels_like', 'humidity', 'description', 'speed', 'dt']
        
    def get_all_cities(self) -> List[str]:
        """
        Get all unique city names from the static weather database.
        
        Returns:
            List[str]: List of unique city names, sorted alphabetically.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT DISTINCT name FROM weather_data
                WHERE name IS NOT NULL
                ORDER BY name ASC
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                cities = df['name'].tolist()
                print(f"[DEBUG] Found {len(cities)} unique cities in static database")
                return cities
            else:
                print("[DEBUG] No cities found in static database")
                return []
        except Exception as e:
            print(f"Error fetching cities from static database: {e}")
            return []

    def _calculate_completeness_score(self, row: pd.Series) -> int:
        """
        Calculate the completeness score for a data record based on non-null fields.
        
        Parameters:
            row (pd.Series): A database row to evaluate.
            
        Returns:
            int: Completeness score (number of filled data fields).
        """
        score = 0
        for field in self.data_fields:
            if field in row and pd.notna(row[field]) and row[field] is not None:
                if isinstance(row[field], str) and row[field].strip() != "":
                    score += 1
                elif not isinstance(row[field], str):
                    score += 1
        return score

    def get_best_record_for_city(self, city: str) -> Optional[pd.Series]:
        """
        Get the record with the most filled data fields for a given city from the static database.
        
        Parameters:
            city (str): The name of the city to search for.
            
        Returns:
            pd.Series: The record with most complete data, or None if not found.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT * FROM static_data
                WHERE name = ?
            """
            df = pd.read_sql_query(query, conn, params=(city,))
            conn.close()

            if df.empty:
                print(f"[DEBUG] No records found for city: {city}")
                return None
                
            print(f"[DEBUG] Found {len(df)} records for {city}")
            
            # Calculate completeness score for each record
            df['completeness_score'] = df.apply(self._calculate_completeness_score, axis=1)
            
            # Sort by completeness score (descending) and then by date (most recent first)
            df_sorted = df.sort_values(['completeness_score', 'dt'], ascending=[False, False])
            
            # Get the best record info for debugging
            best_score = df_sorted.iloc[0]['completeness_score']
            total_fields = len(self.data_fields)
            
            print(f"[DEBUG] Selected record for {city} with completeness score: {best_score}/{total_fields}")
            
            # Return the best record (excluding the completeness_score column we added)
            best_record = df_sorted.iloc[0].drop('completeness_score')
            
            return best_record
            
        except Exception as e:
            print(f"Error fetching best record for {city}: {e}")
            return None

    def get_comparison_data(self, city1: str, city2: str) -> Tuple[Optional[pd.Series], Optional[pd.Series]]:
        """
        Get the best records for two cities for comparison.
        
        Parameters:
            city1 (str): First city name.
            city2 (str): Second city name.
            
        Returns:
            Tuple[pd.Series, pd.Series]: Best records for both cities, or None if not found.
        """
        try:
            print(f"[DEBUG] Fetching comparison data for {city1} vs {city2}")
            
            data1 = self.get_best_record_for_city(city1)
            data2 = self.get_best_record_for_city(city2)
            
            # Log results
            if data1 is not None and data2 is not None:
                print(f"[DEBUG] Successfully retrieved data for both cities")
            elif data1 is None:
                print(f"[DEBUG] Failed to retrieve data for {city1}")
            elif data2 is None:
                print(f"[DEBUG] Failed to retrieve data for {city2}")
            
            return data1, data2
            
        except Exception as e:
            print(f"Error fetching comparison data for {city1} and {city2}: {e}")
            return None, None

    def get_city_count(self) -> int:
        """
        Get the total number of unique cities in the database.
        
        Returns:
            int: Number of unique cities.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT COUNT(DISTINCT name) as city_count FROM static_data
                WHERE name IS NOT NULL
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return df.iloc[0]['city_count'] if not df.empty else 0
            
        except Exception as e:
            print(f"Error getting city count: {e}")
            return 0

    def get_database_stats(self) -> dict:
        """
        Get general statistics about the static database.
        
        Returns:
            dict: Dictionary containing database statistics.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Total records
            total_query = "SELECT COUNT(*) as total_records FROM static_data"
            total_df = pd.read_sql_query(total_query, conn)
            total_records = total_df.iloc[0]['total_records'] if not total_df.empty else 0
            
            # Unique cities
            cities_query = "SELECT COUNT(DISTINCT name) as unique_cities FROM static_data WHERE name IS NOT NULL"
            cities_df = pd.read_sql_query(cities_query, conn)
            unique_cities = cities_df.iloc[0]['unique_cities'] if not cities_df.empty else 0
            
            # Records with feels_like data
            feels_like_query = "SELECT COUNT(*) as feels_like_records FROM static_data WHERE feels_like IS NOT NULL"
            feels_like_df = pd.read_sql_query(feels_like_query, conn)
            feels_like_records = feels_like_df.iloc[0]['feels_like_records'] if not feels_like_df.empty else 0
            
            conn.close()
            
            stats = {
                'total_records': total_records,
                'unique_cities': unique_cities,
                'feels_like_records': feels_like_records,
                'completeness_percentage': (feels_like_records / total_records * 100) if total_records > 0 else 0
            }
            
            print(f"[DEBUG] Database stats: {stats}")
            return stats
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {
                'total_records': 0,
                'unique_cities': 0,
                'feels_like_records': 0,
                'completeness_percentage': 0
            }

    def test_connection(self) -> bool:
        """
        Test if the database connection is working.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='static_data';")
            table_exists = cursor.fetchone() is not None
            conn.close()
            
            if table_exists:
                print(f"[DEBUG] Successfully connected to database at {self.db_path}")
                return True
            else:
                print(f"[DEBUG] Database connected but 'static_data' table not found at {self.db_path}")
                return False
                
        except Exception as e:
            print(f"[DEBUG] Database connection failed: {e}")
            return False