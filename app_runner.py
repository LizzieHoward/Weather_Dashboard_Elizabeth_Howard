"""
Central app runner for Weather Dashboard
This script acts as the main entry point to call all major modules (API, data processing, UI, etc.)
Add new features here as your project grows.
"""
import os
import sys

# Centralized imports
import imports

# Adjust sys.path to include src for absolute imports
SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from API.API_call import get_weather_data, api_key
from DataProcessing.data_to_SQL import save_weather_to_sqlite

# Import the main UI (if you want to launch the GUI)
import main

def fetch_and_store_weather(city):
    print(f"Fetching weather for {city}...")
    db_path = os.path.join(os.path.dirname(__file__), 'Data', 'weather_data.db')
    data = get_weather_data(city, api_key)
    save_weather_to_sqlite(data, db_path=db_path)
    print(f"Weather for {city} saved to database.")

if __name__ == "__main__":
    print("Weather Dashboard Central Runner")
    # Example: fetch and store weather for a city
    fetch_and_store_weather("Boston")
    # To launch the GUI, uncomment below:
    # main.run()
    # Add more feature calls here as you expand your project
