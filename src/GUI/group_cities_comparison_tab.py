# src/GUI/group_cities_comparison.py

"""
This tab allows users to compare weather data between two cities using a static database.
Users select two cities from dropdowns and view a side-by-side comparison of all available weather fields.
The system automatically selects the record with the most complete data for each city.
"""

import customtkinter as ctk
from src.DataProcessing.static_data_query import StaticDataQuery
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Optional


class GroupCitiesComparisonTab(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.has_loaded_once = False
        
        # Load temperature unit preference
        load_dotenv()
        temp_unit = os.getenv("TEMPERATURE_UNIT", "fahrenheit").lower()
        self.unit_symbol = "°F" if temp_unit == "fahrenheit" else "°C"
        self.is_fahrenheit = temp_unit == "fahrenheit"
        
        # Available cities list
        self.available_cities = []
        
        # GUI components
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface components"""
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.header = ctk.CTkLabel(
            self.main_frame,
            text="Group Cities Comparison",
            font=("Arial", 20, "bold")
        )
        self.header.pack(pady=(0, 20))
        
        # City selection frame
        self.selection_frame = ctk.CTkFrame(self.main_frame)
        self.selection_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # City 1 selection
        self.city1_label = ctk.CTkLabel(
            self.selection_frame,
            text="Select First City:",
            font=("Arial", 14, "bold")
        )
        self.city1_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.city1_dropdown = ctk.CTkComboBox(
            self.selection_frame,
            values=["Loading cities..."],
            state="normal",
            width=200
        )
        self.city1_dropdown.grid(row=0, column=1, padx=10, pady=10)
        
        # City 2 selection
        self.city2_label = ctk.CTkLabel(
            self.selection_frame,
            text="Select Second City:",
            font=("Arial", 14, "bold")
        )
        self.city2_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.city2_dropdown = ctk.CTkComboBox(
            self.selection_frame,
            values=["Loading cities..."],
            state="normal",
            width=200
        )
        self.city2_dropdown.grid(row=1, column=1, padx=10, pady=10)
        
        # Compare button
        self.compare_button = ctk.CTkButton(
            self.selection_frame,
            text="Compare Cities",
            command=self.compare_cities,
            state="normal"
        )
        self.compare_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(fill="both", expand=True, padx=20)
        
        # Initial status message
        self.status_label = ctk.CTkLabel(
            self.results_frame,
            text="Select this tab to load available cities",
            font=("Arial", 12),
            text_color="gray"
        )
        self.status_label.pack(pady=20)
        
    def on_tab_selected(self):
        """Called when this tab is clicked/selected - loads cities if not already loaded"""
        print("[DEBUG] Group Cities Comparison tab selected")
        if not self.has_loaded_once:
            self.load_available_cities()
            self.has_loaded_once = True
            
    def load_available_cities(self):
        """Load available cities from the static database"""
        print("[DEBUG] Loading available cities from static database...")
        
        # Update status
        self.status_label.configure(text="Loading cities from database...")
        self.update()
        
        try:
            # Get cities from static database
            self.available_cities = get_all_cities_from_static_db()
            
            if self.available_cities:
                # Update dropdowns
                self.city1_dropdown.configure(values=self.available_cities, state="normal")
                self.city2_dropdown.configure(values=self.available_cities, state="normal")
                self.compare_button.configure(state="normal")
                
                # Set default selections
                self.city1_dropdown.set("Select a city...")
                self.city2_dropdown.set("Select a city...")
                
                # Update status
                self.status_label.configure(
                    text=f"✅ Loaded {len(self.available_cities)} cities. Select two cities to compare.",
                    text_color="green"
                )
                
                print(f"[DEBUG] Successfully loaded {len(self.available_cities)} cities")
            else:
                self.status_label.configure(
                    text="❌ No cities found in database or database not accessible.",
                    text_color="red"
                )
                print("[DEBUG] No cities found in static database")
                
        except Exception as e:
            print(f"[DEBUG] Error loading cities: {e}")
            self.status_label.configure(
                text=f"❌ Error loading cities: {str(e)}",
                text_color="red"
            )
            
    def compare_cities(self):
        """Compare the selected cities"""
        city1 = self.city1_dropdown.get()
        city2 = self.city2_dropdown.get()
        
        # Validate selections
        if city1 == "Select a city..." or city1 not in self.available_cities:
            self.show_error("Please select a valid first city")
            return
            
        if city2 == "Select a city..." or city2 not in self.available_cities:
            self.show_error("Please select a valid second city")
            return
            
        if city1 == city2:
            self.show_error("Please select two different cities")
            return
            
        print(f"[DEBUG] Comparing {city1} vs {city2}")
        
        # Clear previous results
        self.clear_results()
        
        # Show loading message
        loading_label = ctk.CTkLabel(
            self.results_frame,
            text=f"Loading comparison data for {city1} and {city2}...",
            font=("Arial", 12),
            text_color="blue"
        )
        loading_label.pack(pady=10)
        self.update()
        
        try:
            # Get comparison data
            data1, data2 = get_comparison_data(city1, city2)
            
            # Remove loading message
            loading_label.destroy()
            
            if data1 is None or data2 is None:
                self.show_error(f"Could not retrieve data for one or both cities")
                return
                
            # Display comparison
            self.display_comparison(data1, data2)
            
        except Exception as e:
            loading_label.destroy()
            self.show_error(f"Error during comparison: {str(e)}")
            print(f"[DEBUG] Error during comparison: {e}")
            
    def clear_results(self):
        """Clear all widgets from results frame except status label"""
        for widget in self.results_frame.winfo_children():
            if widget != self.status_label:
                widget.destroy()
                
    def show_error(self, message: str):
        """Display an error message"""
        self.clear_results()
        error_label = ctk.CTkLabel(
            self.results_frame,
            text=f"❌ {message}",
            font=("Arial", 12),
            text_color="red"
        )
        error_label.pack(pady=10)
        
    def display_comparison(self, data1: pd.Series, data2: pd.Series):
        """Display side-by-side comparison of the two cities"""
        self.clear_results()
        
        # Comparison header
        comparison_header = ctk.CTkLabel(
            self.results_frame,
            text=f"Weather Comparison: {data1['name']} vs {data2['name']}",
            font=("Arial", 16, "bold")
        )
        comparison_header.pack(pady=(0, 20))
        
        # Create comparison frame with grid layout
        comparison_frame = ctk.CTkFrame(self.results_frame)
        comparison_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Headers
        ctk.CTkLabel(comparison_frame, text="Field", font=("Arial", 14, "bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        ctk.CTkLabel(comparison_frame, text=data1['name'], font=("Arial", 14, "bold")).grid(
            row=0, column=1, padx=10, pady=5
        )
        ctk.CTkLabel(comparison_frame, text=data2['name'], font=("Arial", 14, "bold")).grid(
            row=0, column=2, padx=10, pady=5
        )
        
        # Field mappings for display
        field_mappings = {
            'temp': 'Temperature',
            'feels_like': 'Feels Like',
            'humidity': 'Humidity (%)',
            'description': 'Description',
            'speed': 'Wind Speed (mph)',
            'dt': 'Last Updated'
        }
        
        row = 1
        for field, display_name in field_mappings.items():
            # Field name
            ctk.CTkLabel(comparison_frame, text=display_name, font=("Arial", 12)).grid(
                row=row, column=0, padx=10, pady=2, sticky="w"
            )
            
            # City 1 value
            value1 = self.format_field_value(field, data1.get(field))
            color1 = self.get_field_color(field, data1.get(field), data2.get(field), is_first=True)
            ctk.CTkLabel(comparison_frame, text=value1, font=("Arial", 12), text_color=color1).grid(
                row=row, column=1, padx=10, pady=2
            )
            
            # City 2 value
            value2 = self.format_field_value(field, data2.get(field))
            color2 = self.get_field_color(field, data2.get(field), data1.get(field), is_first=False)
            ctk.CTkLabel(comparison_frame, text=value2, font=("Arial", 12), text_color=color2).grid(
                row=row, column=2, padx=10, pady=2
            )
            
            row += 1
            
        # Add summary
        self.add_comparison_summary(data1, data2)
        
    def format_field_value(self, field: str, value) -> str:
        """Format field values for display"""
        if pd.isna(value) or value is None:
            return "N/A"
            
        if field in ['temp', 'feels_like']:
            try:
                return f"{float(value):.1f}{self.unit_symbol}"
            except (ValueError, TypeError):
                return "N/A"
        elif field == 'humidity':
            try:
                return f"{int(value)}%"
            except (ValueError, TypeError):
                return "N/A"
        elif field == 'speed':
            try:
                return f"{float(value):.1f} mph"
            except (ValueError, TypeError):
                return "N/A"
        else:
            return str(value)
            
    def get_field_color(self, field: str, value1, value2, is_first: bool) -> str:
        """Get color coding for comparison values"""
        if pd.isna(value1) or pd.isna(value2) or value1 is None or value2 is None:
            return "gray"
            
        try:
            if field in ['temp', 'feels_like', 'speed']:
                val1 = float(value1)
                val2 = float(value2)
                
                if field in ['temp', 'feels_like']:
                    # Higher temperature = red, lower = blue
                    if val1 > val2:
                        return "red" if is_first else "blue"
                    elif val1 < val2:
                        return "blue" if is_first else "red"
                elif field == 'speed':
                    # Higher wind speed = orange, lower = green
                    if val1 > val2:
                        return "orange" if is_first else "green"
                    elif val1 < val2:
                        return "green" if is_first else "orange"
                        
        except (ValueError, TypeError):
            pass
            
        return "white"  # Default color
        
    def add_comparison_summary(self, data1: pd.Series, data2: pd.Series):
        """Add a summary of the comparison"""
        summary_frame = ctk.CTkFrame(self.results_frame)
        summary_frame.pack(fill="x", padx=10, pady=20)
        
        summary_label = ctk.CTkLabel(
            summary_frame,
            text="Comparison Summary",
            font=("Arial", 14, "bold")
        )
        summary_label.pack(pady=(10, 5))
        
        # Generate summary text
        summary_text = self.generate_summary_text(data1, data2)
        
        summary_content = ctk.CTkLabel(
            summary_frame,
            text=summary_text,
            font=("Arial", 11),
            justify="left"
        )
        summary_content.pack(padx=20, pady=(5, 15))
        
    def generate_summary_text(self, data1: pd.Series, data2: pd.Series) -> str:
        """Generate summary text comparing the two cities"""
        summary_parts = []
        
        try:
            # Temperature comparison
            if pd.notna(data1.get('temp')) and pd.notna(data2.get('temp')):
                temp1, temp2 = float(data1['temp']), float(data2['temp'])
                temp_diff = abs(temp1 - temp2)
                warmer_city = data1['name'] if temp1 > temp2 else data2['name']
                summary_parts.append(f"🌡️ {warmer_city} is warmer by {temp_diff:.1f}{self.unit_symbol}")
                
            # Wind comparison
            if pd.notna(data1.get('speed')) and pd.notna(data2.get('speed')):
                wind1, wind2 = float(data1['speed']), float(data2['speed'])
                wind_diff = abs(wind1 - wind2)
                windier_city = data1['name'] if wind1 > wind2 else data2['name']
                summary_parts.append(f"💨 {windier_city} has stronger winds by {wind_diff:.1f} mph")
                
            # Humidity comparison
            if pd.notna(data1.get('humidity')) and pd.notna(data2.get('humidity')):
                humid1, humid2 = int(data1['humidity']), int(data2['humidity'])
                humid_diff = abs(humid1 - humid2)
                if humid_diff > 5:  # Only mention if significant difference
                    more_humid_city = data1['name'] if humid1 > humid2 else data2['name']
                    summary_parts.append(f"💧 {more_humid_city} is more humid by {humid_diff}%")
                    
        except (ValueError, TypeError) as e:
            print(f"[DEBUG] Error generating summary: {e}")
            
        return "\n".join(summary_parts) if summary_parts else "Both cities have similar weather conditions."