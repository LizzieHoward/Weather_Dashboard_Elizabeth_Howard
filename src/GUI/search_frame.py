import customtkinter as ctk

class SearchFrame(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        self.city_entry = ctk.CTkEntry(self, width=200)
        self.city_entry.grid(row=0, column=1, padx=5)

        self.fetch_button = ctk.CTkButton(self, text="Get Weather", command=self.fetch_weather)
        self.fetch_button.grid(row=0, column=2, padx=5)

        ctk.CTkLabel(self, text="Enter City:").grid(row=0, column=0, padx=5)

    def fetch_weather(self):
        city = self.city_entry.get()
        if self.controller:
            self.controller.fetch_and_store_weather(city)