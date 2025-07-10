"""
Weather Dashboard Application Entry Point
Run this file to start the Weather Dashboard application.
"""

from weather_app_controller import WeatherAppController

if __name__ == "__main__":
    print("Starting Weather Dashboard Application...")
    try:
        app = WeatherAppController()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")  # Keeps terminal window open on error
