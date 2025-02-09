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
        steps_label = ctk.CTkLabel(
            self, 
            text="FinSightAI", 
            font=("Inter", 18, "bold")
        )
        steps_label.pack(pady=(0, 15), padx=10)
        
        steps = [
            ("Select Data", 'data_selection'),
            ("Prepare Data", 'data_preparation'),
            ("Train Model", 'training'),
            ("Evaluate Results", 'evaluation'),
            ("Export Model", 'export')
        ]
        
        self.step_labels = {}
        
        for step_text, frame_name in steps:
            step_frame = ctk.CTkFrame(self, fg_color="transparent")
            step_frame.pack(pady=5, padx=10, fill=tk.X)
            
            indicator = ctk.CTkLabel(
                step_frame, 
                text="○",
                font=("Inter", 16),
                text_color="gray"
            )
            indicator.pack(side=tk.LEFT, padx=(5, 10))
            
            label = ctk.CTkLabel(
                step_frame,
                text=step_text,
                font=("Inter", 14),
                text_color="gray"
            )
            label.pack(side=tk.LEFT)
            
            self.step_labels[frame_name] = (indicator, label)
            
        self.set_active_step('data_selection')
    
    def set_active_step(self, current_step):
        """Update the visual indication of the current step"""
        steps_order = ['data_selection', 'data_preparation', 'training', 'evaluation', 'export']
        current_index = steps_order.index(current_step)
        
        for i, step in enumerate(steps_order):
            indicator, label = self.step_labels[step]
            if i < current_index:
                indicator.configure(text="●", text_color="green")
                label.configure(text_color="green")
            elif i == current_index:
                indicator.configure(text="●", text_color="blue")
                label.configure(text_color="blue")
            else: 
                indicator.configure(text="○", text_color="gray")
                label.configure(text_color="gray")
    
    def enable_next_step(self, current_step):
        """Update progress indicator when moving to next step"""
        steps_order = ['data_selection', 'data_preparation', 'training', 'evaluation', 'export']
        current_index = steps_order.index(current_step)
        
        if current_index + 1 < len(steps_order):
            next_step = steps_order[current_index + 1]
            self.set_active_step(next_step)

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
