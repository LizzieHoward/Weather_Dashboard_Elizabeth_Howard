import requests
import os

from dotenv import load_dotenv



# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

def get_weather_data(city, api_key):
    """
    Fetches weather data for a given city using the OpenWeatherMap API.

    Parameters:
    city (str): The name of the city to fetch weather data for.
    api_key (str): Your OpenWeatherMap API key.

    Returns:
    dict: A dictionary containing the weather data for the specified city.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
 
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()  # Raise HTTPError for bad responses


