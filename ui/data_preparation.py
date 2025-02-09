import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from CTkMessagebox import CTkMessagebox

class DataPreparationFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.df = None
        self.setup_frame()
        
    def setup_frame(self):
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.info_frame = ctk.CTkFrame(self.main_container)
        self.info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="Data Statistics:",
            font=("Arial", 14, "bold")
        )
        self.info_label.pack(anchor="w")
        
        self.column_frame = ctk.CTkFrame(self.main_container)
        self.column_frame.pack(fill=tk.X, pady=(0, 10))
        
        ctk.CTkLabel(
            self.column_frame,
            text="Manage Columns:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")
        
        self.column_var = tk.StringVar()
        self.column_dropdown = ctk.CTkOptionMenu(
            self.column_frame,
            variable=self.column_var,
            values=[]
        )
        self.column_dropdown.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ctk.CTkButton(
            self.column_frame,
            text="Delete Column",
            command=self.delete_column
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.target_frame = ctk.CTkFrame(self.main_container)
        self.target_frame.pack(fill=tk.X, pady=(0, 10))
        
        ctk.CTkLabel(
            self.target_frame,
            text="Select Target Column (What you want to predict):",
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        self.target_var = tk.StringVar()
        self.target_dropdown = ctk.CTkOptionMenu(
            self.target_frame,
            variable=self.target_var,
            values=["Select"],
            command=self.on_target_selected
        )
        self.target_dropdown.pack(side=tk.LEFT, padx=5)
        
        preview_label = ctk.CTkLabel(
            self.main_container,
            text="Data Preview:",
            font=("Arial", 14, "bold")
        )
        preview_label.pack(anchor="w", pady=(10, 5))
        
        self.tree_frame = ctk.CTkFrame(self.main_container)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.nav_frame = ctk.CTkFrame(self.main_container)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Back to Data Selection",
            command=lambda: self.app.show_frame('data_selection')
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next: Train Model →",
            command=lambda: self.app.show_frame('training'),
            state="disabled"
        )
        self.next_button.pack(side=tk.RIGHT)
        
    def load_data(self, file_path):
        self.df = pd.read_csv(file_path)
        self.process_null_values()
        self.update_column_dropdown()
        self.update_target_dropdown()
        self.display_data_preview()
        
    def process_null_values(self):
        if self.df is not None:
            null_counts = self.df.isnull().sum().sum()
            
            if null_counts > 0:
                self.df.dropna(inplace=True)
            
            self.update_statistics(null_values_removed=null_counts)
            
    def update_statistics(self, null_values_removed=0, column_removed=None, target_column=None):
        stats_text = "Data Statistics:\n\n"
        
        if null_values_removed > 0:
            stats_text += f"• {null_values_removed} rows removed due to missing values\n"
        else:
            stats_text += "• No rows removed due to missing values\n"
        
        if self.df is not None:
            stats_text += f"• {len(self.df)} rows remaining in dataset\n"
            
            categorical_columns = self.df.select_dtypes(include=["object"]).columns
            if len(categorical_columns) > 0:
                stats_text += f"• {len(categorical_columns)} categorical columns will be encoded\n"
            else:
                stats_text += "• No categorical columns to encode\n"
            
            stats_text += "• Data will be normalized and scaled appropriately prior to running the model\n"
            
            if target_column and target_column != "Select":
                value_counts = self.df[target_column].value_counts()
                ratio = value_counts.min() / value_counts.max()
                
                if ratio < 0.3:
                    stats_text += f"• Dataset is imbalanced (ratio: {ratio:.2f})\n"
                    stats_text += "• SMOTE will be used to balance the dataset\n"
                else:
                    stats_text += "• Dataset is relatively balanced\n"
        
        if column_removed:
            stats_text += f"• Column '{column_removed}' has been removed\n"
            
        self.info_label.configure(text=stats_text)

    def update_column_dropdown(self):
        if self.df is not None:
            self.column_dropdown.configure(values=list(self.df.columns))
            if len(self.df.columns) > 0:
                self.column_var.set(self.df.columns[0])
                
    def update_target_dropdown(self):
        if self.df is not None:
            self.target_dropdown.configure(values=["Select"] + list(self.df.columns))
            self.target_var.set("Select")
            
    def on_target_selected(self, choice):
        if choice != "Select":
            self.update_statistics(target_column=choice)
            self.next_button.configure(state="normal")
        else:
            self.next_button.configure(state="disabled")
            
    def delete_column(self):
        if self.df is not None and self.column_var.get():
            column = self.column_var.get()
            
            if column == self.target_var.get() and self.target_var.get() != "Select":
                CTkMessagebox(
                    title="Error",
                    message="Cannot delete the target column!",
                    icon="cancel"
                )
                return
                
            confirm = CTkMessagebox(
                title="Confirm Deletion",
                message=f"Are you sure you want to delete the column '{column}'?",
                icon="warning",
                option_1="Yes",
                option_2="No"
            )
            
            response = confirm.get()
            if response == "Yes":
                self.df.drop(columns=[column], inplace=True)
                self.update_column_dropdown()
                self.update_target_dropdown()
                self.display_data_preview()
                self.update_statistics(column_removed=column)
            
    def display_data_preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if self.df is not None:
            self.tree["columns"] = list(self.df.columns)
            self.tree["show"] = "headings"
            
            for column in self.df.columns:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=100)
                
            for i, row in self.df.head(100).iterrows():
                self.tree.insert("", "end", values=list(row))
