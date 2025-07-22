# root_window.py

import customtkinter as ctk
from tkinter import ttk

# Import your tabs
from weather_dashboard_tab import WeatherDashboardTab
#from weather_alerts_tab import WeatherAlertsTab
#from group_project_tab import GroupProjectTab


class RootWindow(ctk.CTk):
    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller

        # Window config
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Weather App")
        self.geometry("1000x700")
        self.minsize(800, 500)

        # Main notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Add tabs
        self.add_tabs()

    def add_tabs(self):
        # Weather Dashboard tab
        dashboard_tab = WeatherDashboardTab(self.notebook, controller=self.controller)
        self.notebook.add(dashboard_tab, text="Weather Dashboard")

        # Weather Alerts tab
        # alerts_tab = WeatherAlertsTab(self.notebook, controller=self.controller)
        # self.notebook.add(alerts_tab, text="Weather Alerts")

        # # Group Project tab
        # group_tab = GroupProjectTab(self.notebook, controller=self.controller)
        # self.notebook.add(group_tab, text="Group Project")


if __name__ == "__main__":
    app = RootWindow()
    app.mainloop()
