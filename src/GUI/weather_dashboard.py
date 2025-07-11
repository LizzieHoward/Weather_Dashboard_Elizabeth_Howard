# # Start the root GUI window
# import customtkinter as ctk # CustomTkinter for modern UI
# src/GUI/weather_dashboard.py
import customtkinter as ctk
from weather_basic_stats_frame import WeatherInfoFrame
#from stat_graph_frame import GraphFrame
from glass_frame import GlassFrame

class WeatherDashboard(ctk.CTk):
    """
    Standalone View class for the Weather Dashboard.
    Renders the GUI and calls the controller to fetch & display data.
    """

    def __init__(self, controller):
        super().__init__()

        self.controller = controller  # The controller provides business logic

        # Window config
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Weather Dashboard")
        self.geometry("800x600")

        self._build_widgets()

    def _build_widgets(self):
        """Create and place widgets"""
        self.city_label = ctk.CTkLabel(self, text="Enter City:", font=("Arial", 14))
        self.city_label.pack(pady=10)

        self.city_entry = ctk.CTkEntry(self, width=200)
        self.city_entry.pack(pady=5)

        self.fetch_button = ctk.CTkButton(
            self, text="Get Weather", command=self.fetch_weather
        )
        self.fetch_button.pack(pady=10)

        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def fetch_weather(self):
        """Handle button click to fetch weather"""
        city = self.city_entry.get().strip()
        if not city:
            self.show_error("Please enter a city name.")
            return

        try:
            data = self.controller.fetch_and_store_weather(city)
            self.display_weather(data)
        except Exception as e:
            self.show_error(f"Error: {e}")

    def display_weather(self, data):
        """Render weather data in the result frame"""
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        city_name = data.get("name", "Unknown")
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()
        wind_speed = data["wind"]["speed"]

        ctk.CTkLabel(
            self.result_frame, text=f"Weather in {city_name}", font=("Arial", 16, "bold")
        ).pack(pady=10)

        self._make_row("Temperature (°F)", temperature)
        self._make_row("Humidity (%)", humidity)
        self._make_row("Description", description)
        self._make_row("Wind Speed (m/s)", wind_speed)

    def _make_row(self, label_text, value_text):
        frame = ctk.CTkFrame(self.result_frame)
        frame.grid(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=f"{label_text}:", anchor="w")
        label.grid(side="left", padx=5)

        value = ctk.CTkLabel(frame, text=str(value_text), anchor="e")
        value.grid(side="right", padx=5)

    def show_error(self, message):
        """Show an error in a popup"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x100")
        ctk.CTkLabel(error_window, text=message, text_color="red").pack(pady=20)

# class WeatherDashboard(ctk.CTk):
#     def __init__(self, controller=None):
#         super().__init__()
#         self.controller = controller  # Allow passing a controller for separation of concerns

#         # Window config
#         ctk.set_appearance_mode("System")
#         ctk.set_default_color_theme("blue")
#         self.title("Weather Dashboard")
#         self.geometry("800x600")

#         # Widgets
#         self.city_label = ctk.CTkLabel(self, text="Enter City:", font=("Arial", 14))
#         self.city_label.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

#         self.city_entry = ctk.CTkEntry(self, width=200)
#         self.city_entry.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

#         self.fetch_button = ctk.CTkButton(self, text="Get Weather", command=self.fetch_weather)
#         self.fetch_button.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

#         self.result_frame = ctk.CTkFrame(self)
#         self.result_frame.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")

#         # Make the rows/cols expand nicely
#         self.grid_rowconfigure(3, weight=1)
#         self.grid_columnconfigure(0, weight=1)

#     def fetch_weather(self):
#         city = self.city_entry.get().strip()
#         if not city:
#             self.show_error("Please enter a city name.")
#             return

#         if self.controller:
#             # Use controller to fetch real data
#             data = self.controller.fetch_and_store_weather(city)
#             if data:
        #         self.display_weather(data)
        #     else:
        #         self.show_error(f"Could not fetch weather for {city}.")
        # else:
        #     # Fallback: dummy data for standalone testing
    #         print(f"Searching weather for: {city}")
    #         dummy_data = {
    #             "name": city,
    #             "main": {"temp": 21.5, "humidity": 50},
    #             "weather": [{"description": "clear sky"}],
    #             "wind": {"speed": 3.2}
    #         }
    #         self.display_weather(dummy_data)

    # def display_weather(self, data):
    #     for widget in self.result_frame.winfo_children():
    #         widget.destroy()

    #     city_name = data.get("name", "N/A")
    #     temperature = data.get("main", {}).get("temp", "N/A")
    #     humidity = data.get("main", {}).get("humidity", "N/A")
    #     description = data.get("weather", [{}])[0].get("description", "N/A").capitalize()
    #     wind_speed = data.get("wind", {}).get("speed", "N/A")

    #     ctk.CTkLabel(
    #         self.result_frame,
    #         text=f"Weather in {city_name}",
    #         font=("Arial", 16, "bold")
    #     ).grid(pady=10)

    #     self.make_row("Temperature (°F)", temperature)
    #     self.make_row("Humidity ", humidity, "%")
    #     self.make_row("Description", description)
    #     self.make_row("Wind Speed (m/s)", wind_speed)

    # def make_row(self, label_text, value_text, unit=None):
    #     frame = ctk.CTkFrame(self.result_frame)
    #     frame.grid(pady=5, padx=10, fill="x")

    #     label = ctk.CTkLabel(frame, text=label_text + ":", anchor="w")
    #     label.grid(side="left", padx=5)

    #     display_text = f"{value_text} {unit}" if unit else str(value_text)
    #     value = ctk.CTkLabel(frame, text=display_text, anchor="e")
    #     value.grid(side="right", padx=5)

    # def show_error(self, message):
    #     error_window = ctk.CTkToplevel(self)
    #     error_window.title("Error")
    #     error_window.geometry("300x100")
    #     ctk.CTkLabel(error_window, text=message, text_color="red").pack(pady=20)
