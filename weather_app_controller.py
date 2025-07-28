# """
# Central app runner for Weather Dashboard
# """
# import os
# import sys

# # Adjust sys.path to include src for absolute imports
# SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
# if SRC_PATH not in sys.path:
#     sys.path.append(SRC_PATH)

# from DataProcessing.data_query import fetch_last_data_entry
# from src.API.API_call import WeatherAPI
# from src.DataProcessing.data_to_SQL import WeatherDB
# from src.GUI.root_window import RootWindow  # Updated to use full path
# from src.ErrorHandling.error_handling_entry import CityNameHandler

# class WeatherAppController:
#     """
#     Central controller for the Weather Dashboard app.
#     This class handles fetching weather data and updating the GUI.
#     """
#     def __init__(self):
#         print("Welcome to the Weather Dashboard!")
#         self.db = WeatherDB()
#         self.gui = RootWindow(controller=self)
#         self.api = WeatherAPI()  # Use the new class
#         # self.cached_weather_data = None
#         print("here?")
        
#     def fetch_and_store_weather(self, city):
#         # Normalize and validate city name
#         norm_city = CityNameHandler.normalize_city_name(city)
#         if not CityNameHandler.validate_city_name(norm_city):
#             print(f"Invalid city name: {city}")
#             return None
#         print(f"Fetching weather for {norm_city}...")
#         data = self.api.get_weather_data(norm_city)
#         print("test 45")
#         if data and "main" in data and "weather" in data:
#             self.db.save(data)
#             print(f"Weather for {norm_city} saved to database.")
#             return data
#         else:
#             print(f"Failed to fetch weather data for {norm_city}.")
#             return None

#     def get_last_weather_data(self):
#         return fetch_last_data_entry()

#     def run(self):
#         self.gui.mainloop()

# if __name__ == "__main__":
#     app_controller = WeatherAppController()
#     app_controller.run()


"""
Central app runner for Weather Dashboard
"""

import os
import sys

# ✅ 1. Add src to sys.path for consistent imports when run from root
SRC_PATH = os.path.join(os.path.dirname(__file__), 'src')
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

# ✅ 2. Local imports (after sys.path adjustment)
from DataProcessing.data_query import fetch_last_data_entry
from src.API.API_call import WeatherAPI
from src.DataProcessing.data_to_SQL import WeatherDB
from src.GUI.root_window import RootWindow
from src.ErrorHandling.error_handling_entry import CityNameHandler


class WeatherAppController:
    """
    Central controller for the Weather Dashboard app.
    This class handles fetching weather data and updating the GUI.
    """

    def __init__(self):
        print("Welcome to the Weather Dashboard!")

        # Instantiate dependencies
        self.db = WeatherDB()
        self.api = WeatherAPI()
        self.gui = RootWindow(controller=self)
        self.alerts_tab = None  # set by RootWindow after initialization
        print("Controller initialized successfully.")

    

    def fetch_and_store_weather(self, city):
        """
        Normalize, validate, fetch, and store weather data for the given city.
        """
        norm_city = CityNameHandler.normalize_city_name(city)

        if not CityNameHandler.validate_city_name(norm_city):
            print(f"Invalid city name: {city}")
            return None

        print(f"Fetching weather for {norm_city}...")

        data = self.api.get_weather_data(norm_city)

        if data and "main" in data and "weather" in data:
            self.db.save(data)
            print(f"Weather for {norm_city} saved to database.")
            
            # Updates alerts tab after fetching new data from the API call
            if self.alerts_tab:
                self.alerts_tab.display_alerts()
            return data
        
        else:
            print(f"Failed to fetch weather data for {norm_city}.")
            return None

    def get_last_weather_data(self):
        """
        Return the most recent weather data entry from the database.
        """
        city = ""
        if hasattr(self, "dashboard_tab") and hasattr(self.dashboard_tab, "city_entry"):
            city = self.dashboard_tab.city_entry.get().strip()
        if not city:
            city = "Charleston"  # fallback default if empty
        return fetch_last_data_entry(city)

    def run(self):
        """
        Start the GUI loop.
        """
        self.gui.mainloop()


# ✅ 3. Only launch the app when this file is run directly
if __name__ == "__main__":
    app_controller = WeatherAppController()
    app_controller.run()
