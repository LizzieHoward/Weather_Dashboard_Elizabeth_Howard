"""This file's purpose is to retrieve the most 
recent search resuls from the database, 
check both the "feels like" and "wind speed" values against a predefined set of thresholds, then either display 
an alert or state that no alerts are active. the retrieval  should not start until the tab is clicked on by the user.
the alerts should be little buttons or labels that pop up and display the alert message within the weather alerts tab display. 

"""


"""This file's purpose is to retrieve the most 
recent search results from the database, 
check both the "feels like" and "wind speed" values against a predefined set of thresholds, then either display 
an alert or state that no alerts are active. the retrieval should not start until the tab is clicked on by the user.
the alerts should be little buttons or labels that pop up and display the alert message within the weather alerts tab display. 
"""

import customtkinter as ctk
from src.DataProcessing.data_query import fetch_last_data_entry
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Optional

class WeatherAlertsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.has_loaded_once = False  # Track if alerts have been loaded
        
        # Load temperature unit preference
        load_dotenv()
        temp_unit = os.getenv("TEMPERATURE_UNIT", "fahrenheit").lower()
        self.unit_symbol = "°F" if temp_unit == "fahrenheit" else "°C"
        self.is_fahrenheit = temp_unit == "fahrenheit"

        self.alerts_frame = ctk.CTkFrame(self)
        self.alerts_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header = ctk.CTkLabel(
            self.alerts_frame,
            text="Weather Alerts",
            font=("Segoe UI", 20, "bold")
        )
        self.header.pack(pady=(0, 10))

        self.alert_labels = []
        
        # Add a status label for loading/error states
        self.status_label = ctk.CTkLabel(
            self.alerts_frame,
            text="Select this tab to check for weather alerts",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.status_label.pack(pady=5)
        self.alert_labels.append(self.status_label)

    def on_tab_selected(self):
        """Called when this tab is clicked/selected - triggers alert refresh"""
        print("[DEBUG] Weather Alerts tab selected - refreshing alerts...")
        self.has_loaded_once = True
        self.refresh_alerts()

    def refresh_alerts(self):
        """Call this method to refresh the alerts display"""
        print("[DEBUG] Refreshing alerts...")
        self.display_alerts()

    def fetch_most_recent_entry_for_last_city(self, db_path: str = "Data/weather_data.db") -> Optional[pd.Series]:
        """
        Fetch the most recent weather entry for the last searched city from the SQLite database.
        
        Returns:
            pd.Series: The most recent row for the last searched city, or None if not found.
        """
        try:
            conn = sqlite3.connect(db_path)
            
            # First, get the most recent city that was searched
            recent_city_query = """
                SELECT name FROM weather
                ORDER BY dt DESC
                LIMIT 1
            """
            recent_city_df = pd.read_sql_query(recent_city_query, conn)
            
            if recent_city_df.empty:
                conn.close()
                return None
                
            last_city = recent_city_df.iloc[0]['name']
            print(f"[DEBUG] Last searched city: {last_city}")
            
            # Close this connection before calling fetch_last_data_entry
            conn.close()
            
            # Now get the most recent data for that city using the existing function
            data = fetch_last_data_entry(last_city, db_path)
            
            return data
            
        except Exception as e:
            print(f"Error fetching most recent data for last city: {e}")
            return None

    def display_alerts(self):
        print("[DEBUG] display_alerts() called")
        # Clear old alerts
        for label in self.alert_labels:
            label.destroy()
        self.alert_labels.clear()

        # Update status
        self.status_label = ctk.CTkLabel(
            self.alerts_frame,
            text="Loading weather data...",
            font=("Segoe UI", 12),
            text_color="blue"
        )
        self.status_label.pack(pady=5)
        self.alert_labels.append(self.status_label)
        
        # Force UI update
        self.update()

        # Get weather data from database for last searched city
        data = self.fetch_most_recent_entry_for_last_city()
        print(f"[DEBUG] Retrieved data from database: {data}")
        
        # Remove loading status
        self.status_label.destroy()
        self.alert_labels.remove(self.status_label)
        
        if data is None or data.empty:
            no_data = ctk.CTkLabel(
                self.alerts_frame,
                text="No weather data available in database. Search for a city first.",
                font=("Segoe UI", 14),
                text_color="orange"
            )
            no_data.pack(pady=10)
            self.alert_labels.append(no_data)
            return

        # Extract fields from database row (pandas Series)
        city_name = data.get("name", "Unknown")
        feels_like = data.get("feels_like")
        wind_speed = data.get("speed")  # Database uses 'speed' column
        timestamp = data.get("dt", "Unknown time")
        
        print(f"[DEBUG] Alert processing - city: {city_name}, feels_like: {feels_like}{self.unit_symbol}, wind: {wind_speed} mph, timestamp: {timestamp}")

        # Add info about the data being analyzed
        info_label = ctk.CTkLabel(
            self.alerts_frame,
            text=f"Analyzing alerts for: {city_name} (Last updated: {timestamp})",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        info_label.pack(pady=(0, 10))
        self.alert_labels.append(info_label)

        # Check if we have feels_like data
        if feels_like is None or pd.isna(feels_like):
            # Show message for data without feels_like
            limited_data_msg = ctk.CTkLabel(
                self.alerts_frame,
                text="⚠️ Limited alert data: This weather record doesn't include 'feels like' temperature.\nOnly wind alerts will be shown.",
                font=("Segoe UI", 12),
                text_color="orange"
            )
            limited_data_msg.pack(pady=10)
            self.alert_labels.append(limited_data_msg)
            
            # Only show wind alerts
            alerts_triggered = self.get_wind_alerts(wind_speed)
        else:
            # Show full alerts
            alerts_triggered = self.get_active_alerts(feels_like, wind_speed)

        print(f"[DEBUG] Alerts triggered: {alerts_triggered}")

        if not alerts_triggered:
            msg = ctk.CTkLabel(
                self.alerts_frame,
                text="✅ No active weather alerts for current conditions.",
                font=("Segoe UI", 14),
                text_color="green"
            )
            msg.pack(pady=10)
            self.alert_labels.append(msg)
        else:
            for alert in alerts_triggered:
                # Create alert button/label with more prominent styling
                alert_frame = ctk.CTkFrame(self.alerts_frame)
                alert_frame.pack(fill="x", pady=5, padx=10)
                
                alert_button = ctk.CTkLabel(
                    alert_frame,
                    text=alert,
                    text_color="white",
                    font=("Segoe UI", 14, "bold"),
                    fg_color="red",
                    corner_radius=10
                )
                alert_button.pack(fill="x", padx=10, pady=10)
                self.alert_labels.append(alert_frame)

    def get_wind_alerts(self, wind_speed):
        """Get only wind-based alerts"""
        alerts = []
        try:
            print(f"[DEBUG] Processing wind alerts - speed: {wind_speed}")
            if wind_speed is not None and not pd.isna(wind_speed):
                wind_speed = float(wind_speed)
                if wind_speed >= 30:
                    alerts.append(f"💨 High Wind Advisory: Wind speeds {wind_speed:.1f} mph (30+ mph threshold)")
                elif wind_speed >= 20:
                    alerts.append(f"💨 Wind Watch: Wind speeds {wind_speed:.1f} mph (elevated winds)")
        except (TypeError, ValueError) as e:
            print(f"[DEBUG] Error processing wind data: {e}")
            alerts.append("⚠️ Error processing wind data.")
        return alerts

    def get_active_alerts(self, feels_like, wind_speed):
        """Get full alerts including temperature-based ones"""
        alerts = []

        try:
            print(f"[DEBUG] Processing temperature alerts - feels_like: {feels_like}, is_fahrenheit: {self.is_fahrenheit}")
            
            # Process feels_like alerts
            if feels_like is not None and not pd.isna(feels_like):
                feels_like = float(feels_like)
                
                if self.is_fahrenheit:
                    # Fahrenheit thresholds
                    if feels_like >= 105:
                        alerts.append(f"🔥 Extreme Heat Warning: Feels like {feels_like:.1f}°F (105°F+ threshold)")
                    elif feels_like >= 100:
                        alerts.append(f"⚠️ Heat Advisory: Feels like {feels_like:.1f}°F (100°F+ threshold)")
                    
                    if feels_like <= 20:
                        alerts.append(f"❄️ Extreme Cold Warning: Feels like {feels_like:.1f}°F (20°F or lower)")
                    elif feels_like <= 32:
                        alerts.append(f"🥶 Wind Chill Advisory: Feels like {feels_like:.1f}°F (32°F or lower)")
                else:
                    # Celsius thresholds
                    if feels_like >= 40.6:  # 105°F
                        alerts.append(f"🔥 Extreme Heat Warning: Feels like {feels_like:.1f}°C (40.6°C+ threshold)")
                    elif feels_like >= 37.8:  # 100°F
                        alerts.append(f"⚠️ Heat Advisory: Feels like {feels_like:.1f}°C (37.8°C+ threshold)")
                    
                    if feels_like <= -6.7:  # 20°F
                        alerts.append(f"❄️ Extreme Cold Warning: Feels like {feels_like:.1f}°C (-6.7°C or lower)")
                    elif feels_like <= 0:  # 32°F
                        alerts.append(f"🥶 Wind Chill Advisory: Feels like {feels_like:.1f}°C (0°C or lower)")
            
            # Add wind alerts
            wind_alerts = self.get_wind_alerts(wind_speed)
            alerts.extend(wind_alerts)
            
        except (TypeError, ValueError) as e:
            print(f"[DEBUG] Error processing alert data: {e}")
            alerts.append("⚠️ Error processing alert data.")

        return alerts