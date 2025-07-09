import requests
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

def fetch_and_store_weather(city):
    print(f"Fetching weather for {city}...")
    db_path = os.path.join(os.path.dirname(__file__), 'Data', 'weather_data.db')
    data = get_weather_data(city, api_key)
    save_weather_to_sqlite(data, db_path=db_path)
    print(f"Weather for {city} saved to database.")

# --- Save to SQLite using OWM field names ---
def save_weather_to_sqlite(data, db_path="Capstone/Weather_Dashboard_Elizabeth_Howard/Data/weather_data.db"):
    """
    Save OpenWeatherMap API data to SQLite using OWM field names.
    """
    # Map OWM fields (use raw keys where possible)
    record = {
        "name": data.get("name"),                              # city name
        "temp": data["main"]["temp"],                          # temperature
        "humidity": data["main"]["humidity"],                  # humidity
        "description": data["weather"][0]["description"],      # weather description
        "speed": data["wind"]["speed"],                        # wind speed
        "dt": datetime.utcfromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S")  # observation time from OWM
    }

    # Connect to DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table using OWM field names
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

    # Insert record
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
    conn.close()
    print(f"Weather for {record['name']} saved to SQLite.")

# # --- Example usage ---
if __name__ == "__main__":
    # Set up path for new SQLite file in Data folder
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Data", "weather_data.db")
    
    # Example city
    city = "Boston"
    
    # Get weather data using API_call.py's function
    from src.API.API_call import get_weather_data, api_key
    data = get_weather_data(city, api_key)
    
    # Save to SQLite in Data folder
    save_weather_to_sqlite(data, db_path=db_path)

import sqlite3
from datetime import datetime

class WeatherDB:
    """
    Handles saving OpenWeatherMap weather data to SQLite.
    """

    def __init__(self, db_path="Data/weather_data.db"):
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
