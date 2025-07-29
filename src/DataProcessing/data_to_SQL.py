import requests
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

class WeatherDB:
    def __init__(self, db_path=None):
        if db_path is None:
            # Automatically find the Data folder
            project_root = Path(__file__).parent.parent.parent  # Go up from src/DataProcessing/
            data_folder = project_root / "Data"
            data_folder.mkdir(exist_ok=True)  # Create Data folder if it doesn't exist
            self.db_path = str(data_folder / "weather_data.db")
        else:
            self.db_path = db_path
            
        self._ensure_database_exists()
        print(f"[INFO] Using database at: {os.path.abspath(self.db_path)}")

    def _ensure_database_exists(self):
        """Create the database and table if they don't exist, handle migration"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if table exists and get its current structure
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather'")
            table_exists = cursor.fetchone() is not None
            
            if table_exists:
                # Get current column info
                cursor.execute("PRAGMA table_info(weather)")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"[DEBUG] Current table columns: {columns}")
                
                # Check if we need to migrate to new column order
                expected_order = ['id', 'name', 'temp', 'feels_like', 'humidity', 'description', 'speed', 'dt']
                
                if columns != expected_order:
                    print("[INFO] Migrating database to new column order...")
                    self._migrate_table_structure(cursor)
                else:
                    print("[INFO] Database structure is already up to date")
            else:
                # Create new table with correct structure
                print("[INFO] Creating new weather table with OpenWeatherMap field order...")
                cursor.execute("""
                    CREATE TABLE weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        temp REAL,
                        feels_like REAL,
                        humidity INTEGER,
                        description TEXT,
                        speed REAL,
                        dt TEXT
                    )
                """)
            
            conn.commit()
            conn.close()
            print(f"[INFO] Database initialized successfully")
        except Exception as e:
            print(f"[ERROR] Failed to initialize database: {e}")
            raise

    def _migrate_table_structure(self, cursor):
        """Migrate existing table to new column order"""
        try:
            # Create new table with correct structure
            cursor.execute("""
                CREATE TABLE weather_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    temp REAL,
                    feels_like REAL,
                    humidity INTEGER,
                    description TEXT,
                    speed REAL,
                    dt TEXT
                )
            """)
            
            # Copy data from old table to new table
            # Handle the case where feels_like might not exist in old table
            cursor.execute("PRAGMA table_info(weather)")
            old_columns = [row[1] for row in cursor.fetchall()]
            
            if 'feels_like' in old_columns:
                # Old table has feels_like, copy all data
                cursor.execute("""
                    INSERT INTO weather_new (id, name, temp, feels_like, humidity, description, speed, dt)
                    SELECT id, name, temp, feels_like, humidity, description, speed, dt
                    FROM weather
                """)
            else:
                # Old table doesn't have feels_like, set it to NULL
                cursor.execute("""
                    INSERT INTO weather_new (id, name, temp, feels_like, humidity, description, speed, dt)
                    SELECT id, name, temp, NULL, humidity, description, speed, dt
                    FROM weather
                """)
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE weather")
            cursor.execute("ALTER TABLE weather_new RENAME TO weather")
            
            print("[INFO] Database migration completed successfully")
            
        except Exception as e:
            print(f"[ERROR] Database migration failed: {e}")
            # If migration fails, try to clean up
            cursor.execute("DROP TABLE IF EXISTS weather_new")
            raise

    def save_weather_to_sqlite(self, data):
        """
        Save OpenWeatherMap API data to SQLite following OpenWeatherMap field order.
        """
        # Map OWM fields in OpenWeatherMap order
        record = {
            "name": data.get("name"),                              # city name
            "temp": data["main"]["temp"],                          # temperature
            "feels_like": data["main"].get("feels_like"),          # feels like temperature
            "humidity": data["main"]["humidity"],                  # humidity
            "description": data["weather"][0]["description"],      # weather description
            "speed": data["wind"]["speed"],                        # wind speed
            "dt": datetime.utcfromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S")  # observation time from OWM
        }

        try:
            # Connect to DB
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Verify table structure before inserting
            cursor.execute("PRAGMA table_info(weather)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"[DEBUG] Table structure before insert: {columns}")

            # Insert record following OpenWeatherMap field order
            cursor.execute("""
                INSERT INTO weather (name, temp, feels_like, humidity, description, speed, dt)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                record["name"],
                record["temp"],
                record["feels_like"],
                record["humidity"],
                record["description"],
                record["speed"],
                record["dt"]
            ))

            conn.commit()
            conn.close()
            print(f"Weather for {record['name']} saved to SQLite.")
        except Exception as e:
            print(f"[ERROR] Failed to save weather data: {e}")
            print(f"[DEBUG] Record data: {record}")
            raise

    def save(self, data):
        """Alias for save_weather_to_sqlite for convenience"""
        return self.save_weather_to_sqlite(data)