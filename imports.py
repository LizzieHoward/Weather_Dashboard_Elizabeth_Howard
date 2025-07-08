"""
Centralized imports for Weather Dashboard app
Import all modules, packages, and dependencies needed for the entire app here.
"""
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
import requests
import sqlite3
from dotenv import load_dotenv
import customtkinter as ctk

# Project-specific imports (relative to src)
# These will work if sys.path is set up correctly in app_runner.py
from src.API.API_call import get_weather_data, api_key
from DataProcessing.data_to_SQL import save_weather_to_sqlite

# Optionally, import main UI
import main
