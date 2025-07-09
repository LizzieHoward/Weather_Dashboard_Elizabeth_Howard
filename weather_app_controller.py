"""
Central app runner for Weather Dashboard
This script acts as the main entry point to call all major modules (API, data processing, UI, etc.)
Add new features here as your project grows.
"""
import os
import sys

# Adjust sys.path to include src for absolute imports
SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.API.API_call import get_weather_data, api_key
from src.DataProcessing.data_to_SQL import WeatherDB
from src.GUI.weather_dashboard import WeatherDashboard

if __name__ == "__main__":
    print("Weather Dashboard App Starting...")
    app = WeatherDashboard()
    app.mainloop()

if __name__ == "__main__":
    print("Weather Dashboard Central Runner")
    # Example: fetch and store weather for a city
    fetch_and_store_weather()
    # To launch the GUI, uncomment below:
    main.run()
    # Add more feature calls here as you expand your project
