# src/GUI/weather_info_frame.py

import customtkinter as ctk


class WeatherInfoFrame(ctk.CTkFrame):
    """
    Frame displaying the weather information in a compact format.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title_label = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"))
        self.title_label.grid(pady=10)

        self.rows = []  # store row frames so we can update later

    def display_weather(self, data):
        # Clear any previous rows
        for row in self.rows:
            row.destroy()
        self.rows.clear()

        city_name = data.get("name", "Unknown")
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()
        wind_speed = data["wind"]["speed"]

        self.title_label.configure(text=f"Weather in {city_name}")

        self._make_row("Temperature (°F)", temperature)
        self._make_row("Humidity (%)", humidity)
        self._make_row("Description", description)
        self._make_row("Wind Speed (m/s)", wind_speed)

    def _make_row(self, label_text, value_text):
        frame = ctk.CTkFrame(self)
        frame.grid(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=f"{label_text}:", anchor="w")
        label.grid(side="left", padx=5)

        value = ctk.CTkLabel(frame, text=str(value_text), anchor="e")
        value.grid(side="right", padx=5)

        self.rows.append(frame)
