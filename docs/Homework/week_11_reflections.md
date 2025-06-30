📌 Instructions:
This week, you're setting the foundation for your capstone project. Complete the reflection, planning, and setup tasks in the file Week11_Reflection.md. Once done:

Upload the completed file to your GitHub Classroom repository inside the /docs/ folder.

Submit your repo link in Canvas under this assignment.

🔖 Section 0: Fellow Details
Fill out the table below:

Field	Your Entry
Name	Elizabeth Howard
GitHub Username LizzieHoward
Preferred Feature Track	Data 
Team Interest	Yes, Contributor 
✍️ Section 1 Week 11 Reflection
Answer each prompt with 3–5 bullet points:

Key Takeaways: What did you learn about capstone goals and expectations?
-the capstone outline
-the feature requirements 
-
Concept Connections: Which Week 1–10 skills feel strongest? Which need more practice?
-I'm not sure yet, I think as I go I will figure out what's rusty.
Early Challenges: Any blockers (e.g., API keys, folder setup)?
-folder setup was confusing
-
Support Strategies: Which office hours or resources can help you move forward?
- My teammates have helped me a lot, as well as other classmates I will continue to look to them for help as well as attend some office hours. 

🧠 Section 2: Feature Selection Rationale
List three features + one enhancement you plan to build.

| # / Feature Name      | Difficulty (1–3) | Why You Chose It / Learning Goal                                               |
|----------------------|------------------|--------------------------------------------------------------------------------|
| 1. Simple Statistics |        1         | Because I think a weather app needs this at a minimum, it’s a good place to start |
| 2. Weather Icons     |        2         | I like this feature on the weather app I use day to day.                        |
| 3. Weather Alerts    |        2         | I think this is a cool feature to add that would allow the user to customize the app a bit. |
| Enhancement: Mascot Weather Personality | – | I like the idea of a kawaii style app, so I think this fits well.               |
🧩 Tip: Pick at least one “level 3” feature to stretch your skills!

🗂️ Section 3: High-Level Architecture Sketch
Add a diagram or a brief outline that shows:
File/Folder Name                    Description

```
WEATHER_DASHBOARD_ELIZABETH_HOWARD/

├── Data/                           # For saved CSV or text files
|   └── Screenshots/                # images for README
|
|
├── Docs/                           # README and user_guide.md & TPS-25 Homework files
|   └── Homework/
|       └── week_11_reflections.md  # Week 11 Homework
|
|   └── README.md                   # README Markdown file
|   └── user_guide.md               # Markdown file explaining program to User
|
|
├── Features/                       # Feature modules
│   └── Simple Statistics           # Simple Statistics Feature 
|       └── simple_statistics.py    # Simple Statistics main function
|
|   └── Weather Icons               # Weather Icons Feature
|       └── weather_icons.py        # Weather Icons main function
|
|   └── Weather Alerts              # Weather Alerts Feature
|       └── weather_alerts.py       # Weather Alerts main function
|
|   └── Weather Mascot              # Weather Mascot Feature
|       └── weather_mascot.py       # Weather Mascot main function
|
|
├── Tests/                          # Testing 
|   └── test_functions.py
|
|
├── .gitignore                      #Standard git ignore file
├── config.py                       # Your API keys
├── main.py                         # Main app logic
├── requirements.txt                # requirements to run Weather Dashboard
```


Data Flow

WEATHER_DASHBOARD_ELIZABETH_HOWARD (main.py, config.py, etc.)
to
Features (TBD)
to
Data (TBD)


📊 Section 4: Data Model Plan
Fill in your planned data files or tables:

| File/Table Name      | Format (txt, json, csv, other) | Example Row                  |
|---------------------|-------------------------------|------------------------------|
| weather_history.txt | txt                           | 2025-06-09,Denver,76,Sunny   |
| testing_data.txt    | txt                           | 2025-06-09,Denver,76,Sunny   |

📆 Section 5: Personal Project Timeline (Weeks 12–17)
Customize based on your availability:

| Week | Monday            | Tuesday        | Wednesday      | Thursday     | Key Milestone         |
|------|-------------------|---------------|---------------|--------------|-----------------------|
| 12   | API setup         | Error handling| Tkinter shell | Buffer day   | Basic working app     |
| 13   | Simple Statistics |               | Review & Test | Integrate    | Feature 1 complete    |
| 14   | Weather Icons     |               | Review & test | Finish       | Feature 2 complete    |
| 15   | Weather Alerts    | Polish UI     | Error passing | Refactor     | All features complete |
| 16   | Weather Mascot    | Docs          | Tests         | Packaging    | Ready-to-ship app     |
| 17   | Rehearse          | Buffer        | Showcase      | –            | Demo Day              |

⚠️ Section 6: Risk Assessment
Identify at least 3 potential risks and how you’ll handle them.

| Risk                | Likelihood (High/Med/Low) | Impact (High/Med/Low) | Mitigation Plan                                 |
|---------------------|---------------------------|-----------------------|-------------------------------------------------|
| API Rate Limit      | Medium                    | Medium                | Add delays or cache recent results               |
| Incorrect/Missing Data | Medium                 | High                  | Validate API responses & robust error handling   |
| Data Storage Issues | Medium                    | Medium                | Add error handling for file operations           |
| Security of API Keys| Medium                    | High                  | Use .env files and .gitignore for secrets        |

🤝 Section 7: Support Requests
What specific help will you ask for in office hours or on Slack?
Probably help walking through how they did something in the appp, like tying together all pieces. 

✅ Section 8: Before Monday (Start of Week 12)
Complete these setup steps before Monday:

Push main.py, config.py, and a /data/ folder to your repo

Add OpenWeatherMap key to .env (⚠️ Do not commit the key)

Create files for the chosen feature in /features/ 

like this:
# weather_journal.py
"""
Feature: Weather Journal
- Stores daily mood and notes alongside weather data
"""
def add_journal_entry(date, mood, notes):
    # your code goes here
    pass
Commit and push a first-draft README.md

Book office hours if you're still stuck on API setup

📤 Final Submission Checklist:
✅ Week11_Reflection.md completed
✅ File uploaded to GitHub repo /docs/
✅ Repo link submitted on Canvas