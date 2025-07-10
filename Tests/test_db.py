import unittest
import os
import sqlite3
from src.DataProcessing.data_to_SQL import WeatherDB

# class TestWeatherDB(unittest.TestCase):
#     def setUp(self):
#         self.db_path = "tests/test_weather.db"
#         self.db = WeatherDB(self.db_path)

#     def test_save(self):
#         dummy_data = {
#             "name": "TestCity",
#             "main": {"temp": 20.5, "humidity": 60},
#             "weather": [{"description": "clear sky"}],
#             "wind": {"speed": 3.4},
#             "dt": 1720000000
#         }
#         self.db.save(dummy_data)

#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute("SELECT name FROM weather WHERE name='TestCity'")
#         result = cursor.fetchone()
#         conn.close()

#         self.assertIsNotNone(result)
#         self.assertEqual(result[0], "TestCity")

#     def tearDown(self):
#         if os.path.exists(self.db_path):
#             os.remove(self.db_path)

# if __name__ == '__main__':
#     unittest.main()
