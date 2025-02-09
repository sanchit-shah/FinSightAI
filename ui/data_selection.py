import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

class DataSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.file_selected = False
        self.setup_frame()
        
    def setup_frame(self):
        presets_label = ctk.CTkLabel(
            self, 
            text="Preset Datasets",
            font=("Arial", 16, "bold")
        )
        presets_label.pack(pady=(0, 10))
        
        preset_datasets = [
            ("Credit Risk Dataset", "Historical credit data with default rates"),
            ("Fraud Detection Dataset", "Transaction data with fraud labels"),
            ("Loan Approval Dataset", "Loan application data with approval decisions")
        ]
        
        for name, desc in preset_datasets:
            self.create_dataset_frame(name, desc)
            
        self.setup_upload_section()
        
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next: Prepare Data →",
            command=lambda: self.app.show_frame('data_preparation'),
            state="disabled"  # Initially disabled
        )
        self.next_button.pack(side=tk.RIGHT)
        
    def create_dataset_frame(self, name, desc):
        dataset_frame = ctk.CTkFrame(self)
        dataset_frame.pack(fill=tk.X, pady=5, padx=20)
        
        ctk.CTkLabel(dataset_frame, text=name, font=("Arial", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(dataset_frame, text=desc).pack(anchor="w")
        ctk.CTkButton(
            dataset_frame,
            text="Select",
            command=lambda: self.select_preset_dataset(name)
        ).pack(pady=5)
        
    def setup_upload_section(self):
        upload_frame = ctk.CTkFrame(self)
        upload_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ctk.CTkLabel(
            upload_frame,
            text="Upload Custom Dataset",
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        ctk.CTkButton(
            upload_frame,
            text="Browse Files",
            command=self.browse_files
        ).pack(pady=10)
        
    def select_preset_dataset(self, dataset_name):
        if dataset_name == "Credit Risk Dataset":
            self.app.task_type = "credit_risk"
        elif dataset_name == "Fraud Detection Dataset":
            self.app.task_type = "fraud_detection"
        elif dataset_name == "Loan Approval Dataset":
            self.app.task_type = "credit_risk"
            
        print(f"Selected dataset: {dataset_name}")
        self.file_selected = True
        self.next_button.configure(state="normal")
        self.app.show_frame('data_preparation')
        
    def browse_files(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            self.select_task_type(filename)
    
    def select_task_type(self, filename):
        # Create a new dialog window
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Task Type")
        dialog.geometry("300x200")
        dialog.transient(self)  # Make dialog modal
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        task_type = tk.StringVar(value="")
        
        # Label
        ctk.CTkLabel(
            dialog,
            text="Please select the task type:",
            font=("Arial", 14, "bold")
        ).pack(pady=(20, 10))
        
        # Radio buttons
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
        
        # Confirm button
        ctk.CTkButton(
            dialog,
            text="Confirm",
            command=confirm_selection
        ).pack(pady=20)
