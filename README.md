# Weather_Dashboard_Elizabeth_Howard

# To Start the Weather Dashboard app, open main.py and run in python. Pip install requirements.txt if needed. 




File/Folder Name                    Description


```
WEATHER_DASHBOARD_ELIZABETH_HOWARD/
├── Data/                           # For saved CSV or text files
│   └── Screenshots/                # images for README
│
├── Docs/                           # Documentation and homework
│   ├── Homework/
│   │   └── week_11_reflections.md  # Week 11 Homework
│   ├── README.md                   # Project README
│   └── user_guide.md               # User guide
│
├── Features/                       # Feature modules
│   ├── Simple Statistics/
│   │   └── simple_statistics.py    # Simple Statistics main function
│   ├── Weather Icons/
│   │   └── weather_icons.py        # Weather Icons main function
│   ├── Weather Alerts/
│   │   └── weather_alerts.py       # Weather Alerts main function
│   └── Weather Mascot/
│       └── weather_mascot.py       # Weather Mascot main function
│
├── src/                            # Source code modules
│   ├── API/
│   │   ├── API_call.py             # API call logic
│   │   └── __init__.py
│   ├── DataProcessing/
│   │   ├── data_to_SQL.py          # Database logic
│   │   └── __init__.py
│   ├── GUI/
│   │   └── weather_dashboard.py    # Main GUI window
│   └── ErrorHandling/
│       └── error_handling_entry.py # Input normalization and error handling
│
├── Tests/                          # Testing 
│   ├── test_functions.py
│   ├── test_db.py
│   └── test_API.py
│
├── .gitignore                      # Standard git ignore file
├── config.py                       # (Optional) config variables
├── main.py                         # Main app logic/entry point
├── requirements.txt                # requirements to run Weather Dashboard
├── sandbox.py                      # Experimental code
├── debugger.py                     # Project cleanup script
└── weather_app_controller.py       # (If present) app controller
```


# copy and paste bank for file structure above
└── 


## Required Imports

The following Python imports are used throughout the Weather Dashboard app:

**Standard Library:**
- os
- sys
- datetime
- sqlite3

**Third-Party Packages:**
- requests
- python-dotenv (`from dotenv import load_dotenv`)
- customtkinter as ctk

**Project Modules:**
- from API.API_call import get_weather_data, api_key
- from DataProcessing.data_to_SQL import save_weather_to_sqlite
- import main

Make sure all third-party packages are installed (see `requirements.txt`).

