import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

class DataSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.file_selected = False
        self.selected_file = None
        self.setup_frame()
        
    def setup_frame(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        
        text_frame = ctk.CTkFrame(self)
        text_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(
            text_frame,
            text="Welcome to FinSightAI",
            font=("Arial", 32, "bold")
        ).pack(pady=(20, 30), anchor="w")
        
        features = [
            "Complete preprocessing for hundreds of thousands of rows of data in a matter of seconds.",
            "Train custom built models with ease and high accuracy.",
            "Export your model and scale it even furthur."
        ]
        
        for feature in features:
            feature_frame = ctk.CTkFrame(text_frame)
            feature_frame.pack(fill=tk.X, pady=10, padx=20)
            
            ctk.CTkLabel(
                feature_frame,
                text="•",
                font=("Arial", 18)
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            ctk.CTkLabel(
                feature_frame,
                text=feature,
                font=("Arial", 16),
                wraplength=400,
                justify="left"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        upload_frame = ctk.CTkFrame(self)
        upload_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(
            upload_frame,
            text="Upload Dataset",
            font=("Arial", 24, "bold")
        ).pack(pady=(30, 20))
        
        ctk.CTkLabel(
            upload_frame,
            text="Select your CSV file to begin",
            font=("Arial", 14)
        ).pack(pady=(0, 20))
        
        ctk.CTkButton(
            upload_frame,
            text="Browse Files",
            command=self.browse_files,
            height=40,
            font=("Arial", 14)
        ).pack(pady=20)
        
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next: Prepare Data →",
            command=lambda: self.app.show_frame('data_preparation'),
            state="disabled",
            font=("Arial", 14)
        )
        self.next_button.pack(side=tk.RIGHT)
        
    def browse_files(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            self.selected_file = filename
            self.select_task_type(filename)
    
    def select_task_type(self, filename):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Task Type")
        dialog.geometry("300x200")
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        task_type = tk.StringVar(value="")
        
        ctk.CTkLabel(
            dialog,
            text="Please select the task type:",
            font=("Arial", 14, "bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkRadioButton(
            dialog,
            text="Credit Risk",
            variable=task_type,
            value="credit_risk"
        ).pack(pady=5)
        
        ctk.CTkRadioButton(
            dialog,
            text="Fraud Detection",
            variable=task_type,
            value="fraud_detection"
        ).pack(pady=5)
        
        def confirm_selection():
            if task_type.get():
                dialog.destroy()
                self.app.task_type = task_type.get()
                self.file_selected = True
                self.next_button.configure(state="normal")
                self.app.show_frame('data_preparation', filename)
            else:
                CTkMessagebox(
                    title="Error",
                    message="Please select a task type before proceeding.",
                    icon="cancel"
                )
        
        ctk.CTkButton(
            dialog,
            text="Confirm",
            command=confirm_selection
        ).pack(pady=20)
