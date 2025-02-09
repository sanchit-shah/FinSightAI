import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_frame()
        
    def setup_frame(self):
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=20, padx=20, fill=tk.X)
        
        ctk.CTkLabel(
            options_frame,
            text="Export Options",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 10))
        
        self.export_var = tk.StringVar(value="model")
        
        options = [
            ("Export model file (.pkl)", "model"),
            ("Export Python code (.py)", "code")
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
        
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Back to Evaluation",
            command=lambda: self.app.show_frame('evaluation')
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.finish_button = ctk.CTkButton(
            self.nav_frame,
            text="Finish",
            command=self.on_finish
        )
        self.finish_button.pack(side=tk.RIGHT)
        
    def export_model(self):
        export_type = self.export_var.get()
        
        if export_type == "model":
            file_types = [("Model Files", "*.pkl")]
            default_ext = ".pkl"
        else:
            file_types = [("Python Files", "*.py")]
            default_ext = ".py"
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            filetypes=file_types
        )
        
        if save_path:
            try:
                if export_type == "model":
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
        import pickle
        model = self.app.frames['training'].model
        if model is None:
            raise ValueError("No trained model found. Please complete training first.")
            
        if not path.endswith('.pkl'):
            path = path.replace('.h5', '.pkl')
            
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        
    def _save_code(self, path):
        data_file = self.app.frames['data_selection'].selected_file
        target_column = self.app.frames['data_preparation'].target_var.get()
        task_type = self.app.task_type
        
        code_template = f"""import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

# Load and prepare data
df = pd.read_csv('{data_file}')  # Updated with actual file path
target_column = '{target_column}'  # Updated with selected target column
task_type = '{task_type}'  # Updated with selected task type

# Encode categorical variables
categorical_columns = df.select_dtypes(include=["object"]).columns
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

# Split features and target
X = df.drop(columns=[target_column])
y = df[target_column]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply SMOTE for fraud detection
if task_type == "fraud_detection":
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize and train model
model = RandomForestClassifier(
    n_estimators=50 if task_type == "fraud_detection" else 100,
    max_depth=10 if task_type == "fraud_detection" else 15,
    random_state=42,
    class_weight="balanced"
)

# Train the model
model.fit(X_train, y_train)

# Save the trained model
import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
"""
        
        with open(path, 'w') as f:
            f.write(code_template)

    def on_finish(self):
        confirm = CTkMessagebox(
            title="Finish",
            message="Are you sure you want to finish?",
            icon="question",
            option_1="Yes",
            option_2="No"
        )
        if confirm.get() == "Yes":
            self.app.root.quit()
