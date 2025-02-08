import customtkinter as ctk
import tkinter as tk

class EvaluationFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_frame()
        
    def setup_frame(self):
        # Add evaluation widgets here
        pass
        
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Back to Training",
            command=lambda: self.app.show_frame('training')
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next: Export Model →",
            command=lambda: self.app.show_frame('export')
        )
        self.next_button.pack(side=tk.RIGHT)
