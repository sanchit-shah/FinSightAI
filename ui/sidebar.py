import customtkinter as ctk
import tkinter as tk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, width=200)
        self.app = app
        self.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.setup_sidebar()
        
    def setup_sidebar(self):
        steps_label = ctk.CTkLabel(self, text="Build Steps", font=("Arial", 16, "bold"))
        steps_label.pack(pady=(0, 10), padx=10)
        
        steps = [
            ("Select Data", 'data_selection'),
            ("Prepare Data", 'data_preparation'),
            ("Train Model", 'training'),
            ("Evaluate Results", 'evaluation'),
            ("Export Model", 'export')
        ]
        
        for step_text, frame_name in steps:
            btn = ctk.CTkButton(
                self, 
                text=step_text, 
                command=lambda f=frame_name: self.app.show_frame(f)
            )
            btn.pack(pady=5, padx=10, fill=tk.X)
