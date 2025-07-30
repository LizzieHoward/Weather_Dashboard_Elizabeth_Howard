import customtkinter as ctk
from src.DataProcessing.data_query import fetch_last_data_entry
import os
from dotenv import load_dotenv
from typing import Optional

class WeatherAlertsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
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
            font=("Arial", 20, "bold")
        )
        self.header.pack(pady=(0, 10))

        self.alert_labels = []

    def refresh_alerts(self):
        """Call this method to refresh the alerts display"""
        print("[DEBUG] Refreshing alerts...")
        self.display_alerts()

    def display_alerts(self):
        print("[DEBUG] display_alerts() called")
        # Clear old alerts
        for label in self.alert_labels:
            label.destroy()
        self.alert_labels.clear()

        if not self.controller:
            print("[DEBUG] No controller available")
            no_controller = ctk.CTkLabel(
                self.alerts_frame,
                text="No controller available.",
                font=("Arial", 14)
            )
            no_controller.pack(pady=10)
            self.alert_labels.append(no_controller)
            return

        # Get weather data
        data = self.controller.get_last_weather_data()
        print(f"[DEBUG] Retrieved data: {data}")
        
        if not data:
            no_data = ctk.CTkLabel(
                self.alerts_frame,
                text="No weather data available. Search for a city first.",
                font=("Arial", 14)
            )
            no_data.pack(pady=10)
            self.alert_labels.append(no_data)
            return

        # Extract fields
        city_name = data.get("name", "Unknown")
        feels_like = data.get("main", {}).get("feels_like")
        wind_speed = data.get("wind", {}).get("speed")
        has_feels_like = data.get("has_feels_like", feels_like is not None)
        
        print(f"[DEBUG] Alert processing - city: {city_name}, feels_like: {feels_like}{self.unit_symbol}, wind: {wind_speed}, has_feels_like: {has_feels_like}, is_fahrenheit: {self.is_fahrenheit}")

        if not has_feels_like:
            # Show message for old data without feels_like
            old_data_msg = ctk.CTkLabel(
                self.alerts_frame,
                text="⚠️ Limited alert data: This weather record doesn't include 'feels like' temperature.\nPlease search for updated weather data to get full alerts.",
                font=("Arial", 12),
                text_color="orange"
            )
            old_data_msg.pack(pady=10)
            self.alert_labels.append(old_data_msg)
            
            # Only show wind alerts for old data
            alerts_triggered = self.get_wind_alerts(wind_speed)
        else:
            # Show full alerts for new data
            alerts_triggered = self.get_active_alerts(feels_like, wind_speed)

        print(f"[DEBUG] Alerts triggered: {alerts_triggered}")

        if not alerts_triggered:
            msg = ctk.CTkLabel(
                self.alerts_frame,
                text="No active alerts." if has_feels_like else "No wind alerts active.",
                font=("Arial", 14)
            )
            msg.pack(pady=10)
            self.alert_labels.append(msg)
        else:
            for alert in alerts_triggered:
                label = ctk.CTkLabel(
                    self.alerts_frame,
                    text=alert,
                    text_color="red",
                    font=("Arial", 16, "bold"),
                    anchor="w"
                )
                label.pack(fill="x", pady=5)
                self.alert_labels.append(label)

    def get_wind_alerts(self, wind_speed):
        """Get only wind-based alerts for old data"""
        alerts = []
        try:
            print(f"[DEBUG] Processing wind alerts - speed: {wind_speed}")
            if wind_speed is not None and wind_speed >= 30:
                alerts.append("💨 High Wind Advisory: Wind speeds 30+ mph.")
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
            if feels_like is not None:
                if self.is_fahrenheit:
                    # Fahrenheit thresholds
                    if feels_like >= 105:
                        alerts.append("🔥 Extreme Heat Warning: Feels like 105°F or higher.")
                    elif feels_like >= 100:
                        alerts.append("⚠️ Heat Advisory: Feels like 100°F or higher.")
                    
                    if feels_like <= 20:
                        alerts.append("❄️ Extreme Cold Warning: Feels like 20°F or lower.")
                    elif feels_like <= 32:
                        alerts.append("🥶 Wind Chill Advisory: Feels like 32°F or lower.")
                else:
                    # Celsius thresholds
                    if feels_like >= 40.6:  # 105°F
                        alerts.append("🔥 Extreme Heat Warning: Feels like 40.6°C or higher.")
                    elif feels_like >= 37.8:  # 100°F
                        alerts.append("⚠️ Heat Advisory: Feels like 37.8°C or higher.")
                    
                    if feels_like <= -6.7:  # 20°F
                        alerts.append("❄️ Extreme Cold Warning: Feels like -6.7°C or lower.")
                    elif feels_like <= 0:  # 32°F
                        alerts.append("🥶 Wind Chill Advisory: Feels like 0°C or lower.")
            
            # Add wind alerts
            wind_alerts = self.get_wind_alerts(wind_speed)
            alerts.extend(wind_alerts)
            
        except (TypeError, ValueError) as e:
            print(f"[DEBUG] Error processing alert data: {e}")
            alerts.append("⚠️ Error processing alert data.")

        return alerts