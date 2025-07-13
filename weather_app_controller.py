"""
Central app runner for Weather Dashboard
"""
import os
import sys

# Adjust sys.path to include src for absolute imports
SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from src.API.API_call import WeatherAPI
from src.DataProcessing.data_to_SQL import WeatherDB
from src.GUI.weather_dashboard_2 import WeatherDashboard
from src.ErrorHandling.error_handling_entry import CityNameHandler

class WeatherAppController:
    """
    Central controller for the Weather Dashboard app.
    This class handles fetching weather data and updating the GUI.
    """
    def __init__(self):
        print("Welcome to the Weather Dashboard!")
        self.db = WeatherDB()
        self.gui = WeatherDashboard(controller=self)
        self.api = WeatherAPI()  # Use the new class
        print("here?")
        
    def fetch_and_store_weather(self, city):
        # Normalize and validate city name
        norm_city = CityNameHandler.normalize_city_name(city)
        if not CityNameHandler.validate_city_name(norm_city):
            print(f"Invalid city name: {city}")
            return None
        print(f"Fetching weather for {norm_city}...")
        data = self.api.get_weather_data(norm_city)
        print("test 45")
        if data and "main" in data and "weather" in data:
            self.db.save(data)
            print(f"Weather for {norm_city} saved to database.")
            return data
        else:
            print(f"Failed to fetch weather data for {norm_city}.")
            return None

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    app_controller = WeatherAppController()
    app_controller.run()
