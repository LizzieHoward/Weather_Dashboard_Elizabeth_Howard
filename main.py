# Main app logic for Weather Dashboard
import customtkinter as ctk

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  # Example color theme")  

# Create main application window, CTk = CustomTkinter version of Tk
root = ctk.CTk()  
root.title("Weather Dashboard")
root.geometry("800x600")  


#add in responsive design layout


# Add a label
label = ctk.CTkLabel(master=root, text="Enter a City:")
label.grid(pady=10, sticky="nsew")

# Add an entry box
city_entry = ctk.CTkEntry(master=root, width=200)
city_entry.grid(pady=10)

# Add a button
def on_search():
    city = city_entry.get()
    print(f"Searching weather for: {city}")  # Replace this with a real API call

search_button = ctk.CTkButton(master=root, text="Get Weather", command=on_search)
search_button.grid(pady=10)

# Start the main loop
root.mainloop()
if __name__ == "__main__":
    print("Weather Dashboard App Starting...")
    # ...main logic will go here...
