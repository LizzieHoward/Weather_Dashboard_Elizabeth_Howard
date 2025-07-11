# src/GUI/glass_frame.py

import customtkinter as ctk


class GlassFrame(ctk.CTkFrame):
    """
    A reusable CTkFrame styled with a glassmorphism effect.
    """

    LIGHT_BG = "#FFFFFF99"   # semi-transparent white
    DARK_BG = "#1F1F1F99"    # semi-transparent dark
    BORDER_COLOR_LIGHT = "#FFFFFF55"
    BORDER_COLOR_DARK = "#00000055"

    def __init__(self, master, theme="light", corner_radius=15, **kwargs):
        bg_color = self.LIGHT_BG if theme == "light" else self.DARK_BG
        border_color = (
            self.BORDER_COLOR_LIGHT if theme == "light" else self.BORDER_COLOR_DARK
        )

        super().__init__(
            master,
            fg_color=bg_color,
            corner_radius=corner_radius,
            border_width=1,
            border_color=border_color,
            **kwargs,
        )
