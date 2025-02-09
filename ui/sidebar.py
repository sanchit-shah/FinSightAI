import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox

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
        
        self.step_buttons = {}  # Store buttons for later access
        
        for step_text, frame_name in steps:
            btn = ctk.CTkButton(
                self, 
                text=step_text, 
                command=lambda f=frame_name: self.try_navigate(f)
            )
            btn.pack(pady=5, padx=10, fill=tk.X)
            self.step_buttons[frame_name] = btn
            
        # Initially disable all but first step
        for frame_name in self.step_buttons:
            if frame_name != 'data_selection':
                self.step_buttons[frame_name].configure(state="disabled")

    def try_navigate(self, frame_name):
        error_msg = None
        
        if frame_name == 'data_preparation' and not self.app.frames['data_selection'].file_selected:
            error_msg = "Please select a dataset and task type first."
            
        elif frame_name == 'training' and self.app.frames['data_preparation'].target_var.get() == "Select":
            error_msg = "Please select a target column first."
            
        elif frame_name == 'evaluation' and not hasattr(self.app.frames['training'], 'is_training_complete'):
            error_msg = "Please complete model training first."
            
        elif frame_name == 'export' and not self.app.frames['evaluation'].next_button.cget('state') == 'normal':
            error_msg = "Please complete model evaluation first."

        if error_msg:
            CTkMessagebox(
                title="Cannot Proceed",
                message=error_msg,
                icon="warning"
            )
            return
            
        self.app.show_frame(frame_name)

    def enable_next_step(self, current_step):
        """Enable the next step button after completing current step"""
        steps_order = ['data_selection', 'data_preparation', 'training', 'evaluation', 'export']
        current_index = steps_order.index(current_step)
        
        if current_index + 1 < len(steps_order):
            next_step = steps_order[current_index + 1]
            self.step_buttons[next_step].configure(state="normal")
