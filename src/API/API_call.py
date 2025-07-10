"""
OpenWeatherMap API Handler
This module provides a complete interface to the OpenWeatherMap API,
with environment variable management and error handling.
"""

import os
import requests
from typing import Dict, Optional, Any
from dotenv import load_dotenv
import json
from pathlib import Path

class WeatherAPI:
    """Handles all OpenWeatherMap API interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the WeatherAPI with optional API key.
        If no key is provided, loads from environment variables.
        """
        # Load environment variables
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(env_path)
        
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("No API key provided. Set OPENWEATHER_API_KEY in .env file or pass to constructor.")
        
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        print(f"[INFO] WeatherAPI initialized. Using API key: {self.api_key[:5]}...")

    def get_weather_data(self, city: str) -> Dict[str, Any]:
        """
        Fetch weather data for a given city.
        
        Args:
            city (str): Name of the city to get weather for
            
        Returns:
            dict: Weather data from OpenWeatherMap
            
        Raises:
            requests.exceptions.HTTPError: If the API request fails
            ValueError: If city is empty or invalid
        """
        if not city:
            raise ValueError("City name cannot be empty")

        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            print(f"[INFO] Requesting weather data for {city}...")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            print(f"[SUCCESS] Retrieved weather data for {city}")
            return data
            
        except requests.exceptions.HTTPError as http_err:
            print(f"[ERROR] HTTP error occurred: {http_err}")
            if response.status_code == 401:
                print("[ERROR] Check if your API key is valid and activated")
            elif response.status_code == 404:
                print(f"[ERROR] City '{city}' not found")
            raise
            
        except Exception as err:
            print(f"[ERROR] An error occurred: {err}")
            raise

    def save_to_file(self, data: Dict[str, Any], filename: str = "weather_data.json") -> None:
        """Save weather data to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"[INFO] Weather data saved to {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to save data: {e}")

def main():
    """Example usage of the WeatherAPI class"""
    try:
        # Create API instance
        weather_api = WeatherAPI()
        
        # Example cities
        cities = ["London", "New York", "Tokyo"]
        
        # Fetch and save weather data for each city
        for city in cities:
            try:
                data = weather_api.get_weather_data(city)
                print(f"\nWeather in {city}:")
                print(f"Temperature: {data['main']['temp']}°C")
                print(f"Humidity: {data['main']['humidity']}%")
                print(f"Conditions: {data['weather'][0]['description']}")
                
                # Save to file
                weather_api.save_to_file(data, f"{city.lower()}_weather.json")
                
            except Exception as e:
                print(f"[ERROR] Failed to process {city}: {e}")
                continue
                
    except Exception as e:
        print(f"[ERROR] Application error: {e}")

if __name__ == "__main__":
    main()