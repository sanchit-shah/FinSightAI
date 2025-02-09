import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import queue
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
from imblearn.over_sampling import SMOTE
from CTkMessagebox import CTkMessagebox

class TrainingFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.is_training = False
        self.training_thread = None
        self.data_queue = queue.Queue()
        self.training_data = {
            'loss': [], 'accuracy': [],
            'val_loss': [], 'val_accuracy': []
        }
        self.setup_frame()
        self.setup_plot()
        
    def setup_frame(self):
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(pady=10)
        
        self.train_button = ctk.CTkButton(
            controls_frame,
            text="Start Training",
            command=self.toggle_training
        )
        self.train_button.pack(side=tk.LEFT, padx=5)
        
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add status label below the plot
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=5)
        
        # Navigation frame at the bottom
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Back to Data Preparation",
            command=lambda: self.app.show_frame('data_preparation')
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next: Evaluate Results →",
            command=lambda: self.app.show_frame('evaluation')
        )
        self.next_button.pack(side=tk.RIGHT)
        
    def setup_plot(self):
        self.fig, self.ax1 = plt.subplots(figsize=(6, 4))
        self.ax2 = self.ax1.twinx()
        
        self.ax1.set_xlabel('Epoch')
        self.ax1.set_ylabel('Loss', color='tab:blue')
        self.ax2.set_ylabel('Accuracy', color='tab:orange')
        self.fig.suptitle('Training Progress')
        
        # Initialize with empty data
        self.loss_line, = self.ax1.plot([], [], 'b-', label='Training Loss')
        self.val_loss_line, = self.ax1.plot([], [], 'b--', label='Validation Loss')
        self.acc_line, = self.ax2.plot([], [], 'orange', label='Training Accuracy')
        self.val_acc_line, = self.ax2.plot([], [], 'orange', linestyle='--', label='Validation Accuracy')
        
        # Set initial axis limits
        self.ax1.set_xlim(0.8, 2)  # Start with range showing epoch 1
        self.ax1.set_ylim(0, 1)
        self.ax2.set_ylim(0, 1)
        
        self.ax1.tick_params(axis='y', labelcolor='tab:blue')
        self.ax2.tick_params(axis='y', labelcolor='tab:orange')
        
        # Set x-axis to show integer ticks
        self.ax1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        lines1, labels1 = self.ax1.get_legend_handles_labels()
        lines2, labels2 = self.ax2.get_legend_handles_labels()
        self.ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.fig.tight_layout()
        
    def prepare_data(self):
        df = self.app.frames['data_preparation'].df
        target_column = self.app.frames['data_preparation'].target_var.get()
        task_type = self.app.task_type

        # Encode categorical variables
        categorical_columns = df.select_dtypes(include=["object"]).columns
        for col in categorical_columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])

        # Split data
        X = df.drop(columns=[target_column])
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Handle imbalanced data for fraud detection
        if task_type == "fraud_detection":
            smote = SMOTE(random_state=42)
            X_train, y_train = smote.fit_resample(X_train, y_train)

        # Scale features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        return X_train, X_test, y_train, y_test, task_type

    def toggle_training(self):
        if not self.is_training:
            self.start_training()
        else:
            self.stop_training()
            
    def start_training(self):
        self.is_training = True
        self.train_button.configure(text="Stop Training")
        self.training_thread = threading.Thread(target=self.training_loop)
        self.training_thread.start()
        self.update_plot()
        
    def stop_training(self):
        self.is_training = False
        self.train_button.configure(text="Start Training")
        self.status_label.configure(text="Training Stopped")
        if self.training_thread:
            self.training_thread.join()
    
    def training_loop(self):
        X_train, X_test, y_train, y_test, task_type = self.prepare_data()
        
        # Initialize model based on task type
        if task_type == "fraud_detection":
            model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, class_weight="balanced")
        else:  # credit_risk
            model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, class_weight="balanced")

        batch_size = 512
        max_epochs = 30
        early_stopping_patience = 3
        improvement_threshold = 0.01
        epochs_without_improvement = 0
        previous_val_accuracy = 0
        epsilon = 1e-10

        for epoch in range(max_epochs):
            if not self.is_training:
                break

            # Update status label with current epoch
            self.status_label.configure(text=f"Training Epoch {epoch + 1}/{max_epochs}")

            indices = np.random.permutation(len(X_train))
            epoch_metrics = {'loss': 0, 'accuracy': 0, 'val_loss': 0, 'val_accuracy': 0}
            batch_count = 0

            for start_idx in range(0, len(X_train), batch_size):
                if not self.is_training:
                    break

                end_idx = min(start_idx + batch_size, len(X_train))
                batch_indices = indices[start_idx:end_idx]

                X_batch = X_train[batch_indices]
                y_batch = y_train.iloc[batch_indices]

                # Train on batch
                model.fit(X_batch, y_batch)

                # Calculate metrics
                train_pred = model.predict(X_batch)
                val_pred = model.predict(X_test)

                batch_train_acc = accuracy_score(y_batch, train_pred)
                batch_val_acc = accuracy_score(y_test, val_pred)

                batch_train_loss = -np.mean(y_batch * np.log(np.clip(train_pred.astype(float), epsilon, 1 - epsilon)))
                batch_val_loss = -np.mean(y_test * np.log(np.clip(val_pred.astype(float), epsilon, 1 - epsilon)))

                epoch_metrics['loss'] += batch_train_loss
                epoch_metrics['accuracy'] += batch_train_acc
                epoch_metrics['val_loss'] += batch_val_loss
                epoch_metrics['val_accuracy'] += batch_val_acc
                batch_count += 1

            # Average metrics for the epoch
            for key in epoch_metrics:
                epoch_metrics[key] /= batch_count

            self.data_queue.put(epoch_metrics)

            # Early stopping check
            improvement = epoch_metrics['val_accuracy'] - previous_val_accuracy
            if improvement < improvement_threshold:
                epochs_without_improvement += 1
            else:
                epochs_without_improvement = 0

            if epochs_without_improvement >= early_stopping_patience:
                break

            previous_val_accuracy = epoch_metrics['val_accuracy']
            time.sleep(0.1)  # Prevent UI freezing

        # Final evaluation and completion message
        if self.is_training:
            y_test_pred = model.predict(X_test)
            y_test_proba = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_test_pred, average='binary')
            roc_auc = roc_auc_score(y_test, y_test_proba)
            
            final_metrics = {
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'roc_auc': roc_auc,
                'y_test': y_test,
                'y_pred': y_test_pred,
                'y_proba': y_test_proba
            }
            
            # Update evaluation frame with metrics
            self.app.frames['evaluation'].update_metrics(final_metrics)
            
            # Show completion message
            completion_reason = ""
            if epochs_without_improvement >= early_stopping_patience:
                completion_reason = f"Training stopped after {epoch + 1} epochs due to no improvement in validation accuracy for {early_stopping_patience} epochs."
            else:
                completion_reason = f"Training completed successfully after {epoch + 1} epochs."

            CTkMessagebox(
                title="Training Complete",
                message=completion_reason,
                icon="info"
            )
            
            self.status_label.configure(text="Training Complete! You can now proceed to evaluation.")
            self.train_button.configure(text="Start Training")
            self.is_training = False
            self.is_training_complete = True
            self.next_button.configure(state="normal")
            
            # Enable next step in sidebar using the app's sidebar reference
            if hasattr(self.app, 'sidebar'):
                self.app.sidebar.enable_next_step('training')

    def update_plot(self):
        if self.is_training:
            while not self.data_queue.empty():
                data = self.data_queue.get()
                
                if isinstance(data, tuple) and data[0] == 'final_metrics':
                    metrics = data[1]
                    continue
                    
                for key, value in data.items():
                    self.training_data[key].append(value)
                    
            if self.training_data['loss']:  # Check if we have any data
                # Create x values starting from epoch 1
                x = [i + 1 for i in range(len(self.training_data['loss']))]
                
                # Update line data
                self.loss_line.set_data(x, self.training_data['loss'])
                self.val_loss_line.set_data(x, self.training_data['val_loss'])
                self.acc_line.set_data(x, self.training_data['accuracy'])
                self.val_acc_line.set_data(x, self.training_data['val_accuracy'])
                
                # Dynamically adjust x-axis
                self.ax1.set_xlim(0.8, max(x) + 0.2)
                
                # Update y-axis limits
                all_loss_values = self.training_data['loss'] + self.training_data['val_loss']
                all_acc_values = self.training_data['accuracy'] + self.training_data['val_accuracy']
                
                if all_loss_values:
                    loss_min = min(all_loss_values)
                    loss_max = max(all_loss_values)
                    margin = (loss_max - loss_min) * 0.1 if loss_max != loss_min else 0.1
                    self.ax1.set_ylim(max(0, loss_min - margin), loss_max + margin)
                
                if all_acc_values:
                    acc_min = min(all_acc_values)
                    acc_max = max(all_acc_values)
                    margin = (acc_max - acc_min) * 0.1 if acc_max != acc_min else 0.1
                    self.ax2.set_ylim(max(0, acc_min - margin), min(1, acc_max + margin))
                
                self.canvas.draw()
            
            self.after(100, self.update_plot)
