import customtkinter as ctk
from src.GUI.search_frame import SearchFrame
from GUI.weather_alerts_tab import ResultsFrame
from GUI.graph_tab import GraphFrame

class WeatherDashboard(ctk.CTk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Weather Dashboard")
        self.geometry("1000x600")
        self.minsize(800, 400)

        # Create main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create Frames
        self.search_frame = SearchFrame(self.main_frame, controller=self.controller)
        self.search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        self.results_frame = ResultsFrame(self.main_frame)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.graph_frame = GraphFrame(self.main_frame)
        self.graph_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=3)

if __name__ == "__main__":
    app = WeatherDashboard()
    app.mainloop()
