# Weather Dashboard — Elizabeth Howard

A Python desktop application for visualizing and comparing weather data using a clean, multi-tab GUI.  
Built with [customtkinter](https://github.com/TomSchimansky/CustomTkinter), [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), and SQLite.

---

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Features](#features)
- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Credits](#credits)

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LizzieHoward/Weather_Dashboard_Elizabeth_Howard.git
   cd Weather_Dashboard_Elizabeth_Howard
   ```
2. **Install Python (3.8+)** if not already installed.

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python main.py
   ```

---

## Usage Guide

- The app launches a dashboard window with several tabs:
  - **Weather Dashboard:** View real-time weather for your selected city.
  - **Group Cities Comparison:** Compare weather data and statistics for any two cities.
  - **Weather Alerts:** See current alerts for selected cities.
  - **Recent API Calls:** View a chart comparing temperature, humidity, and "feels like" for the three most recent API queries (with city labels).

- **How to Use:**
  - Select tabs to explore different features.
  - Use dropdown menus to pick cities for comparison.
  - Click "Compare" or "Refresh" buttons as needed.
  - Most tabs auto-populate cities from the database.
  - All data can be refreshed as new API calls are made.

---

## Features

- **Live Weather Dashboard:** Current weather for available cities.
- **Group Comparison:** Side-by-side comparison of two cities (auto-selects most complete data).
- **Weather Alerts:** Displays weather alerts for selected cities.
- **Recent API Calls Chart:** Matplotlib chart visualizing temp, humidity, and feels-like for the last three API calls, with city labels and timestamps.
- **Auto-populating Dropdowns:** Cities are loaded from the database for selection.
- **Embedded Charts:** Matplotlib charts are fully integrated in the GUI.
- **Error Handling:** Input is normalized, and helpful error messages are displayed.
- **Modular Feature System:** Easily extend with new weather features (statistics, mascots, icons).

---

## File Structure

```
WEATHER_DASHBOARD_ELIZABETH_HOWARD/
├── Data/
│   ├── Screenshots/             # Images for README
│   └── weather_data.db          # SQLite database
│
├── Docs/
│   ├── Homework/
│   ├── README.md                # Project README
│   └── user_guide.md            # User guide
│
├── Features/
│   ├── Simple Statistics/
│   ├── Weather Icons/
│   ├── Weather Alerts/
│   └── Weather Mascot/
│
├── src/
│   ├── API/
│   ├── DataProcessing/
│   ├── GUI/
│   └── ErrorHandling/
│
├── Tests/
├── .gitignore
├── config.py
├── main.py                      # Entry point
├── requirements.txt
├── sandbox.py
├── debugger.py
└── weather_app_controller.py
```

---

## Requirements

The app uses:
- Python 3.8+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- requests
- python-dotenv
- pandas
- matplotlib
- sqlite3 (built-in)

All dependencies can be installed via `pip install -r requirements.txt`.

---

## Credits

Developed by Elizabeth Howard.  
See `/Docs/user_guide.md` for detailed instructions and `/Features/` for feature modules.
