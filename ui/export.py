import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_frame()
        
    def setup_frame(self):
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=20, padx=20, fill=tk.X)
        
        ctk.CTkLabel(
            options_frame,
            text="Export Options",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 10))
        
        self.export_var = tk.StringVar(value="both")
        
        options = [
            ("Export both model file and Python code", "both"),
            ("Export model file only", "model"),
            ("Export Python code only", "code")
        ]
        
        for text, value in options:
            ctk.CTkRadioButton(
                options_frame,
                text=text,
                variable=self.export_var,
                value=value
            ).pack(pady=5, anchor="w")
            
        ctk.CTkButton(
            options_frame,
            text="Export",
            command=self.export_model
        ).pack(pady=20)
        
    def export_model(self):
        export_type = self.export_var.get()
        
        # Get save location from user
        file_types = []
        if export_type in ["both", "model"]:
            file_types.append(("Model Files", "*.h5"))
        if export_type in ["both", "code"]:
            file_types.append(("Python Files", "*.py"))
        if not file_types:
            file_types = [("All Files", "*.*")]
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=".h5" if export_type == "model" else ".py",
            filetypes=file_types
        )
        
        if save_path:
            try:
                if export_type == "both":
                    self._save_model(save_path + ".h5")
                    self._save_code(save_path + ".py")
                elif export_type == "model":
                    self._save_model(save_path)
                else:
                    self._save_code(save_path)
                    
                tk.messagebox.showinfo(
                    "Success",
                    "Export completed successfully!"
                )
                
            except Exception as e:
                tk.messagebox.showerror(
                    "Export Error",
                    f"An error occurred during export:\n{str(e)}"
                )
                
    def _save_model(self, path):
        # implement actual model saving logic
        print(f"Saving model to: {path}")
        
    def _save_code(self, path):
        # implement actual code generation logic
        print(f"Saving code to: {path}")
