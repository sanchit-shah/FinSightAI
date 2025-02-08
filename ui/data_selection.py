import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

class DataSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
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
            command=lambda: self.app.show_frame('data_preparation')
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
        print(f"Selected dataset: {dataset_name}")
        self.app.show_frame('data_preparation')
        
    def browse_files(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            print(f"Selected file: {filename}")
            self.app.show_frame('data_preparation', filename)
