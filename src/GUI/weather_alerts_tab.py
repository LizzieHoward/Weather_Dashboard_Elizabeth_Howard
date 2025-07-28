import customtkinter as ctk
from src.DataProcessing.data_query import fetch_last_data_entry
import os
from typing import Optional

#this file defines the WeatherAlertsTab class, which displays weather alerts based on the most recent weather data


class WeatherAlertsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        self.alerts_frame = ctk.CTkFrame(self)
        self.alerts_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header = ctk.CTkLabel(
            self.alerts_frame,
            text="Weather Alerts",
            font=("Arial", 20, "bold")
        )
        self.header.pack(pady=(0, 10))

        self.alert_labels = []

        #self.display_alerts()

    def display_alerts(self):
        # Clear old alerts
        for label in self.alert_labels:
            label.destroy()
        self.alert_labels.clear()

        if not self.controller:
            return

        # Now controller.get_last_weather_data() uses the dashboard tab's city_entry
        data = self.controller.get_last_weather_data()
        if not data:
            no_data = ctk.CTkLabel(
                self.alerts_frame,
                text="No weather data available.",
                font=("Arial", 14)
            )
            no_data.pack(pady=10)
            self.alert_labels.append(no_data)
            return

        feels_like = data.get("main", {}).get("feels_like")
        wind_speed = data.get("wind", {}).get("speed")

        alerts_triggered = self.get_active_alerts(feels_like, wind_speed)

        if not alerts_triggered:
            msg = ctk.CTkLabel(
                self.alerts_frame,
                text="No active alerts.",
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

    def get_active_alerts(self, feels_like, wind_speed):
        alerts = []

        try:
            if feels_like is not None:
                if feels_like >= 105:
                    alerts.append("⚠️ Heat Advisory: Feels like 105°F or higher.")
                if feels_like >= 100:
                    alerts.append("🔥 Excessive Heat Warning: Feels like 100°F or higher.")
                if feels_like <= 32:
                    alerts.append("🥶 Wind Chill Advisory: Feels like 32°F or lower.")
                if feels_like <= 20:
                    alerts.append("❄️ Extreme Cold Warning: Feels like 20°F or lower.")
            if wind_speed is not None and wind_speed >= 30:
                alerts.append("💨 High Wind Advisory: Wind speeds 30+ mph.")
        except TypeError:
            alerts.append("⚠️ Error processing alert data.")

        return alerts
