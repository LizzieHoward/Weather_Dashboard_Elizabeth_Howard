# root_window.py

import customtkinter as ctk

# Import your tabs
from src.GUI.weather_dashboard_tab import WeatherDashboardTab
from src.GUI.weather_alerts_tab import WeatherAlertsTab

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

        # Use CTkTabview instead of ttk.Notebook
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Add tabs
        self.add_tabs()
        
        # Set up tab change callback
        self.tabview.configure(command=self.on_tab_changed)

    def add_tabs(self):
        # Create tab frames using CTkTabview
        dashboard_tab_frame = self.tabview.add("Weather Dashboard")
        alerts_tab_frame = self.tabview.add("Weather Alerts")

        # Create your custom tab widgets inside the tab frames
        self.dashboard_tab = WeatherDashboardTab(dashboard_tab_frame, controller=self.controller)
        self.dashboard_tab.pack(fill="both", expand=True)
        
        self.alerts_tab = WeatherAlertsTab(alerts_tab_frame, controller=self.controller)
        self.alerts_tab.pack(fill="both", expand=True)

        # Set controller references
        if self.controller:
            self.controller.dashboard_tab = self.dashboard_tab
            self.controller.alerts_tab = self.alerts_tab

    def on_tab_changed(self):
        """Called when tab selection changes"""
        current_tab = self.tabview.get()
        print(f"[DEBUG] Tab changed to: {current_tab}")
        
        if current_tab == "Weather Alerts":
            # Trigger alerts refresh when alerts tab is selected
            self.alerts_tab.on_tab_selected()

if __name__ == "__main__":
    app = RootWindow()
    app.mainloop()