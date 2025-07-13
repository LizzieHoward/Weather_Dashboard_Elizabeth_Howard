# Start the root GUI window
import customtkinter as ctk # CustomTkinter for modern UI
import src.API.API_call as WeatherAPI  #  API module for fetching weather data
from src.DataProcessing.data_to_SQL import WeatherDB # Data processing module for handling weather data


class WeatherDashboard(ctk.CTk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller

        # Window config
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Weather Dashboard")
        self.geometry("800x600")
        self.minsize(600, 400)  # Set minimum window size

        # Create main container frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(fill="both", expand=True, padx=20, pady=20)

        # Search section
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.grid(fill="x", padx=10, pady=10)

        self.city_label = grid.CTkLabel(self.search_frame, text="Enter City:", font=("Arial", 14))
        self.city_label.grid(side="left", padx=10)

        self.city_entry = ctk.CTkEntry(self.search_frame, width=200)
        self.city_entry.grid(side="left", padx=10)
        self.city_entry.bind("<Return>", lambda e: self.fetch_weather())

        self.fetch_button = ctk.CTkButton(self.search_frame, text="Get Weather", command=self.fetch_weather)
        self.fetch_button.grid(side="left", padx=10)

        # Loading indicator
        self.loading_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12))
        self.loading_label.grid(pady=5)

        # Results section
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.grid(fill="both", expand=True, padx=10, pady=10)

    # def kelvin_to_fahrenheit(self, kelvin):
    #     """Convert Kelvin to Fahrenheit"""
    #     try:
    #         return round(((float(kelvin) - 273.15) * 9/5 + 32), 1)
    #     except (ValueError, TypeError):
    #         return "N/A"

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
                print(f"Searching weather for: {city}")
                dummy_data = {
                    "name": city,
                    "main": {"temp": 294.65, "humidity": 50},  # Temperature in Kelvin
                    "weather": [{"description": "clear sky"}],
                    "wind": {"speed": 3.2}
                }
                self.display_weather(dummy_data)
        finally:
            # Reset loading state
            self.loading_label.configure(text="")
            self.fetch_button.configure(state="normal")

    def display_weather(self, data):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        city_name = data.get("name", "N/A")
        temp_k = data.get("main", {}).get("temp", "N/A")
        temperature = self.kelvin_to_fahrenheit(temp_k)
        humidity = data.get("main", {}).get("humidity", "N/A")
        description = data.get("weather", [{}])[0].get("description", "N/A").capitalize()
        wind_speed = data.get("wind", {}).get("speed", "N/A")

        # Create title with larger font and padding
        title = ctk.CTkLabel(
            self.result_frame,
            text=f"Weather in {city_name}",
            font=("Arial", 24, "bold")
        )
        title.grid(pady=(20, 30))

        # Create a frame for weather details
        details_frame = ctk.CTkFrame(self.result_frame)
        details_frame.grid(fill="x", padx=30, pady=10)

        self.make_row(details_frame, "Temperature", f"{temperature}°F")
        self.make_row(details_frame, "Humidity", f"{humidity}%")
        self.make_row(details_frame, "Description", description)
        self.make_row(details_frame, "Wind Speed", f"{wind_speed} m/s")

    def make_row(self, parent, label_text, value_text):
        frame = ctk.CTkFrame(parent)
        frame.grid(fill="x", pady=5)

        label = ctk.CTkLabel(
            frame, 
            text=f"{label_text}:", 
            font=("Arial", 14),
            anchor="w"
        )
        label.grid(side="left", padx=10)

        value = ctk.CTkLabel(
            frame, 
            text=value_text,
            font=("Arial", 14),
            anchor="e"
        )
        value.grid(side="right", padx=10)

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.transient(self)  # Make it transient to main window
        
        # Center the error window
        error_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - error_window.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - error_window.winfo_height()) // 2
        error_window.geometry(f"+{x}+{y}")
        
        message_label = ctk.CTkLabel(
            error_window, 
            text=message, 
            text_color="red",
            font=("Arial", 14)
        )
        message_label.grid(pady=20)
        
        # Add close button
        close_button = ctk.CTkButton(
            error_window, 
            text="OK", 
            command=error_window.destroy
        )
        close_button.grid(pady=10)
        
        # Force focus and make modal
        error_window.grab_set()
        error_window.focus_force()
