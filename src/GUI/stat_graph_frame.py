# src/GUI/graph_frame.py

import customtkinter as ctk
import matplotlib as plt

class GraphFrame(ctk.CTkFrame):
    """
    Large frame designed to hold graphs or charts in future.
    Styled with glassmorphic design.
    """

    LIGHT_BG = "#FFFFFF99"
    DARK_BG = "#1F1F1F99"
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

        self._build_placeholder()

    def _build_placeholder(self):
        """Temporary placeholder for graph area."""
        placeholder_label = ctk.CTkLabel(
            self,
            text="Graph Area\n(coming soon)",
            font=("Arial", 16),
            text_color="gray"
        )
        placeholder_label.place(relx=0.5, rely=0.5, anchor="center")
