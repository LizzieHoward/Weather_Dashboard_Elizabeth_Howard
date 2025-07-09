# Write the Data to SQLite database
# Save the OpenWeatherMap weather data to SQLite database
import sqlite3
from datetime import datetime
import os

class WeatherDB:
    """
    Handles saving OpenWeatherMap weather data to SQLite.
    """

    def __init__(self, db_path=os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'weather_data.db')):
        self.db_path = db_path
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    temp REAL,
                    humidity INTEGER,
                    description TEXT,
                    speed REAL,
                    dt TEXT
                )
            """)
            conn.commit()

    def save(self, data: dict):
        """
        Save one weather data record into the database.
        """
        record = {
            "name": data.get("name"),
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "speed": data["wind"]["speed"],
            "dt": datetime.utcfromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S")
        }

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO weather (name, temp, humidity, description, speed, dt)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record["name"],
                record["temp"],
                record["humidity"],
                record["description"],
                record["speed"],
                record["dt"]
            ))
            conn.commit()

        print(f"Weather for {record['name']} saved to SQLite.")
