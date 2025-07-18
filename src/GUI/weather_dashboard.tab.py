# imports


# import tabs

# create root frame

# create notebook

# Display "welcome to Weather Dashboard" message

# create widgets
# -text input box for city name
# -button to fetch weather data
# -search box pulling in API call data
# which goes to the stats display 
# simple stats display
# - temp, humidity, description, wind speed

# -along the right hand side will be the icons for each tab 

# weather_dashboard_tab.py

import customtkinter as ctk  # CustomTkinter for modern UI
import tabs  # assuming you have a tabs package to keep it consistent


class WeatherDashboardTab(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        # Welcome message
        welcome_label = ctk.CTkLabel(
            self,
            text="Welcome to Weather Dashboard",
            font=("Arial", 20, "bold")
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

        self.city_label = ctk.CTkLabel(self.search_frame, text="Enter City:", font=("Arial", 14))
        self.city_label.grid(row=0, column=0, padx=10)

        self.city_entry = ctk.CTkEntry(self.search_frame, width=200)
        self.city_entry.grid(row=0, column=1, padx=10)
        self.city_entry.bind("<Return>", lambda e: self.fetch_weather())

        self.fetch_button = ctk.CTkButton(self.search_frame, text="Get Weather", command=self.fetch_weather)
        self.fetch_button.grid(row=0, column=2, padx=10)

        # Loading indicator
        self.loading_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12))
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
                # Fallback dummy data
                dummy_data = {
                    "name": city,
                    "main": {"temp": 294.65, "humidity": 50},
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

        city_name = data.get("name", "N/A")
        temp_k = data.get("main", {}).get("temp", "N/A")
        temperature = self.kelvin_to_fahrenheit(temp_k)
        humidity = data.get("main", {}).get("humidity", "N/A")
        description = data.get("weather", [{}])[0].get("description", "N/A").capitalize()
        wind_speed = data.get("wind", {}).get("speed", "N/A")

        title = ctk.CTkLabel(
            self.result_frame,
            text=f"Weather in {city_name}",
            font=("Arial", 24, "bold")
        )
        title.grid(pady=(20, 30))

        details_frame = ctk.CTkFrame(self.result_frame)
        details_frame.grid(padx=30, pady=10)

        self.make_row(details_frame, "Temperature", f"{temperature}°F")
        self.make_row(details_frame, "Humidity", f"{humidity}%")
        self.make_row(details_frame, "Description", description)
        self.make_row(details_frame, "Wind Speed", f"{wind_speed} m/s")

    def make_row(self, parent, label_text, value_text):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)

        label = ctk.CTkLabel(frame, text=f"{label_text}:", font=("Arial", 14), anchor="w")
        label.pack(side="left", padx=10)

        value = ctk.CTkLabel(frame, text=value_text, font=("Arial", 14), anchor="e")
        value.pack(side="right", padx=10)

    def kelvin_to_fahrenheit(self, kelvin):
        try:
            return round(((float(kelvin) - 273.15) * 9/5 + 32), 1)
        except (ValueError, TypeError):
            return "N/A"

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
            font=("Arial", 14)
        )
        message_label.grid(pady=20)

        close_button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
        close_button.grid(pady=10)

        error_window.grab_set()
        error_window.focus_force()


