import requests
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

class WeatherDB:
    def __init__(self, db_path="Weather_Dashboard_Elizabeth_Howard/Data/weather_data.db"):
        self.db_path = db_path

    # --- Save to SQLite using OWM field names ---
    def save_weather_to_sqlite(self, data):
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
        conn = sqlite3.connect(self.db_path)
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
