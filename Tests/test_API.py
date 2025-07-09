import unittest
from src.API.API_call import WeatherAPI
import os
from dotenv import load_dotenv

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        load_dotenv("Capstone/Weather_Dashboard_Elizabeth_Howard/src/API/API_key.env")
        api_key = os.getenv("OPENWEATHER_API_KEY")
        self.api = WeatherAPI(api_key)

    def test_get_weather_data(self):
        data = self.api.get_weather_data("Boston")
        self.assertIn("main", data)
        self.assertIn("weather", data)
        self.assertEqual(data["name"], "Boston")

if __name__ == '__main__':
    unittest.main()
