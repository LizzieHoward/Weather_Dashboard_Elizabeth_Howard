# Start the root GUI window
import customtkinter as ctk # CustomTkinter for modern UI

class WeatherDashboard(ctk.CTk): # Create main application window, CTk = CustomTkinter version of Tk
    def __init__(self):
        super().__init__()

        # Window config
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Weather Dashboard")
        self.geometry("800x600")

        # Widgets
        self.city_label = ctk.CTkLabel(self, text="Enter City:", font=("Arial", 14))
        self.city_label.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.city_entry = ctk.CTkEntry(self, width=200)
        self.city_entry.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self.fetch_button = ctk.CTkButton(self, text="Get Weather", command=self.fetch_weather)
        self.fetch_button.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")

        # Make the rows/cols expand nicely
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.show_error("Please enter a city name.")
            return

        # Replace with actual API + DB save later
        print(f"Searching weather for: {city}")
        dummy_data = {
            "name": city,
            "main": {"temp": 21.5, "humidity": 50},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 3.2}
        }
        self.display_weather(dummy_data)

    def display_weather(self, data):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        city_name = data.get("name")
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].capitalize()
        wind_speed = data["wind"]["speed"]

        ctk.CTkLabel(
            self.result_frame,
            text=f"Weather in {city_name}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.make_row("Temperature (°C)", temperature)
        self.make_row("Humidity (%)", humidity)
        self.make_row("Description", description)
        self.make_row("Wind Speed (m/s)", wind_speed)

    def make_row(self, label_text, value_text):
        frame = ctk.CTkFrame(self.result_frame)
        frame.pack(pady=5, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text + ":", anchor="w")
        label.pack(side="left", padx=5)

        button = ctk.CTkButton(frame, text=str(value_text))
        button.pack(side="right", padx=5)

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("300x100")
        ctk.CTkLabel(error_window, text=message, text_color="red").pack(pady=20)
