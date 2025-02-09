import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from sklearn.metrics import roc_curve, confusion_matrix

class EvaluationFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_frame()
        
    def setup_frame(self):
        # Metrics Section
        metrics_frame = ctk.CTkFrame(self)
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ctk.CTkLabel(
            metrics_frame,
            text="Model Performance Metrics",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        self.metrics_label = ctk.CTkLabel(
            metrics_frame,
            text="Train the model to see metrics",
            font=("Arial", 12)
        )
        self.metrics_label.pack(pady=5)
        
        # Visualization Section
        viz_frame = ctk.CTkFrame(self)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.fig = Figure(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Navigation Frame
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Back to Training",
            command=lambda: self.app.show_frame('training')
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next: Export Model →",
            command=lambda: self.app.show_frame('export'),
            state="disabled"
        )
        self.next_button.pack(side=tk.RIGHT)

    def update_metrics(self, metrics):
        # Create main metrics text with explanations
        metrics_text = "Model Performance Metrics:\n\n"
        
        # Precision explanation and value
        metrics_text += "Precision (Accuracy of Positive Predictions):\n"
        metrics_text += f"• {metrics['precision']:.4f}\n"
        metrics_text += "Precision shows how many of our positive predictions were actually correct.\n"
        metrics_text += f"In this case, {metrics['precision']*100:.1f}% of the cases we predicted as "
        metrics_text += "risky/fraudulent were actually risky/fraudulent.\n\n"
        
        # Recall explanation and value
        metrics_text += "Recall (Detection Rate):\n"
        metrics_text += f"• {metrics['recall']:.4f}\n"
        metrics_text += "Recall shows how many actual positive cases we caught.\n"
        metrics_text += f"Our model successfully identified {metrics['recall']*100:.1f}% of all "
        metrics_text += "actual risky/fraudulent cases.\n\n"
        
        # F1 Score explanation and value
        metrics_text += "F1 Score (Overall Accuracy):\n"
        metrics_text += f"• {metrics['f1']:.4f}\n"
        metrics_text += "F1 Score balances precision and recall in a single number.\n"
        metrics_text += f"A score of {metrics['f1']:.4f} indicates the model's overall effectiveness.\n\n"
        
        # ROC AUC explanation and value
        metrics_text += "ROC AUC Score (Discrimination Ability):\n"
        metrics_text += f"• {metrics['roc_auc']:.4f}\n"
        metrics_text += "This score shows how well the model can distinguish between normal and risky/fraudulent cases.\n"
        metrics_text += f"Our score of {metrics['roc_auc']:.4f} means the model has "
        
        # Interpret ROC AUC score
        if metrics['roc_auc'] > 0.9:
            metrics_text += "excellent discrimination ability.\n"
        elif metrics['roc_auc'] > 0.8:
            metrics_text += "good discrimination ability.\n"
        elif metrics['roc_auc'] > 0.7:
            metrics_text += "fair discrimination ability.\n"
        else:
            metrics_text += "limited discrimination ability.\n"
        
        self.metrics_label.configure(text=metrics_text)
        
        # Update visualizations with explanations
        self.fig.clear()
        
        # Add ROC curve with explanation
        ax1 = self.fig.add_subplot(121)
        fpr, tpr, _ = roc_curve(metrics['y_test'], metrics['y_proba'])
        ax1.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {metrics["roc_auc"]:.2f})')
        ax1.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax1.set_xlim([0.0, 1.0])
        ax1.set_ylim([0.0, 1.05])
        ax1.set_xlabel('False Positive Rate')
        ax1.set_ylabel('True Positive Rate')
        ax1.set_title('Receiver Operating Characteristic (ROC) Curve\n' +
                     'Shows model\'s ability to balance sensitivity and specificity')
        ax1.legend(loc="lower right")
        
        # Add confusion matrix with explanation
        ax2 = self.fig.add_subplot(122)
        cm = confusion_matrix(metrics['y_test'], metrics['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', ax=ax2, cmap='Blues')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Actual')
        ax2.set_title('Confusion Matrix\n' +
                     'Shows prediction successes and failures')
        
        # Add explanatory text below confusion matrix
        total = cm.sum()
        correct = cm[0,0] + cm[1,1]
        accuracy = correct/total
        
        explanation = (
            f"\nConfusion Matrix Explanation:\n"
            f"• Total Cases: {total}\n"
            f"• Correct Predictions: {correct} ({accuracy:.1%})\n"
            f"• Top-left: Correct normal predictions\n"
            f"• Bottom-right: Correct risky/fraudulent predictions\n"
            f"• Top-right: False alarms\n"
            f"• Bottom-left: Missed detections"
        )
        
        self.explanation_label = ctk.CTkLabel(
            self,
            text=explanation,
            font=("Arial", 12)
        )
        self.explanation_label.pack(pady=10)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Enable next button
        self.next_button.configure(state="normal")
        
        # Enable next step in sidebar
        if hasattr(self.app, 'sidebar'):
            self.app.sidebar.enable_next_step('evaluation')

    def show_frame(self, frame_name):
        if frame_name == 'data_preparation' and not self.frames['data_selection'].file_selected:
            return
        if frame_name == 'training' and self.frames['data_preparation'].target_var.get() == "Select":
            return
        if frame_name == 'evaluation' and not self.frames['training'].is_training_complete:
            return
        
        frame = self.frames[frame_name]
        frame.tkraise()
