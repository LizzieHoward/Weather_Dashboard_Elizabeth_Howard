import customtkinter as ctk
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for embedding
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RecentAPICallsTab(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_path = "Data/weather_data.db"
        self.setup_ui()
        self.load_and_plot_data()

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header = ctk.CTkLabel(
            self.main_frame,
            text="Recent API Calls Comparison",
            font=("Arial", 20, "bold")
        )
        self.header.pack(pady=(0, 20))

        self.refresh_button = ctk.CTkButton(
            self.main_frame,
            text="Refresh",
            command=self.load_and_plot_data,
        )
        self.refresh_button.pack(pady=10)

        self.chart_frame = ctk.CTkFrame(self.main_frame)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(
            self.chart_frame,
            text="Loading recent API calls...",
            font=("Arial", 12),
            text_color="gray"
        )
        self.status_label.pack(pady=20)

        self.canvas = None

    def load_and_plot_data(self):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            if widget != self.status_label:
                widget.destroy()
        self.status_label.configure(text="Loading recent API calls...", text_color="gray")
        self.update()

        try:
            # Connect and query last three rows
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT dt, name, temp, humidity, feels_like
                FROM weather
                ORDER BY datetime(dt) DESC
                LIMIT 3
            """
            df = pd.read_sql_query(query, conn)
            conn.close()

            if df.empty or len(df) < 1:
                self.status_label.configure(
                    text="No API calls found in database.",
                    text_color="red"
                )
                return

            # Reverse to chronological order (oldest first)
            df = df.iloc[::-1].reset_index(drop=True)

            # Prepare plot
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(df['dt'], df['temp'], marker='o', label='Temperature (°F)')
            ax.plot(df['dt'], df['humidity'], marker='o', label='Humidity (%)')
            ax.plot(df['dt'], df['feels_like'], marker='o', label='Feels Like (°F)')

            # Label each point with city name
            for idx, row in df.iterrows():
                ax.annotate(row['name'], (row['dt'], row['temp']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='blue')
                ax.annotate(row['name'], (row['dt'], row['humidity']), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8, color='green')
                ax.annotate(row['name'], (row['dt'], row['feels_like']), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='red')

            ax.set_xlabel("API Call Time")
            ax.set_ylabel("Value")
            ax.set_title("Last 3 API Calls: Temp, Humidity, Feels Like")
            ax.legend()
            ax.grid(True)
            plt.tight_layout()

            # Update chart
            self.status_label.configure(text=f"Showing last {len(df)} API calls.", text_color="green")
            self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)

        except Exception as e:
            self.status_label.configure(text=f"Error loading data: {str(e)}", text_color="red")
