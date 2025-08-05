import customtkinter as ctk
import os
from dotenv import load_dotenv

class WeatherDashboardTab(ctk.CTkFrame): 
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # Load temperature unit preference
        load_dotenv()
        temp_unit = os.getenv("TEMPERATURE_UNIT", "fahrenheit").lower()
        self.unit_symbol = "°F" if temp_unit == "fahrenheit" else "°C"

        # Welcome message
        welcome_label = ctk.CTkLabel(
            self,
            text="Welcome to WeatherFirst!",
            font=("Segoe UI", 20, "bold")
        )
        welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create main container frame for this tab
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Create right-side icons panel (placeholder for now)
        self.icons_frame = ctk.CTkFrame(self, width=100)
        self.icons_frame.grid(row=1, column=1, sticky="ns", padx=10, pady=20)

        # Search section
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.city_label = ctk.CTkLabel(self.search_frame, text="Enter City:", font=("Segoe UI", 14))
        self.city_label.grid(row=0, column=0, padx=10)

        self.city_entry = ctk.CTkEntry(self.search_frame, width=200)
        self.city_entry.grid(row=0, column=1, padx=10)
        self.city_entry.bind("<Return>", lambda e: self.fetch_weather())

        self.fetch_button = ctk.CTkButton(self.search_frame, text="Get Weather", command=self.fetch_weather)
        self.fetch_button.grid(row=0, column=2, padx=10)

        # Loading indicator
        self.loading_label = ctk.CTkLabel(self.main_frame, text="", font=("Segoe UI", 12))
        self.loading_label.grid(row=1, column=0, pady=5)

        # Results section
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Configure row/column weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def fetch_weather(self):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        city = self.city_entry.get().strip()
        if not city:
            self.show_error("Please enter a city name.")
            return

        # Show loading state
        self.loading_label.configure(text="Fetching weather data...")
        self.fetch_button.configure(state="disabled")
        self.update()

        try:
            if self.controller:
                data = self.controller.fetch_and_store_weather(city)
                if data:
                    self.display_weather(data)
                else:
                    self.show_error(f"Could not fetch weather for {city}.")
            else:
                # Fallback dummy data in OpenWeatherMap field order
                dummy_data = {
                    "name": city,
                    "main": {
                        "temp": 30, 
                        "feels_like": 32,
                        "humidity": 50
                    },
                    "weather": [{"description": "clear sky"}],
                    "wind": {"speed": 3.2}
                }
                self.display_weather(dummy_data)
        finally:
            self.loading_label.configure(text="")
            self.fetch_button.configure(state="normal")

    def display_weather(self, data):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Extract fields in OpenWeatherMap order
        city_name = data.get("name", "N/A")
        temperature = data.get("main", {}).get("temp", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        description = data.get("weather", [{}])[0].get("description", "N/A").capitalize()
        wind_speed = data.get("wind", {}).get("speed", "N/A")
        
        # Get unit symbol from API response or use default
        unit_symbol = data.get('_unit_info', {}).get('symbol', self.unit_symbol)

        title = ctk.CTkLabel(
            self.result_frame,
            text=f"Weather in {city_name}",
            font=("Segoe UI", 24, "bold")
        )
        title.grid(pady=(20, 30))

        details_frame = ctk.CTkFrame(self.result_frame)
        details_frame.grid(padx=30, pady=10)

        # Display fields in OpenWeatherMap order
        self.make_row(details_frame, "Temperature", f"{temperature}{unit_symbol}")
        if feels_like != "N/A" and feels_like is not None:
            self.make_row(details_frame, "Feels Like", f"{feels_like}{unit_symbol}")
        self.make_row(details_frame, "Humidity", f"{humidity}%")
        self.make_row(details_frame, "Description", description)
        wind_unit = "mph" if unit_symbol == "°F" else "m/s"
        self.make_row(details_frame, "Wind Speed", f"{wind_speed} {wind_unit}")

    def make_row(self, parent, label_text, value_text):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)

        label = ctk.CTkLabel(frame, text=f"{label_text}:", font=("Segoe UI", 14), anchor="w")
        label.pack(side="left", padx=10)

        value = ctk.CTkLabel(frame, text=value_text, font=("Segoe UI", 14), anchor="e")
        value.pack(side="right", padx=10)

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.transient(self)

        # Center error window
        error_window.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - error_window.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - error_window.winfo_height()) // 2
        error_window.geometry(f"+{x}+{y}")

        message_label = ctk.CTkLabel(
            error_window,
            text=message,
            text_color="red",
            font=("Segoe UI", 14)
        )
        message_label.grid(pady=20)

        close_button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        close_button.grid(pady=10)

        error_window.grab_set()
        error_window.focus_force()

    def on_tab_changed(self):
        current_tab = self.tabview.get()
        if current_tab == "Cities Comparison":
            self.comparison_tab.on_tab_selected()